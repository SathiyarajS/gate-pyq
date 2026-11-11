"""C program traces: what a short C program prints, one statement at a time.

Data: data/animations/ctrace.json. Each entry states the question's program and
the expected answer; the simulator runs the program and the build stops if the
result differs.

This is not a general C interpreter. A program is a list of top-level items in a
small structured form, and the listing on the page is printed from that same
structure, so it always shows exactly what was run:

  "#include <stdio.h>"                     a preprocessor line, shown only
  "int a, b, c = 0;"                       a declaration (also prototypes)
  {"func": "int f(int *p, int m)", "body": [...]}

Statements in a body:

  "x = x + 1;"  "int i = 0, *p;"  "return x;"  "break;"  "continue;"
      simple statements; several in one string share one listing line
  {"if": "a < c", "then": [...] or "stmt;", "else": [...] or "stmt;"}
  {"while": "x > 0", "body": [...] or "stmt;"}
  {"do": [...], "while": "x != y"}
  {"for": "i = 0; i < 5; i++", "body": [...] or "stmt;"}
  {"switch": "i + k", "body": ["case 1:", "case 2: printf(...);", "default: ...;"]}
  {"block": [...]}
  A non-list body goes on the next line, or on the same line with "inline": true.
  A trailing /* comment */ in a string is kept in the listing.

Expressions are C expressions read by a restricted parser (no casts, sizeof,
structs or function pointers). They are evaluated with C's rules for a 32-bit
int: integer division truncates toward zero, % takes the dividend's sign,
unsigned arithmetic wraps, char is a signed 8-bit type promoted to int, float
values are rounded to single precision. Anything the C standard leaves
undefined stops the build instead of producing a trace: signed overflow, reads
of unset variables, pointer arithmetic outside an array, two unsequenced writes
to one object (i++ + i++), printf arguments of the wrong type, division by zero.
If the result could depend on the unspecified order in which operands or
arguments are evaluated (two calls that touch the same variable), the entry must
say "order_independent": true, and the program is run again in the opposite
order; both runs must print the same thing.

Spec fields: program, and either nothing (run main), "call": "f(3, 4)" or
"calls": [...] (one tab each), optional "given": declarations made before the
call (not part of the listing), "builtins" ({"print": "%d "} for a question's
print(x) that writes its argument and a space, {"swap": "exchange"} for a swap()
the question describes but does not list), "size_t": "unsigned int", "assume"
(a sentence shown at the start), and "expect", one of:
  {"output": "..."}     the printed text (trailing newlines ignored)
  {"lines": [...]}      the printed lines, with runs of spaces read as one
  {"printf_count": n}   how many times printf runs
  {"return": v}         the value of the call
  {"final": {"j": 10}}  main's variables when main ends
  {"nonterminating": true}   the program reaches the same state twice in a loop
  {"claims": [{"call": "f(20, 10)", "op": ">", "than": 1048576, "holds": false}, ...]}
"""
import json
import re
import struct

# ---------------------------------------------------------------- types

INT, UINT, LONG, ULONG = ('int',), ('uint',), ('long',), ('ulong',)
CHAR, SHORT, FLOAT, DOUBLE, VOID = ('char',), ('short',), ('float',), ('double',), ('void',)
LIMITS = {'char': (8, True), 'short': (16, True), 'int': (32, True), 'uint': (32, False),
          'long': (64, True), 'ulong': (64, False)}
RANK = {'int': 1, 'uint': 1, 'long': 2, 'ulong': 2}
MAX_STEPS = 400
MAX_DEPTH = 40


def is_int(t):
    return t[0] in LIMITS


def is_float(t):
    return t[0] in ('float', 'double')


def is_arith(t):
    return is_int(t) or is_float(t)


def is_ptr(t):
    return t[0] == 'ptr'


def is_arr(t):
    return t[0] == 'arr'


def ncells(t):
    return t[2] * ncells(t[1]) if is_arr(t) else 1


def tname(t):
    if is_ptr(t):
        return tname(t[1]) + ' *'
    if is_arr(t):
        dims = []
        while is_arr(t):
            dims.append(f'[{t[2]}]')
            t = t[1]
        return tname(t) + ''.join(dims)
    return {'uint': 'unsigned int', 'ulong': 'unsigned long', 'long': 'long'}.get(t[0], t[0])


def promote(t):
    return INT if t[0] in ('char', 'short') else t


def common(a, b):
    if DOUBLE in (a, b):
        return DOUBLE
    if FLOAT in (a, b):
        return FLOAT
    a, b = promote(a), promote(b)
    if a == b:
        return a
    sa, sb = LIMITS[a[0]][1], LIMITS[b[0]][1]
    if sa == sb:
        return a if RANK[a[0]] >= RANK[b[0]] else b
    u, s = (b, a) if sa else (a, b)
    if RANK[u[0]] >= RANK[s[0]]:
        return u
    if LIMITS[s[0]][0] > LIMITS[u[0]][0]:
        return s
    return {'long': ULONG, 'int': UINT}[s[0]]


def fail(msg):
    raise SystemExit('ctrace: ' + msg)


def f32(v):
    try:
        return struct.unpack('f', struct.pack('f', v))[0]
    except (OverflowError, struct.error):
        fail(f'float overflow at {v}')


# ---------------------------------------------------------------- expressions

TOKEN = re.compile(r'''\s*(?:
  (?P<num>0[xX][0-9a-fA-F]+[uUlL]*|(?:\d+\.\d*|\.\d+|\d+)(?:[eE][+-]?\d+)?[uUlLfF]*)
 |(?P<chr>'(?:\\.|[^'\\])+')
 |(?P<str>"(?:\\.|[^"\\])*")
 |(?P<id>[A-Za-z_]\w*)
 |(?P<op><<=|>>=|\+\+|--|->|&&|\|\||<=|>=|==|!=|<<|>>|[-+*/%&|^]=|[-+*/%&|^~!<>=?:,()\[\]{};.])
)''', re.X)
BINARY = {'*': 13, '/': 13, '%': 13, '+': 12, '-': 12, '<<': 11, '>>': 11, '<': 10, '>': 10, '<=': 10,
          '>=': 10, '==': 9, '!=': 9, '&': 8, '^': 7, '|': 6, '&&': 5, '||': 4}
ASSIGN = {'=', '+=', '-=', '*=', '/=', '%=', '&=', '|=', '^=', '<<=', '>>='}
COMPARE = {'<', '>', '<=', '>=', '==', '!='}
ESCAPES = {'n': 10, 't': 9, '0': 0, '\\': 92, "'": 39, '"': 34, 'r': 13, 'a': 7, 'b': 8, 'f': 12, 'v': 11}
TYPE_WORDS = {'int', 'char', 'short', 'long', 'unsigned', 'signed', 'float', 'double', 'void'}
STORAGE = {'static', 'auto', 'register', 'const'}


def tokenize(text):
    toks, pos = [], 0
    text = text.rstrip()
    while pos < len(text):
        m = TOKEN.match(text, pos)
        if not m or m.end() == pos:
            fail(f'cannot read {text[pos:]!r}')
        kind = m.lastgroup
        toks.append((kind, m.group(kind)))
        pos = m.end()
        while pos < len(text) and text[pos].isspace():
            pos += 1
    return toks


def unescape(body):
    out, k = [], 0
    while k < len(body):
        ch = body[k]
        if ch == '\\':
            k += 1
            if body[k] not in ESCAPES:
                fail(f'unsupported escape \\{body[k]}')
            out.append(ESCAPES[body[k]])
        else:
            out.append(ord(ch))
        k += 1
    return out


class Node:
    """One expression node. k is the kind: num chr str name paren un post bin assign cond call index comma."""
    __slots__ = ('k', 'op', 'a', 'b', 'c', 'args', 'v')

    def __init__(self, k, op=None, a=None, b=None, c=None, args=None, v=None):
        self.k, self.op, self.a, self.b, self.c, self.args, self.v = k, op, a, b, c, args, v


class Parser:
    def __init__(self, toks):
        self.t, self.i = toks, 0

    def peek(self, k=0):
        j = self.i + k
        return self.t[j] if j < len(self.t) else (None, None)

    def take(self, want=None):
        tok = self.peek()
        if want is not None and tok[1] != want:
            fail(f'expected {want!r}, found {tok[1]!r}')
        self.i += 1
        return tok

    def at(self, *vals):
        return self.peek()[1] in vals and self.peek()[0] in ('op', 'id')

    def expr(self):
        n = self.assign()
        while self.at(','):
            self.take()
            n = Node('comma', a=n, b=self.assign())
        return n

    def assign(self):
        n = self.cond()
        if self.peek()[0] == 'op' and self.peek()[1] in ASSIGN:
            op = self.take()[1]
            if n.k not in ('name', 'un', 'index', 'paren') or (n.k == 'un' and n.op != '*'):
                fail('assignment to something that is not a variable')
            n = Node('assign', op, n, self.assign())
        return n

    def cond(self):
        n = self.binary(4)
        if self.at('?'):
            self.take()
            a = self.expr()
            self.take(':')
            n = Node('cond', a=n, b=a, c=self.cond())
        return n

    def binary(self, minp):
        n = self.unary()
        while True:
            kind, op = self.peek()
            if kind != 'op' or op not in BINARY or BINARY[op] < minp:
                return n
            self.take()
            n = Node('bin', op, n, self.binary(BINARY[op] + 1))

    def unary(self):
        kind, op = self.peek()
        if kind == 'op' and op in ('++', '--', '+', '-', '!', '~', '*', '&'):
            self.take()
            return Node('un', op, self.unary())
        if kind == 'id' and op == 'sizeof':
            fail('sizeof is not supported')
        if op == '(' and self.peek(1)[0] == 'id' and self.peek(1)[1] in TYPE_WORDS:
            fail('casts are not supported')
        return self.postfix()

    def postfix(self):
        n = self.primary()
        while True:
            if self.at('['):
                self.take()
                n = Node('index', a=n, b=self.expr())
                self.take(']')
            elif self.at('('):
                if n.k != 'name':
                    fail('only named functions can be called')
                self.take()
                args = []
                if not self.at(')'):
                    args.append(self.assign())
                    while self.at(','):
                        self.take()
                        args.append(self.assign())
                self.take(')')
                n = Node('call', a=n, args=args)
            elif self.at('++', '--'):
                n = Node('post', self.take()[1], n)
            elif self.at('.', '->'):
                fail('structures are not supported')
            else:
                return n

    def primary(self):
        kind, val = self.take()
        if kind == 'num':
            return Node('num', v=val)
        if kind == 'chr':
            codes = unescape(val[1:-1])
            if len(codes) != 1:
                fail(f'multi-character constant {val}')
            return Node('chr', v=val)
        if kind == 'str':
            text = val
            while self.peek()[0] == 'str':
                text = text[:-1] + self.take()[1][1:]
            return Node('str', v=text)
        if kind == 'id':
            if val in TYPE_WORDS or val in STORAGE:
                fail(f'unexpected type word {val}')
            return Node('name', v=val)
        if val == '(':
            n = self.expr()
            self.take(')')
            return Node('paren', a=n)
        fail(f'unexpected {val!r}')


