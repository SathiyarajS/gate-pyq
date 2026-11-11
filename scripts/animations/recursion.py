"""Recursive function evaluation: the call tree, grown one call at a time.

Data: data/animations/recursion.json. Each entry states the question's program
as a small structured form (functions made of statements whose expressions are
written as in the question) and the expected answer. The simulator runs the
program with C semantics and the build stops if the result differs.

Program form:
  {"style": "c" | "pascal" | "math",
   "globals":   [{"type": "int", "name": "z", "init": "10"}],    (init optional)
   "functions": [{"name": "f", "type": "int", "params": ["int n"], "body": [...]}],
   "main":      [...],               statements of main (optional)
   "call":      "f(5)",              the first call when there is no main
   "input":     "1234\\n",            what getchar() reads (optional)
   "arg_order": "right-to-left",     only when the question fixes the order
   "fold":      ["bar"]}             draw calls of these functions as one node

Statements (one dict each):
  {"if": "n <= 1", "then": [...], "else": [...]}  "split": true puts a lone
                                                   then-statement on its own line
  {"return": "f(n-1) + f(n-2)"}  {"return": null}
  {"do": "printf(\\"%d\\", n)"}                       an expression statement
  {"local": "int", "vars": [["k", "0"], ["a[]", "{1,2}"], ["t", null]]}
  {"static": "int", "vars": [["i", "1"]]}
  {"for": ["k=1", "k<n", "++k"], "body": [...]}
  {"while": "x > 0", "body": [...]}
Pascal procedures give params as {"name": "x", "mode": "value" | "ref"}; a
Pascal "return" is the assignment to the function's name, and is allowed only
as the last statement of its branch. A "math" function has "cases":
[{"if": cond, "value": expr}, ..., {"value": expr}] and is listed as
"f(n) := if ... then ... else ...".

The listing beside the tree is printed from this same structure, so it is the
program that was run. Expressions are parsed (C operators, or Pascal ones in
the Pascal and math styles) and evaluated with C integer semantics: int
overflow, division by zero, reading an uninitialised variable or an
out-of-range element stops the build. So does any expression whose result
could depend on the unspecified order of evaluation of its operands or
arguments (two operands that both print, or one that changes what the other
reads), unless "arg_order" states the order the question fixes.

Expectations ("expect"): {"returns": v}, {"output": text, "match": "exact" |
"tokens"} (tokens: compare the printed numbers/words, ignoring spaces and
commas, for options typeset with spaces), {"calls": n, "of": name},
{"tree": "main[f1, f2[f3]]"} (the activation tree by function names) and
{"smallest": n} with a "search": {"var", "from", "call", "value"} block: the
smallest var for which call returns value.
"""
import itertools
import json
import re

INT_MIN, INT_MAX = -2 ** 31, 2 ** 31 - 1
MAX_DEPTH, MAX_CALLS, MAX_STEPS = 600, 200000, 160
COLLAPSE_OVER = 24  # draw repeated identical subtrees once when a tree has more calls than this


# ---------------------------------------------------------------- parsing

class Node:
    __slots__ = ('k', 'a', 'b', 'c')

    def __init__(self, k, a=None, b=None, c=None):
        self.k, self.a, self.b, self.c = k, a, b, c


_TOK = re.compile(r"""\s*(?:(\d+)|('(?:\\.|[^'\\])')|("(?:\\.|[^"\\])*")|([A-Za-z_]\w*)|
    (\+\+|--|==|!=|<=|>=|&&|\|\||\+=|-=|\*=|/=|%=|:=|<>|[-+*/%<>=!&()\[\],]))""", re.X)
_ESC = {'n': '\n', '0': '\0', 't': '\t', '\\': '\\', "'": "'", '"': '"'}


def _unescape(s):
    return re.sub(r'\\(.)', lambda m: _ESC.get(m.group(1), m.group(1)), s)


def _tokens(text):
    out, pos, text = [], 0, text.strip()
    while pos < len(text):
        m = _TOK.match(text, pos)
        if not m or m.end() == pos:
            raise SystemExit(f'Cannot read expression {text!r} at {text[pos:]!r}')
        pos = m.end()
        num, ch, st, name, op = m.groups()
        if num:
            out.append(('num', int(num)))
        elif ch:
            out.append(('chr', ord(_unescape(ch[1:-1]))))
        elif st:
            out.append(('str', _unescape(st[1:-1])))
        elif name:
            out.append(('name', name))
        else:
            out.append(('op', op))
    return out


class _Parser:
    def __init__(self, text, pascal):
        self.t, self.i, self.pascal, self.text = _tokens(text), 0, pascal, text

    def peek(self):
        return self.t[self.i] if self.i < len(self.t) else (None, None)

    def take(self, *ops):
        kind, v = self.peek()
        if (kind == 'op' or (kind == 'name' and self.pascal)) and v in ops:
            self.i += 1
            return v
        return None

    def need(self, op):
        if not self.take(op):
            raise SystemExit(f'Expected {op!r} in {self.text!r}')

    def parse(self):
        e = self.assign()
        if self.i != len(self.t):
            raise SystemExit(f'Unexpected {self.peek()[1]!r} in {self.text!r}')
        return e

    def assign(self):
        left = self.lor()
        ops = (':=',) if self.pascal else ('=', '+=', '-=', '*=', '/=', '%=')
        op = self.take(*ops)
        if op:
            if left.k not in ('name', 'index', 'deref'):
                raise SystemExit(f'Cannot assign to {self.text!r}')
            return Node('assign', op, left, self.assign())
        return left

    def binary(self, sub, ops):
        left = sub()
        while True:
            op = self.take(*ops)
            if not op:
                return left
            left = Node('bin', op, left, sub())

    def lor(self):
        return self.binary(self.land, () if self.pascal else ('||',))

    def land(self):
        return self.binary(self.eq, () if self.pascal else ('&&',))

    def eq(self):
        return self.binary(self.rel, ('=', '<>') if self.pascal else ('==', '!='))

    def rel(self):
        return self.binary(self.add, ('<', '<=', '>', '>='))

    def add(self):
        return self.binary(self.mul, ('+', '-'))

    def mul(self):
        return self.binary(self.unary, ('*', 'div', 'mod') if self.pascal else ('*', '/', '%'))

    def unary(self):
        op = self.take('-', '!', '*', '&', '++', '--') if not self.pascal else self.take('-')
        if op in ('++', '--'):
            return Node('pre', op, self.unary())
        if op == '*':
            return Node('deref', self.unary())
        if op:
            return Node('un', op, self.unary())
        return self.postfix()

    def postfix(self):
        e = self.primary()
        while True:
            if self.take('('):
                if e.k != 'name':
                    raise SystemExit(f'Only named functions can be called: {self.text!r}')
                args = []
                if not self.take(')'):
                    args.append(self.assign())
                    while self.take(','):
                        args.append(self.assign())
                    self.need(')')
                e = Node('call', e.a, args)
            elif self.take('['):
                idx = self.assign()
                self.need(']')
                e = Node('index', e, idx)
            elif not self.pascal and self.peek() in (('op', '++'), ('op', '--')):
                e = Node('post', self.take('++', '--'), e)
            else:
                return e

    def primary(self):
        kind, v = self.peek()
        self.i += 1
        if kind == 'num':
            return Node('num', v)
        if kind == 'chr':
            return Node('chr', v)
        if kind == 'str':
            return Node('str', v)
        if kind == 'name':
            return Node('name', v)
        if kind == 'op' and v == '(':
            e = self.assign()
            self.need(')')
            return Node('paren', e)
        raise SystemExit(f'Unexpected {v!r} in {self.text!r}')


