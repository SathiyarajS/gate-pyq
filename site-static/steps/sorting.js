'use strict';
// "Step through it" renderer: sorting traces (a row of array cells with the compared and swapped cells marked).
// Loaded on demand by assets/steps.js; the data comes from scripts/animations/sorting.py (checked against the answer at build time).
window.gateStepsRegister(({h, css}) => {
  css(`
.sort-row{display:flex;flex-wrap:wrap;gap:6px 4px;margin:6px 0 4px;align-items:flex-end}
.sort-cell{display:flex;flex-direction:column;align-items:center;gap:2px}
.sort-cell b{display:flex;align-items:center;justify-content:center;min-width:2.3em;height:2.1em;padding:0 3px;border:1.5px solid var(--line);border-radius:5px;background:var(--panel);font-variant-numeric:tabular-nums;font-size:.92rem;font-weight:650;color:var(--ink)}
.sort-cell small{font-size:.68rem;color:var(--muted);line-height:1}
.sort-cell.gap{margin-left:12px}
.sort-cell.out b{opacity:.38}
.sort-cell.fixed b{border-color:color-mix(in oklab,var(--s2) 70%,var(--line));color:color-mix(in oklab,var(--s2) 55%,var(--ink))}
.sort-cell.piv b{background:color-mix(in oklab,var(--s3) 26%,var(--panel));border-color:var(--s3)}
.sort-cell.cmp b{border:2.5px solid var(--s1)}
.sort-cell.sw b{background:color-mix(in oklab,var(--s0) 24%,var(--panel))}
.sort-cell.run b{background:color-mix(in oklab,var(--accent) 12%,var(--panel))}
.sort-key{display:flex;flex-wrap:wrap;gap:2px 12px;font-size:.78rem;color:var(--muted);margin:0 0 2px}
.sort-key i{display:inline-block;width:.95em;height:.8em;border-radius:2px;margin-right:.35em;vertical-align:-.05em;border:1.5px solid var(--line)}
.sort-key .k-cmp{border:2.5px solid var(--s1)}.sort-key .k-sw{background:color-mix(in oklab,var(--s0) 35%,transparent)}
.sort-key .k-piv{background:color-mix(in oklab,var(--s3) 35%,transparent);border-color:var(--s3)}.sort-key .k-fixed{border-color:var(--s2)}
.sort-key .k-run{background:color-mix(in oklab,var(--accent) 18%,transparent)}
`);

  function cells(step) {
    const row = h('div', 'sort-row'), cmp = new Set(step.cmp || []), sw = new Set(step.sw || []), fixed = new Set(step.fixed || []);
    const starts = new Set((step.runs || []).map(r => r[0]));
    const [lo, hi] = step.rng || [0, step.arr.length - 1];
    step.arr.forEach((v, k) => {
      const c = h('div', 'sort-cell');
      if (k && starts.has(k)) c.classList.add('gap');
      if (step.rng && (k < lo || k > hi)) c.classList.add('out');
      else if (step.runs && step.rng && !step.final) c.classList.add('run');
      if (fixed.has(k) && !step.runs) c.classList.add('fixed');
      if (step.piv === k) c.classList.add('piv');
      if (cmp.has(k)) c.classList.add('cmp');
      if (sw.has(k)) c.classList.add('sw');
      c.append(h('b', null, v));
      if (step.idx) c.append(h('small', null, k));
      row.append(c);
    });
    return row;
  }

  function key(step, alg) {
    const items = [];
    if (step.cmp && step.cmp.length) items.push(['cmp', 'compared']);
    if (step.sw && step.sw.length) items.push(['sw', 'swapped']);
    if (step.piv != null) items.push(['piv', alg === 'selection' ? 'smallest so far' : 'pivot']);
    if (step.runs && step.rng && !step.final) items.push(['run', 'merged here']);
    if ((step.fixed || []).length && !step.runs && !step.final) items.push(['fixed', alg === 'insertion' ? 'sorted so far' : 'in its final place']);
    if (!items.length) return null;
    const k = h('p', 'sort-key');
    items.forEach(([c, t]) => { const s = h('span'); s.append(h('i', 'k-' + c), t); k.append(s); });
    return k;
  }

  return {
    'sort-trace': (s, data, step, i) => {
      const out = [h('p', 'steps-time', step.final ? 'Finished' : i === 0 ? 'Start' : 'Step ' + i), cells(step)];
      const k = key(step, s.alg);
      if (k) out.push(k);
      out.push(h('p', 'steps-ready', `Comparisons so far: ${step.comps}` + (step.swaps ? ` · swaps: ${step.swaps}` : '')));
      return out;
    },
  };
});
