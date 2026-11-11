"""Link timing: stop-and-wait and sliding windows (utilization, throughput, window
and sequence-number sizes), Go-Back-N with lost frames, and the TCP congestion
window round by round after a timeout.

Data: data/animations/window.json. Every entry is simulated at build time with exact
fractions and checked against the expected answer; the build stops on any difference.

Each step is {note, blocks}; a block is one of
  {t: 'timeline', unit, end, marks: [[time, label]], items: [...], now}   sender/receiver time diagram
       item {k: 'data'|'ack'|'batch', a0, a1, b0, b1, label}   leaves its side during a0..a1, arrives during b0..b1
       item {k: 'busy', side: 'S'|'R', a0, a1, label}           processing at one side
  {t: 'attempts', items: [{n, p, s}], now, packets, base, next, acked}   Go-Back-N transmissions
  {t: 'cwnd', unit, rounds: [w], ss: [s], now, goal}            congestion window per round
  {t: 'table', head, rows, hl}                                  a growing table
  {t: 'line', text, cls}                                        one line of text
"""
from fractions import Fraction


def _check(qid, what, got, want):
    if isinstance(want, list) and len(want) == 2 and all(isinstance(x, (int, float)) for x in want):
        if not Fraction(str(want[0])) <= Fraction(got) <= Fraction(str(want[1])):
            raise SystemExit(f'Animation for {qid}: {what} is {float(got)!r}, outside {want!r}')
        return
    if isinstance(want, (int, float)) and not isinstance(want, bool):
        if Fraction(got) != Fraction(str(want)):
            raise SystemExit(f'Animation for {qid}: {what} is {float(got)!r}, not {want!r}')
        return
    if got != want:
        raise SystemExit(f'Animation for {qid}: {what} is {got!r}, not {want!r}')


def table(head, rows, hl=None):
    return dict(t='table', head=list(head), rows=[[str(c) for c in r] for r in rows], hl=hl)


def line(text, cls='steps-ready'):
    return dict(t='line', text=text, cls=cls)


def step(note, *blocks):
    return dict(note=note, blocks=[b for b in blocks if b])


def _finish(kind, short, title, steps, **extra):
    steps[-1]['final'] = True
    return dict(kind=kind, schedules=[dict(short=short, title=title, steps=steps)], count=len(steps), **extra)


def F(x):
    return Fraction(str(x)) if not isinstance(x, Fraction) else x


def dec(x, places=4):
    """Exact decimal if it terminates within `places` digits, else ≈ rounded."""
    x = Fraction(x)
    for k in range(places + 1):
        if (x * 10 ** k).denominator == 1:
            v = x * 10 ** k
            s = str(abs(v.numerator)).rjust(k + 1, '0')
            out = s[:-k] + '.' + s[-k:] if k else s
            return ('−' if x < 0 else '') + out
    s = f'{float(x):.{places}f}'.rstrip('0').rstrip('.')
    return '≈ ' + s.replace('-', '−')


def num(n):
    """Whole numbers of a million or more as d × 10^k when that is short: 500000000 -> 5 × 10^8."""
    n = Fraction(n)
    if n.denominator == 1 and n >= 10 ** 6:
        k = len(str(n.numerator)) - 1
        d = n / 10 ** k
        if (d * 100).denominator == 1:
            return ('' if d == 1 else f'{dec(d)} × ') + f'10^{k}'
    return dec(n)


def rate_text(r):
    r = Fraction(r)
    for f, u in ((10 ** 9, 'Gbit/s'), (10 ** 6, 'Mbit/s'), (10 ** 3, 'kbit/s')):
        if r >= f and (r / f * 1000).denominator == 1:
            return f'{dec(r / f)} {u}'
    return f'{num(r)} bit/s'


class Clock:
    """Times in seconds, shown in ms or s."""
    def __init__(self, end):
        self.unit = 's' if end >= 1 else 'ms'
        self.k = 1 if self.unit == 's' else 1000

    def v(self, t):
        return float(Fraction(t) * self.k)

    def t(self, t):
        return f'{dec(Fraction(t) * self.k, 3)} {self.unit}'

    def eq(self, t):
        v = self.t(t)
        return v if v.startswith('≈') else '= ' + v

    def q(self, t):
        """The same without the ≈ sign, for use inside a formula."""
        return self.t(t).replace('≈ ', '')


