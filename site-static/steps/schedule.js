'use strict';
// "Step through it" renderer: transaction schedules (one column per transaction, one row per operation)
// with the precedence graph built so far.
// Loaded on demand by assets/steps.js; the data comes from scripts/animations/schedule.py (checked against the answer at build time).
window.gateStepsRegister(({el, h, css}) => {
  css(`
.sched{display:flex;flex-wrap:wrap;gap:4px 22px;align-items:flex-start}
.sched-table th,.sched-table td{text-align:center;padding:3px 8px;min-width:3.4em}
.sched-table th:first-child,.sched-table td:first-child{min-width:0;color:var(--muted);font-size:.75rem;padding-right:4px;text-align:right}
.sched-table td.op{font-weight:600}
.sched-table tr.is-later td{color:color-mix(in oklab,var(--muted) 70%,transparent)}.sched-table tr.is-later td.op{font-weight:400}
.sched-table tr.is-running td.op{color:var(--accent);font-weight:800}
.sched-table td.cmp{background:color-mix(in oklab,var(--s1) 22%,transparent);border-radius:3px}
.sched-table td.src{background:color-mix(in oklab,var(--s0) 22%,transparent);border-radius:3px}
.sched-table td.bad{background:color-mix(in oklab,var(--s4) 30%,transparent);border-radius:3px}
.prec{display:block;width:220px;max-width:100%;height:auto;overflow:visible}
.prec .e{stroke:var(--muted);stroke-width:1.8;fill:none}.prec .ah{fill:var(--muted)}
.prec .e.now{stroke:var(--s1);stroke-width:3.2}.prec .ah.now{fill:var(--s1)}
.prec .e.path{stroke:var(--s4);stroke-width:3.4}.prec .ah.path{fill:var(--s4)}
.prec circle{fill:var(--panel);stroke:var(--muted);stroke-width:1.5}
.prec text{font-size:13px;font-weight:700;fill:var(--ink)}
.prec .n.hot circle{stroke:var(--accent);stroke-width:3}
.prec-cap{font-size:.78rem;color:var(--muted);margin:0 0 2px}
.sched-key{display:flex;flex-wrap:wrap;gap:2px 12px;font-size:.78rem;color:var(--muted);margin:2px 0}
.sched-key i{display:inline-block;width:1em;height:.8em;border-radius:2px;margin-right:.35em;vertical-align:-.05em}
.sched-key .k-cmp{background:color-mix(in oklab,var(--s1) 40%,transparent)}.sched-key .k-src{background:color-mix(in oklab,var(--s0) 40%,transparent)}.sched-key .k-bad{background:color-mix(in oklab,var(--s4) 45%,transparent)}
`);

  function timeline(s, step) {
    const t = h('table', 'steps-table sched-table'), head = t.createTHead().insertRow(), body = t.createTBody();
    head.append(h('th', null, ''));
    s.txns.forEach(x => head.append(h('th', null, x)));
    const cmp = new Set(step.cmp || []), live = step.i >= 0 || step.final;
    s.ops.forEach(([tx, label], k) => {
      const tr = body.insertRow();
      tr.insertCell().textContent = k + 1;
      s.txns.forEach(x => { const td = tr.insertCell(); if (x === tx) { td.textContent = label; td.className = 'op'; } });
      const cell = tr.cells[1 + s.txns.indexOf(tx)];
      if (cmp.has(k)) cell.classList.add(step.bad ? 'bad' : 'cmp');
      if (step.src === k) cell.classList.add('src');
      if (live && !step.final && k > step.i) tr.className = 'is-later';
      else if (k === step.i && !step.final) tr.className = 'is-running';
    });
    const w = h('div', 'steps-table-wrap'); w.append(t);
    return w;
  }

  function graph(s, step) {
    const n = s.txns.length, W = 220, r = 17, H = n <= 2 ? 80 : 200, pad = r + 8, pts = {};
    s.txns.forEach((x, k) => {
      if (n <= 2) pts[x] = [k ? W - pad - 20 : pad + 20, H / 2];
      else { const a = -Math.PI / 2 + 2 * Math.PI * k / n, R = (Math.min(W, H) - 2 * pad) / 2; pts[x] = [W / 2 + R * Math.cos(a), H / 2 + R * Math.sin(a)]; }
    });
    const svg = el('svg', {viewBox: `0 0 ${W} ${H}`, class: 'prec', role: 'img', 'aria-label': 'Precedence graph'});
    const es = step.edges || [], key = (u, v) => u + '>' + v, all = new Set(es.map(([u, v]) => key(u, v)));
    const isNew = new Set((step.new || []).map(([u, v]) => key(u, v))), onCycle = new Set();
    if (step.cycle) for (let k = 0; k + 1 < step.cycle.length; k++) onCycle.add(key(step.cycle[k], step.cycle[k + 1]));
    es.forEach(([u, v]) => {
      const [x1, y1] = pts[u], [x2, y2] = pts[v], L = Math.hypot(x2 - x1, y2 - y1) || 1, nx = -(y2 - y1) / L, ny = (x2 - x1) / L;
      const bend = all.has(key(v, u)) ? 18 : 0, cx = (x1 + x2) / 2 + nx * bend, cy = (y1 + y2) / 2 + ny * bend;
      const unit = (ax, ay, bx, by) => { const d = Math.hypot(bx - ax, by - ay) || 1; return [(bx - ax) / d, (by - ay) / d]; };
      const [sx, sy] = unit(x1, y1, cx, cy), [tx, ty] = unit(x2, y2, cx, cy);
      const p0 = [x1 + sx * r, y1 + sy * r], tip = [x2 + tx * (r + 1), y2 + ty * (r + 1)], end = [tip[0] + tx * 8, tip[1] + ty * 8];
      const c = onCycle.has(key(u, v)) ? 'path' : isNew.has(key(u, v)) ? 'now' : '';
      svg.append(el('path', {d: `M${p0[0].toFixed(1)} ${p0[1].toFixed(1)} Q${cx.toFixed(1)} ${cy.toFixed(1)} ${end[0].toFixed(1)} ${end[1].toFixed(1)}`, class: 'e ' + c}));
      const bx = tip[0] + tx * 10, by = tip[1] + ty * 10;
      svg.append(el('polygon', {points: [tip, [bx - ty * 5, by + tx * 5], [bx + ty * 5, by - tx * 5]].map(p => p.map(z => z.toFixed(1)).join(',')).join(' '), class: 'ah ' + c}));
    });
    const hot = step.i >= 0 && !step.final && s.ops[step.i] ? s.ops[step.i][0] : null;
    s.txns.forEach(x => {
      const g = el('g', {class: 'n' + (x === hot ? ' hot' : '')}), [px, py] = pts[x];
      g.append(el('circle', {cx: px.toFixed(1), cy: py.toFixed(1), r}));
      g.append(el('text', {x: px.toFixed(1), y: (py + 4.5).toFixed(1), 'text-anchor': 'middle'}, x));
      svg.append(g);
    });
    const box = h('div');
    box.append(h('p', 'prec-cap', 'Precedence graph'), svg);
    if (step.order) box.append(h('p', 'steps-ready', 'Serial order: ' + step.order.join(' → ')));
    return box;
  }

  function legend(step) {
    const items = [];
    if (step.cmp && step.cmp.length) items.push(step.bad ? ['bad', 'pair in the opposite order'] : step.i < 0 ? ['cmp', 'conflicting pair'] : ['cmp', 'conflicts with this operation']);
    if (step.src != null) items.push(['src', 'the write this read sees']);
    if (!items.length) return null;
    const k = h('p', 'sched-key');
    items.forEach(([c, t]) => { const sp = h('span'); sp.append(h('i', 'k-' + c), t); k.append(sp); });
    return k;
  }

  return {
    'txn-schedule': (s, data, step) => {
      const head = step.final ? 'Finished' : step.i >= 0 ? `Operation ${step.i + 1} of ${s.ops.length}: ${s.ops[step.i][1]}` : step.cmp ? 'Conflicting pair' : 'Start';
      const wrap = h('div', 'sched');
      wrap.append(timeline(s, step));
      if (s.graph) wrap.append(graph(s, step));
      const out = [h('p', 'steps-time', head), wrap];
      const k = legend(step);
      if (k) out.splice(1, 0, k);
      return out;
    },
  };
});
