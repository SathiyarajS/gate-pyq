const fs=require('fs'),vm=require('vm'),assert=require('assert');
const document={documentElement:{classList:{add(){}},dataset:{}},body:{dataset:{base:'../../../',subject:'01-digital-logic'}},querySelector(){return null},querySelectorAll(){return []},addEventListener(){}};
const context={window:{},document,URL,location:{href:'http://localhost/gate-pyq/01-digital-logic/page/2/'},addEventListener(){},get localStorage(){throw Error('Storage blocked')}};
vm.createContext(context);vm.runInContext(fs.readFileSync('site-static/app.js','utf8'),context);
const tests=[['B','B','MCQ',true],['B','A','MCQ',false],['E','E','MCQ',true],['B;C','C B','MSQ',true],['B;C','B','MSQ',false],['2.4 to 2.6','2.5','NAT',true],['2.4 to 2.6','3','NAT',false],['C OR D','C','MCQ',null],['MTA','B','MCQ',null],['3.7 to 3.8 OR 4.0 to 4.1','4','NAT',null],['','B','MCQ',null],['If x then B','B','MCQ',null]];
for(const [k,i,t,e]of tests)assert.strictEqual(context.check(k,i,t),e);
assert.equal(vm.runInContext('base.href',context),'http://localhost/gate-pyq/');
assert.equal(vm.runInContext("new URL('../q/CS-1991-Q1/'.slice(3),base).href",context),'http://localhost/gate-pyq/q/CS-1991-Q1/');
console.log('12 practice cases, blocked-storage initialization and nested base-link checks passed. No browser interaction tested.');

// Exercise the production math wrapper with the real pinned KaTeX parser.
const katex=require('katex');
context.window.katex={render(tex,el,opts){el.html=katex.renderToString(tex,opts)}};
function mathNode(tex){return {dataset:{math:tex,display:'false'},textContent:'\\('+tex+'\\)',classList:{add(){}}};}
const good=mathNode('x^2+1'),bad=mathNode('\\href{https://example.org}{click}'),unknown=mathNode('\\notacommand{x}');
context.renderMath({querySelectorAll(){return [good,bad,unknown]}});
assert.equal(good.dataset.rendered,'true');assert(good.html.includes('katex'));
for(const n of [bad,unknown]){assert.equal(n.dataset.rendered,'unsupported');assert(n.textContent.includes(n.dataset.math));assert(!n.html);}
console.log('Real KaTeX parsing and safe original-text fallback passed; no browser layout claim.');
