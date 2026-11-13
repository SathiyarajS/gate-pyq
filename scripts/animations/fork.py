"""Process creation with fork(): the process tree, grown one fork() at a time.

Data: data/animations/fork.json. Each entry states the question's program as a
list of statements and the expected count. The simulator runs the program for
every process (each fork succeeds; the child gets 0 and the parent the child's
number) and the build stops if the count differs from the expectation.

Statements (one dict each, keyed by "op"):
  {"op": "fork"}                                   fork();
  {"op": "if_fork", "test": "== 0", "then": [...], "else": [...]}
                                                   if (fork() == 0) {...} else {...}
  {"op": "for", "var": "i", "from": 0, "to": 3, "body": [...]}
                                                   for (i = 0; i < 3; i++) {...}
  {"op": "while", "cond": "x > 0", "body": [...]}  while (x > 0) {...}
  {"op": "if", "cond": "i % 2 == 0", "then": [...], "else": [...]}
  {"op": "int", "var": "x", "value": 3}            int x = 3;
  {"op": "dec", "var": "x"}                        x--;
  {"op": "printf", "text": "hello"}                printf("hello");
  {"op": "wait"}                                   wait(NULL);
  {"op": "break"}, {"op": "continue"}, {"op": "return"}, {"op": "exit"}

The program listing shown beside the tree is printed from these statements, so
it is always the program that was simulated.

Processes run in rounds: in each round every process that is ready takes one
turn, in order P0, P1, ..., and a turn lasts until the process calls fork(),
has to wait for a child, or ends. A child created in a round first runs in the
next round, so the calls line up with the usual "each fork doubles" reasoning.
"""
import ast
import json
import operator

ORDINAL = ['first', 'second', 'third', 'fourth', 'fifth', 'sixth', 'seventh', 'eighth']
_BIN = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.Mod: operator.mod,
        ast.FloorDiv: operator.floordiv, ast.Pow: operator.pow, ast.BitXor: operator.pow}
_CMP = {ast.Eq: operator.eq, ast.NotEq: operator.ne, ast.Lt: operator.lt, ast.LtE: operator.le,
        ast.Gt: operator.gt, ast.GtE: operator.ge}
MAX_PROCESSES = 64


def _eval(text, env):
    """Integer expressions over the program's variables: + - * % ** (or ^), comparisons, and/or/not."""
    def ev(n):
        if isinstance(n, ast.Expression):
            return ev(n.body)
        if isinstance(n, ast.Constant) and isinstance(n.value, int):
            return n.value
        if isinstance(n, ast.Name):
            if n.id not in env:
                raise SystemExit(f'Unknown variable {n.id} in {text!r}')
            return env[n.id]
        if isinstance(n, ast.BinOp) and type(n.op) in _BIN:
            return _BIN[type(n.op)](ev(n.left), ev(n.right))
        if isinstance(n, ast.UnaryOp) and isinstance(n.op, ast.USub):
            return -ev(n.operand)
        if isinstance(n, ast.UnaryOp) and isinstance(n.op, ast.Not):
            return int(not ev(n.operand))
        if isinstance(n, ast.BoolOp):
            vals = (ev(v) for v in n.values)
            return int(all(vals) if isinstance(n.op, ast.And) else any(vals))
        if isinstance(n, ast.Compare):
            left = ev(n.left)
            for op, right in zip(n.ops, n.comparators):
                if type(op) not in _CMP:
                    break
                right = ev(right)
                if not _CMP[type(op)](left, right):
                    return 0
                left = right
            else:
                return 1
        raise SystemExit(f'Unsupported expression {text!r}')
    src = text.replace('−', '-').replace('&&', ' and ').replace('||', ' or ')
    return ev(ast.parse(src, mode='eval'))


def _names(text):
    return sorted({n.id for n in ast.walk(ast.parse(text.replace('−', '-'), mode='eval')) if isinstance(n, ast.Name)})


# ---------------------------------------------------------------- listing

