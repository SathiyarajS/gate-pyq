'use strict';
// "Step through it" renderer: IP addressing (address, mask and result rows in aligned bit columns; fragment byte ranges; results table).
// Loaded on demand by assets/steps.js; the data comes from scripts/animations/subnet.py (checked against the answer at build time).
window.gateStepsRegister(({el, h, css}) => {
  css(`
.sn-grid{border-collapse:collapse;margin:4px 0 8px;font-size:.9rem;font-variant-numeric:tabular-nums}
.sn-grid td,.sn-grid th{border:0;min-width:0;width:auto;font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,"Liberation Mono",monospace}
.sn-grid th{font-family:inherit;font-weight:650;font-size:.75rem;color:var(--muted);text-align:right;padding:2px 8px 2px 0;white-space:nowrap}
.sn-grid th:first-child{min-width:0}
.sn-grid td{text-align:center;padding:2px 1px;min-width:.95em;line-height:1.5}
.sn-grid td.dot{min-width:0;padding:2px 2px;color:var(--muted)}
.sn-grid td.val{text-align:left;padding-left:10px;font-size:.8rem;white-space:nowrap}
.sn-grid td.net{color:var(--s0);font-weight:700}
.sn-grid td.host{color:var(--s1)}
.sn-grid td.new{color:var(--accent);font-weight:800}
.sn-grid td.ok{color:var(--s2);font-weight:700}
.sn-grid td.muted{color:var(--muted);opacity:.6}
.sn-grid td.bad{background:color-mix(in oklab,var(--s1) 28%,transparent);font-weight:800;border-radius:2px}
.sn-grid tr.muted td,.sn-grid tr.muted th{opacity:.7}
.sn-grid tr.sum td{border-top:2px solid var(--ink);font-weight:700}
.sn-grid tr.bad td.val{color:var(--s1);font-weight:700}
.sn-grid tr.muted-row th,.sn-grid tr.muted-row td.val{color:var(--muted)}
.sn-grid td.is-now{background:color-mix(in oklab,var(--accent) 12%,transparent)}
.sn-key{display:flex;flex-wrap:wrap;gap:4px 12px;font-size:.75rem;color:var(--muted);margin:0 0 6px}
.sn-key b{font-weight:700}.sn-key .k0{color:var(--s0)}.sn-key .k1{color:var(--s1)}
.sn-frags{width:100%;height:auto;display:block;margin:4px 0 8px}
.sn-frags .lab{font-size:11px;fill:var(--muted);font-weight:650}
.sn-frags .num{font-size:11px;font-weight:700;fill:#0b0b0b}
.sn-frags .tick{font-size:10px;fill:var(--muted)}
.sn-frags rect.f0{fill:var(--s0)}.sn-frags rect.f1{fill:var(--s2)}.sn-frags rect.f2{fill:var(--s3)}.sn-frags rect.f3{fill:var(--s4)}
.sn-frags rect{stroke:var(--panel);stroke-width:1.5}
.sn-frags rect.alt{opacity:.72}
`);
  const wrap = node => { const w = h('div', 'steps-table-wrap'); w.append(node); return w; };

  // Address rows: octets cut by a mask are shown bit by bit, the others in decimal; network bits blue, host bits orange.
  function grid(b) {
    const t = h('table', 'sn-grid'), now = new Set(b.now), body = t.createTBody();
    let coloured = false;
    b.rows.forEach(r => {
      const row = body.insertRow();
      if (r.cls) row.className = r.cls;
      row.append(h('th', null, r.label || ''));
      r.cells.forEach((v, j) => {
        const c = row.insertCell(), [text, cls] = Array.isArray(v) ? v : [v, null];
        c.textContent = text;
        if (cls === 'net' || cls === 'host') coloured = true;
        const k = [cls, now.has(j) ? 'is-now' : ''].filter(Boolean).join(' ');
        if (k) c.className = k;
      });
      const c = row.insertCell(); c.className = 'val'; c.textContent = r.value || '';
    });
    const out = [wrap(t)];
    if (coloured) { const key = h('p', 'sn-key'); key.append(h('b', 'k0', 'network bits'), h('b', 'k1', 'host bits')); out.push(key); }
    return out;
  }

  // Byte ranges of the payload, one bar per stage; each fragment is a box with its size.
  function frags(b, width) {
    const W = Math.max(300, Math.min(680, Math.round(width || 600))), left = 84, right = 8, rowH = 24, gap = 8;
    const H = b.rows.length * (rowH + gap) + 14, x = v => left + (W - left - right) * v / b.total;
    const svg = el('svg', {viewBox: `0 0 ${W} ${H}`, class: 'sn-frags', role: 'img', 'aria-label': 'Payload byte ranges of the fragments'});
    b.rows.forEach((r, k) => {
      const y = k * (rowH + gap);
      svg.append(el('text', {x: left - 6, y: y + rowH / 2 + 4, 'text-anchor': 'end', class: 'lab'}, r.label));
      r.parts.forEach(([start, n, text, cls], j) => {
        const x0 = x(start), w = Math.max(1.5, x(start + n) - x0);
        svg.append(el('rect', {x: x0, y, width: w, height: rowH, rx: 2, class: 'f' + (cls % 4) + (j % 2 ? ' alt' : '')}));
        if (w > 7 * text.length + 6) svg.append(el('text', {x: x0 + w / 2, y: y + rowH / 2 + 4, 'text-anchor': 'middle', class: 'num'}, text));
      });
    });
    const yb = b.rows.length * (rowH + gap) + 6;
    svg.append(el('text', {x: left, y: yb, class: 'tick'}, 'byte 0'));
    svg.append(el('text', {x: W - right, y: yb, 'text-anchor': 'end', class: 'tick'}, String(b.total)));
    return svg;
  }

  function table(b) {
    const t = h('table', 'steps-table'), head = t.createTHead().insertRow(), body = t.createTBody();
    b.head.forEach(c => head.append(h('th', null, c)));
    b.rows.forEach((r, k) => {
      const row = body.insertRow(); r.forEach(v => { row.insertCell().textContent = v; });
      const mark = k === b.hl ? 'is-running' : b.marks && b.marks[k];
      if (mark) row.className = mark;
    });
    return wrap(t);
  }

  const draw = {grid, frags, table, line: b => h('p', b.cls || 'steps-ready', b.text)};
  const view = (s, data, step, i, width) => step.blocks.flatMap(b => draw[b.t](b, width));
  return Object.fromEntries(['same-subnet', 'subnet-size', 'cidr-check', 'lpm', 'fragment', 'fragment-header'].map(k => [k, view]));
});