def parse(text, pascal=False):
    return _Parser(text, pascal).parse()


# ---------------------------------------------------------------- showing expressions in notes

PRETTY = {'*': '×', '-': '−', '<=': '≤', '>=': '≥', '!=': '≠', '<>': '≠', '==': '=', '=': '=', '&&': 'and', '||': 'or'}


def num(v):
    return str(v).replace('-', '−')


def char_text(c):
    return {10: "'\\n'", 0: "'\\0'"}.get(c, "'" + chr(c) + "'")


def show(e, rec=None, mode=None):
    """The expression as text. mode 'label': calls show their argument values;
    mode 'value': names and calls are replaced by the values recorded in rec."""
    def go(e):
        k = e.k
        if mode == 'value' and id(e) in rec and k in ('name', 'index', 'deref', 'call', 'paren') and rec[id(e)] is not None:
            return '(' + value_text(rec[id(e)]) + ')' if k == 'paren' else value_text(rec[id(e)])
        if k == 'num':
            return num(e.a)
        if k == 'chr':
            return char_text(e.a)
        if k == 'str':
            return '"' + e.a.replace('\n', '\\n') + '"'
        if k == 'name':
            return e.a
        if k == 'paren':
            return '(' + go(e.a) + ')'
        if k == 'call':
            if mode and ('args', id(e)) in rec:
                return e.a + '(' + ', '.join(rec[('args', id(e))]) + ')'
            return e.a + '(' + ', '.join(go(x) for x in e.b) + ')'
        if k == 'index':
            return go(e.a) + '[' + go(e.b) + ']'
        if k == 'deref':
            return '*' + go(e.a)
        if k == 'un':
            return ('not ' if e.a == '!' else '−') + go(e.b)
        if k == 'pre':
            return e.a + go(e.b)
        if k == 'post':
            return go(e.b) + e.a
        if k == 'bin':
            return f'{go(e.b)} {PRETTY.get(e.a, e.a)} {go(e.c)}'
        if k == 'assign':
            return f'{go(e.b)} {"=" if e.a == ":=" else e.a} {go(e.c)}'
        raise SystemExit(f'Cannot show {k}')
    return go(e)


def _balanced(text):
    d = 0
    for ch in text:
        d += ch == '('
        d -= ch == ')'
        if d < 0:
            return False
    return d == 0


def _strip(text):
    while text.startswith('(') and text.endswith(')') and _balanced(text[1:-1]):
        text = text[1:-1]
    return text


def explain(e, rec, result, ctype='int'):
    """'f(2) + r = 11 + 5 = 16': the expression with call labels, then with values, then the result."""
    while e.k == 'paren':
        e = e.a
    if e.k in ('num', 'chr', 'name', 'str'):
        return value_text(result, ctype)
    parts = []
    for text in (_strip(show(e, rec, 'label')), _strip(show(e, rec, 'value')), value_text(result, ctype)):
        if not parts or parts[-1] != text:
            parts.append(text)
    return ' = '.join(parts)


# ---------------------------------------------------------------- values and memory

class Obj:
    """A variable or an array: a list of cells. uid tells objects apart for the order-of-evaluation check."""
    __slots__ = ('name', 'cells', 'kind', 'ctype', 'uid')
    made = itertools.count()

    def __init__(self, name, cells, kind, ctype='int'):
        self.name, self.cells, self.kind, self.ctype = name, cells, kind, ctype
        self.uid = next(Obj.made)


class Ptr:
    __slots__ = ('obj', 'idx')

    def __init__(self, obj, idx):
        self.obj, self.idx = obj, idx

    def __eq__(self, other):
        return isinstance(other, Ptr) and self.obj is other.obj and self.idx == other.idx

    @property
    def text(self):
        o = self.obj
        if o.kind == 'string':
            chars = []
            for c in o.cells[self.idx:]:
                if c == 0:
                    break
                chars.append(chr(c))
            return '"' + ''.join(chars) + '"'
        if o.kind == 'array':
            return o.name if self.idx == 0 else f'{o.name}+{self.idx}'
        return '&' + o.name


class Ref:
    """A Pascal variable parameter: another name for the caller's variable."""
    __slots__ = ('obj',)

    def __init__(self, obj):
        self.obj = obj


def value_text(v, ctype='int'):
    if v is None:
        return ''
    if isinstance(v, Ptr):
        return v.text
    if ctype == 'char':
        return char_text(v)
    return num(v)


def _int(v, what):
    if not isinstance(v, int) or isinstance(v, bool):
        raise SystemExit(f'{what}: not an integer')
    if not INT_MIN <= v <= INT_MAX:
        raise SystemExit(f'{what}: int overflow ({v}), which C leaves undefined')
    return v


def _div(a, b, what):
    if b == 0:
        raise SystemExit(f'{what}: division by zero')
    q = abs(a) // abs(b)
    return q if (a >= 0) == (b > 0) else -q


# ---------------------------------------------------------------- the program

class _Return(Exception):
    def __init__(self, value):
        self.value = value