def listing(stmts):
    """Print the statements as C and give each statement the index of its line."""
    lines, forks = [], []

    def out(text, depth):
        lines.append('  ' * depth + text)
        return len(lines) - 1

    def block(body, depth):
        for s in body:
            stmt(s, depth)

    def stmt(s, depth):
        op = s.get('op')
        if op == 'fork':
            s['_line'] = out('fork();', depth)
            forks.append(s)
        elif op == 'if_fork':
            test = s.get('test', '== 0')
            if test not in ('== 0', '!= 0', '> 0'):
                raise SystemExit(f'Unsupported fork() test: {test}')
            s['_line'] = out(f'if (fork() {test}) {{', depth)
            forks.append(s)
            block(s.get('then', []), depth + 1)
            if s.get('else'):
                out('} else {', depth)
                block(s['else'], depth + 1)
            out('}', depth)
        elif op == 'for':
            v = s['var']
            s['_line'] = out(f"for ({v} = {s['from']}; {v} < {s['to']}; {v}++) {{", depth)
            block(s['body'], depth + 1)
            out('}', depth)
        elif op == 'while':
            s['_line'] = out(f"while ({s['cond']}) {{", depth)
            block(s['body'], depth + 1)
            out('}', depth)
        elif op == 'if':
            s['_line'] = out(f"if ({s['cond']}) {{", depth)
            block(s['then'], depth + 1)
            if s.get('else'):
                out('} else {', depth)
                block(s['else'], depth + 1)
            out('}', depth)
        elif op == 'int':
            s['_line'] = out(f"int {s['var']} = {s['value']};", depth)
        elif op == 'dec':
            s['_line'] = out(f"{s['var']}--;", depth)
        elif op == 'printf':
            if '"' in s['text'] or '\\' in s['text']:
                raise SystemExit('printf text must be plain')
            s['_line'] = out(f'printf("{s["text"]}");', depth)
        elif op == 'wait':
            s['_line'] = out('wait(NULL);', depth)
        elif op in ('break', 'continue'):
            s['_line'] = out(op + ';', depth)
        elif op == 'return':
            s['_line'] = out('return 0;', depth)
        elif op == 'exit':
            s['_line'] = out('exit(0);', depth)
        else:
            raise SystemExit(f'Unknown statement: {s}')

    block(stmts, 0)
    for k, s in enumerate(forks):
        s['_ord'] = k
    return lines, len(forks)


# ---------------------------------------------------------------- one process

class _Break(Exception):
    pass


class _Continue(Exception):
    pass


class _End(Exception):
    pass


def _program(stmts, env):
    """A generator for one process. It yields events and receives fork() results."""
    loops = []  # names of the variables that identify the current loop iteration

    def run(body):
        for s in body:
            yield from one(s)

    def one(s):
        op = s['op']
        if op in ('fork', 'if_fork'):
            ctx = {v: env[v] for v in dict.fromkeys(x for names in loops for x in names)}
            r = yield ('fork', s, ctx)
            if op == 'if_fork':
                taken = {'== 0': r == 0, '!= 0': r != 0, '> 0': r > 0}[s.get('test', '== 0')]
                yield from run(s.get('then', []) if taken else s.get('else', []))
        elif op == 'for':
            v = s['var']
            env[v] = _eval(str(s['from']), env)
            loops.append([v])
            try:
                while True:
                    if not _eval(f"{v} < {s['to']}", env):
                        yield ('loop_end', s, f"{v} = {env[v]}")
                        break
                    try:
                        yield from run(s['body'])
                    except _Continue:
                        yield ('continue', s, f'{v} becomes {env[v] + 1}')
                    env[v] += 1
            except _Break:
                yield ('break', s, None)
            loops.pop()
        elif op == 'while':
            loops.append(_names(s['cond']))
            try:
                while True:
                    if not _eval(s['cond'], env):
                        yield ('loop_end', s, ', '.join(f'{v} = {env[v]}' for v in _names(s['cond'])))
                        break
                    try:
                        yield from run(s['body'])
                    except _Continue:
                        pass
            except _Break:
                yield ('break', s, None)
            loops.pop()
        elif op == 'if':
            yield from run(s['then'] if _eval(s['cond'], env) else s.get('else', []))
        elif op == 'int':
            env[s['var']] = s['value']
        elif op == 'dec':
            env[s['var']] -= 1
        elif op == 'printf':
            yield ('printf', s, s['text'])
        elif op == 'wait':
            yield ('wait', s, None)
        elif op == 'break':
            raise _Break
        elif op == 'continue':
            raise _Continue
        elif op in ('return', 'exit'):
            raise _End

    def main():
        try:
            yield from run(stmts)
        except _End:
            pass
        yield ('end', None, None)

    return main()


