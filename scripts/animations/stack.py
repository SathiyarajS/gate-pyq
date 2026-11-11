"""Stacks and expressions: infix to postfix, postfix evaluation, push/pop traces
and which output orders a stack can produce.

Data: data/animations/stack.json. Each entry is simulated at build time and
checked against the expected answer; the build stops on any difference.

Every step has the same shape, so one player draws all four kinds:
  pos     index of the current token in the schedule's strip (or None)
  stacks  [{name, items (bottom to top), cap, new}]  new: the top was just pushed
  queues  [{name, items (front to rear)}]
  out     {label, items} or None
  facts   short lines such as 's = 62'
"""
import re
from collections import deque
from fractions import Fraction

from .common import _fmt, _list


# ---------------------------------------------------------------- shared bits

def _stack(name, items, cap=None, new=False):
    return dict(name=name, items=[str(x) for x in items], cap=cap, new=new)


def _queue(name, items):
    return dict(name=name, items=[str(x) for x in items])


def _out(label, items):
    return dict(label=label, items=[str(x) for x in items])


def _step(note, pos=None, stacks=(), queues=(), out=None, facts=(), **extra):
    return dict(note=note, pos=pos, stacks=list(stacks), queues=list(queues), out=out, facts=list(facts), **extra)


def _seq(xs):
    return ', '.join(str(x) for x in xs)


def _tokens(text):
    return text.split() if isinstance(text, str) else [str(x) for x in text]


def _check(qid, what, got, want):
    if got != want:
        raise SystemExit(f'Animation for {qid} gives {what} {got!r}, not the expected {want!r}')


# ------------------------------------------------------ infix to postfix

# The usual table; a question that states its own precedence or associativity
# gives it in the spec as {op: [level, 'left'|'right']} (a higher level binds tighter).
STANDARD = {'+': [1, 'left'], '-': [1, 'left'], '−': [1, 'left'], '*': [2, 'left'], '×': [2, 'left'],
            '/': [2, 'left'], '^': [3, 'right']}


def _infix_tokens(text, ops, functions):
    out = []
    for tok in re.findall(r'[A-Za-z0-9.]+|\S', text):
        if tok in ops or tok in '()' or tok in functions or re.fullmatch(r'[A-Za-z0-9.]+', tok):
            out.append(tok)
        else:
            raise SystemExit(f'Unknown symbol in expression {text!r}: {tok}')
    return out


def infix_to_postfix(text, precedence=None, functions=()):
    """Shunting-yard conversion. Returns (tokens, steps, postfix tokens)."""
    ops = {k: tuple(v) for k, v in (precedence or STANDARD).items()}
    for op, (_, assoc) in ops.items():
        if assoc not in ('left', 'right'):
            raise SystemExit(f'Associativity of {op} must be left or right')
    functions = set(functions)
    toks = _infix_tokens(text, ops, functions)
    stack, out, steps = [], [], []

    def snap(note, pos, new=False):
        steps.append(_step(note, pos, [_stack('Operator stack', stack, new=new)], out=_out('Postfix output', out)))

    snap('Read the expression from left to right. Operands go straight to the output; operators wait on the stack.', None)
    for i, tok in enumerate(toks):
        if tok == '(':
            stack.append(tok)
            snap('Push ( . It holds back everything until the matching ) arrives.', i, True)
        elif tok == ')':
            popped = []
            while stack and stack[-1] != '(':
                popped.append(stack.pop())
            if not stack:
                raise SystemExit(f'Unbalanced ) in {text!r}')
            stack.pop()
            out.extend(popped)
            note = (f'Pop {_list(popped)} to the output until ( is reached, then discard both brackets.' if popped
                    else 'The top is ( , so discard both brackets.')
            if stack and stack[-1] in functions:
                f = stack.pop()
                out.append(f)
                note += f' The argument of {f} is complete, so {f} goes to the output too.'
            snap(note, i)
        elif tok in functions:
            stack.append(tok)
            snap(f'{tok} is a function, so push it; it is output once its argument is complete.', i, True)
        elif tok in ops:
            level, assoc = ops[tok]
            reasons, popped = [], []
            while stack and stack[-1] in ops:
                top = stack[-1]
                tl = ops[top][0]
                if tl > level:
                    reasons.append(f'{top} has higher precedence than {tok}')
                elif tl == level and assoc == 'left':
                    reasons.append(f'{top} has the same precedence as {tok} and they group left to right' if top != tok
                                   else f'{tok} groups left to right, so the earlier {tok} is applied first')
                else:
                    break
                popped.append(stack.pop())
            out.extend(popped)
            if not stack:
                why = 'the stack is now empty' if popped else 'the stack is empty'
            elif stack[-1] == '(':
                why = 'the top is ('
            elif stack[-1] in functions:
                why = f'the top is the function {stack[-1]}'
            else:
                top = stack[-1]
                if ops[top][0] < level:
                    why = f'{tok} has higher precedence than {top}'
                elif top == tok:
                    why = f'{tok} groups right to left: the {tok} already on the stack waits'
                else:
                    why = f'{tok} and {top} group right to left: {top} waits'
            note = ''.join(f'{r[0].upper() + r[1:]}, so pop {p}. ' for r, p in zip(reasons, popped))
            note += why[0].upper() + why[1:] + (f', and the new {tok} goes on top.' if ':' in why else f', so push {tok}.')
            stack.append(tok)
            snap(note, i, True)
        else:
            out.append(tok)
            snap(f'{tok} is an operand, so it goes straight to the output.', i)
    rest = stack[::-1]
    if '(' in rest:
        raise SystemExit(f'Unbalanced ( in {text!r}')
    stack.clear()
    out.extend(rest)
    snap((f'End of the expression: pop {_list(rest)} to the output, top first.' if rest
          else 'End of the expression; the stack is already empty.'), None)
    return toks, steps, out