class Program:
    def __init__(self, spec, qid='Q'):
        self.qid, self.spec = qid, spec
        self.style = spec.get('style', 'c')
        if self.style not in ('c', 'pascal', 'math'):
            raise SystemExit(f'{qid}: unknown style {self.style}')
        self.pascal = self.style != 'c'
        self.funcs = {}
        for f in spec['functions']:
            f = dict(f)
            if 'cases' in f:
                if self.style != 'math':
                    raise SystemExit(f'{qid}: cases need the math style')
                f['body'] = self._cases(f['cases'])
            f['_params'] = [self._param(p) for p in f.get('params', [])]
            self.funcs[f['name']] = f
        self.main = spec.get('main')
        self.lines = []
        self._listing()
        self._prepare()

    # ---- structure

    def _cases(self, cases):
        if not cases or 'if' in cases[-1]:
            stmts = []
        else:
            stmts = [{'return': cases[-1]['value']}]
            cases = cases[:-1]
        for c in reversed(cases):
            stmts = [{'if': c['if'], 'then': [{'return': c['value']}], 'else': stmts}]
        return stmts

    def _param(self, p):
        if isinstance(p, dict):
            return dict(name=p['name'], mode=p.get('mode', 'value'), ctype='int', ptr=False, decl=p['name'])
        m = re.fullmatch(r'\s*(unsigned\s+int|int|char)\s*(\*?)\s*([A-Za-z_]\w*)\s*(\[\])?\s*', p)
        if not m:
            raise SystemExit(f'{self.qid}: cannot read parameter {p!r}')
        return dict(name=m.group(3), mode='value', ctype=m.group(1).split()[-1], ptr=bool(m.group(2) or m.group(4)), decl=p)

    def _prepare(self):
        """Parse every expression once."""
        def stmts(body):
            for s in body:
                if 'if' in s:
                    s['_cond'] = parse(s['if'], self.pascal)
                    stmts(s['then'])
                    stmts(s.get('else', []))
                elif 'return' in s:
                    s['_expr'] = parse(s['return'], self.pascal) if s['return'] is not None else None
                elif 'do' in s:
                    s['_expr'] = parse(s['do'], self.pascal)
                elif 'local' in s or 'static' in s:
                    for v in s['vars']:
                        if v[1] is not None and not v[1].startswith('{'):
                            v.append(parse(v[1], self.pascal))
                elif 'for' in s:
                    s['_for'] = [parse(x, self.pascal) for x in s['for']]
                    stmts(s['body'])
                elif 'while' in s:
                    s['_cond'] = parse(s['while'], self.pascal)
                    stmts(s['body'])
                else:
                    raise SystemExit(f'{self.qid}: unknown statement {s}')
        for f in self.funcs.values():
            stmts(f['body'])
            kinds, changed = set(), set()
            self._scan(f['body'], kinds, changed)
            params = {p['name'] for p in f['_params']}
            f['_statics'] = 'static' in kinds
            f['_locals'] = 'local' in kinds or bool(changed & params)
        if self.main:
            stmts(self.main)
        self.globals = []
        for g in self.spec.get('globals', []):
            self.globals.append(dict(g, _init=parse(g['init'], self.pascal) if g.get('init') else None))

    def _scan(self, body, kinds, changed):
        """Which declarations a body has and which names it assigns."""
        def names(e):
            if isinstance(e, Node):
                if e.k in ('assign', 'pre', 'post') and e.b.k == 'name':
                    changed.add(e.b.a)
                for x in (e.a, e.b, e.c):
                    names(x)
            elif isinstance(e, list):
                for x in e:
                    names(x)
        for s in body:
            kinds.update(k for k in ('local', 'static') if k in s)
            for key in ('_cond', '_expr', '_for'):
                names(s.get(key))
            for v in s.get('vars', []):
                names(v[2:] if len(v) > 2 else None)
            for key in ('then', 'else', 'body'):
                self._scan(s.get(key, []), kinds, changed)

    # ---- listing

    def _out(self, text, depth):
        self.lines.append('  ' * depth + text)
        return len(self.lines) - 1

    def _listing(self):
        if self.style == 'c':
            for g in self.spec.get('globals', []):
                self._out(f"{g['type']} {g['name']}" + (f" = {g['init']}" if g.get('init') else '') + ';', 0)
            for f in self.funcs.values():
                params = ', '.join(p['decl'] for p in f['_params'])
                self._out(f"{f['type']} {f['name']}({params}) {{", 0)
                self._c_block(f['body'], 1)
                self._out('}', 0)
            if self.main is not None:
                self._out('int main() {', 0)
                self._c_block(self.main, 1)
                self._out('}', 0)
        elif self.style == 'pascal':
            if self.spec.get('program'):
                self._out(f"program {self.spec['program']};", 0)
            for g in self.spec.get('globals', []):
                self._out(f"var {g['name']}: {g.get('type', 'integer')};", 0)
            for f in self.funcs.values():
                plist = ', '.join(('var ' if p['mode'] == 'ref' else '') + p['decl'] for p in f['_params'])
                if f.get('type'):
                    self._out(f"function {f['name']}({plist}: integer): integer;", 0)
                else:
                    self._out(f"procedure {f['name']}({plist});", 0)
                self._out('begin', 0)
                self._p_block(f['body'], 1, f)
                self._out('end;', 0)
            if self.main is not None:
                self._out('begin', 0)
                self._p_block(self.main, 1, None)
                self._out('end.', 0)
        else:
            for f in self.funcs.values():
                head = f"{f['name']}({', '.join(p['decl'] for p in f['_params'])}) := "
                self._m_cases(f, f['body'], head, len(head))

    def _simple(self, s):
        return 'return' in s or 'do' in s

    def _c_stmt_text(self, s):
        if 'return' in s:
            return 'return;' if s['return'] is None else f"return {s['return']};"
        return s['do'] + ';'

    def _c_block(self, body, depth):
        for s in body:
            self._c_stmt(s, depth)

    def _c_stmt(self, s, depth, prefix=''):
        if self._simple(s):
            s['_line'] = self._out(prefix + self._c_stmt_text(s), depth)
        elif 'local' in s or 'static' in s:
            parts = [v[0] + (f' = {v[1]}' if v[1] is not None else '') for v in s['vars']]
            kw = s.get('local') or 'static ' + s['static']
            s['_line'] = self._out(f"{kw} {', '.join(parts)};", depth)
        elif 'if' in s:
            then, other = s['then'], s.get('else', [])
            one = len(then) == 1 and self._simple(then[0]) and not s.get('brace')
            if one and s.get('split'):
                s['_line'] = self._out(f"{prefix}if ({s['if']})", depth)
                self._c_stmt(then[0], depth + 1)
            elif one:
                s['_line'] = self._out(f"{prefix}if ({s['if']}) {self._c_stmt_text(then[0])}", depth)
                then[0]['_line'] = s['_line']
            else:
                s['_line'] = self._out(f"{prefix}if ({s['if']}) {{", depth)
                self._c_block(then, depth + 1)
                if not other:
                    self._out('}', depth)
            if other:
                if not one:
                    if len(other) == 1 and 'if' in other[0]:
                        self.lines[-1:] = []
                        self._c_stmt(other[0], depth, prefix='} else ')
                        return
                    self._out('} else {', depth)
                    self._c_block(other, depth + 1)
                    self._out('}', depth)
                elif len(other) == 1 and 'if' in other[0]:
                    self._c_stmt(other[0], depth, prefix='else ')
                elif len(other) == 1 and self._simple(other[0]) and s.get('split'):
                    self._out('else', depth)
                    self._c_stmt(other[0], depth + 1)
                elif len(other) == 1 and self._simple(other[0]):
                    other[0]['_line'] = self._out('else ' + self._c_stmt_text(other[0]), depth)
                else:
                    self._out('else {', depth)
                    self._c_block(other, depth + 1)
                    self._out('}', depth)
        elif 'for' in s:
            a, b, c = s['for']
            s['_line'] = self._out(f'for ({a}; {b}; {c})' + (' {' if len(s['body']) > 1 else ''), depth)
            self._c_block(s['body'], depth + 1)
            if len(s['body']) > 1:
                self._out('}', depth)
        elif 'while' in s:
            s['_line'] = self._out(f"while ({s['while']})" + (' {' if len(s['body']) > 1 else ''), depth)
            self._c_block(s['body'], depth + 1)
            if len(s['body']) > 1:
                self._out('}', depth)

    def _p_text(self, s, f):
        if 'return' in s:
            if f is None or not f.get('type'):
                raise SystemExit(f'{self.qid}: a Pascal procedure has no result')
            return f"{f['name']} := {s['return']}"
        return s['do']

    def _p_block(self, body, depth, f):
        for k, s in enumerate(body):
            last = k == len(body) - 1
            if 'return' in s and not last:
                raise SystemExit(f'{self.qid}: a Pascal result assignment must end its block')
            self._p_stmt(s, depth, f, '' if last else ';')

    def _p_stmt(self, s, depth, f, end, prefix=''):
        if self._simple(s):
            s['_line'] = self._out(prefix + self._p_text(s, f) + end, depth)
        elif 'if' in s:
            then, other = s['then'], s.get('else', [])
            if len(then) == 1 and self._simple(then[0]):
                s['_line'] = self._out(f"{prefix}if {s['if']} then", depth)
                self._p_stmt(then[0], depth + 1, f, '' if other else end)
            else:
                s['_line'] = self._out(f"{prefix}if {s['if']} then begin", depth)
                self._p_block(then, depth + 1, f)
                self._out('end' + ('' if other else end), depth)
            if other:
                if len(other) == 1 and 'if' in other[0]:
                    self._p_stmt(other[0], depth, f, end, prefix='else ')
                elif len(other) == 1 and self._simple(other[0]):
                    self._out('else', depth)
                    self._p_stmt(other[0], depth + 1, f, end)
                else:
                    self._out('else begin', depth)
                    self._p_block(other, depth + 1, f)
                    self._out('end' + end, depth)
        else:
            raise SystemExit(f'{self.qid}: unsupported Pascal statement {s}')

    def _m_cases(self, f, body, head, pad):
        first = True
        while body:
            s = body[0]
            lead = head if first else ' ' * pad + 'else '
            if 'if' in s:
                s['_line'] = self._out(f"{lead}if {s['if']} then {s['then'][0]['return']}", 0)
                s['then'][0]['_line'] = s['_line']
                body = s.get('else', [])
            else:
                s['_line'] = self._out(lead + s['return'], 0)
                body = []
            first = False