# ---------------------------------------------------------------- all processes

def _ctx_label(ctx):
    return ', '.join(f'{k} = {v}' for k, v in ctx.items())


def simulate(stmts, params=None):
    """Run the program in every process. Returns (steps, nodes, calls, totals)."""
    stmts = json.loads(json.dumps(stmts))  # a private copy; repeated statements become separate dicts
    lines, n_forks = listing(stmts)
    procs = []  # dict(gen, history, parent, status, kids, call, depth, prints)
    calls, call_index = [], {}
    totals = dict(processes=1, children=0, prints=0)

    def start(history, parent, call, depth):
        g = _program(stmts, dict(params or {}))
        ev = next(g)
        for r in history:  # replay what the parent has already done
            while ev[0] != 'fork':
                ev = g.send(None)
            ev = g.send(r)
        p = dict(gen=g, ev=ev, history=list(history), parent=parent, status='ready', kids=[], call=call, depth=depth)
        procs.append(p)
        return len(procs) - 1

    def name(k):
        return f'P{k}'

    def snapshot():
        return ''.join({'ready': 'r', 'wait': 'w', 'done': 'd'}[p['status']] for p in procs)

    start([], None, None, 0)
    steps = [dict(n=1, status='r', actor=None, new=None, line=None, call=None, prints=0, children=0,
                  note='Start: one process, P0, is about to run the program.')]
    zombies, explained = set(), False
    while any(p['status'] == 'ready' for p in procs):
        for k in [k for k, p in enumerate(procs) if p['status'] == 'ready']:
            p = procs[k]
            acts, line, new, call = [], None, None, None
            if p.get('woke') is not None:
                acts.append(f"is woken: its child {name(p.pop('woke'))} has ended, so wait(NULL) returns")
            while True:
                kind, s, info = p['ev']
                if kind == 'fork':
                    if len(procs) >= MAX_PROCESSES:
                        raise SystemExit('Too many processes for the fork player')
                    key = (s['_ord'], tuple(info.items()))
                    if key not in call_index:
                        label = (_ctx_label(info) if info else '') if n_forks == 1 else \
                            (f'fork {s["_ord"] + 1}' + (f', {_ctx_label(info)}' if info else ''))
                        call_index[key] = len(calls)
                        calls.append(dict(label=label or 'fork()', line=s['_line']))
                    call = call_index[key]
                    child = len(procs)
                    which = 'fork()' if n_forks == 1 else f'the {ORDINAL[s["_ord"]]} fork()'
                    where = f' at {_ctx_label(info)}' if info else ''
                    start(p['history'] + [0], k, call, p['depth'] + 1)
                    p['history'].append(child)
                    p['kids'].append(child)
                    totals['processes'] += 1
                    totals['children'] += 1
                    acts.append(f'calls {which}{where} and creates {name(child)}')
                    if s['op'] == 'if_fork' and not explained:
                        explained = True
                        acts[-1] += f': fork() returns 0 in {name(child)} and a non-zero value in {name(k)}'
                    line, new = s['_line'], child
                    p['ev'] = p['gen'].send(child)
                    break
                if kind == 'printf':
                    totals['prints'] += 1
                    acts.append(f'prints "{info}"')
                    line = s['_line']
                elif kind == 'break':
                    acts.append('breaks out of the loop')
                    line = s['_line']
                elif kind == 'continue':
                    acts.append(f'runs continue, so {info}')
                elif kind == 'loop_end':
                    acts.append(f'leaves the loop (now {info})')
                    line = s['_line']
                elif kind == 'wait':
                    line = s['_line']
                    done = [c for c in p['kids'] if c in zombies]
                    live = [c for c in p['kids'] if procs[c]['status'] != 'done']
                    if done:
                        zombies.discard(done[0])
                        p['kids'].remove(done[0])
                        acts.append(f'calls wait(NULL), which returns at once: its child {name(done[0])} has already ended')
                    elif live:
                        p['status'] = 'wait'
                        acts.append(f'calls wait(NULL) and waits for {"its child " + name(live[0]) if len(live) == 1 else "one of its children"} to end')
                        p['ev'] = p['gen'].send(None)
                        break
                    else:
                        acts.append('calls wait(NULL), which returns at once because it has no children')
                elif kind == 'end':
                    p['status'] = 'done'
                    acts.append('ends')
                    zombies.add(k)
                    q = p['parent']
                    if q is not None and procs[q]['status'] == 'wait' and k in procs[q]['kids']:
                        procs[q]['status'], procs[q]['woke'] = 'ready', k
                        zombies.discard(k)
                        procs[q]['kids'].remove(k)
                    break
                p['ev'] = p['gen'].send(None)
            # A process that only reaches the end of the program adds nothing to show.
            if acts == ['ends'] or (acts[-1] == 'ends' and all(a.startswith('leaves the loop') for a in acts[:-1])):
                continue
            if len(acts) > 1 and acts[-1] == 'ends':
                acts[-2:] = [acts[-2] + ' and ends']
            note = f'{name(k)} {acts[0]}.' + ''.join(f' It {a}.' for a in acts[1:])
            tally = []
            if new is not None:
                tally.append(f'{totals["processes"]} processes now')
            if any(a.startswith('prints') for a in acts):
                tally.append(f'{totals["prints"]} printf call{"s" if totals["prints"] > 1 else ""} so far')
            if tally:
                text = '; '.join(tally)
                note += ' ' + text[0].upper() + text[1:] + '.'
            steps.append(dict(n=len(procs), status=snapshot(), actor=k, new=new, line=line, call=call,
                              prints=totals['prints'], children=totals['children'], note=note))
    # The first time a call runs, say how many processes make it in all.
    made = [sum(1 for p in procs if p['call'] == c) for c in range(len(calls))]
    seen = set()
    for st in steps:
        c = st['call']
        if st['new'] is not None and c not in seen:
            seen.add(c)
            if made[c] > 1:
                st['note'] += f' This call is made by {made[c]} processes in all, one child each.'
    nodes = [[p['parent'], p['call'], p['depth']] for p in procs]
    return dict(steps=steps, nodes=nodes, calls=calls, lines=lines, totals=totals, status=snapshot())


