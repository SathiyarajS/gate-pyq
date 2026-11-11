'use strict';
// "Step through it" renderer: Banker's algorithm and deadlock detection (Allocation/Max/Need table and Work).
// Loaded on demand by assets/steps.js; the data comes from scripts/animations/banker.py (checked against the answer at build time).
window.gateStepsRegister(({h, css}) => {
  css(`
.bank-table th:first-child{min-width:0}
.bank-table td.v{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:.8rem;letter-spacing:-.02em}
.bank-table td.st{font-size:.75rem;font-weight:650;color:var(--muted)}
.bank-table tr.is-running td.st{color:var(--accent)}
.bank-table tr.is-waits td.st{color:var(--s1)}
.bank-table tr.is-done td{color:var(--muted)}.bank-table tr.is-done td.st{font-weight:400}
.bank-table tr.is-gone td{color:var(--muted);text-decoration:line-through}.bank-table tr.is-gone td.st{text-decoration:none}
.bank-table tr.is-asks td{background:color-mix(in oklab,var(--s0) 12%,transparent)}
.bank-work{font-size:.88rem;margin:4px 0 2px}.bank-work b{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:.85rem}
.bank-work .arrow{color:var(--accent);font-weight:700}
`);

  const vec = v => v.length > 1 ? '(' + v.join(', ') + ')' : String(v[0]);
  const vcompact = v => v.length > 1 ? '(' + v.join(',') + ')' : String(v[0]);
  const STATUS = {finishes: 'finishes', waits: 'must wait', done: 'done', aborted: 'aborted', asks: 'asks', '': ''};

  function table(s, step) {
    const t = h('table', 'steps-table bank-table'), head = t.createTHead().insertRow(), body = t.createTBody();
    s.cols.forEach(c => head.append(h('th', null, c)));
    step.rows.forEach(([p, alloc, max, need, status]) => {
      const tr = body.insertRow();
      tr.insertCell().textContent = p;
      [alloc].concat(max ? [max] : [], [need]).forEach(v => { const td = tr.insertCell(); td.className = 'v'; td.textContent = vcompact(v); });
      const st = tr.insertCell(); st.className = 'st'; st.textContent = STATUS[status];
      tr.className = {finishes: 'is-running', waits: 'is-waits', done: 'is-done', aborted: 'is-gone', asks: 'is-asks'}[status] || '';
    });
    const w = h('div', 'steps-table-wrap'); w.append(t);
    return w;
  }

  return {
    banker: (s, data, step) => {
      const work = h('p', 'bank-work');
      work.append((step.final ? 'Work at the end' : step.head === 'Start' || /^Abort|asks/.test(step.head) ? 'Available' : 'Work') + ' = ', h('b', null, vec(step.work)));
      if (step.next) work.append(' ', h('span', 'arrow', '→'), ' ', h('b', null, vec(step.next)));
      return [h('p', 'steps-time', step.final ? 'Finished' : step.head), h('p', 'steps-policy', 'Resources: ' + data.resources.join(', ')), table(s, step), work];
    },
  };
});