# ---------------------------------------------------------------- running it


class CallNode:
    """One call: what it did, in order, and its result."""

    def __init__(self, fname, label, parent):
        self.fname, self.label, self.parent = fname, label, parent
        self.items = []        # ('act', text) | ('print', text) | ('call', CallNode), each with the listing line
        self.value = None
        self.ret = None        # dict(expl, cond, line, tail) for a return statement
        self.calls = 1         # calls in this subtree, this one included
        self.enter = self.exit = None   # snapshots of the variables
        self.sig = None


class Frame:
    def __init__(self, func, node):
        self.func, self.node = func, node
        self.vars = {}
        self.conds = []
        self.line = None


class Machine:
    def __init__(self, prog, quiet=False, memo=None):
        self.p, self.quiet, self.memo = prog, quiet, memo
        self.globals, self.statics, self.shown = {}, {}, []
        self.collect, self.out = [], []
        self.input = list(prog.spec.get('input', ''))
        self.calls = self.depth = 0
        self.order = prog.spec.get('arg_order')
        if self.order not in (None, 'right-to-left', 'left-to-right'):
            raise SystemExit(f'{prog.qid}: unknown arg_order {self.order}')
        for g in prog.globals:
            o = Obj(g['name'], [None], 'var', 'int')
            self.globals[g['name']] = o
            self.shown.append((g['name'], o))
            if g['_init'] is not None:
                o.cells[0] = self.ev(g['_init'], None, {})

    # ---- effects, to catch results that depend on the order of evaluation

    def _note(self, slot, item):
        for c in self.collect:
            c[slot].add(item)

    def _unordered(self, thunks, what):
        """Evaluate operands whose order C leaves unspecified, left to right, and stop the
        build if another order could give a different result."""
        sets, vals = [], []
        for t in thunks:
            c = (set(), set(), set())
            self.collect.append(c)
            try:
                vals.append(t())
            finally:
                self.collect.pop()
            sets.append(c)
            for outer in self.collect:
                for k in range(3):
                    outer[k].update(c[k])
        for i in range(len(sets)):
            for j in range(i + 1, len(sets)):
                ri, wi, oi = sets[i]
                rj, wj, oj = sets[j]
                if (wi & (rj | wj)) or (wj & ri) or (oi and oj):
                    raise SystemExit(f'{self.p.qid}: the result of {what} depends on the order of evaluation, which C leaves unspecified')
        return vals

    # ---- variables

    def lookup(self, frame, name):
        if frame is not None and name in frame.vars:
            o = frame.vars[name]
            return o.obj if isinstance(o, Ref) else o
        if frame is not None and (frame.func['name'], name) in self.statics:
            return self.statics[(frame.func['name'], name)]
        if name in self.globals:
            return self.globals[name]
        raise SystemExit(f'{self.p.qid}: unknown variable {name}')

    def load(self, obj, i):
        if not 0 <= i < len(obj.cells):
            raise SystemExit(f'{self.p.qid}: reads outside {obj.name}')
        self._note(0, (obj.uid, i))
        v = obj.cells[i]
        if v is None:
            raise SystemExit(f'{self.p.qid}: reads {obj.name} before it is set')
        return v

    def store(self, obj, i, v):
        if not 0 <= i < len(obj.cells):
            raise SystemExit(f'{self.p.qid}: writes outside {obj.name}')
        if obj.kind == 'string':
            raise SystemExit(f'{self.p.qid}: writes into a string literal')
        if isinstance(v, int) and obj.ctype == 'char' and not -128 <= v <= 127:
            raise SystemExit(f'{self.p.qid}: {v} does not fit in a char')
        self._note(1, (obj.uid, i))
        obj.cells[i] = v

    def lvalue(self, e, frame, rec):
        if e.k == 'paren':
            return self.lvalue(e.a, frame, rec)
        if e.k == 'name':
            o = self.lookup(frame, e.a)
            if o.kind == 'array':
                raise SystemExit(f'{self.p.qid}: cannot assign to the array {e.a}')
            return o, 0
        if e.k == 'deref':
            p = self.ev(e.a, frame, rec)
        elif e.k == 'index':
            base, idx = self._unordered([lambda: self.ev(e.a, frame, rec), lambda: self.ev(e.b, frame, rec)], 'an index')
            p = self._arith('+', base, idx)
        else:
            raise SystemExit(f'{self.p.qid}: {show(e)} cannot be assigned')
        if not isinstance(p, Ptr):
            raise SystemExit(f'{self.p.qid}: {show(e)} is not a pointer')
        return p.obj, p.idx

    def _lname(self, e, frame, rec):
        """How a note names the variable an assignment changes."""
        while e.k == 'paren':
            e = e.a
        if e.k == 'name':
            v = frame.vars.get(e.a) if frame else None
            return f'{v.obj.name} (through {e.a})' if isinstance(v, Ref) else e.a
        p = None
        if e.k == 'deref':
            p = rec.get(id(e.a))
        elif e.k == 'index' and isinstance(rec.get(id(e.a)), Ptr) and isinstance(rec.get(id(e.b)), int):
            p = Ptr(rec[id(e.a)].obj, rec[id(e.a)].idx + rec[id(e.b)])
        if isinstance(p, Ptr):
            target = p.obj.name if p.obj.kind == 'var' else f'{p.obj.name}[{p.idx}]'
            return f'{target} (through {show(e)})' if p.obj.kind == 'var' else target
        return show(e)

    # ---- expressions

    def ev(self, e, frame, rec):
        v = self._ev(e, frame, rec)
        rec[id(e)] = v
        return v

    def _ev(self, e, frame, rec):
        k = e.k
        if k in ('num', 'chr'):
            return e.a
        if k == 'str':
            return Ptr(Obj('string', [ord(c) for c in e.a] + [0], 'string', 'char'), 0)
        if k == 'name':
            o = self.lookup(frame, e.a)
            return Ptr(o, 0) if o.kind == 'array' else self.load(o, 0)
        if k == 'paren':
            return self.ev(e.a, frame, rec)
        if k in ('deref', 'index'):
            return self.load(*self.lvalue(e, frame, rec))
        if k == 'un' and e.a == '&':
            o, i = self.lvalue(e.b, frame, rec)
            if o.kind != 'var':
                raise SystemExit(f'{self.p.qid}: & is only supported for plain variables')
            return Ptr(o, i)
        if k == 'un':
            v = self.ev(e.b, frame, rec)
            return int(not v) if e.a == '!' else _int(-v, self.p.qid)
        if k in ('pre', 'post'):
            o, i = self.lvalue(e.b, frame, rec)
            old = self.load(o, i)
            new = self._arith('+' if e.a == '++' else '-', old, 1)
            self.store(o, i, new)
            self._act(frame, f'{self._lname(e.b, frame, rec)} = {value_text(new, o.ctype)}')
            return new if k == 'pre' else old
        if k == 'assign':
            (o, i), r = self._unordered([lambda: self.lvalue(e.b, frame, rec), lambda: self.ev(e.c, frame, rec)], 'an assignment')
            v = r if e.a in ('=', ':=') else self._arith(e.a[0], self.load(o, i), r)
            self.store(o, i, v)
            name = self._lname(e.b, frame, rec)
            if e.a in ('=', ':=') and not (e.c.k == 'call' and e.c.a == 'getchar'):
                text = f'{name} = {explain(e.c, rec, v, o.ctype)}'
            else:
                text = f'{name} = {value_text(v, o.ctype)}'
            self._act(frame, text)
            return v
        if k == 'bin':
            op = e.a
            if op in ('&&', '||'):
                left = self.ev(e.b, frame, rec)
                if (op == '&&') != bool(left):
                    return int(bool(left))
                return int(bool(self.ev(e.c, frame, rec)))
            a, b = self._unordered([lambda: self.ev(e.b, frame, rec), lambda: self.ev(e.c, frame, rec)], show(e))
            return self._arith(op, a, b)
        if k == 'call':
            return self.call(e, frame, rec)
        raise SystemExit(f'{self.p.qid}: cannot evaluate {k}')

    def _arith(self, op, a, b):
        what = self.p.qid
        if isinstance(a, Ptr) or isinstance(b, Ptr):
            if op in ('+', '-') and isinstance(a, Ptr) and isinstance(b, int):
                idx = a.idx + (b if op == '+' else -b)
                if not 0 <= idx <= len(a.obj.cells):
                    raise SystemExit(f'{what}: a pointer leaves {a.obj.name}')
                return Ptr(a.obj, idx)
            raise SystemExit(f'{what}: unsupported pointer arithmetic')
        if op == '+':
            return _int(a + b, what)
        if op == '-':
            return _int(a - b, what)
        if op == '*':
            return _int(a * b, what)
        if op in ('/', 'div'):
            return _int(_div(a, b, what), what)
        if op in ('%', 'mod'):
            return _int(a - b * _div(a, b, what), what)
        return int({'==': a == b, '=': a == b, '!=': a != b, '<>': a != b, '<': a < b, '<=': a <= b,
                    '>': a > b, '>=': a >= b}[op])

    # ---- calls

    def _act(self, frame, text, kind='act'):
        if frame is not None and not self.quiet:
            frame.node.items.append((kind, text, frame.line))

    def _args(self, e, frame, rec, params=None):
        thunks = []
        for k, a in enumerate(e.b):
            if params and params[k]['mode'] == 'ref':
                if a.k != 'name':
                    raise SystemExit(f'{self.p.qid}: a variable parameter needs a variable')
                thunks.append(lambda a=a: Ref(self.lookup(frame, a.a)))
            else:
                thunks.append(lambda a=a: self.ev(a, frame, rec))
        if self.order == 'right-to-left':
            return [t() for t in reversed(thunks)][::-1]
        if self.order == 'left-to-right':
            return [t() for t in thunks]
        return self._unordered(thunks, f'the arguments of {e.a}')

    def _builtin(self, e, frame, rec):
        name, what = e.a, self.p.qid
        if name == 'getchar':
            self._note(2, 'io')
            if not self.input:
                raise SystemExit(f'{what}: getchar() reads past the input')
            c = ord(self.input.pop(0))
            self._act(frame, f'reads {char_text(c)}', 'read')
            return c
        args = self._args(e, frame, rec)
        if name in ('max', 'min'):
            if len(args) != 2:
                raise SystemExit(f'{what}: {name} takes two arguments')
            return max(args) if name == 'max' else min(args)
        self._note(2, 'io')
        if name == 'putchar':
            text = chr(args[0])
        elif name in ('writeln', 'write'):
            text = ''.join(str(a) for a in args) + ('\n' if name == 'writeln' else '')
        else:
            fmt, rest = args[0], list(args[1:])
            if not isinstance(fmt, Ptr) or fmt.obj.kind != 'string' or fmt.idx:
                raise SystemExit(f'{what}: printf needs a format string')

            def conv(m):
                if m.group(0) == '%%':
                    return '%'
                if not rest or not isinstance(rest[0], int):
                    raise SystemExit(f'{what}: printf has too few arguments')
                v = rest.pop(0)
                return chr(v) if m.group(1) == 'c' else str(v)
            text = re.sub(r'%%|%([duc])', conv, ''.join(chr(c) for c in fmt.obj.cells[:-1]))
            if rest or re.search(r'%(?![duc%])', text):
                raise SystemExit(f'{what}: unsupported printf call')
        self.out.append(text)
        if frame is not None and not self.quiet:
            frame.node.items.append(('print', text, frame.line))
        return len(text) if name == 'printf' else args[0] if name == 'putchar' else None

    def call(self, e, frame, rec):
        if e.a not in self.p.funcs:
            if e.a in BUILTINS:
                return self._builtin(e, frame, rec)
            raise SystemExit(f'{self.p.qid}: unknown function {e.a}')
        f = self.p.funcs[e.a]
        params = f['_params']
        if len(e.b) != len(params):
            raise SystemExit(f'{self.p.qid}: {e.a} takes {len(params)} arguments')
        args = self._args(e, frame, rec, params)
        labels = [a.obj.name if isinstance(a, Ref) else value_text(a, 'int' if p['ptr'] else p['ctype']) for a, p in zip(args, params)]
        rec[('args', id(e))] = labels
        return self.invoke(f, args, labels, frame)

    def invoke(self, f, args, labels, caller):
        key = None
        if self.memo is not None:
            key = (f['name'], tuple(args))
            if key in self.memo:
                return self.memo[key]
        self.calls += 1
        self.depth += 1
        if self.calls > MAX_CALLS or self.depth > MAX_DEPTH:
            raise SystemExit(f'{self.p.qid}: too many or too deep calls; the program may not terminate')
        node = CallNode(f['name'], f"{f['name']}({', '.join(labels)})", caller.node if caller else None)
        if caller is not None and not self.quiet:
            caller.node.items.append(('call', node, caller.line))
        fr = Frame(f, node)
        for p, a in zip(f['_params'], args):
            if isinstance(a, Ref):
                fr.vars[p['name']] = a
                self._act(fr, f"{p['name']} is another name for {a.obj.name}", 'say')
            else:
                if p['ptr'] != isinstance(a, Ptr):
                    raise SystemExit(f"{self.p.qid}: {f['name']} gets the wrong kind of argument for {p['name']}")
                fr.vars[p['name']] = Obj(p['name'], [a], 'var', p['ctype'])
        node.enter = self.snap(fr)
        try:
            self.block(f['body'], fr)
            if f.get('type') not in (None, 'void'):
                raise SystemExit(f'{self.p.qid}: {node.label} ends without returning a value')
            value = None
        except _Return as r:
            value = r.value
        self.depth -= 1
        node.value = value
        node.exit = self.snap(fr)
        if key is not None:
            self.memo[key] = value
        return value

    def run_main(self):
        node = CallNode('main', 'main', None)
        fr = Frame(dict(name='main', body=self.p.main, type='int', _params=[]), node)
        self.main_frame = fr
        node.enter = self.snap(fr)
        try:
            self.block(self.p.main, fr)
        except _Return as r:
            node.value = r.value
            node.ret = None
        node.exit = self.snap(fr)
        return node

    def run_call(self, text):
        e = parse(text, self.p.pascal)
        if e.k != 'call' or e.a not in self.p.funcs:
            raise SystemExit(f'{self.p.qid}: {text} is not a call of a listed function')
        rec = {}
        args = [self.ev(a, None, rec) for a in e.b]
        holder = Frame(dict(name=''), CallNode('', '', None))
        self.invoke(self.p.funcs[e.a], args, [value_text(a) for a in args], holder)
        node = holder.node.items[0][1]
        node.parent = None
        return node

    # ---- statements

    def block(self, body, fr):
        for s in body:
            self.stmt(s, fr)

    def stmt(self, s, fr):
        fr.line = s.get('_line')
        rec = {}
        if 'if' in s:
            if self.ev(s['_cond'], fr, rec):
                fr.conds.append((s['_cond'], rec, s['then']))
                try:
                    self.block(s['then'], fr)
                finally:
                    fr.conds.pop()
            else:
                self.block(s.get('else', []), fr)
        elif 'return' in s:
            e = s['_expr']
            value = self.ev(e, fr, rec) if e is not None else None
            fr.line = s.get('_line')
            if not self.quiet and fr.func['name'] != 'main':
                inner = e
                while inner is not None and inner.k == 'paren':
                    inner = inner.a
                tail = inner is not None and inner.k == 'call' and inner.a in self.p.funcs
                cond = fr.conds[-1] if fr.conds and any(x is s for x in fr.conds[-1][2]) else None
                fr.node.ret = dict(expl=explain(e, rec, value) if e is not None else None, line=s.get('_line'), tail=tail,
                                   cond=_cond_text(cond) if cond else None)
            raise _Return(value)
        elif 'do' in s:
            self.ev(s['_expr'], fr, rec)
        elif 'local' in s or 'static' in s:
            ctype = (s.get('local') or s['static']).split()[-1]
            for v in s['vars']:
                name, arr = v[0].rstrip('[]'), v[0].endswith('[]')
                if 'static' in s:
                    key = (fr.func['name'], name)
                    if key not in self.statics:
                        if v[1] is None or not re.fullmatch(r'-?\d+', v[1]):
                            raise SystemExit(f'{self.p.qid}: a static needs a constant initialiser')
                        o = Obj(name, [int(v[1])], 'var', ctype)
                        self.statics[key] = o
                        self.shown.append((f"{fr.func['name']}: static {name}", o))
                    continue
                if arr:
                    items = [x.strip() for x in v[1].strip('{}').split(',')]
                    o = Obj(name, [int(x) for x in items], 'array', ctype)
                else:
                    o = Obj(name, [None], 'var', ctype)
                fr.vars[name] = o
                if fr.func['name'] == 'main':
                    self.shown.append((name, o))
                if arr:
                    self._act(fr, f'{name} = {{{", ".join(items)}}}')
                elif v[1] is not None:
                    val = self.ev(v[2], fr, rec)
                    self.store(o, 0, val)
                    self._act(fr, f'{name} = {explain(v[2], rec, val, ctype)}')
        elif 'for' in s:
            init, cond, step = s['_for']
            self.ev(init, fr, rec)
            while True:
                fr.line = s.get('_line')
                if not self.ev(cond, fr, {}):
                    break
                self.block(s['body'], fr)
                fr.line = s.get('_line')
                self.ev(step, fr, {})
        elif 'while' in s:
            while True:
                fr.line = s.get('_line')
                if not self.ev(s['_cond'], fr, {}):
                    break
                self.block(s['body'], fr)

    # ---- what a step shows

    def snap(self, fr):
        """The variables worth showing: globals, statics, main's variables, the input left,
        and the active call's own variables when its function changes or declares any."""
        if self.quiet:
            return None
        rows = []
        ptrs = [o.cells[0] for o in fr.vars.values() if isinstance(o, Obj) and isinstance(o.cells[0], Ptr)]
        for label, o in self.shown:
            if o.kind == 'array':
                at = next((p.idx for p in ptrs if p.obj is o), None)
                rows.append(dict(k=label, arr=[value_text(x, o.ctype) for x in o.cells], at=at))
            else:
                rows.append(dict(k=label, v=value_text(o.cells[0], o.ctype) if o.cells[0] is not None else '?'))
        if self.p.spec.get('input') is not None:
            left = ''.join(self.input).replace('\n', '↵')
            rows.append(dict(k='input left', v=left or '(none)'))
        if fr.func['name'] != 'main' and fr.func.get('_locals'):
            for name, o in fr.vars.items():
                if isinstance(o, Obj) and not isinstance(o.cells[0], Ptr) and o.kind == 'var':
                    rows.append(dict(k=name, v=value_text(o.cells[0], o.ctype) if o.cells[0] is not None else '?', own=1))
        return rows