def parse_expr(text):
    p = Parser(tokenize(text))
    n = p.expr()
    if p.i != len(p.t):
        fail(f'unexpected {p.peek()[1]!r} in {text!r}')
    return n


def show(n):
    """The expression as it is listed (and was run)."""
    k = n.k
    if k in ('num', 'chr', 'str', 'name'):
        return n.v
    if k == 'paren':
        return f'({show(n.a)})'
    if k == 'un':
        inner = show(n.a)
        sep = ' ' if inner[:1] == n.op[-1] and n.op in ('-', '+') else ''
        return n.op + sep + inner
    if k == 'post':
        return show(n.a) + n.op
    if k in ('bin', 'assign'):
        return f'{show(n.a)} {n.op} {show(n.b)}'
    if k == 'comma':
        return f'{show(n.a)}, {show(n.b)}'
    if k == 'cond':
        return f'{show(n.a)} ? {show(n.b)} : {show(n.c)}'
    if k == 'index':
        return f'{show(n.a)}[{show(n.b)}]'
    if k == 'call':
        return f'{show(n.a)}({", ".join(show(x) for x in n.args)})'
    fail(f'cannot show node {k}')


def strip_paren(n):
    while n.k == 'paren':
        n = n.a
    return n


# ---------------------------------------------------------------- declarations

class Declarator:
    __slots__ = ('name', 'stars', 'dims', 'init', 'params')

    def __init__(self, name, stars, dims, init, params=None):
        self.name, self.stars, self.dims, self.init, self.params = name, stars, dims, init, params


def base_type(words):
    ws = [w for w in words if w not in STORAGE]
    key = ' '.join(sorted(w for w in ws if w != 'signed'))
    table = {'int': INT, 'char': CHAR, 'short': SHORT, 'int short': SHORT, 'long': LONG, 'int long': LONG,
             'unsigned': UINT, 'int unsigned': UINT, 'long unsigned': ULONG, 'int long unsigned': ULONG,
             'float': FLOAT, 'double': DOUBLE, 'void': VOID}
    if key not in table:
        fail(f'unsupported type {" ".join(words)!r}')
    return table[key]


def parse_init(p):
    if p.at('{'):
        p.take()
        items = []
        while not p.at('}'):
            items.append(parse_init(p))
            if p.at(','):
                p.take()
            elif not p.at('}'):
                fail('bad initializer list')
        p.take('}')
        return items
    return p.assign()


def show_init(x):
    return '{' + ', '.join(show_init(y) for y in x) + '}' if isinstance(x, list) else show(x)


def parse_params(p):
    """The parameter list after '(' (which has been taken): [(words, Declarator)]."""
    params = []
    if p.at(')'):
        p.take()
        return params
    if p.at('void') and p.peek(1)[1] == ')':
        p.take()
        p.take()
        return params
    while True:
        words = []
        while p.peek()[0] == 'id' and (p.peek()[1] in TYPE_WORDS or p.peek()[1] in STORAGE):
            words.append(p.take()[1])
        if not words:
            fail('parameter without a type')
        stars = 0
        while p.at('*'):
            p.take()
            stars += 1
        name = p.take()[1] if p.peek()[0] == 'id' else None
        dims = []
        while p.at('['):
            p.take()
            dims.append(None if p.at(']') else p.take()[1])
            p.take(']')
        params.append((words, Declarator(name, stars, dims, None)))
        if p.at(','):
            p.take()
            continue
        p.take(')')
        return params


def parse_decl(text):
    """A declaration: (words, [Declarator])."""
    p = Parser(tokenize(text))
    words = []
    while p.peek()[0] == 'id' and (p.peek()[1] in TYPE_WORDS or p.peek()[1] in STORAGE):
        words.append(p.take()[1])
    decls = []
    while True:
        stars = 0
        while p.at('*'):
            p.take()
            stars += 1
        kind, name = p.take()
        if kind != 'id':
            fail(f'bad declaration {text!r}')
        dims, init, params = [], None, None
        if p.at('('):
            p.take()
            params = parse_params(p)
        while p.at('['):
            p.take()
            dims.append(None if p.at(']') else p.take()[1])
            p.take(']')
        if p.at('='):
            p.take()
            init = parse_init(p)
        decls.append(Declarator(name, stars, dims, init, params))
        if p.at(','):
            p.take()
            continue
        break
    if p.i != len(p.t):
        fail(f'unexpected {p.peek()[1]!r} in declaration {text!r}')
    return words, decls


def show_param(words, d):
    return ' '.join(words) + (' ' if d.name or d.stars else '') + '*' * d.stars + (d.name or '') + \
        ''.join(f'[{x or ""}]' for x in d.dims)


def show_decl(words, decls):
    def one(d):
        s = '*' * d.stars + d.name
        if d.params is not None:
            s += '(' + (', '.join(show_param(w, x) for w, x in d.params) or 'void') + ')'
        s += ''.join(f'[{x or ""}]' for x in d.dims)
        if d.init is not None:
            s += ' = ' + show_init(d.init)
        return s
    return ' '.join(words) + ' ' + ', '.join(one(d) for d in decls) + ';'


def decl_type(words, d, init=None):
    t = base_type(words)
    for _ in range(d.stars):
        t = ('ptr', t)
    dims = list(d.dims)
    for k in range(len(dims) - 1, -1, -1):
        n = dims[k]
        if n is None:
            if k != 0:
                fail('only the first array size may be left out')
            if isinstance(init, list):
                n = len(init)
            elif init is not None and strip_paren(init).k == 'str':
                n = len(unescape(strip_paren(init).v[1:-1])) + 1
            else:
                fail(f'size of {d.name} is missing')
        t = ('arr', t, int(n))
    return t


def parse_header(text):
    """A function header 'int f(int *p, int m)' or 'main()': (words, name, stars, params)."""
    p = Parser(tokenize(text))
    words = []
    while p.peek()[0] == 'id' and (p.peek()[1] in TYPE_WORDS or p.peek()[1] in STORAGE):
        words.append(p.take()[1])
    stars = 0
    while p.at('*'):
        p.take()
        stars += 1
    name = p.take()[1]
    p.take('(')
    params = parse_params(p)
    if p.i != len(p.t):
        fail(f'bad function header {text!r}')
    return words, name, stars, params




def param_type(words, d):
    t = base_type(words)
    for _ in range(d.stars):
        t = ('ptr', t)
    if d.dims:
        for n in reversed(d.dims[1:]):
            if n is None:
                fail('only the first array size may be left out')
            t = ('arr', t, int(n))
        t = ('ptr', t)
    return t


# ---------------------------------------------------------------- statements

class S:
    """A statement. kind: decl proto expr return break continue empty label if while do for switch block.
    Compound statements keep their bodies as lists of groups; a group is the statements of one listing line."""

    def __init__(self, kind, **kw):
        self.kind, self.line, self.text, self.comment = kind, None, '', ''
        self.__dict__.update(kw)


COMMENT = re.compile(r'\s*(/\*.*?\*/|//.*)$')
COMPOUND = {'if', 'while', 'for', 'do', 'switch', 'block'}


def split_simple(text):
    """Split 'a=5; b=11;' at top-level semicolons."""
    parts, depth, cur, q, esc = [], 0, '', None, False
    for ch in text:
        cur += ch
        if q:
            if esc:
                esc = False
            elif ch == '\\':
                esc = True
            elif ch == q:
                q = None
            continue
        if ch in '"\'':
            q = ch
        elif ch in '([{':
            depth += 1
        elif ch in ')]}':
            depth -= 1
        elif ch == ';' and depth == 0:
            parts.append(cur.strip())
            cur = ''
    if cur.strip():
        fail(f'statement without a semicolon: {cur.strip()!r}')
    return parts


def simple(text):
    """One listing line of simple statements, with optional leading case labels and a trailing comment."""
    comment = ''
    m = COMMENT.search(text)
    if m:
        comment, text = m.group(1), text[:m.start()]
    out = []
    while True:
        m = re.match(r'\s*(?:case\s+([^:]+)|default)\s*:\s*', text)
        if not m:
            break
        if m.group(1):
            v = parse_expr(m.group(1))
            out.append(S('label', value=v, text=f'case {show(v)}:'))
        else:
            out.append(S('label', value=None, text='default:'))
        text = text[m.end():]
    for part in split_simple(text) if text.strip() else []:
        body = part[:-1].strip()
        first = re.match(r'[A-Za-z_]\w*', body)
        word = first.group(0) if first else ''
        if body == '':
            out.append(S('empty', text=';'))
        elif word in TYPE_WORDS or word in STORAGE:
            words, decls = parse_decl(body)
            kind = 'proto' if any(d.params is not None for d in decls) else 'decl'
            out.append(S(kind, words=words, decls=decls, text=show_decl(words, decls)))
        elif word == 'return':
            rest = body[6:].strip()
            e = parse_expr(rest) if rest else None
            out.append(S('return', e=e, text='return' + (' ' + show(e) if e else '') + ';'))
        elif body in ('break', 'continue'):
            out.append(S(body, text=body + ';'))
        else:
            e = parse_expr(body)
            out.append(S('expr', e=e, text=show(e) + ';'))
    if comment:
        if not out:
            fail('a comment needs a statement')
        out[-1].comment = comment
    return out