QUERIES = {'children': 'child processes created', 'processes': 'processes in all', 'prints': 'printf calls'}


def _expected(expect, params, qid):
    if isinstance(expect, int):
        return expect
    if isinstance(expect, str):
        return _eval(expect.replace('^', '**'), params)
    raise SystemExit(f'Unsupported expectation for {qid}: {expect!r}')


def fork_animation(qid, spec):
    query = spec['query']
    if query not in QUERIES:
        raise SystemExit(f'Unknown fork query for {qid}: {query}')
    cases = spec.get('cases') or [{}]
    schedules, lines = [], None
    for params in cases:
        out = simulate(spec['program'], params)
        lines = out['lines']
        got, want = out['totals'][query], _expected(spec['expect'], params, qid)
        if got != want:
            raise SystemExit(f'Animation for {qid} {params or ""} gives {got} {QUERIES[query]}, not {want}')
        t = out['totals']
        note = f"All done: {t['processes']} processes in all, the original P0 and {t['children']} child{'ren' if t['children'] != 1 else ''}."
        if out['lines'] and any('printf' in x for x in out['lines']):
            note += f" printf ran {t['prints']} time{'s' if t['prints'] != 1 else ''}."
        if isinstance(spec['expect'], str):
            note += f" With {_ctx_label(params)}, {spec['expect']} = {want}."
        note += f" Answer: {got} {QUERIES[query]}."
        out['steps'].append(dict(n=len(out['nodes']), status=out['status'], actor=None, new=None, line=None, call=None,
                                 prints=t['prints'], children=t['children'], final=True, note=note))
        label = _ctx_label(params)
        schedules.append(dict(short=label or 'fork', title=('Process tree, ' + label) if label else 'Process tree',
                              steps=out['steps'], nodes=out['nodes'], calls=out['calls']))
    return dict(kind='fork-tree', code=lines, prints=any('printf' in x for x in lines), schedules=schedules,
                count=sum(len(s['steps']) for s in schedules))


# Animation kinds this family provides, and the player file that draws them.
KINDS = {'fork-tree': fork_animation}
PLAYER = 'fork'
TABS = 'cases'
