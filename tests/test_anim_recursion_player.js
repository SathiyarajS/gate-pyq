'use strict';
// DOM-shape smoke test, not a substitute for real Chromium layout review.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const {execFileSync} = require('node:child_process');
const root = path.resolve(__dirname, '..');
const payload = JSON.parse(execFileSync(process.env.PYTHON || 'python', ['-c', `
import json,sys
sys.path.insert(0,'scripts')
from animations.recursion import recursion_animation
specs=json.load(open('data/animations/recursion.json'))['questions']
print(json.dumps({qid:recursion_animation(qid,s) for qid,s in specs.items()}))
`], {cwd: root, maxBuffer: 8 * 1024 * 1024}));
function element(tag, attrs, text) {
  return {tag, attrs, text, children: [], append(...children) {
    assert(children.every(c => c !== undefined && c !== null));
    this.children.push(...children);
  }};
}
let renderers, styles;
vm.runInNewContext(fs.readFileSync(path.join(root, 'site-static/steps/recursion.js'), 'utf8'), {
  window: {gateStepsRegister(register) {
    renderers = register({el: element, h: (tag, cls, text) => element(tag, {class: cls}, text), css: s => {styles = s;}});
  }}, document: {createTextNode: text => ({text})},
});
assert(styles.includes('overflow-x:auto'));
let frames = 0;
for (const data of Object.values(payload)) {
  for (const schedule of data.schedules) {
    for (const width of [280, 390, 900]) {
      schedule.steps.forEach((step, i) => {
        const nodes = renderers[data.kind](schedule, data, step, i, width);
        assert(nodes.length >= 2);
        assert(!JSON.stringify(nodes).includes('NaN'));
        frames++;
      });
    }
  }
}
console.log(`Recursion renderer DOM smoke passed: ${frames} frames. Browser geometry remains a separate check.`);
