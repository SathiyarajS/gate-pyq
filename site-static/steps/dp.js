'use strict';
// "Step through it" renderer: dynamic-programming tables filled cell by cell.
// Loaded on demand by assets/steps.js; the data comes from scripts/animations/dp.py (checked against the answer at build time).
// A tab gives the row and column labels, the base cells, and the filled cells in fill order;
// each step says how many are filled and which cells the newest one was computed from.
window.gateStepsRegister(({h, css}) => {
  css(`
.dp-table th,.dp-table td{text-align:center;padding:3px 5px;min-width:1.9em;font-size:.8rem}
.dp-table thead th{white-space:nowrap}
.dp-table td{border-left:1px solid color-mix(in oklab,var(--line) 55%,transparent)}
.dp-table th:first-child,.dp-table td:first-child{min-width:0;border-left:0}
.dp-table td.base{color:var(--muted)}
.dp-table td.blank{background:color-mix(in oklab,var(--muted) 8%,transparent)}
.dp-table td.dp-current{background:color-mix(in oklab,var(--accent) 22%,transparent);font-weight:800;color:var(--ink);outline:2px solid var(--accent);outline-offset:-2px}
.dp-table td.dep{background:color-mix(in oklab,var(--s1) 26%,transparent);font-weight:700}
.dp-table td.alt{background:color-mix(in oklab,var(--s1) 9%,transparent)}
.dp-table td.dp-trace{background:color-mix(in oklab,var(--s2) 26%,transparent);font-weight:700}
.dp-table tr.took td{background:color-mix(in oklab,var(--s2) 18%,transparent);font-weight:700}
.dp-key{display:flex;flex-wrap:wrap;gap:2px 12px;font-size:.78rem;color:var(--muted);margin:2px 0}
.dp-key i{display:inline-block;width:1em;height:.8em;border-radius:2px;margin-right:.35em;vertical-align:-.05em}
.dp-key .k-now{background:color-mix(in oklab,var(--accent) 35%,transparent);outline:1.5px solid var(--accent)}.dp-key .k-dep{background:color-mix(in oklab,var(--s1) 40%,transparent)}
.dp-key .k-alt{background:color-mix(in oklab,var(--s1) 15%,transparent)}.dp-key .k-path{background:color-mix(in oklab,var(--s2) 40%,transparent)}
`);

  const at = (r, c) => r + ',' + c;

  function table(s, step) {
    const t = h('table', 'steps-table steps-grid dp-table'), head = t.createTHead().insertRow(), body = t.createTBody();
    head.append(h('th', null, s.corner));
    s.cols.forEach(c => head.append(h('th', null, c)));
    const val = {}, cls = {};
    s.base.forEach(([r, c, v]) => { val[at(r, c)] = v; cls[at(r, c)] = 'base'; });
    s.blank.forEach(([r, c]) => { cls[at(r, c)] = 'blank'; });
    s.fill.forEach(([r, c, v], k) => { if (k <= step.at) { val[at(r, c)] = v; delete cls[at(r, c)]; } });
    (step.alts || []).forEach(([r, c]) => { cls[at(r, c)] = 'alt'; });
    (step.deps || []).forEach(([r, c]) => { cls[at(r, c)] = 'dep'; });
    (step.path || []).forEach(([r, c]) => { cls[at(r, c)] = 'dp-trace'; });
    if (step.at >= 0 && !step.final) {
      const [r, c] = s.fill[step.at];
      cls[at(r, c)] = 'dp-current is-now';
    } else if (step.path?.length) {
      const [r, c] = step.path[0];
      cls[at(r, c)] = 'dp-trace is-now';
    }
    const took = new Set((step.took || []).map(k => k - 1));
    s.rows.forEach((label, r) => {
      const tr = body.insertRow();
      tr.insertCell().textContent = label;
      s.cols.forEach((_, c) => { const td = tr.insertCell(), k = at(r, c); if (val[k] != null) td.textContent = val[k]; if (cls[k]) td.className = cls[k]; });
      if (took.has(r)) tr.className = 'took';
    });
    const w = h('div', 'steps-table-wrap'); w.append(t);
    return w;
  }

  function key(step) {
    const items = [];
    if (step.at >= 0 && !step.final) items.push(['now', 'this cell']);
    if ((step.deps || []).length) items.push(['dep', 'the value it came from']);
    if ((step.alts || []).length) items.push(['alt', 'other options tried']);
    if ((step.path || []).length) items.push(['path', 'one optimal trace']);
    if ((step.took || []).length) items.push(['path', 'taken']);
    if (!items.length) return null;
    const k = h('p', 'dp-key');
    items.forEach(([c, t]) => { const sp = h('span'); sp.append(h('i', 'k-' + c), t); k.append(sp); });
    return k;
  }

  return {
    'dp-table': (s, data, step, i) => {
      const filled = Math.max(0, step.at + 1);
      const head = step.final ? 'Finished' : i === 0 ? 'Start' : s.fill.length ? `Cell ${filled} of ${s.fill.length}` : 'Step ' + i;
      const out = [h('p', 'steps-time', head), table(s, step)];
      const k = key(step);
      if (k) out.push(k);
      return out;
    },
  };
});