# ---------------------------------------------------------------- one frame and its ACK

def _bits(spec, prefix, kilo):
    if prefix + '_bits' in spec:
        return F(spec[prefix + '_bits'])
    if prefix + '_bytes' in spec:
        return F(spec[prefix + '_bytes']) * 8
    if prefix + '_kb' in spec:
        return F(spec[prefix + '_kb']) * kilo * 8
    return None


def arq_model(spec, kilo):
    rate = F(spec['rate'])
    L = _bits(spec, 'frame', kilo)
    if 'prop_ms' in spec:
        tp = F(spec['prop_ms']) / 1000
    elif 'distance_m' in spec:
        tp = F(spec['distance_m']) / F(spec['speed_mps'])
    else:
        tp = None  # to be solved for
    ack = _bits(spec, 'ack', kilo) or 0
    ack_rate = F(spec.get('ack_rate', spec['rate']))
    proc = F(spec.get('processing_ms', 0)) / 1000
    over = F(spec.get('overhead_bytes', 0)) * 8
    t_tx, t_ack = L / rate, ack / ack_rate
    if tp is None:
        e = F(spec['efficiency'])
        cycle = (L - over) / rate / e
        tp = (cycle - t_tx - t_ack - 2 * proc) / 2
        if tp <= 0:
            raise SystemExit('The efficiency leaves no time for propagation')
    cycle = t_tx + tp + proc + t_ack + tp + proc
    useful = (L - over) / rate
    m = dict(rate=rate, L=L, tp=tp, ack=ack, ack_rate=ack_rate, proc=proc, over=over, t_tx=t_tx, t_ack=t_ack, cycle=cycle, useful=useful)
    goal = spec['goal']
    if goal in ('window', 'seqbits'):
        target = F(spec.get('target', 1))
        need = target * cycle / t_tx
        W = -(-need.numerator // need.denominator)
        m.update(target=target, need=need, W=W)
        if goal == 'seqbits':
            proto = spec['protocol']
            k = 1
            while (2 ** k - 1 if proto == 'gbn' else 2 ** (k - 1)) < W:
                k += 1
            m['k'] = k
    return m


def arq_answer(spec, m):
    goal = spec['goal']
    if goal == 'utilization':
        return dict(utilization_percent=m['useful'] / m['cycle'] * 100)
    if goal == 'throughput':
        return dict(throughput=(m['L'] - m['over']) / 8 / m['cycle'])
    if goal == 'prop':
        return dict(prop_ms=m['tp'] * 1000)
    if goal == 'window':
        return dict(window=m['W'])
    return dict(window=m['W'], bits=m['k'])


def arq_animation(qid, spec):
    kilos = [1000, 1024] if any(k.endswith('_kb') for k in spec) else [1000]
    models = [arq_model(spec, k) for k in kilos]
    answers = [arq_answer(spec, m) for m in models]
    if len(models) > 1 and answers[0] != answers[1]:
        # Only an answer that does not depend on what "1 KB" means is shown.
        if {k: v for k, v in answers[0].items() if k != 'window'} != {k: v for k, v in answers[1].items() if k != 'window'}:
            raise SystemExit(f'Animation for {qid}: the answer depends on whether 1 KB is 1000 or 1024 bytes')
    m = models[-1]
    goal, proto = spec['goal'], spec.get('protocol', 'stop-and-wait')
    t_tx, tp, t_ack, proc, cycle = m['t_tx'], m['tp'], m['t_ack'], m['proc'], m['cycle']
    W = m.get('W', 1)
    end = max(cycle, W * t_tx) * Fraction(21, 20)
    ck = Clock(max(cycle, W * t_tx))
    rows, steps, items, marks = [], [], [], [[0, '0']]

    def tl(now=None):
        return dict(t='timeline', unit=ck.unit, end=ck.v(end), marks=[[ck.v(a), b] for a, b in marks],
                    items=[dict(it) for it in items], now=None if now is None else ck.v(now))

    def tab():
        return table(['Quantity', 'Value', 'How'], rows, len(rows) - 1)

    frame_text = (f'{num(m["L"] / 8)}-byte' if 'frame_bytes' in spec else f'{num(spec["frame_kb"])} KB' if 'frame_kb' in spec else f'{num(m["L"])}-bit')
    kb = ' (1 KB = 1024 bytes)' if len(kilos) > 1 else ''
    # 1. sending the frame
    rows.append(['Frame time', ck.t(t_tx), f'{num(m["L"])} bits ÷ {rate_text(m["rate"])}'])
    items.append(dict(k='send', a0=0, a1=ck.v(t_tx), label='frame 1'))
    marks.append([t_tx, ck.t(t_tx)])
    if goal == 'prop':
        e = F(spec['efficiency'])
        steps.append(step(f'Sending a {frame_text} frame{kb} at {rate_text(m["rate"])} takes {num(m["L"])} bits ÷ {rate_text(m["rate"])} {ck.eq(t_tx)}.', tl(t_tx), tab()))
        rows.append(['Cycle', ck.t(cycle), f'{ck.t(m["useful"])} ÷ {dec(e * 100)}%'])
        steps.append(step(f'An efficiency of {dec(e * 100)}% means the {ck.t(t_tx)} of sending is {dec(e * 100)}% of one cycle, so a cycle lasts {ck.q(t_tx)} ÷ {dec(e)} = {ck.t(cycle)}.', tl(t_tx), tab()))
        rest = cycle - t_tx - t_ack - 2 * proc
        rows.append(['Propagation', ck.t(tp), f'({ck.t(cycle)} − {ck.t(t_tx)}) ÷ 2'])
        items[-1] = dict(k='data', a0=0, a1=ck.v(t_tx), b0=ck.v(tp), b1=ck.v(t_tx + tp), label='frame 1')
        items.append(dict(k='ack', a0=ck.v(t_tx + tp), a1=ck.v(t_tx + tp + t_ack), b0=ck.v(cycle - t_ack), b1=ck.v(cycle), label='ACK'))
        marks += [[t_tx + tp, ck.t(t_tx + tp)], [cycle, ck.t(cycle)]]
        steps.append(step(f'The rest of the cycle, {ck.t(cycle)} − {ck.t(t_tx)} = {ck.t(rest)}, is the trip there and back, so the one-way propagation delay is {ck.t(rest)} ÷ 2 = {ck.t(tp)}.',
                          tl(), tab(), line(f'Propagation delay: {ck.t(tp)}', 'steps-time')))
        out = dict(prop_ms=tp * 1000)
        for k, v in spec['expect'].items():
            _check(qid, k, out.get(k), v)
        return _finish('arq', 'Timeline', 'Stop-and-wait: one frame and its acknowledgement', steps)
    steps.append(step(f'Sending a {frame_text} frame{kb} at {rate_text(m["rate"])} takes {num(m["L"])} bits ÷ {rate_text(m["rate"])} {ck.eq(t_tx)}.', tl(t_tx), tab()))
    # 2. propagation
    items[-1] = dict(k='data', a0=0, a1=ck.v(t_tx), b0=ck.v(tp), b1=ck.v(t_tx + tp), label='frame 1')
    marks.append([t_tx + tp, ck.t(t_tx + tp)])
    rows.append(['Propagation', ck.t(tp), f'{num(spec["distance_m"])} m ÷ {num(spec["speed_mps"])} m/s' if 'distance_m' in spec else 'one way, given'])
    steps.append(step(f'Its last bit reaches the receiver {ck.t(tp)} later, at {ck.t(t_tx + tp)}.' +
                      (f' (The distance {num(spec["distance_m"] / 1000)} km at {num(spec["speed_mps"])} m/s gives {ck.t(tp)}.)' if 'distance_m' in spec else ''), tl(t_tx + tp), tab()))
    at = t_tx + tp
    if proc:
        items.append(dict(k='busy', side='R', a0=ck.v(at), a1=ck.v(at + proc), label='processing'))
        rows.append(['Processing', ck.t(proc), 'each received frame'])
        steps.append(step(f'The receiver processes the frame for {ck.t(proc)}, until {ck.t(at + proc)}.', tl(at + proc), tab()))
        at += proc
    # 3. the ACK
    if t_ack:
        rows.append(['ACK time', ck.t(t_ack), f'{num(m["ack"])} bits ÷ {rate_text(m["ack_rate"])}'])
        items.append(dict(k='ack', a0=ck.v(at), a1=ck.v(at + t_ack), b0=ck.v(at + tp), b1=ck.v(at + t_ack + tp), label='ACK'))
        marks.append([at + t_ack, ck.t(at + t_ack)])
        ack_text = f'{num(m["ack"] / 8)}-byte ACK ({num(m["ack"])} bits)' if 'ack_bytes' in spec else f'{num(m["ack"])}-bit ACK'
        steps.append(step(f'Sending the {ack_text} at {rate_text(m["ack_rate"])} takes {ck.t(t_ack)}, until {ck.t(at + t_ack)}.', tl(at + t_ack), tab()))
    else:
        items.append(dict(k='ack', a0=ck.v(at), a1=ck.v(at), b0=ck.v(at + tp), b1=ck.v(at + tp), label='ACK'))
    at += t_ack
    marks.append([at + tp, ck.t(at + tp)])
    first_ack = at + tp
    steps.append(step(('The ACK takes no time to send, and' if not t_ack else 'It') + f' arrives back at the sender {ck.t(tp)} later, at {ck.t(first_ack)}.', tl(first_ack), tab()))
    if proc:
        items.append(dict(k='busy', side='S', a0=ck.v(first_ack), a1=ck.v(first_ack + proc), label='processing'))
        steps.append(step(f'The sender processes the ACK for {ck.t(proc)}, so it can send the next frame at {ck.t(cycle)}.', tl(cycle), tab()))
    rows.append(['Cycle', ck.t(cycle), ' + '.join(ck.q(x) for x in [t_tx, tp, proc, t_ack, tp, proc] if x)])
    out = {}
    if goal in ('utilization', 'throughput'):
        u = m['useful'] / cycle
        if goal == 'utilization':
            pct = u * 100
            rows.append(['Utilization', dec(pct, 2) + '%', f'{ck.t(m["useful"])} ÷ {ck.t(cycle)}'])
            if m['over']:
                data = (m['L'] - m['over']) / 8
                useful = (f'The frame\'s {num(m["over"] / 8)} overhead bytes are not useful data, so only its {num(data)} data bytes count: '
                          f'{num(data * 8)} bits ÷ {rate_text(m["rate"])} = {ck.t(m["useful"])} of useful sending.')
            else:
                useful = f'The link is sending for {ck.t(m["useful"])} of it.'
            text = f'One cycle lasts {ck.t(cycle)}. {useful} Utilization = {ck.q(m["useful"])} ÷ {ck.q(cycle)} {"= " if not dec(pct, 2).startswith("≈") else ""}{dec(pct, 2)}%.'
            out['utilization_percent'] = pct
            if 'options' in spec:
                best = min(spec['options'], key=lambda o: abs(F(o) - pct))
                if sorted(abs(F(o) - pct) for o in spec['options'])[:2].count(abs(F(best) - pct)) > 1:
                    raise SystemExit(f'Animation for {qid}: two options are equally near {float(pct)}')
                out['option'] = str(best)
                text += f' The nearest option is {best}.'
            steps.append(step(text, tl(), table(['Quantity', 'Value', 'How'], rows, len(rows) - 1),
                              line(f'Utilization: {dec(pct, 2)}%' + (f' (option {out["option"]})' if 'option' in out else ''), 'steps-time')))
        else:
            thr = (m['L'] - m['over']) / 8 / cycle
            rows.append(['Throughput', f'{dec(thr, 2)} bytes/s', f'{num((m["L"] - m["over"]) / 8)} bytes ÷ {ck.t(cycle)}'])
            steps.append(step(f'Each cycle of {ck.t(cycle)} delivers one {num((m["L"] - m["over"]) / 8)}-byte frame, so the throughput is {num((m["L"] - m["over"]) / 8)} ÷ {dec(cycle)} s = {dec(thr, 2)} bytes/s.',
                              tl(), table(['Quantity', 'Value', 'How'], rows, len(rows) - 1), line(f'Throughput: {dec(thr, 2)} bytes/s', 'steps-time')))
            out['throughput'] = thr
    else:
        target, need = m['target'], m['need']
        pct = dec(target * 100)
        rows.append(['Window', f'{W} frames', f'{pct}% × {ck.q(cycle)} ÷ {ck.q(t_tx)} = {dec(need, 3).replace("≈ ", "")}, rounded up'])
        steps.append(step(f'The first ACK is back at {ck.t(cycle)}. A window of W frames keeps the sender busy for W × {ck.q(t_tx)}; '
                          f'{pct}% use needs W × {ck.q(t_tx)} ≥ {pct}% × {ck.q(cycle)}, so W ≥ {dec(need, 3).replace("≈ ", "")}, that is W = {W}.',
                          tl(), table(['Quantity', 'Value', 'How'], rows, len(rows) - 1)))
        items.append(dict(k='batch', a0=0, a1=ck.v(W * t_tx), b0=ck.v(tp), b1=ck.v(W * t_tx + tp), label=f'{W} frames'))
        marks.append([W * t_tx, ck.t(W * t_tx)])
        u = min(Fraction(1), W * t_tx / cycle)
        prev = W - 1
        check = f' With {prev} frames the sender would manage only {dec(min(1, prev * t_tx / cycle) * 100, 2)}%.' if prev else ''
        if len(kilos) > 1:
            other = models[0]
            check += f' Taking 1 KB as 1000 bytes gives W = {other["W"]}' + (', the same.' if other['W'] == W else '.')
        last = step(f'Sending {W} frames takes {W} × {ck.q(t_tx)} = {ck.t(W * t_tx)}, which covers {dec(u * 100, 2)}% of the cycle.{check}', tl(), table(['Quantity', 'Value', 'How'], rows, len(rows) - 1))
        steps.append(last)
        out['window'] = W
        if goal == 'window':
            if 'options' in spec:
                fits = [o for o in spec['options'] if o >= W]
                out['option'] = str(min(fits))
                last['note'] += f' Among the options, the smallest window that works is {out["option"]}.'
            last['blocks'].append(line(f'Window: {W} frames', 'steps-time'))
        else:
            k = m['k']
            name, rule = ('Go-Back-N', 'W ≤ 2^k − 1') if proto == 'gbn' else ('Selective Repeat', 'W ≤ 2^(k−1), so 2^k ≥ 2W')
            cap = [[j, 2 ** j, (2 ** j - 1) if proto == 'gbn' else 2 ** (j - 1)] for j in range(max(1, k - 2), k + 1)]
            steps.append(step(f'{name} with k-bit sequence numbers allows {rule}. ' +
                              f'k = {k - 1} allows only {cap[-2][2]} frames; k = {k} allows {cap[-1][2]} ≥ {W}, so {k} bits are needed.',
                              table(['Bits k', 'Numbers 2^k', 'Largest window'], cap, len(cap) - 1), line(f'Sequence-number bits: {k}', 'steps-time')))
            out['bits'] = k
    for k, v in spec['expect'].items():
        _check(qid, k, out.get(k), v)
    title = {'stop-and-wait': 'Stop-and-wait: one frame and its acknowledgement', 'gbn': 'Go-Back-N: filling the pipe',
             'sr': 'Selective Repeat: filling the pipe', 'sliding': 'Sliding window: filling the pipe'}[proto]
    return _finish('arq', 'Timeline', title, steps)


# ---------------------------------------------------------------- Go-Back-N with periodic losses

def gbn_animation(qid, spec):
    n, W, every = spec['packets'], spec['window'], spec['lose_every']
    base, nxt, expected, attempt = 1, 1, 1, 0
    items, steps = [], []

    def view(now=None):
        return dict(t='attempts', items=[dict(x) for x in items], now=now, packets=n, base=base, next=nxt, acked=expected - 1, window=W)

    steps.append(step(f'A has packets 1 to {n} and may have up to {W} unacknowledged packets out. Every {every}th transmission is lost; B accepts only the next packet in order and acknowledges it at once.', view()))
    while base <= n:
        if nxt < base + W and nxt <= n:
            attempt += 1
            lost = attempt % every == 0
            if lost:
                s, why = 'lost', f'Transmission {attempt} carries packet {nxt} and is lost (every {every}th one is).'
            elif nxt == expected:
                s = 'ok'
                expected += 1
                base = expected
                why = f'Transmission {attempt} delivers packet {nxt}. B acknowledges it, so the window now starts at {base}.'
            else:
                s, why = 'discard', f'Transmission {attempt} carries packet {nxt}, but B is still waiting for packet {expected}, so it discards it.'
            items.append(dict(n=attempt, p=nxt, s=s))
            nxt += 1
            steps.append(step(why, view(attempt)))
        else:
            steps.append(step(f'The window {base}–{min(base + W - 1, n)} is used up and packet {base} is not acknowledged, so A times out and goes back to packet {base}.', view()))
            items.append(dict(n=None, p=None, s='timeout'))
            nxt = base
    lost = [x['n'] for x in items if x['s'] == 'lost']
    steps.append(step(f'All {n} packets have arrived in order after {attempt} transmissions (transmissions {", ".join(map(str, lost))} were lost).', view(),
                      line(f'Transmissions: {attempt}', 'steps-time')))
    _check(qid, 'transmissions', attempt, spec['expect']['transmissions'])
    return _finish('gbn', 'Go-Back-N', f'Go-Back-N, window {W}, every {every}th transmission lost', steps)


# ---------------------------------------------------------------- TCP congestion window

def cwnd_animation(qid, spec):
    mss = F(spec.get('mss', 1))
    unit = spec.get('unit', 'MSS')
    w0 = F(spec['cwnd_at_timeout']) / mss
    if w0.denominator != 1 or w0 < 2:
        raise SystemExit(f'Animation for {qid}: the window at the timeout is not a whole number of segments')
    ss = w0 / 2
    rtt = F(spec['rtt_ms']) if 'rtt_ms' in spec else None

    def size(w):
        return f'{dec(w)} MSS' if unit == 'MSS' else f'{dec(w)} MSS = {dec(w * mss)} {unit}'

    goal = Fraction(spec['until']) / mss if 'until' in spec else None
    last = spec.get('round')
    rounds, steps, rows = [], [], []

    def chart(now):
        return dict(t='cwnd', unit='MSS', rounds=[float(x) for x in rounds], ss=float(ss), now=now,
                    goal=float(goal) if goal is not None else None)

    when = (lambda r: f'{dec(rtt * (r - 1))}–{dec(rtt * r)} ms') if rtt else (lambda r: '')
    at = (lambda r: f' ({when(r)})') if rtt else (lambda r: '')
    steps.append(step(f'At the timeout the window is {size(w0)}. TCP sets the threshold to half of it, {size(ss)}, and restarts slow start from 1 MSS.',
                      chart(None), table(['Round', 'Time', 'Window', 'Phase'], rows)))
    w, r = Fraction(1), 1
    while True:
        if goal is not None and w >= goal:
            break
        rounds.append(w)
        phase = 'slow start' if w < ss else 'congestion avoidance'
        rows.append([r, when(r), size(w), phase])
        if last is not None and r == last:
            steps.append(step(f'Round {r}{at(r)} sends with a window of {size(w)}.', chart(r - 1),
                              table(['Round', 'Time', 'Window', 'Phase'], rows, len(rows) - 1), line(f'Window in round {r}: {size(w)}', 'steps-time')))
            out = dict(cwnd=w * mss)
            break
        if w < ss:
            nw = 2 * w
            if nw > ss:
                # Doubling past the threshold needs a convention the question does not give.
                raise SystemExit(f'Animation for {qid}: slow start would jump from {w} past the threshold {ss}')
            note = f'Round {r}{at(r)}: window {size(w)}, below the threshold, so slow start doubles it to {size(nw)}' + \
                (', which reaches the threshold.' if nw == ss else '.')
        else:
            nw = w + 1
            note = f'Round {r}{at(r)}: window {size(w)}, ' + ('at' if w == ss else 'above') + f' the threshold, so congestion avoidance adds 1 MSS: {size(nw)}.'
        steps.append(step(note, chart(r - 1), table(['Round', 'Time', 'Window', 'Phase'], rows, len(rows) - 1)))
        w, r = nw, r + 1
        if r > 500:
            raise SystemExit(f'Animation for {qid}: the window never reaches the goal')
    if goal is not None:
        t = rtt * (r - 1)
        rounds.append(w)
        rows.append([r, f'from {dec(t)} ms' if rtt else '', size(w), 'reached'])
        steps.append(step(f'After {r - 1} round trips the window is back to {size(w)}: {r - 1} × {dec(rtt)} ms = {dec(t)} ms.', chart(r - 1),
                          table(['Round', 'Time', 'Window', 'Phase'], rows, len(rows) - 1), line(f'Time: {dec(t)} ms', 'steps-time')))
        out = dict(time_ms=t, rtts=r - 1)
    for k, v in spec['expect'].items():
        _check(qid, k, out.get(k), v)
    return _finish('tcp-cwnd', 'Window', f'TCP congestion window after a timeout at {size(w0)}', steps)


KINDS = {'arq': arq_animation, 'gbn': gbn_animation, 'tcp-cwnd': cwnd_animation}
PLAYER = 'window'
TABS = 'parts'