def build(item):
    """One body item (a string or a dict) as a group of statements."""
    if isinstance(item, str):
        return simple(item)
    if not isinstance(item, dict):
        fail(f'bad statement {item!r}')
    inline = bool(item.get('inline'))
    if 'if' in item:
        return [S('if', cond=parse_expr(item['if']), then=grouped(item['then']), els=grouped(item.get('else')),
                  braces=isinstance(item['then'], list), ebraces=isinstance(item.get('else'), list), inline=inline)]
    if 'do' in item:
        return [S('do', body=grouped(item['do']), cond=parse_expr(item['while']))]
    if 'while' in item:
        return [S('while', cond=parse_expr(item['while']), body=grouped(item['body']),
                  braces=isinstance(item['body'], list), inline=inline)]
    if 'for' in item:
        parts = [x.strip() for x in item['for'].split(';')]
        if len(parts) != 3:
            fail(f'for needs three parts: {item["for"]!r}')
        init = None
        if parts[0]:
            init = simple(parts[0] + ';')
            if len(init) != 1 or init[0].kind not in ('decl', 'expr') or 'static' in getattr(init[0], 'words', ()):
                fail('bad for initializer')
            init = init[0]
        return [S('for', init=init, cond=parse_expr(parts[1]) if parts[1] else None,
                  update=parse_expr(parts[2]) if parts[2] else None, body=grouped(item['body']),
                  braces=isinstance(item['body'], list), inline=inline)]
    if 'switch' in item:
        return [S('switch', e=parse_expr(item['switch']), body=grouped(item['body']))]
    if 'block' in item:
        return [S('block', body=grouped(item['block']))]
    fail(f'unknown statement {item!r}')


def grouped(x):
    if x is None:
        return None
    return [build(item) for item in (x if isinstance(x, list) else [x])]


def flat(gs):
    return [] if gs is None else [s for g in gs for s in g]


# ---------------------------------------------------------------- listing

class Listing:
    def __init__(self):
        self.lines = []

    def out(self, text, depth):
        self.lines.append('  ' * depth + text)
        return len(self.lines) - 1

    def group(self, stmts, depth):
        text = ' '.join(s.text for s in stmts) + (' ' + stmts[-1].comment if stmts[-1].comment else '')
        line = self.out(text, depth)
        for s in stmts:
            s.line = line
        return line

    def body(self, gs, depth):
        for g in gs:
            if len(g) == 1 and g[0].kind in COMPOUND:
                self.compound(g[0], depth)
            elif any(s.kind in COMPOUND for s in g):
                fail('a compound statement must be its own body item')
            else:
                self.group(g, depth)

    def tail(self, header, gs, braces, inline, depth):
        """A header and its body: braces, the same line, or the next line."""
        if braces:
            line = self.out(header + ' {', depth)
            self.body(gs, depth + 1)
            self.out('}', depth)
            return line
        if len(gs) != 1:
            fail('a body without braces has one statement')
        if inline and all(s.kind not in COMPOUND for s in gs[0]):
            line = self.out(header + ' ' + ' '.join(s.text for s in gs[0]), depth)
            for s in gs[0]:
                s.line = line
            return line
        line = self.out(header, depth)
        self.body(gs, depth + 1)
        return line

    def compound(self, s, depth):
        if s.kind == 'if':
            head = f'if ({show(s.cond)})'
            if s.braces and s.els is not None and s.ebraces:
                s.line = self.out(head + ' {', depth)
                self.body(s.then, depth + 1)
                s.else_line = self.out('} else {', depth)
                self.body(s.els, depth + 1)
                self.out('}', depth)
            else:
                s.line = self.tail(head, s.then, s.braces, s.inline, depth)
                if s.els is not None:
                    s.else_line = self.tail('else', s.els, s.ebraces, s.inline, depth)
        elif s.kind == 'while':
            s.line = self.tail(f'while ({show(s.cond)})', s.body, s.braces, s.inline, depth)
        elif s.kind == 'for':
            init = s.init.text[:-1] if s.init else ''
            cond = show(s.cond) if s.cond else ''
            upd = show(s.update) if s.update else ''
            head = 'for (' + init + ';' + (' ' + cond if cond else '') + ';' + (' ' + upd if upd else '') + ')'
            s.line = self.tail(head, s.body, s.braces, s.inline, depth)
            if s.init is not None:
                s.init.line = s.line
        elif s.kind == 'do':
            s.top = self.out('do {', depth)
            self.body(s.body, depth + 1)
            s.line = self.out(f'}} while ({show(s.cond)});', depth)
        elif s.kind == 'switch':
            s.line = self.out(f'switch ({show(s.e)}) {{', depth)
            self.body(s.body, depth + 1)
            self.out('}', depth)
        elif s.kind == 'block':
            s.line = self.out('{', depth)
            self.body(s.body, depth + 1)
            self.out('}', depth)


# ---------------------------------------------------------------- run-time values

class Obj:
    __slots__ = ('id', 'name', 't', 'cells', 'kind', 'owner', 'frame', 'depth', 'tag', 'readonly')

    def __init__(self, oid, name, t, kind, owner=None, frame=None, depth=0, tag=None):
        self.id, self.name, self.t, self.kind, self.owner = oid, name, t, kind, owner
        self.frame, self.depth, self.tag, self.readonly = frame, depth, tag, False
        self.cells = [None] * ncells(t)


class Ptr:
    """A pointer to cell idx of obj; t is the pointed-to type and lo..hi the cells of the array it may move in."""
    __slots__ = ('obj', 'idx', 't', 'lo', 'hi')

    def __init__(self, obj, idx, t, lo, hi):
        self.obj, self.idx, self.t, self.lo, self.hi = obj, idx, t, lo, hi

    def same(self, other):
        return self.obj is other.obj and (self.obj is None or self.idx == other.idx)


def null(t=VOID):
    return Ptr(None, 0, t, 0, 0)


class LV:
    """An object, or one element of it: cell idx of obj, of type t, inside the array of cells lo..hi."""
    __slots__ = ('obj', 'idx', 't', 'lo', 'hi')

    def __init__(self, obj, idx, t, lo, hi):
        self.obj, self.idx, self.t, self.lo, self.hi = obj, idx, t, lo, hi


class Func:
    def __init__(self, ret, name, params, body, head, line):
        self.ret, self.name, self.params, self.body, self.head, self.line = ret, name, params, body, head, line


class Eff:
    """Cells read and written by an expression, directly (r, w) or inside the functions it calls (cr, cw)."""
    __slots__ = ('r', 'w', 'cr', 'cw')

    def __init__(self, r=(), w=(), cr=(), cw=()):
        self.r, self.w, self.cr, self.cw = set(r), set(w), set(cr), set(cw)

    def __or__(self, o):
        return Eff(self.r | o.r, self.w | o.w, self.cr | o.cr, self.cw | o.cw)


class Brk(Exception):
    pass


class Cont(Exception):
    pass


class Ret(Exception):
    def __init__(self, value, t):
        super().__init__()
        self.value, self.t = value, t


class Stop(Exception):
    """The run is cut off: a repeated loop state, or too many steps."""


class Frame:
    def __init__(self, func, call):
        self.func, self.call, self.scopes, self.objs, self.acc = func, call, [{}], [], Eff()


def zero_of(t):
    return null(t[1]) if is_ptr(t) else (0.0 if is_float(t) else 0)


def scalar_of(t):
    while is_arr(t):
        t = t[1]
    return t


# ---------------------------------------------------------------- the run