BUILTINS = ('getchar', 'max', 'min', 'printf', 'putchar', 'writeln', 'write')


def _cond_text(cond):
    """The part of a true condition that holds: for 'a or b', the first true one."""
    e, rec = cond[0], cond[1]
    while e.k == 'paren':
        e = e.a
    if e.k == 'bin' and e.a == '||':
        for side in (e.b, e.c):
            if rec.get(id(side)):
                return _cond_text((side, rec))
    return _strip(show(e))


# ---------------------------------------------------------------- the call tree as steps

def _sig(node):
    """Everything a call did; two calls with the same signature behaved identically."""
    if node.sig is None:
        parts = [node.label]
        for it in node.items:
            parts.append('[' + _sig(it[1]) + ']' if it[0] == 'call' else it[0] + ':' + it[1])
        parts.append('=' + value_text(node.value))
        node.sig = '|'.join(parts)
    return node.sig


def _count(node):
    node.calls = 1 + sum(_count(it[1]) for it in node.items if it[0] == 'call')
    return node.calls


def _output_of(node):
    return ''.join(it[1] if it[0] == 'print' else _output_of(it[1]) if it[0] == 'call' else '' for it in node.items)


def _nodes_of(node):
    yield node
    for it in node.items:
        if it[0] == 'call':
            yield from _nodes_of(it[1])