def postfix_animation(qid, spec):
    toks, steps, out = infix_to_postfix(spec['infix'], spec.get('precedence'), spec.get('functions', ()))
    want = _tokens(spec['expect']['postfix'])
    _check(qid, 'postfix', out, want)
    last = dict(steps[-1])
    last.update(final=True, note=last['note'] + ' Postfix: ' + ' '.join(out) + '.')
    steps[-1] = last
    title = 'Infix to postfix with an operator stack'
    if spec.get('precedence'):
        ops = sorted(spec['precedence'].items(), key=lambda kv: -kv[1][0])
        title += '; precedence ' + ' > '.join(k for k, _ in ops)
        right = [k for k, v in ops if v[1] == 'right']
        if right:
            title += '; ' + _list(right) + ' right-associative'
    return dict(kind='stack-postfix', schedules=[dict(short='Convert', title=title, strip=dict(label='Infix', tokens=toks), steps=steps)],
                count=len(steps))


# ------------------------------------------------------ postfix evaluation

BINARY = {'+': lambda a, b: a + b, '-': lambda a, b: a - b, '−': lambda a, b: a - b, '*': lambda a, b: a * b,
          '×': lambda a, b: a * b, '/': None, '^': None}


def _apply(op, a, b):
    if op == '/':
        if b == 0:
            raise SystemExit('Division by zero')
        if Fraction(a, b).denominator != 1:
            raise SystemExit(f'{a} / {b} is not exact; the question must say how division rounds')
        return Fraction(a, b)
    if op == '^':
        if b.denominator != 1 or b < 0:
            raise SystemExit(f'Exponent {b} is not a non-negative integer')
        return a ** int(b)
    return BINARY[op](a, b)


def _infix_of(tree):
    if isinstance(tree, str):
        return tree
    op, l, r = tree
    wrap = lambda t: t if isinstance(t, str) else '(' + _infix_of(t) + ')'
    return f'{wrap(l)} {op} {wrap(r)}'


def _order(tree, order):
    if isinstance(tree, str):
        return [tree]
    op, l, r = tree
    parts = {'root': [op], 'left': _order(l, order), 'right': _order(r, order)}
    return [x for part in order for x in parts[part]]


