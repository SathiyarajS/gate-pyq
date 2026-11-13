'use strict';
// "Step through it" renderer: Karnaugh maps (Gray-code grid, cells, group outlines).
// Loaded on demand by assets/steps.js; the data comes from scripts/animations/ (checked against the answer at build time).
window.gateStepsRegister(({el, h, css}) => {
  css(`
.km-map{display:block;max-width:100%;height:auto;margin:4px 0 6px;font-variant-numeric:tabular-nums}
.km-map text{fill:var(--ink)}.km-map .km-head{font-size:13px;font-weight:650;fill:var(--muted)}.km-map .km-vars{font-size:12px;font-weight:700;fill:var(--muted)}
.km-map .km-cell{fill:var(--bg);stroke:var(--line);stroke-width:1}.km-map .km-cell.is-hi{fill:color-mix(in oklab,var(--accent) 20%,var(--bg))}
.km-map .km-idx{font-size:9px;fill:var(--muted);paint-order:stroke;stroke:var(--bg);stroke-width:3px;stroke-linejoin:round}.km-map .km-val{font-size:17px;font-weight:700}.km-map .km-val.v0{font-weight:400;fill:var(--muted)}.km-map .km-val.vX{font-style:italic;fill:var(--muted)}
.km-map .km-bad{fill:none;stroke:var(--ink);stroke-width:1.5;stroke-dasharray:3 2}
.km-map .km-frame{fill:none;stroke:var(--muted);stroke-width:1.2}.km-map .km-diag{stroke:var(--line);stroke-width:1}
.km-map .km-g{fill:none;stroke:currentColor;stroke-width:2.2;stroke-linecap:round;stroke-linejoin:round}
.km-map .km-g.new{stroke-width:3.4}.km-map .km-g.new.fill{fill:color-mix(in oklab,currentColor 12%,transparent)}
.km-map .km-g.ess,.km-map .km-g.pick{stroke-width:3}.km-map .km-g.off{stroke-width:1.4;stroke-dasharray:4 3;opacity:.45}
.km-legend{list-style:none;margin:2px 0 6px;padding:0;font-size:.85rem}.km-legend li{display:flex;align-items:baseline;gap:.5em;flex-wrap:wrap;margin:2px 0}
.km-legend .km-sw{display:inline-block;width:1.6em;border-top:3px solid currentColor;vertical-align:middle;flex:none;transform:translateY(-.2em)}
.km-legend li.off{color:var(--muted)}.km-legend li.off .km-sw{border-top-style:dashed;opacity:.6}
.km-legend .km-term{font-weight:700;color:var(--ink)}.km-legend .km-cells{color:var(--muted)}.km-legend .km-tag{font-size:.75rem;font-weight:650;color:var(--muted);text-transform:uppercase;letter-spacing:.03em}
.km-expr{font-weight:700}.km-key{color:var(--muted)}
`);

  const TAG = {new: 'new', ess: 'essential', pick: 'in the answer', off: 'not used', pi: ''};
  const colour = k => `var(--s${k % 6})`;

  // Index runs along one side of the map, split where the group wraps round the edge.
  function runs(idx, n) {
    if (idx.length === n) return [{a: 0, b: n - 1, lo: false, hi: false}];
    const out = [];
    idx.forEach(i => { const r = out[out.length - 1]; if (r && i === r.b + 1) r.b = i; else out.push({a: i, b: i, lo: false, hi: false}); });
    if (out.length === 2 && out[0].a === 0 && out[1].b === n - 1) { out[0].lo = true; out[1].hi = true; }
    return out;
  }

  function mapSvg(data, step, width) {
    const R = data.rcodes.length, C = data.ccodes.length, rowName = data.rows.map(i => data.vars[i]).join(''), colName = data.cols.map(i => data.vars[i]).join('');
    const L = Math.max(46, 10 + 7 * rowName.length + 18), T = 40;
    const avail = Math.min(Math.max(260, Math.round(width || 360)), 400);
    const cs = Math.max(42, Math.min(62, Math.floor((avail - L - 6) / C)));
    const W = L + C * cs + 4, H = T + R * cs + 4;
    const svg = el('svg', {viewBox: `0 0 ${W} ${H}`, width: W, height: H, class: 'km-map', role: 'img',
      'aria-label': `Karnaugh map, rows ${rowName}, columns ${colName}`});
    svg.append(el('line', {x1: 2, y1: 2, x2: L, y2: T, class: 'km-diag'}));
    svg.append(el('text', {x: 4, y: T - 4, class: 'km-vars'}, rowName));
    svg.append(el('text', {x: L - 2, y: 13, 'text-anchor': 'end', class: 'km-vars'}, colName));
    data.ccodes.forEach((c, j) => svg.append(el('text', {x: L + (j + .5) * cs, y: T - 8, 'text-anchor': 'middle', class: 'km-head'}, c)));
    data.rcodes.forEach((r, i) => svg.append(el('text', {x: L - 8, y: T + (i + .5) * cs + 5, 'text-anchor': 'end', class: 'km-head'}, r)));
    const hi = new Set(step.hi || []), bad = new Set(step.bad || []);
    data.grid.forEach((row, i) => row.forEach((m, j) => {
      const x = L + j * cs, y = T + i * cs, v = step.cells[m];
      svg.append(el('rect', {x, y, width: cs, height: cs, class: 'km-cell' + (hi.has(m) ? ' is-hi' : '')}));
      if (v != null) svg.append(el('text', {x: x + cs / 2, y: y + cs / 2 + 7, 'text-anchor': 'middle', class: 'km-val v' + v}, v));
      if (bad.has(m)) svg.append(el('rect', {x: x + 5, y: y + 5, width: cs - 10, height: cs - 10, rx: 4, class: 'km-bad'}));
    }));
    svg.append(el('rect', {x: L, y: T, width: C * cs, height: R * cs, class: 'km-frame'}));
    // Group outlines: each group is a block of rows x columns; a block that wraps is drawn
    // in pieces whose wrapping side is left open.
    const maxInset = cs / 2 - 9;
    (step.groups || []).forEach(([k, state], layer) => {
      const cells = new Set(data.pis[k].cells);
      const rs = [], cs_ = [];
      data.grid.forEach((row, i) => { if (row.some(m => cells.has(m))) rs.push(i); });
      data.grid[0].forEach((_, j) => { if (data.grid.some(row => cells.has(row[j]))) cs_.push(j); });
      const d = Math.min(4 + 3 * layer, maxInset), g = el('g', {style: `color:${colour(k)}`});
      runs(rs, R).forEach(r => runs(cs_, C).forEach(c => {
        const x0 = c.lo ? L - 3 : L + c.a * cs + d, x1 = c.hi ? L + C * cs + 3 : L + (c.b + 1) * cs - d;
        const y0 = r.lo ? T - 3 : T + r.a * cs + d, y1 = r.hi ? T + R * cs + 3 : T + (r.b + 1) * cs - d;
        const cls = 'km-g ' + state;
        if (!c.lo && !c.hi && !r.lo && !r.hi) { g.append(el('rect', {x: x0, y: y0, width: x1 - x0, height: y1 - y0, rx: 9, class: cls + ' fill'})); return; }
        // Open sides: draw only the closed edges.
        const p = [];
        if (!r.lo) p.push(`M${x0} ${y0}H${x1}`);
        if (!c.hi) p.push(`M${x1} ${y0}V${y1}`);
        if (!r.hi) p.push(`M${x0} ${y1}H${x1}`);
        if (!c.lo) p.push(`M${x0} ${y0}V${y1}`);
        g.append(el('path', {d: p.join(''), class: cls}));
      }));
      svg.append(g);
    });
    // Minterm numbers go on top of the outlines so they stay readable.
    data.grid.forEach((row, i) => row.forEach((m, j) => svg.append(el('text', {x: L + j * cs + 5, y: T + i * cs + 12, class: 'km-idx'}, m))));
    return svg;
  }

  function legend(data, step) {
    const ul = h('ul', 'km-legend');
    (step.groups || []).forEach(([k, state]) => {
      const p = data.pis[k], li = h('li', state === 'off' ? 'off' : null), sw = h('span', 'km-sw');
      li.style.color = colour(k);
      li.append(sw, h('span', 'km-term', p.text), h('span', 'km-cells', '(' + p.cells.join(', ') + ')'));
      if (TAG[state]) li.append(h('span', 'km-tag', TAG[state]));
      ul.append(li);
    });
    return ul;
  }

  return {
    kmap: (s, data, step, i, width) => {
      const out = [h('p', 'steps-time', step.phase), mapSvg(data, step, width)];
      if (step.groups && step.groups.length) out.push(legend(data, step));
      if (step.key) out.push(h('p', 'steps-ready km-key', step.key));
      if (step.expr) out.push(h('p', 'steps-ready km-expr', step.expr));
      return out;
    },
  };
});
