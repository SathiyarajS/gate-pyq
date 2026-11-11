'use strict';
// "Step through it" renderer: stacks and expressions (infix to postfix, postfix evaluation,
// push/pop traces and possible output orders). Every kind uses the same step shape:
// a token strip with the current token marked, stacks drawn top-up, queues and the output so far.
// Loaded on demand by assets/steps.js; the data comes from scripts/animations/ (checked against the answer at build time).
window.gateStepsRegister(({h, css}) => {
  css(`
.stk-strip{display:flex;flex-wrap:wrap;align-items:center;gap:4px;margin:4px 0 10px}
.stk-strip-label,.stk-label{font-size:.78rem;font-weight:650;color:var(--muted);margin-right:4px}
.stk-tok,.stk-cell,.stk-chip{display:inline-flex;align-items:center;justify-content:center;min-width:1.9em;padding:2px 6px;border:1px solid var(--line);border-radius:4px;font-variant-numeric:tabular-nums;font-size:.9rem;line-height:1.35;background:var(--bg)}
.stk-tok.is-done{color:var(--muted);border-color:transparent;background:transparent}
.stk-tok.is-now{background:var(--accent);border-color:var(--accent);color:var(--bg);font-weight:700}
.stk-panel{display:flex;flex-wrap:wrap;align-items:flex-start;gap:12px 18px}
.stk-col{display:flex;flex-direction:column;align-items:center;min-width:3.6em;max-width:100%}
.stk-col .stk-label{margin:0 0 3px}
.stk-box{display:flex;flex-direction:column;gap:3px;padding:4px;min-width:3.2em;min-height:1.9em;max-width:100%;border:2px solid var(--muted);border-top:0;border-radius:0 0 6px 6px}
.stk-cell{position:relative;background:var(--panel);overflow-wrap:anywhere;text-align:center;max-width:100%}
.stk-cell.is-top{border-color:var(--accent)}
.stk-cell.is-new{background:color-mix(in oklab,var(--accent) 16%,var(--panel));font-weight:700}
.stk-cell.is-free{border-style:dashed;background:transparent;color:transparent}
.stk-empty{font-size:.78rem;color:var(--muted);text-align:center;padding:2px 4px}
.stk-side{flex:1 1 170px;min-width:0;display:flex;flex-direction:column;gap:8px}
.stk-row{display:flex;flex-wrap:wrap;align-items:center;gap:4px}
.stk-row .stk-label{flex-basis:100%}
.stk-chip.is-last{border-color:var(--accent);font-weight:700}
.stk-none{font-size:.85rem;color:var(--muted)}
.stk-facts{margin:0;font-size:.9rem;font-weight:650}
`);

  function strip(s, step, i) {
    const t = s.strip, n = t.tokens.length, now = step.pos;
    // A 'Wanted' strip is the required output: what has been output so far is done.
    const done = t.label === 'Wanted' ? step.out.items.length : now != null ? now : (step.final || i > 0 ? n : 0);
    const row = h('div', 'stk-strip');
    row.append(h('span', 'stk-strip-label', t.label));
    t.tokens.forEach((tok, k) => row.append(h('span', 'stk-tok' + (k === now ? ' is-now' : k < done ? ' is-done' : ''), tok)));
    return row;
  }

  // A stack is a cup open at the top: the top item is drawn first, free capacity as dashed slots.
  function stack(st) {
    const col = h('div', 'stk-col'), box = h('div', 'stk-box');
    col.append(h('span', 'stk-label', st.name));
    const items = st.items.slice().reverse();
    if (st.cap != null) for (let k = st.items.length; k < st.cap; k++) box.append(h('span', 'stk-cell is-free', '·'));
    items.forEach((v, k) => box.append(h('span', 'stk-cell' + (k === 0 ? ' is-top' : '') + (k === 0 && st.new ? ' is-new' : ''), v)));
    if (!items.length && st.cap == null) box.append(h('span', 'stk-empty', 'empty'));
    col.append(box);
    return col;
  }

  function row(label, items, last) {
    const r = h('div', 'stk-row');
    r.append(h('span', 'stk-label', label));
    if (!items.length) r.append(h('span', 'stk-none', 'empty'));
    items.forEach((v, k) => r.append(h('span', 'stk-chip' + (last && k === items.length - 1 ? ' is-last' : ''), v)));
    return r;
  }

  function heading(s, step, i) {
    if (step.final) return 'Finished';
    if (step.label) return step.label;
    if (s.strip && step.pos != null) {
      const tok = s.strip.tokens[step.pos];
      return s.strip.label === 'Wanted' ? 'Next wanted: ' + tok : `Token ${step.pos + 1} of ${s.strip.tokens.length}: ${tok}`;
    }
    return i === 0 ? 'Start' : 'End of input';
  }

  function view(s, data, step, i) {
    const out = [h('p', 'steps-time', heading(s, step, i))];
    if (s.strip) out.push(strip(s, step, i));
    const panel = h('div', 'stk-panel'), side = h('div', 'stk-side');
    step.stacks.forEach(st => panel.append(stack(st)));
    step.queues.forEach(q => side.append(row(q.name + ' (front → rear)', q.items)));
    if (step.out) {
      const prev = i > 0 ? s.steps[i - 1].out : null;
      side.append(row(step.out.label, step.out.items, !step.final && prev && step.out.items.length > prev.items.length));
    }
    if (step.facts.length) side.append(h('p', 'stk-facts', step.facts.join(',  ')));
    if (side.children.length) panel.append(side);
    out.push(panel);
    return out;
  }

  return {'stack-postfix': view, 'stack-eval': view, 'stack-ops': view, 'stack-split': view, 'stack-moves': view};
});