def _printed(text):
    if text == '\n':
        return 'a newline'
    if text.endswith('\n'):
        return f'"{text[:-1]}" and a newline'
    return f'"{text}"'


def _join(parts):
    return parts[0] if len(parts) == 1 else ', '.join(parts[:-1]) + ' and ' + parts[-1]


def _phrase(acts):
    """Group consecutive assignments: 'sets n = 2 and i = 2, prints "5"'."""
    out, sets = [], []
    for kind, text in acts:
        if kind == 'act':
            sets.append(text)
            continue
        if sets:
            out.append('sets ' + _join(sets))
            sets = []
        out.append(f'prints {_printed(text)}' if kind == 'print' else text)
    if sets:
        out.append('sets ' + _join(sets))
    return out


class Steps:
    """Walk the finished call tree in execution order: one step per call and per return."""

    def __init__(self, root, collapse, fold):
        self.root, self.collapse, self.fold = root, collapse, set(fold or [])
        self.nodes, self.steps, self.status = [], [], []
        self.calls, self.out, self.seen = 0, '', set()

    def add(self, node, kind, parent):
        self.nodes.append(dict(p=parent, label=node.label, v=None, kind=kind))
        self.status.append('a')
        return len(self.nodes) - 1

    def emit(self, active, line, note, fresh, snap, own=True, **extra):
        rows = [r for r in (snap or []) if own or not r.get('own')]
        self.steps.append(dict(n=len(self.nodes), st=''.join(self.status), act=active, line=line, calls=self.calls,
                               out=self.out, fresh=fresh, vars=rows, note=note, **extra))

    def activate(self, idx):
        self.status = ['w' if c == 'a' else c for c in self.status]
        self.status[idx] = 'a'

    def run(self):
        root = self.root
        self.add(root, 'call', None)
        if root.fname != 'main':
            self.calls = 1
        self.emit(0, None, 'Start: main runs.' if root.fname == 'main' else f'Start: the first call is {root.label}.', 0, root.enter)
        self.walk(root, 0)
        return self.nodes, self.steps

    def walk(self, node, idx):
        acts, fresh = [], 0
        for kind, payload, line in node.items:
            if kind == 'say':
                continue
            if kind != 'call':
                acts.append((kind, payload))
                if kind == 'print':
                    self.out += payload
                    fresh += len(payload)
                continue
            child, lead = payload, self.lead(node, acts)
            sig = _sig(child)
            repeat = self.collapse and child.calls > 1 and sig in self.seen
            folded = child.fname in self.fold
            cidx = self.add(child, 'repeat' if repeat else 'fold' if folded else 'call', idx)
            self.activate(cidx)
            if repeat or folded:
                self.calls += child.calls
                out = _output_of(child)
                self.out += out
                self.status[cidx] = 'd'
                self.nodes[cidx].update(v=value_text(child.value) if child.value is not None else None, calls=child.calls)
                if repeat:
                    what = f'it was worked out before with the same arguments, so it repeats those {child.calls} calls'
                else:
                    what = f'it makes {child.calls} call{"s" if child.calls > 1 else ""} of {child.fname} in all'
                    chain = self.chain(child)
                    if chain:
                        what += f' (down to {chain})'
                if out:
                    what += f', prints {_printed(out)}'
                what += f' and returns {value_text(child.value)}' if child.value is not None else ' and returns'
                self.status[idx] = 'a'
                self.emit(cidx, line, f'{lead}calls {child.label}: {what}.', fresh + len(out), child.exit, own=False)
            else:
                self.seen.add(sig)
                self.calls += 1
                says = [it[1] for it in child.items if it[0] == 'say']
                where = f'; in it, {_join(says)}' if says else ''
                self.emit(cidx, line, f'{lead}calls {child.label}{where}.', fresh, child.enter)
                self.walk(child, cidx)
                self.status[idx] = 'a'
            acts, fresh = [], 0
        self.finish(node, idx, acts, fresh)

    def finish(self, node, idx, acts, fresh):
        r = node.ret or {}
        self.status = ['w' if c == 'a' else c for c in self.status]
        self.status[idx] = 'd'
        if node.value is not None:
            self.nodes[idx]['v'] = value_text(node.value)
        lead = self.lead(node, acts)
        if node.fname == 'main':
            self.emit(idx, r.get('line'), f'{lead}ends.' if acts else 'main ends.', fresh, node.exit)
            return
        why = f', since {r["cond"]}' if r.get('cond') else ''
        prev = self.steps[-1]
        # Calls that only pass a child's result back up are shown together.
        chain = prev.get('_chain')
        if r.get('tail') and not acts and chain and self.nodes[chain[-1]]['p'] == idx and prev.get('_value') == node.value:
            chain.append(idx)
            labels = [self.nodes[k]['label'] for k in chain[1:]]
            prev.update(st=''.join(self.status), act=idx, line=r.get('line'), vars=[x for x in node.exit or [] if not x.get('own')],
                        note=f"{prev['_first']} The waiting calls then pass {value_text(node.value)} back up: "
                             + (labels[0] if len(labels) == 1 else f'{labels[0]}, …, {labels[-1]} ({len(labels)} calls)') + ' each return it.')
        elif node.ret is None:
            self.emit(idx, None, f'{lead}returns.' if acts else f'{node.label} ends and returns.', fresh, node.exit)
        else:
            note = f'{lead}returns{" " + r["expl"] if r.get("expl") else ""}{why}.'
            self.emit(idx, r.get('line'), note, fresh, node.exit, _chain=[idx], _value=node.value, _first=note)
        parent = self.nodes[idx]['p']
        if parent is not None:
            self.status[parent] = 'a'

    @staticmethod
    def lead(node, acts):
        words = _phrase(acts)
        return f'{node.label} {_join(words)}, then ' if words else f'{node.label} '

    @staticmethod
    def chain(node):
        """The deepest call, when the folded calls form a single chain."""
        cur = node
        while True:
            kids = [it[1] for it in cur.items if it[0] == 'call']
            if not kids:
                return cur.label if cur is not node else None
            if len(kids) > 1:
                return None
            cur = kids[0]