class Run:
    def __init__(self, items, spec, order='ltr'):
        self.spec, self.order = spec, order
        self.builtins = dict(spec.get('builtins') or {})
        self.size_t = UINT if spec.get('size_t') == 'unsigned int' else ULONG
        self.nobj, self.objs, self.globals, self.funcs, self.statics = 0, [], {}, {}, {}
        self.frames, self.steps, self.out, self.prints = [], [], '', 0
        self.writes, self.reads, self.ctx = [], [], None
        self.literals, self.seen_static, self.unspecified, self.states = {}, set(), [], set()
        self.breakable, self.cur_line, self.fall = [], None, None
        self.repeat, self.stopped, self.final_main = False, False, {}
        lst = Listing()
        for item in items:
            if isinstance(item, str) and item.startswith('#'):
                if not re.match(r'#include\s*<(stdio|string|stdlib)\.h>$', item):
                    fail(f'unsupported preprocessor line {item!r}')
                lst.out(item, 0)
            elif isinstance(item, str):
                stmts = simple(item)
                for s in stmts:
                    if s.kind not in ('decl', 'proto'):
                        fail(f'only declarations at file scope: {item!r}')
                    if s.kind == 'decl' and set(s.words) & {'auto', 'register'}:
                        fail('auto or register at file scope')
                    self.declare_global(s)
                lst.group(stmts, 0)
            elif isinstance(item, dict) and 'func' in item:
                words, name, stars, params = parse_header(item['func'])
                ret = base_type(words) if words else INT
                for _ in range(stars):
                    ret = ('ptr', ret)
                plist = ', '.join(show_param(w, d) for w, d in params) if params else \
                    ('void' if re.search(r'\(\s*void\s*\)', item['func']) else '')
                head = (' '.join(words) + ' ' if words else '') + '*' * stars + name + '(' + plist + ')'
                body = grouped(item['body'])
                line = lst.out(head + ' {', 0)
                lst.body(body, 1)
                end = lst.out('}', 0)
                if name in self.funcs:
                    fail(f'{name} is defined twice')
                f = Func(ret, name, params, body, head, line)
                f.end = end
                self.funcs[name] = f
            else:
                fail(f'bad top-level item {item!r}')
        self.lines = lst.lines
        for f in self.funcs.values():
            self.statics[f.name] = {}
            self.find_statics(f, flat(f.body))
        self.writes = []

    # ------------------------------------------------ objects

    def new_obj(self, name, t, kind, **kw):
        self.nobj += 1
        o = Obj(self.nobj, name, t, kind, **kw)
        self.objs.append(o)
        return o

    def declare_global(self, s, kind='global'):
        if s.kind == 'proto':
            return
        for d in s.decls:
            if d.name in self.globals:
                fail(f'{d.name} is declared twice')
            o = self.new_obj(d.name, decl_type(s.words, d, d.init), kind)
            self.globals[d.name] = o
            self.initialize(o, d.init, static=True)

    def find_statics(self, f, stmts):
        for s in stmts:
            if s.kind == 'decl' and 'static' in s.words:
                objs = []
                for d in s.decls:
                    o = self.new_obj(d.name, decl_type(s.words, d, d.init), 'static', owner=f.name)
                    self.initialize(o, d.init, static=True)
                    objs.append(o)
                self.statics[f.name][id(s)] = objs
            for attr in ('then', 'els', 'body'):
                sub = getattr(s, attr, None)
                if sub and s.kind in COMPOUND:
                    self.find_statics(f, flat(sub))

    def initialize(self, o, init, static=False):
        """Fill o from its initializer. Static storage starts at zero; automatic storage starts unset."""
        if static or (init is not None and is_arr(o.t)):
            z = zero_of(scalar_of(o.t))
            o.cells = [z] * len(o.cells)
        if init is None:
            return Eff()
        if not is_arr(o.t):
            if isinstance(init, list):
                if len(init) != 1 or isinstance(init[0], list):
                    fail(f'bad initializer for {o.name}')
                init = init[0]
            return self.store(LV(o, 0, o.t, 0, 1), init)
        node = None if isinstance(init, list) else strip_paren(init)
        if node is not None and node.k == 'str':
            if o.t[1] != CHAR:
                fail('a string initializes only a char array')
            codes = unescape(node.v[1:-1])
            if len(codes) > o.t[2]:
                fail(f'string too long for {o.name}')
            for k, c in enumerate(codes):
                o.cells[k] = c
            for k in range(len(o.cells)):
                self.writes.append((LV(o, k, CHAR, 0, len(o.cells)), o.cells[k]))
            return Eff()
        if node is not None:
            fail(f'array {o.name} needs a brace initializer')
        items = []

        def fill(t, xs, start):
            """C's brace elision: initialize type t at cell start from xs; returns how many items it used."""
            if not is_arr(t):
                if isinstance(xs[0], list):
                    fail(f'too many braces for {o.name}')
                items.append((start, t, xs[0]))
                return 1
            pos = 0
            for e in range(t[2]):
                if pos >= len(xs):
                    break
                at = start + e * ncells(t[1])
                if isinstance(xs[pos], list):
                    if fill(t[1], xs[pos], at) < len(xs[pos]):
                        fail(f'too many initializers for {o.name}')
                    pos += 1
                else:
                    pos += fill(t[1], xs[pos:], at)
            return pos
        if fill(o.t, init, 0) < len(init):
            fail(f'too many initializers for {o.name}')
        eff = Eff()
        written = {at for at, _, _ in items}
        for at, t, x in items:
            eff = eff | self.store(LV(o, at, t, 0, len(o.cells)), x)
        for k in range(len(o.cells)):
            if k not in written:
                self.writes.append((LV(o, k, scalar_of(o.t), 0, len(o.cells)), o.cells[k]))
        return eff

    def store(self, lv, node):
        v, t, eff = self.rv(node)
        self.write(lv, v, t, node, eff)
        return eff

    # ------------------------------------------------ names

    def lookup(self, name):
        if self.frames:
            for sc in reversed(self.frames[-1].scopes):
                if name in sc:
                    return sc[name]
        return self.globals.get(name)

    def live_objs(self):
        out = [o for o in self.objs if o.kind in ('global', 'given', 'static')]
        for fr in self.frames:
            out.extend(fr.objs)
        return out

    def label(self, o):
        """o's name in a sentence, qualified when another live variable has the same name."""
        if o.kind == 'literal':
            return o.name
        live = [x for x in self.live_objs() if x.name == o.name]
        if len(live) <= 1:
            return o.name
        if o.kind in ('global', 'given'):
            return f'the global {o.name}'
        if o.kind == 'static':
            return f"{o.owner}'s static {o.name}"
        fr = o.frame
        same = [f for f in self.frames if f.func.name == fr.func.name]
        who = fr.func.name if len(same) == 1 else f'{fr.func.name} (call {same.index(fr) + 1})'
        mine = [x for x in live if x.frame is fr]
        inner = 'inner ' if len(mine) > 1 and o.depth > min(x.depth for x in mine) else ''
        return f"{who}'s {inner}{o.name}"

    def place(self, lv):
        """'a[2]', 'x' or '"abc"[1]' for the cell lv names."""
        o, idx, t, s = lv.obj, lv.idx, lv.obj.t, ''
        while t != lv.t and is_arr(t):
            n = ncells(t[1])
            s += f'[{idx // n}]'
            idx %= n
            t = t[1]
        return self.label(o) + s

    # ------------------------------------------------ memory

    def read(self, lv, eff):
        if is_arr(lv.t):
            return Ptr(lv.obj, lv.idx, lv.t[1], lv.idx, lv.idx + ncells(lv.t)), ('ptr', lv.t[1])
        v = lv.obj.cells[lv.idx]
        if v is None:
            fail(f'{self.place(lv)} is read before it is set')
        eff.r.add((lv.obj.id, lv.idx))
        self.reads.append((lv.obj.id, lv.idx))
        return v, lv.t

    def write(self, lv, v, t, node=None, eff=None):
        if lv.obj.readonly:
            fail('writing into a string literal')
        if is_arr(lv.t):
            fail('assignment to a whole array')
        v = self.convert(v, t, lv.t, node)
        lv.obj.cells[lv.idx] = v
        if eff is not None:
            eff.w.add((lv.obj.id, lv.idx))
        self.writes.append((lv, v))
        return v

    def convert(self, v, frm, to, node=None):
        """C's conversion of v from type frm to type to (for assignment, arguments and arithmetic)."""
        if to == VOID:
            return None
        if is_ptr(to):
            if is_ptr(frm):
                if frm[1] == to[1]:
                    return v
                if v.obj is None:
                    return null(to[1])
                fail(f'a {tname(frm)} stored in a {tname(to)}')
            if is_int(frm) and v == 0 and node is not None and strip_paren(node).k == 'num':
                return null(to[1])
            fail(f'an integer stored in a {tname(to)}')
        if is_ptr(frm):
            fail(f'a pointer stored in a {tname(to)}')
        if is_float(to):
            v = float(v)
            return f32(v) if to == FLOAT else v
        if is_float(frm):
            r = int(v)
            if r != v and self.ctx is not None:
                self.ctx['cuts'].append((v, r, tname(to)))
            v = r
        bits, signed = LIMITS[to[0]]
        if signed:
            if not -(1 << bits - 1) <= v < 1 << bits - 1:
                fail(f'{v} does not fit in {tname(to)}')
            return v
        r = v % (1 << bits)
        if r != v and self.ctx is not None:
            self.ctx['wraps'].append((v, r, tname(to)))
        return r

    # ------------------------------------------------ expressions

    def unseq(self, a, b):
        """Join the effects of two unsequenced operands, stopping on undefined behaviour."""
        if a.w & (b.r | b.w) or b.w & a.r:
            fail('two unsequenced accesses to one variable (undefined behaviour)')
        if a.cw & (b.r | b.w | b.cr | b.cw) or b.cw & (a.r | a.w | a.cr) or a.w & b.cr or b.w & a.cr:
            self.unspecified.append(self.cur_line)
            if self.ctx is not None:
                self.ctx['unspec'] = True
        return a | b

    def pair(self, x, y):
        if self.order == 'ltr':
            a = self.rv(x)
            b = self.rv(y)
        else:
            b = self.rv(y)
            a = self.rv(x)
        return a, b, self.unseq(a[2], b[2])

    def work(self, node, v, t):
        """Remember an intermediate value for the 'working' line."""
        if self.ctx is None or node.k in ('num', 'chr', 'name', 'str', 'paren'):
            return
        item = [show(node), self.fmt(v, t)]
        if item[0] != item[1] and item not in self.ctx['work']:
            self.ctx['work'].append(item)

    def literal(self, node):
        text = node.v
        hexa = text.lower().startswith('0x')
        body = text.rstrip('uUlL') if hexa else text.rstrip('uUlLfF')
        suf = text[len(body):].lower()
        if not hexa and re.search(r'[.eE]', body):
            return (f32(float(body)), FLOAT) if 'f' in suf else (float(body), DOUBLE)
        n = int(body, 16) if hexa else int(body, 8) if re.match(r'0\d', body) else int(body)
        if 'u' in suf:
            return n, (ULONG if 'l' in suf or n >= 1 << 32 else UINT)
        return n, (LONG if 'l' in suf or n >= 1 << 31 else INT)

    def rv(self, node):
        """Evaluate node for its value: (value, type, effects)."""
        k = node.k
        if k == 'num':
            v, t = self.literal(node)
            return v, t, Eff()
        if k == 'chr':
            return unescape(node.v[1:-1])[0], INT, Eff()
        if k == 'paren':
            return self.rv(node.a)
        if k == 'name' and node.v == 'NULL' and self.lookup('NULL') is None:
            return null(), ('ptr', VOID), Eff()
        if k in ('str', 'name', 'index') or (k == 'un' and node.op == '*'):
            lv, eff = self.lv(node)
            v, t = self.read(lv, eff)
            if k != 'name' and k != 'str':
                self.work(node, v, t)
            return v, t, eff
        if k == 'un':
            if node.op == '&':
                lv, eff = self.lv(node.a)
                v = Ptr(lv.obj, lv.idx, lv.t, lv.lo, lv.hi)
                self.work(node, v, ('ptr', lv.t))
                return v, ('ptr', lv.t), eff
            if node.op in ('++', '--'):
                return self.incdec(node.a, node.op, True, node)
            v, t, eff = self.rv(node.a)
            if node.op == '!':
                r = int(not self.truth(v, t))
                self.work(node, r, INT)
                return r, INT, eff
            if not is_arith(t) or (node.op == '~' and not is_int(t)):
                fail(f'{node.op} applied to a {tname(t)}')
            t2 = promote(t)
            v = self.convert(v, t, t2)
            r = -v if node.op == '-' else v if node.op == '+' else ~v
            if node.op == '~' and not LIMITS[t2[0]][1]:
                r %= 1 << LIMITS[t2[0]][0]
            r = self.fix(r, t2, show(node))
            self.work(node, r, t2)
            return r, t2, eff
        if k == 'post':
            return self.incdec(node.a, node.op, False, node)
        if k == 'bin':
            return self.binop(node)
        if k == 'assign':
            return self.assign(node)
        if k == 'comma':
            a = self.rv(node.a)
            b = self.rv(node.b)
            return b[0], b[1], a[2] | b[2]
        if k == 'cond':
            c, ct, ce = self.rv(node.a)
            taken = node.b if self.truth(c, ct) else node.c
            v, t, e = self.rv(taken)
            other = self.static_type(node.c if taken is node.b else node.b)
            if is_arith(t) and is_arith(other):
                rt = common(t, other)
                v, t = self.convert(v, t, rt), rt
            elif t != other:
                fail('?: with operands of different types')
            self.work(node, v, t)
            return v, t, ce | e
        if k == 'call':
            return self.call(node)
        fail(f'cannot evaluate {k}')

    def static_type(self, node):
        """The type of an expression without running it (the branch of ?: not taken)."""
        n = strip_paren(node)
        if n.k == 'num':
            return self.literal(n)[1]
        if n.k == 'chr':
            return INT
        if n.k == 'call':
            f = self.funcs.get(n.a.v)
            return f.ret if f else {'strlen': self.size_t}.get(n.a.v) or fail(f'type of {show(n)}')
        if n.k == 'name':
            o = self.lookup(n.v)
            if o is not None and not is_arr(o.t):
                return o.t
        fail(f'cannot tell the type of {show(node)}')

    def lv(self, node):
        """Evaluate node for the object it designates: (LV, effects)."""
        k = node.k
        if k == 'paren':
            return self.lv(node.a)
        if k == 'name':
            o = self.lookup(node.v)
            if o is None:
                fail(f'unknown name {node.v}')
            return LV(o, 0, o.t, 0, len(o.cells)), Eff()
        if k == 'str':
            if id(node) not in self.literals:
                codes = unescape(node.v[1:-1]) + [0]
                o = self.new_obj(node.v, ('arr', CHAR, len(codes)), 'literal')
                o.cells, o.readonly = list(codes), True
                self.literals[id(node)] = o
            o = self.literals[id(node)]
            return LV(o, 0, o.t, 0, len(o.cells)), Eff()
        if k == 'un' and node.op == '*':
            v, t, eff = self.rv(node.a)
            return self.deref(v, t), eff
        if k == 'index':
            (a, ta, _), (b, tb, _), eff = self.pair(node.a, node.b)
            if is_int(ta) and is_ptr(tb):
                a, ta, b, tb = b, tb, a, ta
            p, pt = self.ptr_add(a, ta, b, tb, '+')
            return self.deref(p, pt), eff
        fail(f'{show(node)} is not a variable')

    def deref(self, v, t):
        if not is_ptr(t):
            fail(f'* applied to a {tname(t)}')
        if v.obj is None:
            fail('null pointer dereference')
        if t[1] == VOID:
            fail('dereference of a void pointer')
        if not (v.lo <= v.idx and v.idx + ncells(t[1]) <= v.hi):
            fail('a pointer past the end of its array is dereferenced')
        return LV(v.obj, v.idx, t[1], v.lo, v.hi)

    def ptr_add(self, a, ta, b, tb, op):
        if not is_ptr(ta) or not is_int(tb):
            fail('bad pointer arithmetic')
        if a.obj is None:
            fail('arithmetic on a null pointer')
        idx = a.idx + (b if op == '+' else -b) * ncells(ta[1])
        if not a.lo <= idx <= a.hi:
            fail('pointer arithmetic leaves its array (undefined behaviour)')
        return Ptr(a.obj, idx, ta[1], a.lo, a.hi), ta

    def truth(self, v, t):
        return v.obj is not None if is_ptr(t) else v != 0

    def fix(self, r, t, text):
        """The result of arithmetic in type t: signed overflow stops the build, unsigned wraps."""
        if is_float(t):
            return f32(r) if t == FLOAT else r
        bits, signed = LIMITS[t[0]]
        if signed:
            if not -(1 << bits - 1) <= r < 1 << bits - 1:
                fail(f'signed overflow in {text}')
            return r
        w = r % (1 << bits)
        if w != r and self.ctx is not None:
            self.ctx['wraps'].append((r, w, tname(t)))
        return w

    def arith(self, op, a, ta, b, tb, text):
        if op in ('<<', '>>'):
            if not is_int(ta) or not is_int(tb):
                fail('shift of a non-integer')
            t = promote(ta)
            a, b = self.convert(a, ta, t), self.convert(b, tb, promote(tb))
            bits, signed = LIMITS[t[0]]
            if not 0 <= b < bits:
                fail(f'shift by {b}')
            if signed and a < 0:
                fail('shift of a negative value')
            return self.fix(a << b if op == '<<' else a >> b, t, text), t
        if is_ptr(ta) or is_ptr(tb):
            if op in COMPARE:
                if not (is_ptr(ta) and is_ptr(tb)):
                    fail('a pointer compared with an integer')
                if op in ('==', '!='):
                    return int(a.same(b) == (op == '==')), INT
                if a.obj is not b.obj or a.obj is None:
                    fail('ordering pointers into different objects')
                x, y = a.idx, b.idx
                return int({'<': x < y, '>': x > y, '<=': x <= y, '>=': x >= y}[op]), INT
            if op == '-' and is_ptr(ta) and is_ptr(tb):
                if a.obj is not b.obj or (a.lo, a.hi) != (b.lo, b.hi) or ta != tb:
                    fail('subtracting pointers into different arrays')
                return (a.idx - b.idx) // ncells(ta[1]), LONG
            if op == '+' and is_int(ta):
                a, ta, b, tb = b, tb, a, ta
            if op not in ('+', '-') or is_ptr(tb):
                fail(f'{op} on pointers')
            return self.ptr_add(a, ta, b, tb, op)
        if not is_arith(ta) or not is_arith(tb):
            fail(f'{op} on {tname(ta)} and {tname(tb)}')
        t = common(ta, tb)
        a, b = self.convert(a, ta, t), self.convert(b, tb, t)
        if op in COMPARE:
            return int({'<': a < b, '>': a > b, '<=': a <= b, '>=': a >= b, '==': a == b, '!=': a != b}[op]), INT
        if op in ('&', '|', '^', '%') and is_float(t):
            fail(f'{op} on floating values')
        if op in ('/', '%') and b == 0:
            fail('division by zero')
        if is_float(t):
            return self.fix({'+': a + b, '-': a - b, '*': a * b, '/': a / b}[op], t, text), t
        if op in ('/', '%'):
            q = abs(a) // abs(b) * (1 if (a < 0) == (b < 0) else -1)
            r = q if op == '/' else a - b * q
        else:
            r = {'+': a + b, '-': a - b, '*': a * b, '&': a & b, '|': a | b, '^': a ^ b}[op]
        return self.fix(r, t, text), t

    def binop(self, node):
        op = node.op
        if op in ('&&', '||'):
            a, ta, ea = self.rv(node.a)
            left = self.truth(a, ta)
            if self.ctx is not None:
                self.ctx['logic'].append((show(node.a), left, show(node.b), (op == '&&') != left))
            if (op == '&&') != left:
                r = int(left)
                self.work(node, r, INT)
                return r, INT, ea
            b, tb, eb = self.rv(node.b)
            r = int(self.truth(b, tb))
            self.work(node, r, INT)
            return r, INT, ea | eb
        (a, ta, _), (b, tb, _), eff = self.pair(node.a, node.b)
        r, t = self.arith(op, a, ta, b, tb, show(node))
        self.work(node, r, t)
        return r, t, eff

    def incdec(self, target, op, prefix, node):
        lv, eff = self.lv(target)
        v, t = self.read(lv, eff)
        if is_ptr(t):
            nv, _ = self.ptr_add(v, t, 1, INT, '+' if op == '++' else '-')
        else:
            nv, nt = self.arith('+' if op == '++' else '-', v, t, 1, INT, show(node))
            nv = self.convert(nv, nt, t)
        self.write(lv, nv, t, eff=eff)
        r, rt = (nv if prefix else v), (promote(t) if is_arith(t) else t)
        self.work(node, r, rt)
        return r, rt, eff

    def assign(self, node):
        op = node.op
        if self.order == 'ltr':
            lv, el = self.lv(node.a)
            b, tb, er = self.rv(node.b)
        else:
            b, tb, er = self.rv(node.b)
            lv, el = self.lv(node.a)
        eff = self.unseq(el, er)
        target = (lv.obj.id, lv.idx)
        if target in er.w or target in el.w:
            fail(f'{show(node)} writes one variable twice (undefined behaviour)')
        if op != '=':
            a, ta = self.read(lv, eff)
            if target in er.cw:
                self.unspecified.append(self.cur_line)
                if self.ctx is not None:
                    self.ctx['unspec'] = True
            b, tb = self.arith(op[:-1], a, ta, b, tb, show(node))
            self.work(Node('bin', op[:-1], node.a, node.b), b, tb)
        v = self.write(lv, b, tb, node.b if op == '=' else None, eff)
        return v, lv.t, eff

    # ------------------------------------------------ calls

    def call(self, node):
        name = node.a.v
        if self.order == 'ltr':
            args = [self.rv(a) for a in node.args]
        else:
            args = [self.rv(a) for a in reversed(node.args)][::-1]
        eff = Eff()
        for a in args:
            eff = self.unseq(eff, a[2])
        if name in self.funcs:
            return self.user_call(self.funcs[name], node, args, eff)
        return self.library(name, node, args, eff)

    def library(self, name, node, args, eff):
        if name in ('printf', 'print'):
            if name == 'print':
                if 'print' not in self.builtins:
                    fail('print() is not described by the question')
                fmt, vals = self.builtins['print'], args
            else:
                if not args or args[0][1] != ('ptr', CHAR):
                    fail('printf needs a format string')
                fmt, vals = self.cstring(args[0][0]), args[1:]
            text = self.format(fmt, vals)
            self.out += text
            self.prints += 1
            if self.ctx is not None:
                self.ctx['printed'] += text
            return len(text), INT, eff | Eff(cw=[('out', 0)])
        if name == 'strlen':
            if len(args) != 1 or args[0][1] != ('ptr', CHAR):
                fail('strlen needs a char pointer')
            p = args[0][0]
            s = self.cstring(p)
            self.work(node, len(s), self.size_t)
            return len(s), self.size_t, eff | Eff(cr=[(p.obj.id, p.idx + k) for k in range(len(s) + 1)])
        if name == 'swap' and self.builtins.get('swap') == 'exchange':
            if len(args) != 2 or args[0][1] != ('ptr', INT) or args[1][1] != ('ptr', INT):
                fail('swap needs two int pointers')
            lp, lq = self.deref(args[0][0], args[0][1]), self.deref(args[1][0], args[1][1])
            e = Eff()
            x, _ = self.read(lp, e)
            y, _ = self.read(lq, e)
            self.write(lp, y, INT, eff=e)
            self.write(lq, x, INT, eff=e)
            if self.ctx is not None:
                self.ctx['swaps'].append((self.place(lp), self.place(lq), y, x))
            return None, VOID, eff | Eff(cr=e.r, cw=e.w)
        fail(f'unknown function {name}')

    def cstring(self, p):
        if p.obj is None:
            fail('a null pointer used as a string')
        out, k = [], p.idx
        while True:
            if k >= p.hi:
                fail('a string without its terminating null')
            c = p.obj.cells[k]
            if c is None:
                fail('an unset character in a string')
            if c == 0:
                return ''.join(chr(x) for x in out)
            out.append(c)
            k += 1

    def format(self, fmt, vals):
        out, k, n = '', 0, 0
        while k < len(fmt):
            if fmt[k] != '%':
                out += fmt[k]
                k += 1
                continue
            m = re.match(r'%(l?[dicusf%])', fmt[k:])
            if not m:
                fail(f'unsupported printf format {fmt[k:k + 3]!r}')
            k += m.end()
            spec = m.group(1)
            if spec == '%':
                out += '%'
                continue
            if n >= len(vals):
                fail('printf has too few arguments')
            v, t, _ = vals[n]
            n += 1
            pt = INT if t in (CHAR, SHORT) else DOUBLE if t == FLOAT else t
            if spec in ('d', 'i'):
                if not (pt == INT or (pt == UINT and v < 1 << 31)):
                    fail(f'%d with an argument of type {tname(t)}')
                out += str(v)
            elif spec == 'u':
                if not (pt == UINT or (pt == INT and v >= 0)):
                    fail(f'%u with an argument of type {tname(t)}')
                out += str(v)
            elif spec in ('ld', 'lu'):
                if pt != (LONG if spec == 'ld' else ULONG):
                    fail(f'%{spec} with an argument of type {tname(t)}')
                out += str(v)
            elif spec == 'c':
                if pt != INT or not 0 <= v < 128:
                    fail('%c needs a character code')
                out += chr(v)
            elif spec == 's':
                if t != ('ptr', CHAR):
                    fail('%s needs a char pointer')
                out += self.cstring(v)
            elif spec == 'f':
                if pt != DOUBLE:
                    fail(f'%f with an argument of type {tname(t)}')
                out += '%f' % v
            else:
                fail(f'unsupported printf format %{spec}')
        if n != len(vals):
            fail('printf has too many arguments')
        return out

    def user_call(self, f, node, args, eff):
        if len(args) != len(f.params):
            fail(f'{f.name} called with {len(args)} arguments')
        if len(self.frames) >= MAX_DEPTH:
            fail('calls nest too deeply')
        caller_ctx, line_was = self.ctx, self.cur_line
        fr = Frame(f, show(node))
        made = []
        for (words, d), (v, t, _) in zip(f.params, args):
            o = self.new_obj(d.name, param_type(words, d), 'param', frame=fr)
            if d.name in fr.scopes[0]:
                fail(f'two parameters named {d.name}')
            fr.scopes[0][d.name] = o
            fr.objs.append(o)
            made.append((o, v, t))
        self.frames.append(fr)
        self.ctx = None
        for o, v, t in made:
            self.write(LV(o, 0, o.t, 0, 1), v, t)
        desc = _list([f'{o.name} = {self.fmt(o.cells[0], o.t)}' for o, _, _ in made])
        self.emit(f.line, f'{show(node)} starts' + (f' with {desc}.' if desc else '.'))
        result = None
        try:
            self.run_block(f.body, new_scope=False)
            if f.ret != VOID and f.name != 'main':
                fail(f'{f.name} ends without returning a value')
            self.emit(f.end, f'{f.name} reaches its end and returns.')
            result = (0, INT) if f.name == 'main' and f.ret == INT else (None, VOID)
        except Ret as r:
            result = (r.value, r.t)
        if f.name == 'main' and len(self.frames) == 1:
            self.final_main = {o.name: self.fmt(o.cells[0], o.t) for o in fr.objs if not is_arr(o.t)}
        self.frames.pop()
        self.ctx, self.cur_line = caller_ctx, line_was
        if self.ctx is not None:
            call = f'{show(node)} returns'
            if f.ret != VOID:
                call += f' {self.fmt(*result)}'
            self.ctx['calls'].append(call)
        if f.ret != VOID:
            self.work(node, *result)
        body = fr.acc
        return result[0], result[1], eff | Eff(cr=body.r | body.cr, cw=body.w | body.cw)

    # ------------------------------------------------ display

    def fmt(self, v, t):
        if is_ptr(t):
            return self.fmt_ptr(v)
        if v is None:
            return '?'
        if is_float(t):
            return _num(v)
        if t == CHAR:
            return _char(v)
        return str(v)

    def fmt_ptr(self, p):
        if p is None:
            return '?'
        if p.obj is None:
            return 'NULL'
        o = p.obj
        t, idx, s = o.t, p.idx, ''
        while t != p.t and is_arr(t):
            n = ncells(t[1])
            if idx == ncells(t):
                return f'→ just past {self.label(o)}{s}'
            s += f'[{idx // n}]'
            idx %= n
            t = t[1]
        if t != p.t or idx:
            fail('a pointer into the middle of a value')
        return f'→ {self.label(o)}{s}'

    def snapshot(self):
        written = {(lv.obj.id, lv.idx) for lv, _ in self.writes}
        read = set(self.reads)
        cur = self.frames[-1] if self.frames else None
        in_scope = {id(o) for sc in cur.scopes for o in sc.values()} if cur else set()

        def row(o, hidden=False):
            r = dict(n=o.name, t=tname(o.t))
            if any((o.id, k) in written for k in range(len(o.cells))):
                r['w'] = 1
            if hidden:
                r['h'] = 1
            if o.tag:
                r['tag'] = o.tag
            if not is_arr(o.t):
                r['v'] = self.fmt(o.cells[0], o.t)
                return r
            dims, base = [], o.t
            while is_arr(base):
                dims.append(base[2])
                base = base[1]
            last, shown = dims[-1], len(o.cells)
            if base == CHAR and len(o.cells) > 16:
                used = [k for k, c in enumerate(o.cells) if c not in (0, None) or (o.id, k) in written]
                shown = min(len(o.cells), max(used, default=-1) + 2)
            rows = []
            for rr in range(-(-shown // last)):
                cells = []
                for c in range(last):
                    k = rr * last + c
                    if k < shown:
                        cells.append([c, _cell(o.cells[k], base, self), 'w' if (o.id, k) in written else
                                      'r' if (o.id, k) in read else ''])
                prefix = o.name + ''.join(f'[{(rr // _prod(dims[j + 1:-1])) % dims[j]}]' for j in range(len(dims) - 1))
                rows.append(dict(p=prefix, c=cells))
            r['rows'] = rows
            if shown < len(o.cells):
                r['more'] = len(o.cells) - shown
            if base == CHAR and len(dims) == 1 and 0 in o.cells:
                end = o.cells.index(0)
                if None not in o.cells[:end]:
                    r['s'] = _quote(''.join(chr(c) for c in o.cells[:end]))
            return r

        groups = []
        for kind, title in (('given', 'given'), ('global', 'globals')):
            objs = [o for o in self.objs if o.kind == kind]
            if objs:
                groups.append(dict(title=title, rows=[row(o, hidden=bool(cur) and self.lookup(o.name) is not o) for o in objs]))
        for fname, decls in self.statics.items():
            objs = [o for os in decls.values() for o in os]
            if objs:
                active = cur is not None and cur.func.name == fname
                g = dict(title=f'static in {fname}', rows=[
                    row(o, hidden=active and id(o) in in_scope and self.lookup(o.name) is not o) for o in objs])
                if active:
                    g['cur'] = 1
                groups.append(g)
        names = [fr.func.name for fr in self.frames]
        for k, fr in enumerate(self.frames):
            title = fr.func.name if names.count(fr.func.name) == 1 else f'{fr.func.name} (call {names[:k + 1].count(fr.func.name)})'
            g = dict(title=title, rows=[row(o, hidden=fr is cur and self.lookup(o.name) is not o) for o in fr.objs])
            if fr is cur:
                g['cur'] = 1
            groups.append(g)
        return groups

    def emit(self, line, note, work=None, printed=''):
        if len(self.steps) >= MAX_STEPS:
            self.stopped = True
            raise Stop()
        st = dict(line=line, note=note, vars=self.snapshot(), out=self.out)
        if printed:
            st['new'] = len(printed)
        if work:
            st['work'] = work[:8]
        if self.frames:
            st['fn'] = self.frames[-1].func.name
        self.steps.append(st)
        self.writes, self.reads = [], []

    # ------------------------------------------------ statements

    def new_ctx(self):
        self.ctx = dict(work=[], calls=[], wraps=[], cuts=[], printed='', logic=[], swaps=[], unspec=False)
        return self.ctx

    def full(self, node, line):
        """Evaluate a full expression."""
        self.cur_line = line
        v, t, eff = self.rv(node)
        if self.frames:
            self.frames[-1].acc = self.frames[-1].acc | eff
        return v, t

    def changes(self, ctx, initial=False):
        """What a statement changed, as clauses."""
        parts = [f'swap exchanges {a} and {b}, which now hold {x} and {y}' for a, b, x, y in ctx['swaps']]
        swapped = {p for s in ctx['swaps'] for p in s[:2]}
        last = {}
        for lv, v in self.writes:
            if lv.obj.kind == 'param' and lv.obj.frame is not (self.frames[-1] if self.frames else None):
                continue
            last.pop((lv.obj.id, lv.idx), None)
            last[(lv.obj.id, lv.idx)] = (lv, v)
        whole = {}
        for lv, v in last.values():
            if initial and is_arr(lv.obj.t):
                whole.setdefault(lv.obj.id, lv.obj)
                continue
            name = self.place(lv)
            if name in swapped:
                continue
            if is_ptr(lv.t):
                what = 'is NULL' if v.obj is None else f'points to {self.fmt_ptr(v)[2:]}'
                parts.append(f'{name} {what}' if initial else f'{name} {"becomes NULL" if v.obj is None else "now " + what}')
            else:
                parts.append(f'{name} {"is" if initial else "becomes"} {self.fmt(v, lv.t)}')
        for o in whole.values():
            parts.append(f'{self.label(o)} holds {self.array_text(o)}')
        return parts

    def array_text(self, o):
        base = scalar_of(o.t)
        if base == CHAR and 0 in o.cells:
            return _quote(''.join(chr(c) for c in o.cells[:o.cells.index(0)]))
        vals = [self.fmt(c, base) for c in o.cells]
        if len(vals) > 12:
            vals = vals[:10] + ['…']
        return '{' + ', '.join(vals) + '}'

    def describe(self, ctx, initial=False):
        """A clause list for one statement: calls made, values skipped, what changed, what was printed."""
        lead = []
        if ctx['calls']:
            lead.append(_list(ctx['calls']))
        for a, ta, b, skipped in ctx['logic']:
            if skipped:
                lead.append(f'{a} is {"true" if ta else "false"}, so {b} is not evaluated')
        eff = self.changes(ctx, initial)
        if ctx['printed']:
            eff.append('printf prints ' + _quote(ctx['printed']) if self.prints else 'prints ' + _quote(ctx['printed']))
        text = '; '.join(lead)
        if eff:
            text += (', so ' if text else '') + _list(eff)
        for v, r, tn in ctx['cuts']:
            text += f' ({_num(v)} is cut to {r} to fit in an {tn})'
        for v, r, tn in ctx['wraps']:
            text += f' ({tn} arithmetic wraps around: {v} becomes {r})'
        if ctx['unspec']:
            text += '. C does not fix which of these calls runs first, and the other order gives the same result'
        return text

    def run_block(self, gs, new_scope=True):
        fr = self.frames[-1]
        if new_scope:
            fr.scopes.append({})
        try:
            for s in flat(gs):
                self.run(s)
        finally:
            if new_scope:
                self.close_scope(fr)

    def close_scope(self, fr):
        gone = {id(o) for o in fr.scopes.pop().values()}
        fr.objs = [o for o in fr.objs if id(o) not in gone]

    def declare_local(self, s, tag=None):
        fr = self.frames[-1]
        if 'static' in s.words:
            objs = self.statics[fr.func.name][id(s)]
            for o in objs:
                fr.scopes[-1][o.name] = o
            return objs
        made = []
        depth = len(fr.scopes) - 1
        for d in s.decls:
            if d.name in fr.scopes[-1]:
                fail(f'{d.name} is declared twice in one block')
            o = self.new_obj(d.name, decl_type(s.words, d, d.init), 'local', frame=fr, depth=depth,
                             tag=tag or ('inner block' if depth > 0 else None))
            fr.scopes[-1][d.name] = o
            fr.objs.append(o)
            self.cur_line = s.line
            fr.acc = fr.acc | self.initialize(o, d.init)
            made.append(o)
        return made

    def value_of(self, node):
        """The value a sub-expression had in the statement just run, as shown on the working line."""
        x = strip_paren(node)
        if x.k in ('num', 'chr'):
            return x.v
        if x.k == 'name':
            o = self.lookup(x.v)
            if o is not None and not is_arr(o.t):
                return self.fmt(o.cells[0], o.t)
        for text, val in self.ctx['work']:
            if text == show(x):
                return val
        return show(x)

    def test(self, s, node, line, yes, no):
        """Evaluate and display the test of an if or a loop before its body runs."""
        ctx = self.new_ctx()
        v, t = self.full(node, line)
        truth = self.truth(v, t)
        if ctx['unspec']:
            fail('a test whose value depends on evaluation order')
        n = strip_paren(node)
        parts = []
        if ctx['calls']:
            parts.append(_list(ctx['calls']))
        if n.k == 'bin' and n.op in ('&&', '||'):
            for a, ta, b, skipped in ctx['logic'][:1]:
                parts.append(f'{a} is {"true" if ta else "false"}' + (f', so {b} is not evaluated' if skipped else
                                                                       f' and {b} is {self.value_of(n.b)}'))
        changed = self.changes(ctx)
        if changed:
            parts.append(_list(changed))
        if ctx['printed']:
            parts.append('prints ' + _quote(ctx['printed']))
        if n.k == 'bin' and n.op in COMPARE:
            main = f'{self.value_of(n.a)} {n.op} {self.value_of(n.b)} {"holds" if truth else "fails"}'
        elif n.k == 'bin' and n.op in ('&&', '||'):
            main = f'the test is {"true" if truth else "false"}'
        elif is_ptr(t):
            main = f'{show(n)} is {"not NULL" if truth else "NULL"}'
        else:
            shown = self.fmt(v, t)
            main = f'{shown} is {"not zero" if truth else "zero"}' if n.k == 'call' else \
                f'{show(n)} is {shown}, {"not zero" if truth else "zero"}'
        parts.append(main)
        sentence = f'Test {show(node)}: {"; ".join(parts)}, so {yes if truth else no}.'
        self.emit(line, sentence, work=ctx['work'], printed=ctx['printed'])
        self.ctx = None
        if s.kind != 'if':
            self.check_loop(s)
        return truth

    def check_loop(self, s):
        """A loop test reached twice with every variable the same never ends: the program is deterministic."""
        state = (id(s), tuple(id(f) for f in self.frames),
                 tuple((o.id, tuple(_key(c) for c in o.cells)) for o in self.live_objs()))
        if state in self.states:
            self.repeat = True
            raise Stop()
        self.states.add(state)

    def run(self, s):
        k = s.kind
        if k in ('empty', 'proto'):
            return
        if k == 'label':
            self.fall = s.text[:-1]
            return
        if k == 'decl':
            self.run_decl(s)
            return
        if k == 'expr':
            ctx = self.new_ctx()
            self.full(s.e, s.line)
            text = self.describe(ctx) or 'nothing changes'
            self.emit(s.line, self.fallen(f'{s.text[:-1]}: {text}.'), work=ctx['work'], printed=ctx['printed'])
            self.ctx = None
            return
        if k == 'return':
            self.run_return(s)
        if k in ('break', 'continue'):
            if not self.breakable or (k == 'continue' and 'loop' not in self.breakable):
                fail(f'{k} outside a loop')
            if k == 'break':
                self.emit(s.line, self.fallen(f'break leaves the {self.breakable[-1]}.'))
                raise Brk()
            self.emit(s.line, 'continue skips the rest of the loop body.')
            raise Cont()
        if k == 'block':
            self.run_block(s.body)
        elif k == 'if':
            yes = 'the if branch runs' if s.els is not None else 'its body runs'
            no = 'the else branch runs' if s.els is not None else 'its body is skipped'
            truth = self.test(s, s.cond, s.line, yes, no)
            if truth:
                self.run_block(s.then)
            elif s.els is not None:
                self.run_block(s.els)
        elif k == 'while':
            self.loop(s, s.cond, None, s.body)
        elif k == 'for':
            fr = self.frames[-1]
            fr.scopes.append({})
            try:
                if s.init is not None:
                    if s.init.kind == 'decl':
                        self.run_decl(s.init, tag='for loop')
                    else:
                        self.run(s.init)
                self.loop(s, s.cond, s.update, s.body)
            finally:
                self.close_scope(fr)
        elif k == 'do':
            self.breakable.append('loop')
            try:
                while True:
                    try:
                        self.run_block(s.body)
                    except Cont:
                        pass
                    if not self.test(s, s.cond, s.line, 'the loop runs again', 'the loop ends'):
                        break
            except Brk:
                pass
            finally:
                self.breakable.pop()
        elif k == 'switch':
            self.run_switch(s)
        else:
            fail(f'cannot run {k}')

    def run_decl(self, s, tag=None):
        ctx = self.new_ctx()
        objs = self.declare_local(s, tag)
        if 'static' in s.words:
            if id(s) not in self.seen_static:
                self.seen_static.add(id(s))
                names = _list([f'{o.name} = {self.fmt(o.cells[0], o.t) if not is_arr(o.t) else self.array_text(o)}' for o in objs])
                self.emit(s.line, f'{s.text[:-1]}: this was done once, before the program started ({names}), '
                                  f'so this line changes nothing now.')
            self.ctx = None
            return
        unset = [o.name for o, d in zip(objs, s.decls) if d.init is None]
        if len(unset) < len(objs):
            note = self.describe(ctx, initial=True)
            if unset:
                note += f'; {_list(unset)} {"is" if len(unset) == 1 else "are"} not set yet'
        else:
            note = f'{_list(unset)} {"is" if len(unset) == 1 else "are"} created but not set yet'
        self.emit(s.line, self.fallen(f'During this declaration, {note}.'), work=ctx['work'], printed=ctx['printed'])
        self.ctx = None

    def run_return(self, s):
        fr = self.frames[-1]
        ctx = self.new_ctx()
        if s.e is None:
            if fr.func.ret != VOID:
                fail('return without a value')
            self.emit(s.line, self.fallen(f'{fr.func.name} returns.'))
            self.ctx = None
            raise Ret(None, VOID)
        if fr.func.ret == VOID:
            fail('a void function returns a value')
        v, t = self.full(s.e, s.line)
        v = self.convert(v, t, fr.func.ret, s.e)
        pre = self.describe(ctx)
        note = f'{fr.func.name} returns {self.fmt(v, fr.func.ret)}'
        if pre:
            note = f'Before returning, {pre}. {note}'
        self.emit(s.line, self.fallen(note + '.'), work=ctx['work'], printed=ctx['printed'])
        self.ctx = None
        raise Ret(v, fr.func.ret)

    def run_switch(self, s):
        ctx = self.new_ctx()
        v, t = self.full(s.e, s.line)
        if not is_int(t):
            fail('switch on a non-integer')
        v = self.convert(v, t, promote(t))
        stmts = flat(s.body)
        target = None
        for j, x in enumerate(stmts):
            if x.kind == 'label' and x.value is not None and self.rv(x.value)[0] == v:
                target = j
        if target is None:
            target = next((j for j, x in enumerate(stmts) if x.kind == 'label' and x.value is None), None)
        where = f'jumps to {stmts[target].text[:-1]}' if target is not None else 'skips the whole switch: no case matches'
        self.emit(s.line, f'switch ({show(s.e)}): {show(s.e)} is {self.fmt(v, promote(t))}, so control {where}.',
                  work=ctx['work'])
        self.ctx = None
        if target is None:
            return
        fr = self.frames[-1]
        self.breakable.append('switch')
        fr.scopes.append({})
        self.fall = None
        try:
            for x in stmts[target + 1:]:
                self.run(x)
        except Brk:
            pass
        finally:
            self.close_scope(fr)
            self.breakable.pop()
            self.fall = None

    def fallen(self, note):
        if self.fall:
            lab, self.fall = self.fall, None
            return f'No break, so control falls through to {lab}. {note}'
        return note

    def loop(self, s, cond, update, body):
        self.breakable.append('loop')
        first = True
        try:
            while True:
                if not first and update is not None:
                    ctx = self.new_ctx()
                    self.full(update, s.line)
                    text = self.describe(ctx) or 'nothing changes'
                    self.emit(s.line, f'{show(update)}: {text}.', work=ctx['work'], printed=ctx['printed'])
                    self.ctx = None
                first = False
                if cond is None:
                    self.check_loop(s)
                elif not self.test(s, cond, s.line, 'the loop body runs', 'the loop ends'):
                    break
                try:
                    self.run_block(body)
                except Cont:
                    pass
        except Brk:
            pass
        finally:
            self.breakable.pop()

    # ------------------------------------------------ entry

    def start(self, call=None, given=()):
        for g in given:
            for s in simple(g):
                if s.kind != 'decl':
                    fail('given items are declarations')
                self.declare_global(s, kind='given')
        self.writes = []
        intro = []
        for kind, word in (('given', 'given'), ('global', 'global')):
            objs = [o for o in self.objs if o.kind == kind]
            if objs:
                intro.append(_list([f'{o.name} = {self.array_text(o) if is_arr(o.t) else self.fmt(o.cells[0], o.t)}'
                                    for o in objs]) + f' ({word})')
        st = [o for o in self.objs if o.kind == 'static']
        if st:
            intro.append(_list([f'{o.name} = {self.fmt(o.cells[0], o.t) if not is_arr(o.t) else self.array_text(o)}'
                                f' (static in {o.owner})' for o in st]))
        if call is None:
            if 'main' not in self.funcs:
                fail('the program has no main')
            entry = parse_expr('main()')
            note = ('Before main runs, the variables with static storage are set up: ' + '; '.join(intro) + '.') \
                if intro else 'The program starts in main.'
        else:
            entry = parse_expr(call)
            if entry.k != 'call' or entry.a.v not in self.funcs:
                fail(f'{call} is not a call of a listed function')
            note = f'{call} is called.' + (' Already set up: ' + '; '.join(intro) + '.' if intro else '')
        if self.spec.get('assume'):
            note += ' ' + self.spec['assume']
        self.emit(None, note)
        try:
            self.new_ctx()
            v, t, _ = self.rv(entry)
            self.ctx = None
            return (v, t)
        except Stop:
            return None


def _prod(xs):
    p = 1
    for x in xs:
        p *= x
    return p


def _key(c):
    return ('p', c.obj.id if c.obj else None, c.idx) if isinstance(c, Ptr) else c


def _list(xs):
    xs = list(xs)
    if not xs:
        return ''
    return xs[0] if len(xs) == 1 else ', '.join(xs[:-1]) + ' and ' + xs[-1]


def _quote(text):
    return '"' + text.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n') + '"'


def _num(v):
    r = repr(float(v))
    return r[:-2] if r.endswith('.0') else r


def _char(v):
    if v == 0:
        return "'\\0'"
    if v == 10:
        return "'\\n'"
    return f"'{chr(v)}'" if 32 <= v < 127 else str(v)


def _cell(v, t, run):
    """A cell as drawn in the variables table: characters without quotes."""
    if v is None:
        return '?'
    if t == CHAR:
        return '\\0' if v == 0 else '\\n' if v == 10 else chr(v) if 32 <= v < 127 else str(v)
    return run.fmt(v, t)


# ---------------------------------------------------------------- the family

def _lines(text):
    return [' '.join(x.split()) for x in text.strip().split('\n')]


def simulate(spec, call=None, order='ltr'):
    """Run a spec once: returns (run, result) where result is (value, type) or None if the run was cut off."""
    run = Run(spec['program'], spec, order)
    return run, run.start(call=call, given=spec.get('given', ()))


def _closing(qid, spec, run, result, call):
    """Check the run against the expectation and say the answer."""
    exp = spec['expect']
    if exp.get('nonterminating'):
        if not run.repeat:
            fail(f'{qid}: the program does not repeat a state, but the answer says it never ends')
        return 'This test has been reached before with every variable the same, so the loop repeats forever and the program never ends.'
    if result is None:
        fail(f'{qid}: the program does not end, or runs too long for a step-through')
    out = run.out
    if 'output' in exp:
        if out.rstrip('\n') != exp['output']:
            fail(f'{qid}: prints {out!r}, not {exp["output"]!r}')
        return f'The output is {_quote(out.rstrip(chr(10)))}.'
    if 'lines' in exp:
        if _lines(out) != exp['lines']:
            fail(f'{qid}: prints the lines {_lines(out)!r}, not {exp["lines"]!r}')
        return 'The output lines are ' + _list([_quote(x) for x in exp['lines']]) + '.'
    if 'printf_count' in exp:
        if run.prints != exp['printf_count']:
            fail(f'{qid}: printf runs {run.prints} times, not {exp["printf_count"]}')
        return f'printf ran {run.prints} times.'
    if 'return' in exp:
        v = run.fmt(*result)
        if v != str(exp['return']):
            fail(f'{qid}: {call} returns {v}, not {exp["return"]}')
        return f'{call} returns {v}.'
    if 'final' in exp:
        for name, want in exp['final'].items():
            if run.final_main.get(name) != str(want):
                fail(f'{qid}: {name} ends as {run.final_main.get(name)}, not {want}')
        return 'When main ends, ' + _list([f'{n} = {v}' for n, v in exp['final'].items()]) + '.'
    fail(f'{qid}: unknown expectation {exp!r}')


CLAIM_OPS = {'>': lambda a, b: a > b, '<': lambda a, b: a < b, '==': lambda a, b: a == b}


def ctrace_animation(qid, spec):
    exp = spec.get('expect')
    if not exp:
        fail(f'{qid}: no expectation')
    if 'claims' in exp:
        calls = list(dict.fromkeys(c['call'] for c in exp['claims']))
    else:
        calls = spec.get('calls') or [spec.get('call')]
    schedules, lines = [], None
    for call in calls:
        run, result = simulate(spec, call)
        lines = run.lines
        if 'claims' in exp:
            if result is None:
                fail(f'{qid}: {call} does not end')
            v, said = result[0], []
            for c in exp['claims']:
                if c['call'] == call:
                    holds = CLAIM_OPS[c['op']](v, c['than'])
                    if holds != c['holds']:
                        fail(f'{qid}: {call} = {v}, so "{c["text"]}" is {holds}, not {c["holds"]}')
                    said.append(f'{"True" if holds else "False"}: {c["text"]}.')
            closing = f'{call} returns {v}. ' + ' '.join(said)
        else:
            closing = _closing(qid, spec, run, result, call)
        if run.unspecified:
            if not spec.get('order_independent'):
                fail(f'{qid}: the result could depend on the order of evaluation')
            other, oresult = simulate(spec, call, order='rtl')
            if other.out != run.out or (result and oresult and run.fmt(*result) != other.fmt(*oresult)):
                fail(f'{qid}: the other order of evaluation gives a different result')
        elif spec.get('order_independent'):
            fail(f'{qid}: order_independent is set, but nothing depends on the order')
        last = run.steps[-1]
        note = closing if run.repeat else ('The program ends. ' if call is None else 'Finished. ') + closing
        run.steps.append(dict(line=None, note=note, vars=last['vars'] if run.repeat else
                              [g for g in last['vars'] if g['title'] in ('given', 'globals') or g['title'].startswith('static')],
                              out=run.out, final=True))
        for st in run.steps:
            if st.get('line') is None:
                st.pop('line', None)
        schedules.append(dict(short=call or 'main', title=f'Running {call}' if call else 'Running the program',
                              steps=run.steps))
    return dict(kind='c-trace', code=lines, schedules=schedules, count=sum(len(s['steps']) for s in schedules))


KINDS = {'c-trace': ctrace_animation}
PLAYER = 'ctrace'
TABS = 'calls'
