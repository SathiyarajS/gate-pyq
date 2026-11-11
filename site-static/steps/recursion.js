'use strict';
// "Step through it" renderer: recursive calls. The call tree grows one call at a time; each node is
// labelled with its arguments and gets its return value when it returns. Beside it: the program
// (the line that runs is marked), the output so far and the variables that matter.
// Loaded on demand by assets/steps.js; the data comes from scripts/animations/recursion.py (checked against the answer at build time).
window.gateStepsRegister(({el, h, css}) => {
  css(`
.rec-tally{display:flex;flex-wrap:wrap;gap:6px 14px;margin:4px 0 6px;font-size:.85rem}
.rec-tally span{color:var(--muted)}.rec-tally b{color:var(--ink);font-variant-numeric:tabular-nums;margin-left:.3em}
.rec-main{display:flex;gap:14px;align-items:flex-start}.rec-main.stacked{flex-direction:column;gap:6px}
.rec-main>div{min-width:0;max-width:100%}
.rec-code{margin:2px 0 4px;padding:6px 0;font-size:.78rem;line-height:1.45;background:var(--panel);border-radius:6px;overflow-x:auto;flex:0 0 auto;max-width:100%}
.rec-code span{display:block;padding:0 10px;white-space:pre}.rec-code span.is-now{background:color-mix(in oklab,var(--accent) 18%,transparent);box-shadow:inset 3px 0 0 var(--accent)}
.rec-wrap{overflow-x:auto;max-width:100%}
.rec-tree{display:block;height:auto;font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}
.rec-tree .edge{fill:none;stroke:var(--line);stroke-width:1.5}.rec-tree .edge.live{stroke:var(--accent);stroke-width:2}
.rec-tree .node rect{fill:var(--bg);stroke:var(--muted);stroke-width:1.2}.rec-tree .node text{fill:var(--ink);font-variant-numeric:tabular-nums}
.rec-tree .node .val{font-weight:700}.rec-tree .node .tag{fill:var(--muted)}
.rec-tree .node.wait rect{stroke:var(--accent);stroke-width:2}
.rec-tree .node.now rect{fill:var(--accent);stroke:var(--accent)}.rec-tree .node.now text{fill:var(--bg)}
.rec-tree .node.done rect{stroke:var(--line)}.rec-tree .node.done .lab{fill:var(--muted)}
.rec-tree .node.repeat rect,.rec-tree .node.fold rect{stroke-dasharray:4 3}
.rec-tree .row rect{fill:none}
.rec-tree .row.now rect{fill:color-mix(in oklab,var(--accent) 18%,transparent)}
.rec-tree .row text{fill:var(--ink)}.rec-tree .row.done .lab{fill:var(--muted)}.rec-tree .row.wait .lab,.rec-tree .row.now .lab{font-weight:700}
.rec-tree .row .val{font-weight:700;fill:var(--ink)}.rec-tree .row .tag{fill:var(--muted)}
.rec-tree .row.repeat .lab,.rec-tree .row.fold .lab{text-decoration:underline dashed;text-underline-offset:3px}
.rec-out{display:flex;align-items:baseline;gap:8px;margin:6px 0 2px;font-size:.85rem}
.rec-out>span{color:var(--muted);font-weight:650;font-size:.78rem;flex:0 0 auto}
.rec-out code{padding:2px 8px;border:1px solid var(--line);border-radius:4px;background:var(--bg);white-space:pre-wrap;overflow-wrap:anywhere;font-size:.85rem}
.rec-out mark{background:color-mix(in oklab,var(--accent) 25%,transparent);color:inherit;font-weight:700;border-radius:2px}
.rec-vars{display:flex;flex-wrap:wrap;align-items:center;gap:4px 12px;margin:4px 0 2px;font-size:.82rem;font-variant-numeric:tabular-nums}
.rec-vars>span{white-space:nowrap}.rec-vars .k{color:var(--muted)}.rec-vars .is-new{font-weight:750;color:var(--accent)}
.rec-vars .own{padding:1px 6px;border-radius:4px;background:var(--panel)}
.rec-arr{display:inline-flex;gap:2px;vertical-align:middle}.rec-arr i{font-style:normal;min-width:1.5em;padding:1px 3px;text-align:center;border:1px solid var(--line);border-radius:3px}
.rec-arr i.at{border-color:var(--accent);background:color-mix(in oklab,var(--accent) 15%,transparent);font-weight:700}
.rec-key{font-size:.75rem;color:var(--muted);margin:2px 0}
`);

  const CH = 7.25, FS = 12; // monospace character width and font size in the tree

  function shape(nodes) {
    const kids = nodes.map(() => []), depth = [];
    nodes.forEach((n, k) => { depth[k] = n.p == null ? 0 : depth[n.p] + 1; if (n.p != null) kids[n.p].push(k); });
    return {kids, depth, maxDepth: Math.max(...depth)};
  }

  const valueText = n => n.v == null ? '' : n.v;
  const tagText = n => n.kind === 'repeat' ? 'again' : n.kind === 'fold' ? `${n.calls} call${n.calls > 1 ? 's' : ''}` : '';
  const cls = (st, k, n, step) => (st === 'a' && !step.final ? ' now' : st === 'w' ? ' wait' : st === 'd' ? ' done' : '') + (n.kind !== 'call' ? ' ' + n.kind : '');

  // Top-down: boxes placed from the final tree (leaves left to right, parents centred), so nodes never move.
  function topDown(s, step, W, sh) {
    const nodes = s.nodes, boxW = nodes.map(n => Math.max(n.label.length, valueText(n).length + 2, tagText(n).length) * CH + 12);
    const slot = Math.max(...boxW) + 8, pos = [];
    let leaf = 0;
    const walk = k => { if (!sh.kids[k].length) { pos[k] = leaf++; return; } sh.kids[k].forEach(walk); pos[k] = (pos[sh.kids[k][0]] + pos[sh.kids[k].at(-1)]) / 2; };
    walk(0);
    if (leaf * slot > W) return null;
    const bh = 34, rowH = 56, pad = 2, Wt = Math.max(leaf * slot, 0);
    const at = k => [pad + (pos[k] + 0.5) * slot, pad + sh.depth[k] * rowH];
    const svg = el('svg', {viewBox: `0 0 ${Wt + 2 * pad} ${2 * pad + bh + sh.maxDepth * rowH}`, width: Wt + 2 * pad, class: 'rec-tree', role: 'img', 'aria-label': 'Call tree'});
    for (let k = 1; k < step.n; k++) {
      const [x1, y1] = at(nodes[k].p), [x2, y2] = at(k), live = step.st[k] !== 'd' && !step.final;
      svg.append(el('path', {d: `M${x1} ${y1 + bh}C${x1} ${y1 + bh + 14} ${x2} ${y2 - 14} ${x2} ${y2}`, class: 'edge' + (live ? ' live' : '')}));
    }
    for (let k = 0; k < step.n; k++) {
      const n = nodes[k], st = step.st[k], [x, y] = at(k), w = boxW[k];
      const g = el('g', {class: 'node' + cls(st, k, n, step)});
      g.append(el('rect', {x: x - w / 2, y, width: w, height: bh, rx: 6}));
      g.append(el('text', {x, y: y + 14, 'text-anchor': 'middle', 'font-size': FS, class: 'lab'}, n.label));
      const v = st === 'd' ? (n.v != null ? '= ' + n.v : tagText(n) || 'done') : '';
      if (v) g.append(el('text', {x, y: y + 28, 'text-anchor': 'middle', 'font-size': FS, class: n.v != null ? 'val' : 'tag'}, v));
      const t = el('title', {}, n.label + (n.v != null && st === 'd' ? ' returns ' + n.v : '') + (n.kind === 'repeat' ? ' (same as an earlier call)' : ''));
      g.append(t);
      svg.append(g);
    }
    return svg;
  }

  // Outline: one row per call, indented by depth, with elbow lines to the caller. Fits any tree at phone width.
  function outline(s, step, W, sh) {
    const nodes = s.nodes, rowH = 22, pad = 3;
    const text = k => nodes[k].label.length + (nodes[k].v != null ? valueText(nodes[k]).length + 3 : 0) + (tagText(nodes[k]) ? tagText(nodes[k]).length + 3 : 0);
    const longest = Math.max(...nodes.map((_, k) => text(k) * CH + sh.depth[k] * 0)), maxD = Math.max(1, sh.maxDepth);
    const ind = Math.max(10, Math.min(22, Math.floor((W - 2 * pad - 14 - Math.max(...nodes.map((_, k) => text(k) * CH))) / maxD)));
    const Wt = Math.max(W, Math.ceil(Math.max(...nodes.map((_, k) => pad + 12 + sh.depth[k] * ind + text(k) * CH + 8)))), H = 2 * pad + nodes.length * rowH;
    void longest;
    const svg = el('svg', {viewBox: `0 0 ${Wt} ${H}`, width: Wt, class: 'rec-tree', role: 'img', 'aria-label': 'Call tree'});
    const x0 = k => pad + 6 + sh.depth[k] * ind, yc = k => pad + k * rowH + rowH / 2;
    for (let k = 1; k < step.n; k++) {
      const p = nodes[k].p, live = step.st[k] !== 'd' && !step.final;
      svg.append(el('path', {d: `M${x0(p)} ${yc(p) + 7}V${yc(k)}H${x0(k) - 3}`, class: 'edge' + (live ? ' live' : '')}));
    }
    for (let k = 0; k < step.n; k++) {
      const n = nodes[k], st = step.st[k], x = x0(k), y = yc(k);
      const g = el('g', {class: 'row' + cls(st, k, n, step)});
      g.append(el('rect', {x: x - 4, y: y - rowH / 2 + 1, width: (n.label.length + (st === 'd' && n.v != null ? valueText(n).length + 3 : 0)) * CH + 8, height: rowH - 2, rx: 4}));
      const t = el('text', {x, y: y + 4, 'font-size': FS});
      const lab = el('tspan', {class: 'lab'}, n.label); t.append(lab);
      if (st === 'd' && n.v != null) t.append(el('tspan', {class: 'val'}, ' → ' + n.v));
      if (st === 'd' && tagText(n)) t.append(el('tspan', {class: 'tag'}, '  ' + tagText(n)));
      g.append(t);
      g.append(el('title', {}, n.label + (n.v != null && st === 'd' ? ' returns ' + n.v : '') + (n.kind === 'repeat' ? ' (same as an earlier call)' : '')));
      svg.append(g);
    }
    return svg;
  }

  function code(data, step) {
    const pre = h('pre', 'rec-code');
    data.code.forEach((line, k) => pre.append(h('span', k === step.line ? 'is-now' : null, line)));
    return pre;
  }

  function vars(step, prev) {
    if (!step.vars || !step.vars.length) return null;
    const box = h('div', 'rec-vars'), before = new Map((prev && prev.vars || []).map(r => [r.k + (r.own ? '@' : ''), r]));
    const active = step.act != null ? null : null; void active;
    let ownLabel = false;
    step.vars.forEach(r => {
      const old = before.get(r.k + (r.own ? '@' : '')), sp = h('span', r.own ? 'own' : null);
      if (r.own && !ownLabel) { ownLabel = true; }
      sp.append(h('span', 'k', r.k + ' = '));
      if (r.arr) {
        const a = h('span', 'rec-arr');
        r.arr.forEach((x, i) => a.append(h('i', i === r.at ? 'at' : null, x)));
        sp.append(a);
      } else {
        sp.append(h('b', old && old.v !== r.v && prev && !(r.own && prev.act !== step.act) ? 'is-new' : null, r.v));
      }
      box.append(sp);
    });
    return box;
  }

  function view(s, data, step, i, width) {
    const W = Math.max(280, Math.round(width || 560)), prev = i > 0 ? s.steps[i - 1] : null;
    const out = [];
    const tally = h('p', 'rec-tally'), stat = (label, v) => { const sp = h('span', null, label); sp.append(h('b', null, v)); tally.append(sp); };
    stat('Calls so far', step.calls);
    const live = step.final ? 0 : [...step.st].filter(c => c !== 'd').length;
    if (!step.final) stat('Calls in progress', live);
    out.push(tally);
    const longest = Math.max(...data.code.map(x => x.length)), codeW = longest * 7.1 + 24, side = W - codeW - 14 >= 300;
    const main = h('div', 'rec-main' + (side ? '' : ' stacked'));
    main.append(code(data, step));
    const right = h('div'), treeW = side ? W - codeW - 14 : W, sh = shape(s.nodes);
    const wrap = h('div', 'rec-wrap');
    wrap.append(topDown(s, step, treeW, sh) || outline(s, step, treeW, sh));
    right.append(wrap);
    if (s.steps.some(x => x.out)) {
      const o = h('p', 'rec-out'), c = h('code');
      o.append(h('span', null, 'Output'));
      const text = step.out.replace(/\n/g, '↵'), fresh = Math.min(step.fresh || 0, text.length);
      c.append(document.createTextNode(text.slice(0, text.length - fresh) || (fresh ? '' : ' ')));
      if (fresh) c.append(h('mark', null, text.slice(text.length - fresh)));
      o.append(c);
      right.append(o);
    }
    const v = vars(step, prev);
    if (v) right.append(v);
    if (!step.final) {
      const key = ['filled: running now', 'outlined: waiting for a call it made'];
      if (s.nodes.slice(0, step.n).some(n => n.kind === 'repeat')) key.push('dashed: same as an earlier call');
      if (s.nodes.slice(0, step.n).some(n => n.kind === 'fold')) key.push('dashed: its inner calls not drawn');
      right.append(h('p', 'rec-key', key.join(' · ')));
    }
    main.append(right);
    out.push(main);
    return out;
  }

  return {'call-tree': view};
});
