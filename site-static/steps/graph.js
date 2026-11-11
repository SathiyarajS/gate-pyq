'use strict';
// "Step through it" renderer: graph algorithms (BFS/DFS orders, shortest paths, Kruskal, topological orders).
// Loaded on demand by assets/steps.js; the data comes from scripts/animations/graph.py (checked against the answer at build time).
// Each step says which vertices and edges to highlight (n, e), short labels beside vertices (tag),
// an optional side table and status lines; this file only draws them.
window.gateStepsRegister(({el, h, css}) => {
  css(`
.graph{display:block;width:100%;max-width:560px;height:auto;margin:4px 0;font-family:inherit;overflow:visible}
.graph .e{fill:none;stroke:var(--muted);stroke-opacity:.55;stroke-width:1.6;stroke-linecap:round}
.graph .arrow{fill:var(--muted);fill-opacity:.7}
.graph .e.tree{stroke:var(--accent);stroke-opacity:1;stroke-width:3.5}.graph .arrow.tree{fill:var(--accent);fill-opacity:1}
.graph .e.path{stroke:var(--s2);stroke-opacity:1;stroke-width:4.5}.graph .arrow.path{fill:var(--s2);fill-opacity:1}
.graph .e.now{stroke:var(--s1);stroke-opacity:1;stroke-width:4}.graph .arrow.now{fill:var(--s1);fill-opacity:1}
.graph .e.bad{stroke-dasharray:4 4;stroke-opacity:.45}.graph .arrow.bad{fill-opacity:.4}
.graph .e.off,.graph .arrow.off{stroke-opacity:.18;fill-opacity:.18}
.graph .w{font-size:11px;font-weight:600;fill:var(--ink);paint-order:stroke;stroke:var(--bg);stroke-width:3.5px;stroke-linejoin:round;font-variant-numeric:tabular-nums}
.graph .w.off,.graph .w.bad{fill:var(--muted)}.graph .w.now,.graph .w.path{font-weight:800}
.graph .n circle{fill:var(--panel);stroke:var(--muted);stroke-width:1.5}
.graph .n text{font-size:12px;font-weight:700;fill:var(--ink)}
.graph .n.seen circle{stroke:var(--accent);stroke-width:3}
.graph .n.done circle{fill:var(--accent);stroke:var(--accent)}.graph .n.done text{fill:var(--bg)}
.graph .n.now circle{fill:var(--s1);stroke:var(--s1)}.graph .n.now text{fill:#0b0b0b}
.graph .n.off{opacity:.35}
.graph .tag{font-size:11px;font-weight:700;fill:var(--accent);paint-order:stroke;stroke:var(--bg);stroke-width:3.5px;stroke-linejoin:round;font-variant-numeric:tabular-nums}
.graph-key{display:flex;flex-wrap:wrap;gap:2px 14px;margin:0 0 6px;font-size:.78rem;color:var(--muted)}
.graph-key span{white-space:nowrap}.graph-key i{display:inline-block;vertical-align:middle;margin-right:.4em}
.graph-key .k-n{width:.85em;height:.85em;border-radius:50%;border:1.5px solid var(--muted);background:var(--panel)}
.graph-key .k-n.seen{border:3px solid var(--accent)}.graph-key .k-n.done{background:var(--accent);border-color:var(--accent)}.graph-key .k-n.now{background:var(--s1);border-color:var(--s1)}
.graph-key .k-e{width:1.4em;height:0;border-top:3.5px solid var(--accent)}.graph-key .k-e.now{border-top:4px solid var(--s1)}
.graph-key .k-e.path{border-top:4.5px solid var(--s2)}.graph-key .k-e.bad{border-top:2px dashed var(--muted)}
`);

  const RANK = {'': 0, off: 0, bad: 1, tree: 2, path: 3, now: 4};

  function layout(data, W, r) {
    const pad = r + 14, pts = {};
    let H;
    if (data.pos) {
      const xs = data.nodes.map(v => data.pos[v][0]), ys = data.nodes.map(v => data.pos[v][1]);
      const x0 = Math.min(...xs), y0 = Math.min(...ys), sx = Math.max(...xs) - x0 || 1, sy = Math.max(...ys) - y0 || 1;
      const maxH = Math.min(W, 440), s = Math.min((W - 2 * pad) / sx, (maxH - 2 * pad) / sy);
      const ox = (W - sx * s) / 2;
      H = sy * s + 2 * pad;
      data.nodes.forEach(v => { pts[v] = [ox + (data.pos[v][0] - x0) * s, pad + (data.pos[v][1] - y0) * s]; });
    } else {
      const R = (Math.min(W, 400) - 2 * pad) / 2, n = data.nodes.length;
      H = 2 * R + 2 * pad;
      data.nodes.forEach((v, k) => { const a = 2 * Math.PI * k / n; pts[v] = [W / 2 + R * Math.sin(a), pad + R - R * Math.cos(a)]; });
    }
    return {pts, H};
  }

  // Where a vertex's label goes: the compass direction farthest from its edges, preferring up.
  function tagSpot(v, pts, data, r) {
    const [x, y] = pts[v];
    const dirs = data.edges.filter(([a, b]) => a === v || b === v).map(([a, b]) => { const [px, py] = pts[a === v ? b : a]; return Math.atan2(py - y, px - x); });
    let best = -Math.PI / 2, gap = -1;
    for (let k = 0; k < 8; k++) {
      const a = -Math.PI / 2 + k * Math.PI / 4;
      const g = dirs.length ? Math.min(...dirs.map(d => { const t = Math.abs(a - d) % (2 * Math.PI); return Math.min(t, 2 * Math.PI - t); })) : Math.PI;
      if (g > gap + 1e-6) { gap = g; best = a; }
    }
    return [x + Math.cos(best) * (r + 10), y + Math.sin(best) * (r + 10) + 4];
  }

  function graphSvg(data, step, width) {
    const W = Math.max(280, Math.min(560, Math.round(width || 560))), r = W < 360 ? 14 : 15;
    const {pts, H} = layout(data, W, r);
    const svg = el('svg', {viewBox: `0 0 ${W} ${H}`, class: 'graph', role: 'img', 'aria-label': (data.directed ? 'Directed' : 'Undirected') + ' graph'});
    const ecls = step.e || {}, ncls = step.n || {};
    const both = new Set(data.edges.map(([u, v]) => u + '\u0001' + v));
    const order = data.edges.map((e, i) => i).sort((a, b) => (RANK[ecls[a] || ''] - RANK[ecls[b] || '']) || a - b);
    const labels = [];
    order.forEach(i => {
      const [u, v, w] = data.edges[i], c = ecls[i] || '';
      const [x1, y1] = pts[u], [x2, y2] = pts[v], L = Math.hypot(x2 - x1, y2 - y1) || 1;
      const nx = -(y2 - y1) / L, ny = (x2 - x1) / L;
      // A pair of opposite arcs bends apart so both stay visible.
      const bend = data.directed && both.has(v + '\u0001' + u) ? 26 : 0;
      const cx = (x1 + x2) / 2 + nx * bend, cy = (y1 + y2) / 2 + ny * bend;
      const unit = (ax, ay, bx, by) => { const d = Math.hypot(bx - ax, by - ay) || 1; return [(bx - ax) / d, (by - ay) / d]; };
      const [sx, sy] = unit(x1, y1, cx, cy), [tx, ty] = unit(x2, y2, cx, cy);
      const p0 = [x1 + sx * r, y1 + sy * r], tip = [x2 + tx * r, y2 + ty * r];
      const end = data.directed ? [tip[0] + tx * 9, tip[1] + ty * 9] : tip;
      svg.append(el('path', {d: `M${p0[0].toFixed(1)} ${p0[1].toFixed(1)} Q${cx.toFixed(1)} ${cy.toFixed(1)} ${end[0].toFixed(1)} ${end[1].toFixed(1)}`, class: 'e ' + c}));
      if (data.directed) {
        const bx = tip[0] + tx * 10, by = tip[1] + ty * 10;
        svg.append(el('polygon', {points: [tip, [bx - ty * 5, by + tx * 5], [bx + ty * 5, by - tx * 5]].map(p => p.map(z => z.toFixed(1)).join(',')).join(' '), class: 'arrow ' + c}));
      }
      if (w != null) labels.push(el('text', {x: ((x1 + x2) / 2 + nx * bend / 2).toFixed(1), y: ((y1 + y2) / 2 + ny * bend / 2 + 4).toFixed(1), 'text-anchor': 'middle', class: 'w ' + c}, w));
    });
    labels.forEach(t => svg.append(t));
    data.nodes.forEach(v => {
      const [x, y] = pts[v], g = el('g', {class: 'n ' + (ncls[v] || '')});
      g.append(el('circle', {cx: x.toFixed(1), cy: y.toFixed(1), r}));
      g.append(el('text', {x: x.toFixed(1), y: (y + 4).toFixed(1), 'text-anchor': 'middle'}, v));
      svg.append(g);
    });
    Object.entries(step.tag || {}).forEach(([v, t]) => {
      const [x, y] = tagSpot(v, pts, data, r);
      svg.append(el('text', {x: x.toFixed(1), y: y.toFixed(1), 'text-anchor': 'middle', class: 'tag'}, t));
    });
    return svg;
  }

  function key(legend) {
    const k = h('p', 'graph-key');
    legend.forEach(([what, text]) => { const s = h('span'), [type, cls] = what.split('-'); s.append(h('i', 'k-' + type + ' ' + cls), text); k.append(s); });
    return k;
  }

  function table(t) {
    const tab = h('table', 'steps-table'), head = tab.createTHead().insertRow(), body = tab.createTBody();
    t.head.forEach(c => head.append(h('th', null, c)));
    t.rows.forEach((row, k) => { const tr = body.insertRow(); row.forEach(v => { tr.insertCell().textContent = v; }); if ((t.now || []).includes(k)) tr.className = 'is-running'; });
    const w = h('div', 'steps-table-wrap'); w.append(tab);
    return w;
  }

  function view(s, data, step, i, width) {
    const out = [h('p', 'steps-time', step.final ? 'Finished' : step.head || 'Step ' + (i + 1)), graphSvg(data, step, width)];
    if (s.legend) out.push(key(s.legend));
    (step.line || []).forEach(t => out.push(h('p', 'steps-ready', t)));
    if (step.table && step.table.rows.length) out.push(table(step.table));
    return out;
  }

  return {'graph-paths': view, 'graph-mst': view, 'graph-search': view, 'graph-topo': view};
});
