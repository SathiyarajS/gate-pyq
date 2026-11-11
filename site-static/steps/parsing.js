'use strict';
// "Step through it" renderer: compiler parsing (FIRST/FOLLOW, LL(1) tables, LR item sets,
// shift-reduce and predictive traces, derivations). Every step shows the grammar with the
// production in use highlighted, then one view: sets, ll1, lr, sr or derive.
// Loaded on demand by assets/steps.js; the data comes from scripts/animations/parsing.py (checked against the answer at build time).
window.gateStepsRegister(({h, css}) => {
  css(`
.prs-sets th:first-child,.prs-grid th:first-child,.prs-trace th:first-child{min-width:0}
.prs-gram{display:flex;flex-wrap:wrap;gap:4px 6px;list-style:none;margin:2px 0 8px;padding:0}
.prs-gram li{margin:0;padding:1px 7px;border:1px solid var(--line);border-radius:4px;background:var(--panel);font-size:.82rem;white-space:normal;overflow-wrap:anywhere;max-width:100%}
.prs-gram li.on{border-color:var(--accent);background:color-mix(in oklab,var(--accent) 18%,var(--panel));font-weight:700}
.prs-set{display:inline-flex;flex-wrap:wrap;gap:0;align-items:center}
.prs-set b{font-weight:400;color:var(--muted)}
.prs-sym{display:inline-block;min-width:1.2em;padding:0 4px;border-radius:3px;text-align:center;font-variant-numeric:tabular-nums}
.prs-sym.new{background:color-mix(in oklab,var(--accent) 26%,var(--panel));font-weight:800;box-shadow:inset 0 0 0 1px var(--accent)}
.prs-sets td{white-space:normal}
.prs-sets th:first-child,.prs-sets td:first-child{font-weight:650}
.prs-grid td{white-space:nowrap;font-size:.78rem;vertical-align:top}
.prs-grid td div{line-height:1.35}
.prs-grid td.is-new{background:color-mix(in oklab,var(--accent) 14%,var(--bg))}
.prs-grid td.bad{background:color-mix(in oklab,var(--s1) 22%,var(--bg));font-weight:700}
.prs-grid td.blank{color:var(--muted)}
.prs-small{font-size:.78rem;margin-top:4px}
.prs-chips{display:flex;flex-wrap:wrap;gap:3px}
.prs-chip{padding:0 5px;border:1px solid var(--line);border-radius:3px;background:var(--panel);font-size:.8rem}
.prs-none{color:var(--muted)}
.prs-cards{display:flex;flex-wrap:wrap;gap:6px;align-items:flex-start;margin:2px 0 6px}
.prs-card{border:1px solid var(--line);border-radius:6px;background:var(--panel);padding:3px 7px 4px;font-size:.78rem;line-height:1.4;min-width:0;max-width:100%}
.prs-card.cur{border:2px solid var(--accent);background:color-mix(in oklab,var(--accent) 10%,var(--panel))}
.prs-card.src{border:2px dashed var(--accent)}
.prs-card.bad{border-color:var(--s1);box-shadow:inset 0 0 0 1px var(--s1)}
.prs-card h4{margin:0;font-size:.8rem;font-weight:800;display:flex;gap:6px;align-items:baseline;flex-wrap:wrap}
.prs-card h4 small{font-weight:650;color:var(--s1)}
.prs-card ul{list-style:none;margin:0;padding:0}
.prs-card li{margin:0;white-space:normal;overflow-wrap:anywhere;max-width:100%}
.prs-card li.k{font-weight:650}
.prs-card li.more{color:var(--muted);font-size:.74rem}
.prs-card .go{color:var(--muted);font-size:.72rem;margin-top:1px;white-space:normal}
.prs-trace td{font-variant-numeric:tabular-nums}
.prs-trace td:first-child{text-align:right}
.prs-trace td.in{color:var(--muted)}
.prs-trace th{white-space:nowrap}
.prs-trace td:nth-child(3){white-space:normal;min-width:6.5em}
.prs-trace.top td:first-child{text-align:left}
.prs-stk{display:inline-flex;gap:3px;flex-wrap:nowrap;align-items:baseline}
.prs-stk span sub{font-size:.68rem;color:var(--accent);font-weight:700;margin-left:1px}
.prs-stk .act{color:var(--muted);font-size:.74rem}
.prs-der{list-style:none;margin:2px 0 6px;padding:0;font-size:.95rem;line-height:1.7}
.prs-der li{margin:0;white-space:nowrap}
.prs-der li .arr{display:inline-block;width:1.4em;color:var(--muted)}
.prs-der li.last{font-weight:650}
.prs-der .hi{text-decoration:underline;text-decoration-color:var(--accent);text-decoration-thickness:2px;text-underline-offset:3px;font-weight:800}
.prs-der .new{background:color-mix(in oklab,var(--accent) 20%,var(--panel));border-radius:3px}
.prs-der .eps{color:var(--muted)}
`);

  const wrap = node => { const w = h('div', 'steps-table-wrap'); w.append(node); return w; };

  function grammar(s, step) {
    const ul = h('ul', 'prs-gram');
    ul.setAttribute('aria-label', 'Grammar');
    s.grammar.forEach((p, i) => ul.append(h('li', step.rule === i ? 'on' : null, p)));
    return ul;
  }

  function set(items, fresh) {
    const span = h('span', 'prs-set');
    span.append(h('b', null, '{'));
    items.forEach((x, k) => {
      span.append(h('span', 'prs-sym' + (fresh && fresh.includes(x) ? ' new' : ''), x));
      if (k < items.length - 1) span.append(h('b', null, ', '));
    });
    span.append(h('b', null, '}'));
    return span;
  }

  function setsTable(rows, step, small) {
    const tab = h('table', 'steps-table prs-sets' + (small ? ' prs-small' : '')), head = tab.createTHead().insertRow(), body = tab.createTBody();
    ['', 'FIRST', 'FOLLOW'].forEach(c => head.append(h('th', null, c)));
    const nf = (step && step.new) || {first: {}, follow: {}};
    const followOn = !step || step.head !== 'FIRST sets';
    rows.forEach(([a, first, follow]) => {
      const row = body.insertRow();
      row.insertCell().textContent = a;
      row.insertCell().append(set(first, nf.first[a]));
      const c = row.insertCell();
      if (followOn) c.append(set(follow, nf.follow[a])); else c.textContent = '';
      if (nf.first[a] || nf.follow[a]) row.className = 'is-running';
    });
    return wrap(tab);
  }

  function grid(g, step) {
    const tab = h('table', 'steps-table steps-grid prs-grid'), head = tab.createTHead().insertRow(), body = tab.createTBody();
    head.append(h('th', null, 'M'));
    g.cols.forEach(c => head.append(h('th', null, c)));
    const fresh = new Set((g.new || []).map(([r, c]) => r + ':' + c)), bad = new Set((step.bad || []).map(([r, c]) => r + ':' + c));
    g.rows.forEach((a, r) => {
      const row = body.insertRow();
      row.insertCell().textContent = a;
      g.cells[r].forEach((ps, c) => {
        const td = row.insertCell(), key = r + ':' + c;
        if (!ps.length) { td.textContent = ''; }
        ps.forEach(p => td.append(h('div', null, p)));
        td.className = (bad.has(key) ? 'bad' : '') + (fresh.has(key) ? ' is-new' : '');
      });
    });
    return wrap(tab);
  }

  function cards(s, step) {
    const box = h('div', 'prs-cards');
    (step.cards || []).forEach(ref => {
      const c = s.cards[ref.c], d = h('div', 'prs-card' + (ref.cur ? ' cur' : '') + (ref.src ? ' src' : '') + (ref.bad ? ' bad' : ''));
      const t = h('h4', null, c.name);
      if (ref.bad) t.append(h('small', null, 'conflict on ' + ref.bad.join(', ')));
      d.append(t);
      const ul = h('ul');
      const lines = ref.full ? c.items : c.items.slice(0, c.k);
      lines.forEach((x, k) => ul.append(h('li', k < c.k && ref.full && c.items.length > c.k ? 'k' : null, x)));
      if (!ref.full && c.items.length > c.k) ul.append(h('li', 'more', `+ ${c.items.length - c.k} closure item${c.items.length - c.k > 1 ? 's' : ''}`));
      d.append(ul);
      if (c.go.length) d.append(h('div', 'go', c.go.map(([x, n]) => `${x} → ${n}`).join('   ')));
      box.append(d);
    });
    return box;
  }

  function stackCell(items, top) {
    const span = h('span', 'prs-stk');
    const list = top ? items : [['$', null]].concat(items);
    list.forEach(([x, v]) => {
      const e = h('span', x[0] === '{' && x.length > 2 ? 'act' : null, x);
      if (v != null) e.append(h('sub', null, v));
      span.append(e);
    });
    return span;
  }

  function trace(s, step) {
    const top = !!step.top;
    const tab = h('table', 'steps-table prs-trace' + (top ? ' top' : '')), head = tab.createTHead().insertRow(), body = tab.createTBody();
    s.cols.forEach((c, k) => head.append(h('th', null, k === 0 && top ? 'Stack (top first)' : c)));
    s.rows.slice(0, step.n).forEach((r, k) => {
      const row = body.insertRow();
      row.insertCell().append(stackCell(r.stack, top));
      const inp = row.insertCell(); inp.className = 'in'; inp.textContent = r.input.join(' ');
      row.insertCell().textContent = r.action;
      if (s.cols.length > 3) row.insertCell().textContent = r.out || '';
      if (k === step.n - 1) row.className = 'is-running';
    });
    return wrap(tab);
  }

  function derive(step, spaced) {
    const ol = h('ol', 'prs-der');
    step.lines.forEach((l, k) => {
      const li = h('li', k === step.lines.length - 1 ? 'last' : null);
      li.append(h('span', 'arr', k ? '⇒' : ''));
      const hi = new Set(l.hi), nw = new Set(l.new);
      if (!l.syms.length) li.append(h('span', 'eps' + (k ? ' new' : ''), 'ε'));
      l.syms.forEach((x, i) => {
        if (i && spaced) li.append(' ');
        li.append(h('span', (hi.has(i) && k === step.lines.length - 2 ? 'hi' : '') + (nw.has(i) && k === step.lines.length - 1 ? ' new' : ''), x));
      });
      ol.append(li);
    });
    return wrap(ol);
  }

  // What each nonterminal derives among the pieces of a string that is not generated.
  function pieces(step) {
    const tab = h('table', 'steps-table prs-sets'), head = tab.createTHead().insertRow(), body = tab.createTBody();
    ['', 'Derives these pieces'].forEach(c => head.append(h('th', null, c)));
    step.rows.forEach(([a, ps]) => {
      const row = body.insertRow();
      row.insertCell().textContent = a;
      const c = row.insertCell(), box = h('span', 'prs-chips');
      if (!ps.length) box.append(h('span', 'prs-none', 'none'));
      ps.forEach(p => box.append(h('span', 'prs-chip', p)));
      c.append(box);
    });
    return wrap(tab);
  }

  function view(s, data, step) {
    const out = [h('p', 'steps-time', step.head), grammar(s, step)];
    if (step.view === 'sets') out.push(setsTable(step.sets, step));
    else if (step.view === 'll1') { out.push(grid(step.grid, step)); if (s.sets) out.push(setsTable(s.sets, null, true)); }
    else if (step.view === 'lr') out.push(cards(s, step));
    else if (step.view === 'sr') out.push(trace(s, step));
    else if (step.view === 'derive') out.push(derive(step, s.spaced));
    else if (step.view === 'pieces') out.push(pieces(step));
    return out;
  }

  return {'parse-sets': view, 'parse-ll1': view, 'parse-lr': view, 'parse-sr': view, 'parse-ll': view, 'parse-trees': view};
});