def _tree_text(node):
    kids = [it[1] for it in node.items if it[0] == 'call']
    return node.fname + ('[' + ', '.join(_tree_text(k) for k in kids) + ']' if kids else '')


def _tokens_of(text):
    return [t for t in re.split(r'[\s,]+', text) if t]


def trace(prog, entry=None):
    """Run the program once: (machine, root call)."""
    m = Machine(prog)
    root = m.run_main() if entry is None and prog.main is not None else m.run_call(entry or prog.spec['call'])
    _count(root)
    return m, root


def _search(prog, sr):
    """The smallest value of sr['var'] from sr['from'] up for which sr['call'] returns sr['value'].
    Results are reused between tries, which is sound because the functions must not print,
    read input or touch anything but their own variables (checked on every call)."""
    memo = {}
    m = Machine(prog, quiet=True, memo=memo)
    if prog.globals or prog.spec.get('input'):
        raise SystemExit(f'{prog.qid}: the search needs functions without globals or input')
    for f in prog.funcs.values():
        if f.get('_statics') or any(p['ptr'] or p['mode'] == 'ref' for p in f['_params']):
            raise SystemExit(f'{prog.qid}: the search needs functions of plain values')
    n = sr['from']
    # Parse the call once. An argument that is just the search variable takes n directly;
    # anything else is evaluated from the call text with n substituted, as before.
    template = parse(sr['call'], prog.pascal)
    direct = all(a.k == 'name' and a.a == sr['var'] for a in template.b)
    while n < 10 ** 6:
        m.calls = 0
        if direct:
            e, args = template, [n] * len(template.b)
        else:
            e = parse(sr['call'].replace(sr['var'], str(n)), prog.pascal)
            args = [m.ev(a, None, {}) for a in e.b]
        if m.out:
            raise SystemExit(f'{prog.qid}: the search needs functions that do not print')
        if m.invoke(prog.funcs[e.a], args, [], None) == sr['value']:
            return n
        n += 1
    raise SystemExit(f'{prog.qid}: no {sr["var"]} found')


