'use strict';
// "Step through it" renderer: functional dependencies (FD list, closure, keys, normal forms, decompositions).
// Loaded on demand by assets/steps.js; the data comes from scripts/animations/fd.py (checked against the answer at build time).
window.gateStepsRegister(({h, css}) => {
  css(`
.fd-list{display:flex;flex-wrap:wrap;gap:6px;list-style:none;margin:4px 0 8px;padding:0}
.fd-list li{margin:0;padding:2px 8px;border:1px solid var(--line);border-radius:4px;background:var(--panel);font-size:.85rem;white-space:nowrap;font-variant-numeric:tabular-nums}
.fd-list li.used{border-color:var(--s2)}
.fd-list li.used::before{content:"✓ ";color:var(--s2);font-weight:700}
.fd-list li.on{border-color:var(--accent);background:color-mix(in oklab,var(--accent) 16%,var(--panel));font-weight:700}
.fd-list li.bad{border-color:var(--s1);background:color-mix(in oklab,var(--s1) 18%,var(--panel));font-weight:700}
.fd-list li.bad::before{content:"✗ ";color:var(--s1)}
.fd-list li.gone{text-decoration:line-through;color:var(--muted);border-style:dashed}
.fd-set{display:flex;flex-wrap:wrap;align-items:center;gap:4px;margin:2px 0 8px}
.fd-set .fd-lab{font-weight:650;font-size:.85rem;margin-right:4px}
.fd-set .fd-a{min-width:1.9em;padding:2px 6px;text-align:center;border:1px dashed var(--line);border-radius:4px;font-size:.85rem;color:var(--muted)}
.fd-set .fd-a.in{border:1px solid var(--s0);background:color-mix(in oklab,var(--s0) 14%,var(--panel));color:var(--ink);font-weight:650}
.fd-set .fd-a.new{border-color:var(--accent);background:color-mix(in oklab,var(--accent) 24%,var(--panel));font-weight:800}
.fd-table td{white-space:normal;min-width:2.2em;overflow-wrap:normal}
.fd-table th{white-space:nowrap}
.fd-list li,.fd-set .fd-a,.fd-tab td{overflow-wrap:normal}
.fd-tab td,.fd-tab th{text-align:center}
.fd-tab td.fd-av{font-weight:750;color:var(--ink)}
.fd-tab td.fd-bv{color:var(--muted)}
.fd-tab td.is-new{background:color-mix(in oklab,var(--accent) 30%,var(--bg));color:var(--ink);font-weight:800;box-shadow:inset 0 0 0 2px var(--accent)}
`);

  function fdList(s, step) {
    const ul = h('ul', 'fd-list'), on = step.fire || [], used = step.used || [], bad = step.bad || [], gone = step.gone || [];
    ul.setAttribute('aria-label', 'Functional dependencies');
    (step.fdlist || s.fds).forEach((text, i) => {
      const li = h('li', gone.includes(i) ? 'gone' : bad.includes(i) ? 'bad' : on.includes(i) ? 'on' : used.includes(i) ? 'used' : null, text);
      ul.append(li);
    });
    return ul;
  }

  function closureStrip(s, set) {
    const d = h('div', 'fd-set');
    d.setAttribute('aria-label', `${set.label}: ${set.have.join(', ')}`);
    d.append(h('span', 'fd-lab', set.label + ' ='));
    s.attrs.forEach(a => d.append(h('span', 'fd-a' + (set.have.includes(a) ? ' in' : '') + (set.new.includes(a) ? ' new' : ''), a)));
    return d;
  }

  function table(t) {
    const tab = h('table', 'steps-table fd-table'), head = tab.createTHead().insertRow(), body = tab.createTBody();
    t.cols.forEach(c => head.append(h('th', null, c)));
    t.rows.forEach((r, k) => {
      const row = body.insertRow();
      r.forEach(v => { row.insertCell().textContent = v; });
      if ((t.hi || []).includes(k)) row.className = 'is-running';
    });
    const w = h('div', 'steps-table-wrap'); w.append(tab); return w;
  }

  // The chase: one row per relation, a = known value, b = unknown.
  function tableau(t) {
    const tab = h('table', 'steps-table steps-grid fd-tab'), head = tab.createTHead().insertRow(), body = tab.createTBody();
    head.append(h('th', null, 'Relation'));
    t.cols.forEach(c => head.append(h('th', null, c)));
    const fresh = new Set(t.new.map(([r, c]) => r + ':' + c));
    t.cells.forEach((cells, r) => {
      const row = body.insertRow();
      row.insertCell().textContent = t.rows[r];
      cells.forEach((v, c) => {
        const td = row.insertCell(); td.textContent = v;
        td.className = (v === 'a' ? 'fd-av' : 'fd-bv') + (fresh.has(r + ':' + c) ? ' is-new' : '');
      });
      if (cells.every(v => v === 'a')) row.className = 'is-running';
    });
    const w = h('div', 'steps-table-wrap'); w.append(tab); return w;
  }

  return {
    fd: (s, data, step) => {
      const out = [h('p', 'steps-time', step.head), fdList(s, step)];
      if (step.set) out.push(closureStrip(s, step.set));
      if (step.chips) { const d = h('div', 'fd-set'); d.append(h('span', 'fd-lab', step.chips.label)); step.chips.items.forEach(x => d.append(h('span', 'fd-a in', x))); out.push(d); }
      if (step.tableau) out.push(tableau(step.tableau));
      if (step.table) out.push(table(step.table));
      return out;
    },
  };
});
