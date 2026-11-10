// Real Pagefind WASM/index test with local file-backed fetch, not browser QA.
import fs from 'node:fs/promises';
import path from 'node:path';
import os from 'node:os';
import assert from 'node:assert/strict';
import {fileURLToPath,pathToFileURL} from 'node:url';
const repo=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const root=path.resolve(repo,process.argv[2]||'_site');
globalThis.window=globalThis;
globalThis.document={currentScript:null,querySelector:()=>null,documentElement:{lang:'en'}};
globalThis.location=new URL('http://local.test/gate-pyq/');
globalThis.fetch=async(input)=>{
 const u=new URL(typeof input==='string'?input:input.url,location);
 const p=path.resolve(root,decodeURIComponent(u.pathname).replace(/^\/gate-pyq\//,''));
 if(!p.startsWith(root+path.sep))return new Response('',{status:403});
 try{return new Response(await fs.readFile(p),{headers:{'Content-Type':p.endsWith('.wasm')?'application/wasm':'application/octet-stream'}})}catch{return new Response('',{status:404})}
};
const tmp=await fs.mkdtemp(path.join(os.tmpdir(),'gate-search-review-'));
try{
 const module=path.join(tmp,'pagefind.mjs');await fs.copyFile(path.join(root,'pagefind/pagefind.js'),module);
 const pf=await import(pathToFileURL(module));await pf.options({basePath:'/gate-pyq/pagefind/',baseUrl:'/gate-pyq/'});
 const all=await pf.search('cache'),filtered=await pf.search('cache',{filters:{year:'2026'}});
 assert(all.results.length>0);assert(filtered.results.length>0);assert(filtered.results.length<=all.results.length);
 for(const hit of filtered.results){const r=await hit.data();assert(r.meta.question_id);assert(r.filters.year.includes('2026'));assert(r.url.startsWith('/gate-pyq/search-docs/'));}
 const data=JSON.parse(await fs.readFile(path.join(root,'search.json'),'utf8'));assert.equal(data.length,3406);assert.equal(new Set(data.map(q=>q.id)).size,3406);
 console.log(`PASS: 3406 unique search records, real WASM search (${all.results.length} cache results), year filter (${filtered.results.length}), nested-base URLs. Browser interaction/layout not tested.`);
}finally{await fs.rm(tmp,{recursive:true,force:true})}
