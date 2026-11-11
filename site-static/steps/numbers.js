'use strict';
// "Step through it" renderer: number systems (working tables, digits aligned in columns, bit groups).
// Loaded on demand by assets/steps.js; the data comes from scripts/animations/numbers.py (checked against the answer at build time).
window.gateStepsRegister(({h, css}) => {
  css(`
.num-mono,.num-grid td,.num-g span{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,"Liberation Mono",monospace}
.num-table sub,.num-grid sub{font-size:.72em}
.num-grid{border-collapse:collapse;margin:4px 0 8px;font-size:.92rem;font-variant-numeric:tabular-nums}
.num-grid th,.num-grid td{border:0;min-width:0;width:auto}
.num-grid th{font-weight:650;font-size:.75rem;color:var(--muted);text-align:right;padding:2px 8px 2px 0;white-space:nowrap}
.num-grid td{text-align:center;padding:2px 1px;min-width:1.05em;line-height:1.55}
.num-grid td.gap{padding-left:7px}
.num-grid.dense{font-size:.84rem}.num-grid.dense td{min-width:.95em}
.num-table td.num-wrap{white-space:normal;min-width:7em}
.num-grid tr.carry td{font-size:.74rem;color:var(--s1);font-weight:700}
.num-grid tr.sum td{border-top:2px solid var(--ink);font-weight:700}
.num-grid tr.muted td{color:var(--muted)}
.num-grid td.is-now{background:color-mix(in oklab,var(--accent) 18%,transparent)}
.num-groups{display:flex;flex-wrap:wrap;align-items:flex-end;gap:6px;margin:4px 0 8px}
.num-glabel{flex-basis:100%;font-size:.75rem;font-weight:650;color:var(--muted)}
.num-g{border:1px solid var(--line);border-radius:5px;padding:1px 6px 3px;text-align:center;background:var(--panel);min-width:1.9em}
.num-g b{display:block;font-size:.72rem;font-weight:650;color:var(--muted);white-space:nowrap}
.num-g span{display:block;font-size:.9rem;letter-spacing:.03em;white-space:nowrap;min-height:1.3em}
.num-g.c0{border-color:var(--s0);background:color-mix(in oklab,var(--s0) 12%,var(--panel))}
.num-g.c1{border-color:var(--s1);background:color-mix(in oklab,var(--s1) 12%,var(--panel))}
.num-g.c2{border-color:var(--s2);background:color-mix(in oklab,var(--s2) 12%,var(--panel))}
.num-g.is-now{box-shadow:0 0 0 2px var(--accent)}
.steps-table tr.is-good td{color:var(--accent);font-weight:650}
`);

  // A numeral written 224_5 or 13_r in the data is drawn with its base as a subscript.
  function rich(node, text) {
    const re = /([0-9A-Za-z.]+)_([0-9a-z]+)/g;
    let at = 0, m;
    while ((m = re.exec(text))) {
      if (m.index > at) node.append(text.slice(at, m.index));
      node.append(m[1], h('sub', null, m[2]));
      at = re.lastIndex;
    }
    if (at < text.length) node.append(text.slice(at));
    return node;
  }
  const wrap = node => { const w = h('div', 'steps-table-wrap'); w.append(node); return w; };

  // A table that grows by one row per step; the newest row is highlighted until the end.
  function table(b) {
    const t = h('table', 'steps-table num-table'), head = t.createTHead().insertRow(), body = t.createTBody();
    b.head.forEach(c => head.append(rich(h('th'), c)));
    b.rows.forEach((r, k) => {
      const row = body.insertRow();
      r.forEach((v, j) => {
        const c = row.insertCell(), cls = [];
        rich(c, v);
        if (b.mono.includes(j)) cls.push('num-mono');
        if ((b.wrap || []).includes(j)) cls.push('num-wrap');
        if (cls.length) c.className = cls.join(' ');
      });
      const mark = k === b.hl ? 'is-running' : b.marks && b.marks[k];
      if (mark) row.className = mark;
    });
    return wrap(t);
  }

  // Digits in fixed columns (carries, operands, sum); the column being worked on is shaded.
  function grid(b) {
    const wide = Math.max(...b.rows.map(r => r.cells.length)) > 14;
    const t = h('table', wide ? 'num-grid dense' : 'num-grid'), body = t.createTBody();
    b.rows.forEach(r => {
      const row = body.insertRow();
      if (r.cls) row.className = r.cls;
      row.append(rich(h('th'), r.label));
      r.cells.forEach((v, j) => {
        const c = row.insertCell(), cls = [];
        c.textContent = v;
        if (b.now.includes(j)) cls.push('is-now');
        if (b.gaps.includes(j)) cls.push('gap');
        if (cls.length) c.className = cls.join(' ');
      });
    });
    return wrap(t);
  }

  // Boxes of bits with a caption on top: a digit and its bits, or the sign/exponent/fraction fields.
  function groups(b) {
    const box = h('div', 'num-groups');
    if (b.label) box.append(h('span', 'num-glabel', b.label));
    b.items.forEach(it => {
      const g = h('div', 'num-g' + (it.c != null && it.c < 3 ? ' c' + it.c : '') + (it.now ? ' is-now' : ''));
      g.append(h('b', null, it.top || ' '), h('span', null, it.bits || ' '));
      box.append(g);
    });
    return box;
  }

  const draw = {table, grid, groups, line: b => rich(h('p', b.cls || 'steps-ready'), b.text)};
  const view = (s, data, step) => step.blocks.map(b => draw[b.t](b));
  return Object.fromEntries(['radix-convert', 'radix-compare', 'radix-equation', 'base-arith', 'signed-encode',
    'signed-decode', 'signed-ops', 'ieee754', 'booth'].map(k => [k, view]));
});