def build(prog, entry=None):
    m, root = trace(prog, entry)
    total = root.calls - (root.fname == 'main')
    collapse = total > COLLAPSE_OVER
    nodes, steps = Steps(root, collapse, prog.spec.get('fold')).run()
    for s in steps:
        for k in ('_chain', '_value', '_first'):
            s.pop(k, None)
    if len(steps) > MAX_STEPS:
        raise SystemExit(f'{prog.qid}: {len(steps)} steps are too many to step through')
    return m, root, nodes, steps, collapse


def _check(qid, spec, prog, m, root, entry):
    """Compare the run with the expected answer; return the sentences that state it."""
    expect, facts = spec['expect'], []
    out = ''.join(m.out)
    for key, want in expect.items():
        if key in ('match', 'of'):
            continue
        if key == 'returns':
            if root.fname == 'main' or root.value != want:
                raise SystemExit(f'Animation for {qid}: {root.label} returns {root.value}, not {want}')
            facts.append(f'Answer: {value_text(want)}.')
        elif key == 'output':
            how = expect.get('match', 'exact')
            if how not in ('exact', 'tokens'):
                raise SystemExit(f'{qid}: unknown match {how}')
            if (out != want) if how == 'exact' else (_tokens_of(out) != _tokens_of(want)):
                raise SystemExit(f'Animation for {qid} prints {out!r}, not {want!r}')
            facts.append(f'The output is {out.rstrip(chr(10))}' + (' followed by a newline.' if out.endswith('\n') else '.'))
        elif key == 'calls':
            of = expect.get('of')
            got = sum(1 for n in _nodes_of(root) if (n.fname == of if of else n.fname != 'main'))
            if got != want:
                raise SystemExit(f'Animation for {qid} makes {got} calls{" of " + of if of else ""}, not {want}')
            facts.append(f'Answer: {got} calls{" of " + of if of else ""}, counting the first.')
        elif key == 'tree':
            got = _tree_text(root)
            if got.replace(' ', '') != want.replace(' ', ''):
                raise SystemExit(f'Animation for {qid} gives the activation tree {got}, not {want}')
            facts.append(f'Answer: the activation tree {got.replace(",", ", ")}, children in calling order.')
        elif key == 'smallest':
            sr = spec['search']
            got = _search(prog, sr)
            if got != want:
                raise SystemExit(f'Animation for {qid}: the smallest {sr["var"]} is {got}, not {want}')
            call = sr['call'].replace(sr['var'], str(want))
            if root.label.replace(' ', '') != call.replace(' ', '') or root.value != sr['value']:
                raise SystemExit(f'{qid}: the first run must trace {call}')
            facts.append(f'Every {sr["var"]} from {sr["from"]} to {want - 1} was also tried, and none gives {sr["value"]}. '
                         f'Answer: {want}.')
        else:
            raise SystemExit(f'{qid}: unknown expectation {key}')
    return facts


def recursion_animation(qid, spec):
    prog = Program(json.loads(json.dumps(spec['program'])), qid)
    schedules = []
    for k, entry in enumerate(spec.get('runs') or [None]):
        m, root, nodes, steps, collapsed = build(prog, entry)
        made = root.calls - (root.fname == 'main')
        if root.fname == 'main':
            last = f'Done: {made} call{"s" if made != 1 else ""} of the functions besides main.'
        else:
            last = f'Done: {made} call{"s" if made != 1 else ""} in all' + \
                (f', and {root.label} returns {value_text(root.value)}.' if root.value is not None else '.')
        facts = _check(qid, spec, prog, m, root, entry) if k == 0 else []
        if any(n['kind'] == 'repeat' for n in nodes):
            last += ' A dashed node repeats an earlier call with the same arguments.'
        if any(n['kind'] == 'fold' for n in nodes):
            last += f' Calls of {_join(sorted(set(prog.spec["fold"])))} are drawn as one node each.'
        note = ' '.join([last] + facts)
        steps.append(dict(steps[-1], note=note, final=True, fresh=0, line=None, act=None))
        label = root.label
        schedules.append(dict(short=label, title=('Calls made by ' if label == 'main' else 'Call tree of ') + label,
                              nodes=nodes, steps=steps))
    return dict(kind='call-tree', code=prog.lines, schedules=schedules, count=sum(len(s['steps']) for s in schedules))


KINDS = {'call-tree': recursion_animation}
PLAYER = 'recursion'
TABS = 'calls'