def postfix_evaluate(tokens, stop=None, tree=False):
    """Evaluate (or, with tree=True, build the expression tree of) a postfix expression.

    stop: None for the whole expression, {'tokens': n} to stop after n tokens, or
    {'after': op, 'occurrence': k} to stop right after the k-th time op is applied.
    """
    toks = _tokens(tokens)
    stack, steps, seen = [], [], {}
    show = (lambda v: _infix_of(v)) if tree else (lambda v: _fmt(v))
    snap = lambda note, pos, new=False: steps.append(_step(note, pos, [_stack('Stack', [show(v) for v in stack], new=new)]))
    snap('Read the tokens from left to right. An operand is pushed; an operator pops two values, right operand first.'
         if not tree else 'Read the tokens from left to right. An operand becomes a one-node tree and is pushed; an operator pops two trees, right child first, and pushes the joined tree.', None)
    stopped = None
    for i, tok in enumerate(toks):
        if tok in BINARY:
            if len(stack) < 2:
                raise SystemExit(f'Operator {tok} at token {i + 1} needs two operands')
            b, a = stack.pop(), stack.pop()
            if tree:
                v = (tok, a, b)
                note = f'{tok} pops {show(b)} (right child) and {show(a)} (left child) and pushes the tree {_infix_of(v)}.'
            else:
                v = _apply(tok, a, b)
                note = f'{tok} pops {show(b)} (right) and then {show(a)} (left), and pushes {show(a)} {tok} {show(b)} = {show(v)}.'
            stack.append(v)
            snap(note, i, True)
            seen[tok] = seen.get(tok, 0) + 1
        else:
            if tree:
                v = tok
            else:
                try:
                    v = Fraction(tok)
                except ValueError:
                    raise SystemExit(f'Operand {tok!r} is not a number')
            stack.append(v)
            snap(f'{tok} is an operand, so push it.', i, True)
        if stop and (stop.get('tokens') == i + 1 or (stop.get('after') == tok and seen.get(tok) == stop.get('occurrence', 1))):
            stopped = i + 1
            break
    if stop and stopped is None:
        raise SystemExit(f'The stopping point {stop} is never reached')
    if not stop and len(stack) != 1:
        raise SystemExit(f'Postfix expression leaves {len(stack)} values on the stack')
    return toks, steps, stack, stopped


def eval_animation(qid, spec):
    tree = bool(spec.get('traversal'))
    toks, steps, stack, stopped = postfix_evaluate(spec['postfix'], spec.get('stop'), tree)
    expect, last = spec['expect'], dict(steps[-1])
    show = (lambda v: _infix_of(v)) if tree else _fmt
    where = (f'After the first {stopped} tokens ({" ".join(toks[:stopped])})' if spec.get('stop') else 'At the end')
    notes = []
    if not expect:
        raise SystemExit(f'Animation for {qid} has nothing to check')
    if 'stack' in expect:
        _check(qid, 'stack', [show(v) for v in stack], [str(x) for x in expect['stack']])
        notes.append(f'{where} the stack, bottom to top, is {_seq(show(v) for v in stack)}.')
    if 'top' in expect:
        n = len(expect['top'])
        got = [show(v) for v in stack[::-1][:n]]
        _check(qid, 'top of stack', got, [str(x) for x in expect['top']])
        notes.append(f'{where} the top {"two values are" if n == 2 else str(n) + " values are" if n > 1 else "value is"} {_seq(got)}' + (', top first.' if n > 1 else '.'))
    if 'value' in expect:
        if len(stack) != 1:
            raise SystemExit(f'Animation for {qid} leaves {len(stack)} values, not one')
        _check(qid, 'value', show(stack[0]), str(expect['value']))
        notes.append(f'The stack holds one value, {show(stack[0])}: the answer.')
    if 'traversal' in expect:
        order = spec['traversal']
        if sorted(order) != ['left', 'right', 'root']:
            raise SystemExit(f'Traversal for {qid} must name root, left and right once each')
        seq = _order(stack[0], order)
        _check(qid, 'traversal', seq, _tokens(expect['traversal']))
        steps.append(last)
        last = dict(last, pos=None, out=_out('Visited', seq), stacks=[])
        notes = [f'The stack holds the whole tree. Visiting it {", ".join(order[:2])}, {order[2]} at every node gives {" ".join(seq)}.']
    last.update(final=True, note=(last['note'] + ' ' if 'traversal' not in expect else '') + ' '.join(notes))
    steps[-1] = last
    title = ('Building the expression tree with a stack' if tree else 'Postfix evaluation with an operand stack')
    return dict(kind='stack-eval', schedules=[dict(short='Evaluate', title=title, strip=dict(label='Postfix', tokens=toks), steps=steps)],
                count=len(steps))


