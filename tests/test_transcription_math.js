// Static KaTeX regression; this does not replace browser or visual review.
'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const katex = require('../node_modules/katex');
const source = fs.readFileSync('site-static/app.js', 'utf8');
const start = source.indexOf('function renderMath(');
const end = source.indexOf('\nfunction hydrate(', start);
assert(start >= 0 && end > start);
function run(math, display = false) {
  const element = {textContent: '$' + math + '$', dataset: {math, display: String(display)}, classList: {add(){}}};
  const root = {querySelectorAll(){return [element];}};
  const context = {document:root, window:{katex:{render(input, el, options){
    assert.equal(options.trust, false);
    assert.equal(options.strict, 'error');
    el.output = katex.renderToString(input, options);
  }}}};
  vm.runInNewContext(source.slice(start,end) + '\nrenderMath();', context);
  return element;
}
for (const expression of ['x^2 + y^2', '\\frac{1}{2}', '\\overline{AB}', '\\begin{array}{cc}1&2\\\\3&4\\end{array}', '\\Theta(n \\log n)']) {
  const result = run(expression);
  assert.equal(result.dataset.rendered, 'true');
  assert(result.output.includes('katex-mathml'));
}
assert(run('x^2', true).output.includes('katex-display'));
for (const expression of ['\\href{https://example.com}{x}', '\\htmlStyle{color:red}{x}', '\\includegraphics{https://example.com/x}', '\\notARealCommand']) {
  const result = run(expression);
  assert.equal(result.dataset.rendered, 'unsupported');
  assert.equal(result.textContent, '$' + expression + '$');
}
console.log('KaTeX static regression passed: inline/display math and safe unsupported fallback.');
