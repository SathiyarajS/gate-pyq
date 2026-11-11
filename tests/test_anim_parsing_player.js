'use strict';
// DOM-contract unit test, not a substitute for Chromium layout/screenshot review.
// Pipe the JSON result of parse_animation for each retained spec into this script.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
class Element {
  constructor(tag) { this.tag = tag; this.children = []; this.textContent = ''; }
  append(...children) { this.children.push(...children); }
  setAttribute(name, value) { this[name] = value; }
  child(tag) { const e = new Element(tag); this.append(e); return e; }
  createTHead() { return this.child('thead'); }
  createTBody() { return this.child('tbody'); }
  insertRow() { return this.child('tr'); }
  insertCell() { return this.child('td'); }
}
let renderers;
const h = (tag, cls, text) => {
  const e = new Element(tag);
  e.className = cls || '';
  e.textContent = text == null ? '' : String(text);
  return e;
};
vm.runInNewContext(fs.readFileSync(path.join(__dirname, '../site-static/steps/parsing.js'), 'utf8'), {
  window: {gateStepsRegister: factory => { renderers = factory({h, css: () => {}}); }},
});
const data = JSON.parse(fs.readFileSync(0, 'utf8'));
let count = 0;
for (const [qid, result] of Object.entries(data)) {
  assert.equal(typeof renderers[result.kind], 'function', qid);
  for (const schedule of result.schedules) {
    schedule.steps.forEach((step, index) => {
      const nodes = renderers[result.kind](schedule, result, step, index, 390);
      assert(nodes.length >= 3, `${qid} ${index}: missing view`);
      assert(nodes.every(node => node instanceof Element));
      count++;
    });
  }
}
console.log(`Parsing renderer DOM-contract passed for ${Object.keys(data).length} entries and ${count} steps. Layout not tested.`);