# ------------------------------------------------------ push / pop traces

_OP = re.compile(r'^(?:(\w+)\s*=\s*)?(push|pop|enqueue|dequeue)(?:\s+(dequeue|pop|-?\d+))?$')


def run_ops(ops):
    """Run push/pop/enqueue/dequeue operations on one stack S and one queue Q.

    Forms: 'push 5', 'pop', 's = pop', 'enqueue 5', 'dequeue', 'q = dequeue',
    'push dequeue' (move the front of Q onto S) and 'enqueue pop'.
    Returns (steps, stack, queue, popped, variables).
    """
    S, Q, popped, var = [], [], [], {}
    use_q = any(re.search(r'queue', o) for o in ops)
    steps = []

    def snap(note, new=False, text=None):
        label = f'Operation {len(steps)} of {len(ops)}: {text}' if text else None
        steps.append(_step(note, None, [_stack('Stack S', S, new=new)], [_queue('Queue Q', Q)] if use_q else [],
                           out=_out('Popped from S', popped), facts=[f'{k} = {v}' for k, v in var.items()], label=label))

    def take(kind):
        if kind == 'pop':
            if not S:
                raise SystemExit('pop on an empty stack')
            x = S.pop()
            popped.append(x)
            return x
        if not Q:
            raise SystemExit('dequeue on an empty queue')
        return Q.pop(0)

    snap('Both start empty.' if use_q else 'The stack starts empty.')
    for op in ops:
        m = _OP.match(op.strip())
        if not m:
            raise SystemExit(f'Unknown operation: {op}')
        name, verb, arg = m.groups()
        if verb in ('push', 'enqueue'):
            if name or arg is None:
                raise SystemExit(f'Unknown operation: {op}')
            if arg in ('pop', 'dequeue'):
                x = take(arg)
                (S if verb == 'push' else Q).append(x)
                snap(f'Dequeue {x} from the front of Q and push it onto S.' if verb == 'push'
                     else f'Pop {x} from the top of S and enqueue it at the rear of Q.', verb == 'push', f'{verb}({arg}())')
            else:
                x = int(arg)
                (S if verb == 'push' else Q).append(x)
                snap(f'Push {x}; it is now the top.' if verb == 'push' else f'Enqueue {x} at the rear.', verb == 'push', f'{verb}({x})')
        else:
            if arg:
                raise SystemExit(f'Unknown operation: {op}')
            x = take(verb)
            if name:
                var[name] = x
            if verb == 'pop':
                note = f'Pop removes {x}, the most recent item still on the stack' + (f', so {name} = {x}.' if name else '.')
            else:
                note = f'Dequeue removes {x}, the oldest item in the queue' + (f', so {name} = {x}.' if name else '.')
            snap(note, text=(f'{name} = ' if name else '') + verb + '()')
    return steps, S, Q, popped, var


def ops_animation(qid, spec):
    steps, S, Q, popped, var = run_ops(spec['ops'])
    expect, notes = spec['expect'], []
    if not expect:
        raise SystemExit(f'Animation for {qid} has nothing to check')
    if 'popped' in expect:
        _check(qid, 'popped values', popped, expect['popped'])
        notes.append(f'The pops return {_seq(popped)}, in that order.')
    if 'vars' in expect:
        _check(qid, 'values', var, expect['vars'])
    if 'answer' in expect:
        names = [x.strip() for x in spec['answer'].split('+')]
        if any(n not in var for n in names):
            raise SystemExit(f'Animation for {qid}: {spec["answer"]} names a value that is never set')
        total = sum(var[n] for n in names)
        _check(qid, spec['answer'], total, expect['answer'])
        notes.append(f'{spec["answer"]} = {" + ".join(str(var[n]) for n in names)} = {total}.')
    if 'top' in expect:
        if not S:
            raise SystemExit(f'Animation for {qid} ends with an empty stack')
        _check(qid, 'top', S[-1], expect['top'])
        notes.append(f'The stack, bottom to top, is {_seq(S)}, so the top is {S[-1]}.')
    steps.append(dict(steps[-1], final=True, note=' '.join(notes)))
    title = 'Stack and queue operations' if any('queue' in o for o in spec['ops']) else 'Stack operations'
    return dict(kind='stack-ops', schedules=[dict(short='Trace', title=title, steps=steps)], count=len(steps))


