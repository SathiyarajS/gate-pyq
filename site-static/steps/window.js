'use strict';
// "Step through it" renderer: link timing (sender/receiver time diagram, Go-Back-N transmissions, TCP congestion window per round).
// Loaded on demand by assets/steps.js; the data comes from scripts/animations/window.py (checked against the answer at build time).
window.gateStepsRegister(({el, h, css}) => {
  css(`
.wn-time{width:100%;max-width:560px;height:auto;display:block;margin:4px 0 8px}
.wn-time .axis{stroke:var(--ink);stroke-width:2}
.wn-time .side{font-size:12px;font-weight:700;fill:var(--ink)}
.wn-time .mark{stroke:var(--muted)}.wn-time .mark-label{font-size:10.5px;fill:var(--muted)}
.wn-time .data{fill:color-mix(in oklab,var(--s0) 55%,transparent);stroke:var(--s0)}
.wn-time .batch{fill:color-mix(in oklab,var(--s0) 22%,transparent);stroke:var(--s0);stroke-dasharray:4 3}
.wn-time .ack{fill:color-mix(in oklab,var(--s2) 55%,transparent);stroke:var(--s2);stroke-width:1.5}
.wn-time .send{fill:var(--s0)}.wn-time .busy{fill:var(--s3)}
.wn-time .item-label{font-size:11px;font-weight:700;fill:var(--ink)}
.wn-time .now{stroke:var(--accent);stroke-width:1.5;stroke-dasharray:5 3}
.wn-att{display:flex;flex-wrap:wrap;gap:5px;margin:4px 0 8px;align-items:stretch}
.wn-att span{display:flex;flex-direction:column;align-items:center;justify-content:center;min-width:2.3em;padding:1px 4px 3px;border:1px solid var(--line);border-radius:5px;background:var(--panel);font-size:.9rem;font-weight:700;line-height:1.2}
.wn-att span small{font-size:.66rem;font-weight:500;color:var(--muted)}
.wn-att .ok{border-color:var(--s2);background:color-mix(in oklab,var(--s2) 16%,var(--panel))}
.wn-att .lost{border-color:var(--s1);background:color-mix(in oklab,var(--s1) 22%,var(--panel));text-decoration:line-through}
.wn-att .discard{color:var(--muted);border-style:dashed}
.wn-att .timeout{min-width:0;border:0;background:none;color:var(--s1);font-size:.72rem;font-weight:700;writing-mode:vertical-rl;padding:0}
.wn-att .is-now{box-shadow:0 0 0 2px var(--accent)}
.wn-label{font-size:.75rem;font-weight:650;color:var(--muted);margin:6px 0 0}
.wn-win span{min-width:1.9em}
.wn-win .acked{border-color:var(--s2);background:color-mix(in oklab,var(--s2) 16%,var(--panel))}
.wn-win .inwin{border:2px solid var(--accent)}
.wn-key{display:flex;flex-wrap:wrap;gap:4px 12px;font-size:.75rem;color:var(--muted);margin:0 0 6px}
.wn-key i{display:inline-block;width:.8em;height:.8em;border-radius:2px;margin-right:.35em;vertical-align:-.1em;border:1px solid var(--line)}
.wn-key .ok{background:color-mix(in oklab,var(--s2) 30%,var(--panel));border-color:var(--s2)}
.wn-key .lost{background:color-mix(in oklab,var(--s1) 35%,var(--panel));border-color:var(--s1)}
.wn-key .discard{border-style:dashed}
.wn-cwnd{width:100%;max-width:620px;height:auto;display:block;margin:4px 0 8px}
.wn-cwnd .ss{fill:var(--s0)}.wn-cwnd .ca{fill:var(--s2)}.wn-cwnd .reach{fill:var(--s3)}
.wn-cwnd rect.is-now{stroke:var(--ink);stroke-width:2}
.wn-cwnd .val{font-size:10.5px;font-weight:700;fill:var(--ink)}
.wn-cwnd .tick{font-size:10px;fill:var(--muted)}
.wn-cwnd .thr{stroke:var(--s1);stroke-width:1.5;stroke-dasharray:5 3}.wn-cwnd .thr-label{font-size:10.5px;fill:var(--s1);font-weight:700}
.wn-cwnd .base{stroke:var(--line)}
`);
  const wrap = node => { const w = h('div', 'steps-table-wrap'); w.append(node); return w; };

  // Time runs downwards: the sender's line on the left, the receiver's on the right; a frame is a band between them.
  function timeline(b, width) {
    const W = Math.max(300, Math.min(560, Math.round(width || 520))), sx = 96, rx = W - 34, top = 26, H = 250;
    const y = t => top + H * t / b.end;
    const svg = el('svg', {viewBox: `0 0 ${W} ${top + H + 10}`, class: 'wn-time', role: 'img', 'aria-label': 'Sender and receiver time diagram'});
    svg.append(el('text', {x: sx, y: 14, 'text-anchor': 'middle', class: 'side'}, 'Sender'), el('text', {x: rx, y: 14, 'text-anchor': 'middle', class: 'side'}, 'Receiver'));
    svg.append(el('line', {x1: sx, x2: sx, y1: top, y2: top + H, class: 'axis'}), el('line', {x1: rx, x2: rx, y1: top, y2: top + H, class: 'axis'}));
    const labels = [];
    for (const it of b.items) {
      if (it.k === 'send') { svg.append(el('rect', {x: sx - 4, y: y(it.a0), width: 8, height: Math.max(2, y(it.a1) - y(it.a0)), class: 'send'})); continue; }
      if (it.k === 'busy') { const x = it.side === 'S' ? sx : rx; svg.append(el('rect', {x: x - 5, y: y(it.a0), width: 10, height: Math.max(2, y(it.a1) - y(it.a0)), class: 'busy'})); continue; }
      const [from, to] = it.k === 'ack' ? [rx, sx] : [sx, rx];
      const pts = [[from, y(it.a0)], [from, Math.max(y(it.a1), y(it.a0) + 1.5)], [to, Math.max(y(it.b1), y(it.b0) + 1.5)], [to, y(it.b0)]];
      svg.append(el('polygon', {points: pts.map(p => p.join(',')).join(' '), class: it.k}));
      labels.push([(from + to) / 2 + (it.k === 'ack' ? -6 : 6), (y(it.a0) + y(it.b1)) / 2 + (it.k === 'batch' ? 0 : -4), it.label]);
    }
    labels.forEach(([x, yy, text]) => svg.append(el('text', {x, y: yy, 'text-anchor': 'middle', class: 'item-label'}, text)));
    // Time marks on the sender's side; a label is skipped where it would overlap the previous one.
    let last = -Infinity;
    [...b.marks].sort((p, q) => p[0] - q[0]).forEach(([t, text], k, all) => {
      const yy = y(t);
      svg.append(el('line', {x1: sx - 8, x2: sx, y1: yy, y2: yy, class: 'mark'}));
      if (yy - last >= 13 || k === all.length - 1) { svg.append(el('text', {x: sx - 11, y: yy + 4, 'text-anchor': 'end', class: 'mark-label'}, text)); last = yy; }
    });
    if (b.now != null) svg.append(el('line', {x1: sx - 4, x2: rx + 4, y1: y(b.now), y2: y(b.now), class: 'now'}));
    return svg;
  }

  // Go-Back-N: every transmission as a box (packet number, attempt number), then the sender's window over the packets.
  function attempts(b) {
    const out = [h('p', 'wn-label', 'Transmissions')], box = h('div', 'wn-att');
    b.items.forEach(it => {
      if (it.s === 'timeout') { box.append(h('span', 'timeout', 'timeout')); return; }
      const s = h('span', it.s + (it.n === b.now ? ' is-now' : ''));
      s.append('P' + it.p, h('small', null, '#' + it.n));
      box.append(s);
    });
    if (!b.items.length) box.append(h('span', 'discard', '–'));
    const key = h('p', 'wn-key');
    [['ok', 'delivered'], ['lost', 'lost'], ['discard', 'discarded']].forEach(([c, t]) => { const k = h('span'); k.append(h('i', c), t); key.append(k); });
    const win = h('div', 'wn-att wn-win');
    for (let p = 1; p <= b.packets; p++) {
      const s = h('span', p <= b.acked ? 'acked' : (p >= b.base && p < b.base + b.window) ? 'inwin' : null, String(p));
      win.append(s);
    }
    out.push(box, key, h('p', 'wn-label', `Packets (window ${b.window}; acknowledged ones shaded)`), win);
    return out;
  }

  // Congestion window per round as bars, with the threshold as a dashed line.
  function cwnd(b, width) {
    const W = Math.max(300, Math.min(620, Math.round(width || 560))), left = 26, right = 8, top = 16, H = 150, n = Math.max(b.rounds.length, 4);
    const max = Math.max(...b.rounds, b.ss, b.goal || 0) * 1.15, slot = (W - left - right) / n, y = v => top + H - H * v / max;
    const svg = el('svg', {viewBox: `0 0 ${W} ${top + H + 20}`, class: 'wn-cwnd', role: 'img', 'aria-label': 'Congestion window per round'});
    svg.append(el('line', {x1: left, x2: W - right, y1: top + H, y2: top + H, class: 'base'}));
    b.rounds.forEach((v, k) => {
      const x = left + k * slot + slot * .15, w = slot * .7, reach = b.goal != null && v >= b.goal;
      svg.append(el('rect', {x, y: y(v), width: w, height: top + H - y(v), rx: 2, class: (reach ? 'reach' : v < b.ss ? 'ss' : 'ca') + (k === b.now ? ' is-now' : '')}));
      svg.append(el('text', {x: x + w / 2, y: y(v) - 3, 'text-anchor': 'middle', class: 'val'}, v));
      if (slot >= 14 || k % 2 === 0) svg.append(el('text', {x: x + w / 2, y: top + H + 13, 'text-anchor': 'middle', class: 'tick'}, k + 1));
    });
    svg.append(el('line', {x1: left, x2: W - right, y1: y(b.ss), y2: y(b.ss), class: 'thr'}));
    svg.append(el('text', {x: left + 2, y: y(b.ss) - 4, class: 'thr-label'}, `threshold ${b.ss}`));
    svg.append(el('text', {x: 2, y: top + H + 13, class: 'tick'}, 'RTT'));
    const key = h('p', 'wn-key');
    [['ss', 'var(--s0)', 'slow start'], ['ca', 'var(--s2)', 'congestion avoidance']].forEach(([, c, t]) => { const k = h('span'), i = h('i'); i.style.background = c; k.append(i, t); key.append(k); });
    return [svg, key];
  }

  function table(b) {
    const t = h('table', 'steps-table'), head = t.createTHead().insertRow(), body = t.createTBody();
    b.head.forEach(c => head.append(h('th', null, c)));
    b.rows.forEach((r, k) => { const row = body.insertRow(); r.forEach(v => { row.insertCell().textContent = v; }); if (k === b.hl) row.className = 'is-running'; });
    return wrap(t);
  }

  const draw = {timeline, attempts, cwnd, table, line: b => h('p', b.cls || 'steps-ready', b.text)};
  const view = (s, data, step, i, width) => step.blocks.flatMap(b => draw[b.t](b, width));
  return {arq: view, gbn: view, 'tcp-cwnd': view};
});
