'use strict';

window.gateStepsRegister(({h, css}) => {
  css(`
.ctrace-layout{display:grid;grid-template-columns:minmax(0,1fr);gap:6px 16px;align-items:start}
@media(min-width:900px){.ctrace-layout:has(.ctrace-state){grid-template-columns:minmax(0,1fr) minmax(0,1fr)}}
.ctrace-code{margin:2px 0 6px;padding:6px 0;background:var(--panel);font-size:.8rem;line-height:1.45}
.ctrace-code span{display:block;padding:0 10px;white-space:pre-wrap;overflow-wrap:anywhere}
.ctrace-code span[aria-current=true]{background:color-mix(in oklab,var(--accent) 18%,transparent);box-shadow:inset 3px 0 0 var(--accent)}
.ctrace-vars{width:100%}
.ctrace-vars th:first-child{min-width:0;vertical-align:top}
.ctrace-vars th,.ctrace-vars td{white-space:normal;overflow-wrap:anywhere}
.ctrace-vars tbody th{color:var(--ink)}
.ctrace-vars th small,.ctrace-vars .ctrace-shadow{display:block;font-weight:400;color:var(--muted)}
.ctrace-array{display:flex;flex-wrap:wrap;gap:3px;margin:3px 0}
.ctrace-cell{display:inline-grid;text-align:center;min-width:1.65em;padding:1px 4px;border:1px solid var(--line);border-radius:3px;background:var(--panel)}
.ctrace-cell small{color:var(--muted);line-height:1.2}
.ctrace-cell.is-read{border-color:var(--accent)}
.ctrace-cell.is-written{border-color:var(--accent);background:color-mix(in oklab,var(--accent) 18%,var(--panel));font-weight:700}
.ctrace-output{margin:2px 0 6px;padding:4px 8px;border:1px solid var(--line);background:var(--panel);font-size:.85rem;white-space:pre-wrap;overflow-wrap:anywhere}
.ctrace-output mark{background:color-mix(in oklab,var(--accent) 18%,var(--panel));color:var(--ink);font-weight:700}
`);

  function listing(lines, active) {
    const pre = h('pre', 'ctrace-code');
    const code = h('code');
    lines.forEach((line, index) => {
      const row = h('span', null, line || ' ');
      if (index === active) row.setAttribute('aria-current', 'true');
      code.append(row);
    });
    pre.append(code);
    return pre;
  }

  function arrayValue(row) {
    const value = h('div');
    if (row.s != null) value.append(h('code', null, row.s));
    for (const {p: name, c: cells} of row.rows) {
      if (name !== row.n) value.append(h('code', null, name));
      const group = h('div', 'ctrace-array');
      for (const [index, content, access] of cells) {
        const state = access === 'w' ? ' is-written' : access === 'r' ? ' is-read' : '';
        const cell = h('span', 'ctrace-cell' + state);
        cell.append(h('small', null, index), h('code', null, content === ' ' ? '␠' : content));
        group.append(cell);
      }
      value.append(group);
    }
    if (row.more) value.append(h('small', 'ctrace-shadow', `+${row.more} more cells`));
    return value;
  }

  function variables(group) {
    const wrap = h('div', 'steps-table-wrap');
    const table = h('table', 'steps-table ctrace-vars');
    const header = table.createTHead().insertRow();
    header.append(h('th', null, group.title), h('th', null, 'Value'));
    const body = table.createTBody();
    for (const row of group.rows) {
      const tr = body.insertRow();
      if (row.w) tr.className = 'is-running';
      const name = h('th', null, row.n);
      name.scope = 'row';
      name.append(h('small', null, row.t));
      if (row.h) name.append(h('small', null, 'Shadowed'));
      const value = h('td');
      value.append(row.rows ? arrayValue(row) : h('code', null, row.v));
      tr.append(name, value);
    }
    wrap.append(table);
    return wrap;
  }

  function output(text, appended) {
    const section = h('div');
    const pre = h('pre', 'ctrace-output');
    if (appended) {
      pre.textContent = text.slice(0, -appended);
      pre.append(h('mark', null, text.slice(-appended)));
    } else {
      pre.textContent = text;
    }
    section.append(h('div', 'steps-time', 'Output'), pre);
    return section;
  }

  function expressions(work) {
    const table = h('table', 'steps-table ctrace-vars');
    table.createTHead().insertRow().append(h('th', null, 'Expression'), h('th', null, 'Value'));
    const body = table.createTBody();
    for (const [expression, value] of work) {
      const row = body.insertRow();
      row.insertCell().append(h('code', null, expression));
      row.insertCell().append(h('code', null, value));
    }
    return table;
  }

  return {
    'c-trace': (_schedule, data, step) => {
      const layout = h('div', 'ctrace-layout');
      layout.append(listing(data.code, step.line));
      const state = h('div', 'ctrace-state');
      for (const group of step.vars) {
        if (group.rows.length) state.append(variables(group));
      }
      if (step.work) state.append(expressions(step.work));
      if (step.out) state.append(output(step.out, step.new));
      if (state.childElementCount) layout.append(state);
      return [layout];
    },
  };
});
