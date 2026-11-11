'use strict';
// Renderer contract test without a browser. Browser/layout QA remains separate.
// Usage: node tests/test_anim_automata_player.js [precomputed-results.json]
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
class Node {
  constructor(tag, cls, text) { this.tag = tag; this.cls = cls; this.text = text; this.children = []; }
  append(...nodes) { this.children.push(...nodes); }
}
let renderers, styles='';
vm.runInNewContext(fs.readFileSync('site-static/steps/automata.js','utf8'), {
  window: {gateStepsRegister: make => {renderers=make({
    h: (tag, cls, text) => new Node(tag, cls, text), css: text => { styles += text; }
  });}}
});
assert.equal(Object.keys(renderers).length,7);
assert.match(styles,/th:first-child\s*\{min-width:0\}/);
const payload = process.argv[2] ? fs.readFileSync(process.argv[2], 'utf8') :
  require('node:child_process').execFileSync('python3', ['-c', `
import json, sys
sys.path.insert(0, 'scripts')
from animations import automata as a
specs = json.load(open('data/animations/automata.json'))['questions']
print(json.dumps({q: a.KINDS[s['kind']](q, s) for q, s in specs.items()}))
`], {encoding:'utf8', maxBuffer:16*1024*1024});
const results=JSON.parse(payload);
let count=0;
for(const data of Object.values(results)) for(const schedule of data.schedules) {
  for(const width of [390,900]) for(const [i, step] of schedule.steps.entries()) {
    const nodes=renderers[data.kind](schedule,data,step,i,width);
    assert.equal(nodes.length,1);assert.equal(nodes[0].cls,'fa-view');
    const strings=[];
    function walk(n){if(n.text!=null)strings.push(String(n.text));n.children.forEach(walk);}
    walk(nodes[0]);assert(strings.length>0);assert(!strings.includes('[object Object]'));
    for(const name of schedule.fa.states)assert(strings.some(t=>t.includes(name)));
    count++;
  }
}
console.log(`Automata renderer contract passed: ${count} step/width renders.`);