# ------------------------------------------------------ stack + queue split

def split_animation(qid, spec):
    """Items arrive in order; those in the option's set go on stack S, the rest on queue Q.
    Then S is emptied, then Q. Which options give the target output?"""
    items, target = spec['items'], spec['target']
    schedules, valid = [], []
    for chosen in spec['options']:
        if any(x not in items for x in chosen):
            raise SystemExit(f'Option {chosen} for {qid} names an item that never arrives')
        S, Q, out, steps = [], [], [], []
        snap = lambda note, new=False, label=None, pos=None: steps.append(_step(note, pos, [_stack('Stack S', S, new=new)], [_queue('Queue Q', Q)], _out('Output', out), label=label))
        snap(f'Items {_seq(items)} arrive in this order. {_list([str(x) for x in chosen])} go on the stack; the others join the queue.')
        for x in items:
            if x in chosen:
                S.append(x)
                snap(f'{x} arrives and is pushed onto S.', True, f'{x} arrives')
            else:
                Q.append(x)
                snap(f'{x} arrives and joins the rear of Q.', label=f'{x} arrives')
        while S:
            out.append(S.pop())
            snap(f'Empty S first: pop {out[-1]} from the top.', label='Empty S', pos=len(out) - 1)
        while Q:
            out.append(Q.pop(0))
            snap(f'Then empty Q: dequeue {out[-1]} from the front.', label='Empty Q', pos=len(out) - 1)
        ok = out == target
        if ok:
            valid.append(list(chosen))
        steps.append(dict(steps[-1], final=True, pos=None, note=f'Output {_seq(out)} ' + ('matches' if ok else 'differs from') + f' the required {_seq(target)}' + ('.' if ok else ', so this split does not work.')))
        schedules.append(dict(short='S = {' + ', '.join(map(str, chosen)) + '}', title=f'Stack gets {{{_seq(chosen)}}}, queue gets the rest; target {_seq(target)}',
                              strip=dict(label='Wanted', tokens=[str(x) for x in target]), steps=steps))
    _check(qid, 'working splits', valid, spec['expect'])
    return dict(kind='stack-split', schedules=schedules, count=sum(len(s['steps']) for s in schedules))


# ------------------------------------------------------ which outputs are possible

def stack_moves(spec, target):
    """Search every sequence of moves for one that outputs `target`.

    spec: input (arrival order, may be empty), stacks {name: {init, cap}},
    moves [{name, from, to}] where from is 'input' or a stack and to is a stack or 'output'.
    Returns (found, path) where path is the list of move names: the shortest one that
    outputs target, or else the longest of the shortest runs that output as much of target as possible.
    """
    names = list(spec['stacks'])
    inp = list(spec.get('input', []))
    caps = [spec['stacks'][n].get('cap') for n in names]
    start = (0, tuple(tuple(spec['stacks'][n].get('init', [])) for n in names), 0)
    for n, c, s in zip(names, caps, start[1]):
        if c is not None and len(s) > c:
            raise SystemExit(f'{n} starts with more than its capacity')
    moves = spec['moves']
    for m in moves:
        if m['from'] not in names + ['input'] or m['to'] not in names + ['output']:
            raise SystemExit(f'Unknown move {m}')
    prev, frontier = {start: None}, deque([start])
    while frontier:
        st = frontier.popleft()
        i, stacks, k = st
        if k == len(target):
            break
        for m in moves:
            if m['from'] == 'input':
                if i >= len(inp):
                    continue
                x, ni, ns = inp[i], i + 1, list(stacks)
            else:
                a = names.index(m['from'])
                if not stacks[a]:
                    continue
                x, ni, ns = stacks[a][-1], i, list(stacks)
                ns[a] = stacks[a][:-1]
            if m['to'] == 'output':
                if x != target[k]:
                    continue
                nk = k + 1
            else:
                b = names.index(m['to'])
                if caps[b] is not None and len(ns[b]) >= caps[b]:
                    continue
                ns[b] = ns[b] + (x,)
                nk = k
            nxt = (ni, tuple(ns), nk)
            if nxt not in prev:
                prev[nxt] = (st, m['name'])
                frontier.append(nxt)
    best = max(prev, key=lambda s: s[2])
    found = best[2] == len(target)
    if not found:
        # Among the states that get furthest, show the one the longest run reaches.
        depth = {}
        for s in prev:
            d, t = 0, s
            while prev[t]:
                t, d = prev[t][0], d + 1
            depth[s] = d
        best = max((s for s in prev if s[2] == best[2]), key=lambda s: (depth[s], s))
    path, st = [], best
    while prev[st]:
        st, name = prev[st]
        path.append(name)
    return found, path[::-1]


