'use strict';
// "Step through it" renderer: error control (CRC long division in aligned bit columns, Hamming bit-position table, code distances).
// Loaded on demand by assets/steps.js; the data comes from scripts/animations/errorcode.py (checked against the answer at build time).
window.gateStepsRegister(({h, css}) => {
  css(`
.ec-grid{border-collapse:collapse;margin:4px 0 8px;font-size:.92rem;font-variant-numeric:tabular-nums}
.ec-grid td,.ec-grid th{border:0;min-width:0;width:auto;font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,"Liberation Mono",monospace}
.ec-grid th{font-family:inherit;font-weight:650;font-size:.75rem;color:var(--muted);text-align:right;padding:2px 8px 2px 0;white-space:nowrap}
.ec-grid thead th{text-align:center;padding:0 1px;font-size:.68rem;font-weight:500}
.ec-grid th:first-child{min-width:0}
.ec-grid td{text-align:center;padding:2px 1px;min-width:1.15em;line-height:1.5;white-space:nowrap}
.ec-grid td.gap,.ec-grid thead th.gap{padding-left:9px}
.ec-grid td.val{text-align:left;padding-left:10px;font-family:inherit;font-size:.8rem;color:var(--muted);white-space:nowrap}
.ec-grid td.muted,.ec-grid tr.muted td{color:var(--muted);opacity:.75}
.ec-grid td.hit{color:var(--s0);font-weight:700}
.ec-grid td.new{color:var(--accent);font-weight:800}
.ec-grid td.unk{color:var(--s1);font-weight:800;font-style:italic}
.ec-grid tr.sum td{border-top:2px solid var(--ink)}
.ec-grid tr.hl td,.ec-grid tr.hl th{background:color-mix(in oklab,var(--accent) 12%,transparent)}
.ec-grid td.is-now,.ec-grid thead th.is-now{background:color-mix(in oklab,var(--accent) 16%,transparent)}
.ec-grid tr.sum.muted td{border-top-color:var(--line)}
`);
  const wrap = node => { const w = h('div', 'steps-table-wrap'); w.append(node); return w; };

  // Bits in fixed columns. A cell is text or [text, class]; the columns being worked on are shaded.
  function grid(b) {
    const t = h('table', 'ec-grid'), gaps = new Set(b.gaps), now = new Set(b.now);
    if (b.head) {
      const r = t.createTHead().insertRow(); r.append(h('th'));
      b.head.forEach((v, j) => { const c = h('th', [gaps.has(j) ? 'gap' : '', now.has(j) ? 'is-now' : ''].join(' ').trim() || null, v); r.append(c); });
    }
    const body = t.createTBody();
    b.rows.forEach(r => {
      const row = body.insertRow();
      if (r.cls) row.className = r.cls;
      row.append(h('th', null, r.label || ''));
      r.cells.forEach((v, j) => {
        const c = row.insertCell(), [text, cls] = Array.isArray(v) ? v : [v, null];
        c.textContent = text;
        const k = [cls, gaps.has(j) ? 'gap' : '', now.has(j) ? 'is-now' : ''].filter(Boolean).join(' ');
        if (k) c.className = k;
      });
      if (r.value != null) { const c = row.insertCell(); c.className = 'val'; c.textContent = r.value; }
    });
    return wrap(t);
  }

  function table(b) {
    const t = h('table', 'steps-table'), head = t.createTHead().insertRow(), body = t.createTBody();
    b.head.forEach(c => head.append(h('th', null, c)));
    b.rows.forEach((r, k) => { const row = body.insertRow(); r.forEach(v => { row.insertCell().textContent = v; }); if (k === b.hl) row.className = 'is-running'; });
    return wrap(t);
  }

  const draw = {grid, table, line: b => h('p', b.cls || 'steps-ready', b.text)};
  const view = (s, data, step) => step.blocks.map(b => draw[b.t](b));
  return {crc: view, 'hamming-fill': view, 'code-distance': view};
});