def moves_animation(qid, spec):
    names = list(spec['stacks'])
    inp = list(spec.get('input', []))
    caps = {n: spec['stacks'][n].get('cap') for n in names}
    moves = {m['name']: m for m in spec['moves']}
    schedules, possible = [], []
    for target in spec['targets']:
        found, path = stack_moves(spec, target)
        if found:
            possible.append(list(target))
        st = {n: list(spec['stacks'][n].get('init', [])) for n in names}
        rest, out, steps = list(inp), [], []

        def snap(note, new=None, label=None):
            qs = [_queue('Input', rest)] if inp else []
            stacks = [_stack(n, st[n], caps[n], n == new) for n in names]
            steps.append(_step(note, len(out) if len(out) < len(target) else None, stacks, qs, _out('Output', out), label=label))

        start = []
        if inp:
            start.append(f'Items {_seq(inp)} arrive in this order.')
        call = lambda n: 'The stack' if len(names) == 1 else n
        start += [f'{call(n)} holds {_seq(st[n])}, bottom to top' + (f' (capacity {caps[n]})' if caps[n] else '') + '.' if st[n]
                  else f'{call(n)} is empty' + (f' (capacity {caps[n]})' if caps[n] else '') + '.' for n in names]
        snap(' '.join(start) + f' Goal: output {_seq(target)}.')
        for k, name in enumerate(path, 1):
            m = moves[name]
            x = rest.pop(0) if m['from'] == 'input' else st[m['from']].pop()
            label = f'Move {k} of {len(path)}: {name} ({m["from"].capitalize()} → {m["to"].capitalize()})'
            if m['to'] == 'output':
                out.append(x)
                src = 'the stack' if len(names) == 1 else m['from']
                snap(f'{x} is on top of {src} and is the next item wanted, so output it.', label=label)
            else:
                st[m['to']].append(x)
                dst = 'the stack' if len(names) == 1 else m['to']
                snap((f'Push {x}, the next arrival, onto {dst}.' if m['from'] == 'input'
                      else f'Move {x} from the top of {m["from"]} onto {dst}.'), m['to'], label)
        if found:
            note = f'Output {_seq(target)} is possible: the moves above produce it.'
        else:
            want = target[len(out)]
            done = f'after {_seq(out)}' if out else 'first'
            where = [n for n in names if want in st[n]]
            why = ''
            if where and st[where[0]][-1] != want:
                above = st[where[0]][st[where[0]].index(want) + 1:]
                why = f' {want} is under {_list([str(a) for a in above[::-1]])} in {"the stack" if len(names) == 1 else where[0]}.'
            note = f'Stuck.{why} Trying every possible sequence of moves shows that none outputs {want} {done}, so {_seq(target)} is impossible.'
        steps.append(dict(steps[-1], final=True, pos=None if found else len(out), note=note))
        schedules.append(dict(short=' '.join(map(str, target)), title=('Possible' if found else 'Impossible') + f': output {_seq(target)}',
                              strip=dict(label='Wanted', tokens=[str(x) for x in target]), steps=steps))
    _check(qid, 'possible outputs', possible, spec['expect'])
    return dict(kind='stack-moves', schedules=schedules, count=sum(len(s['steps']) for s in schedules))


# Animation kinds this family provides, and the player file that draws them.
KINDS = {'stack-postfix': postfix_animation, 'stack-eval': eval_animation, 'stack-ops': ops_animation,
         'stack-split': split_animation, 'stack-moves': moves_animation}
PLAYER = 'stack'
TABS = 'options'
