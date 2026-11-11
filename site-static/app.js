'use strict';
document.documentElement.classList.add('js');
const read=(key,fallback)=>{try{return JSON.parse(localStorage.getItem(key))??fallback;}catch{return fallback;}};
const write=(key,value)=>{try{localStorage.setItem(key,JSON.stringify(value));}catch{}};
let state=read('gate-practice-v1',{});if(!state||typeof state!=='object'||Array.isArray(state))state={};
const theme=read('gate-theme',null);if(['dark','light'].includes(theme))document.documentElement.dataset.theme=theme;
document.querySelector('#theme')?.addEventListener('click',()=>{const dark=document.documentElement.dataset.theme?document.documentElement.dataset.theme==='dark':matchMedia('(prefers-color-scheme:dark)').matches;document.documentElement.dataset.theme=dark?'light':'dark';write('gate-theme',dark?'light':'dark');});
const base=new URL(document.body.dataset.base,location.href);
// Offline support (published site only): sw.js keeps the shell, saved subjects and visited pages available without a connection.
if(document.body.dataset.sw&&'serviceWorker' in navigator&&/^https?:$/.test(location.protocol))navigator.serviceWorker.register(new URL('sw.js',base)).catch(()=>{});
function progress(){const el=document.querySelector('.progress');if(el){const s=document.body.dataset.subject;el.textContent=Object.values(state).filter(x=>x&&x.subject===s&&x.attempted).length+' attempted';}}
function renderMath(root=document){if(!window.katex)return;root.querySelectorAll('.math-source:not([data-rendered])').forEach(el=>{const original=el.textContent;try{if(/\\(?:href|url|includegraphics|htmlClass|htmlId|htmlStyle|htmlData)\b/.test(el.dataset.math))throw Error('External or HTML-producing math command is not supported');window.katex.render(el.dataset.math,el,{displayMode:el.dataset.display==='true',throwOnError:true,trust:false,strict:'error',maxExpand:1000,maxSize:20,output:'htmlAndMathml'});el.dataset.rendered='true';}catch{el.textContent=original;el.dataset.rendered='unsupported';el.title='Unsupported mathematical syntax; original text preserved.';el.classList.add('math-unsupported');}});}
function hydrate(){renderMath();document.querySelectorAll('.question[data-id]').forEach(article=>{const s=state[article.dataset.id]||{};const b=article.querySelector('.bookmark');b?.setAttribute('aria-pressed',String(!!s.bookmarked));if(b)b.textContent=s.bookmarked?'Bookmarked':'Bookmark';});progress();}
function save(article,patch){const id=article.dataset.id;state[id]={...state[id],...patch,subject:article.dataset.subject};write('gate-practice-v1',state);hydrate();}
function check(key,input,type){
 // Never infer option counts or parse a conditional derivation as a scoring key.
 if(type==='MCQ'&&/^[A-Z]$/.test(key)&&/^[A-Z]$/.test(input))return input===key;
 if(type==='MSQ'&&/^[A-Z](;[A-Z])*$/.test(key)&&/^[A-Z]([;, ]+[A-Z])*$/.test(input)){const normalize=s=>[...new Set(s.match(/[A-Z]/g))].sort().join('');return normalize(input)===normalize(key);}
 if(type==='NAT'&&input.trim()!==''&&Number.isFinite(Number(input))){const m=key.match(/^(-?\d+(?:\.\d+)?) to (-?\d+(?:\.\d+)?)$/);if(m)return Number(input)>=Number(m[1])&&Number(input)<=Number(m[2]);}
 return null;
}
document.addEventListener('click',async event=>{const b=event.target.closest('button');if(!b)return;const article=b.closest('.question');if(!article)return;
 if(b.classList.contains('bookmark'))save(article,{bookmarked:!(state[article.dataset.id]?.bookmarked)});
 if(b.classList.contains('copy-link')){const url=new URL('q/'+article.dataset.id+'/',base).href;try{await navigator.clipboard.writeText(url);b.textContent='Copied';}catch{prompt('Copy this link',url);}}
 if(b.classList.contains('choice')&&b.classList.contains('multi')){b.setAttribute('aria-pressed',String(b.getAttribute('aria-pressed')!=='true'));return;}
 if(b.classList.contains('choice')||b.classList.contains('check-answer')){
  const type=article.dataset.type,key=article.dataset.key;let input='';
  if(b.classList.contains('choice')){input=b.dataset.choice;article.querySelectorAll('.choice').forEach(c=>{c.classList.remove('picked','right','wrong');c.setAttribute('aria-pressed','false');});b.classList.add('picked');b.setAttribute('aria-pressed','true');}
  else if(type==='MSQ')input=[...article.querySelectorAll('.choice[aria-pressed="true"]')].map(c=>c.dataset.choice).join(';');
  else input=(article.querySelector('.attempt-input')?.value||'').trim().toUpperCase();
  const result=check(key,input,type);article.querySelector('.answer').open=true;
  if(result!==null)article.querySelectorAll('.choice.picked,.choice[aria-pressed="true"]').forEach(c=>c.classList.add(result?'right':'wrong'));
  article.querySelector('.attempt-result').textContent=result===null?(input?'No official key to check against — compare with our answer below.':'Answer shown below.'):(result?(article.dataset.keySource==='derived'?'Correct — matches our answer (no official key located).':'Correct — matches the official key.'):(article.dataset.keySource==='derived'?'Not quite — our answer (no official key located) is shown below.':'Not quite — the official key is shown below.'));
  save(article,{attempted:true,result,input});}
});hydrate();
// Subject and topic lists hold every question. Filters hide cards; 50 per page (the default) or all at once.
const list=document.querySelector('#questions'),pagers=[...document.querySelectorAll('.list-pages')];
if(list&&pagers.length){const cards=[...list.querySelectorAll(':scope>article.question')],form=document.querySelector('#filters'),status=document.querySelector('#filter-status');
 let page=1,perPage=50,shown=cards,filter=null;try{perPage=localStorage.getItem('gate-per-page')==='all'?0:50;}catch{}
 const radios=[...document.querySelectorAll('input[name="per-page"]')];
 radios.forEach(r=>{r.checked=(r.value==='50')===(perPage===50);r.addEventListener('change',()=>{perPage=r.value==='50'?50:0;try{localStorage.setItem('gate-per-page',perPage?'50':'all');}catch{}page=1;render();});});
 if(!radios.length)perPage=0;
 const keep=(c,f)=>{if(!f)return true;const d=c.dataset,y=Number(d.year);return y>=Number(f.get('from')||-Infinity)&&y<=Number(f.get('to')||Infinity)&&(!f.get('marks')||d.marks===f.get('marks'))&&(!f.get('type')||d.type===f.get('type'))&&(!f.has('discrepancy')||d.disc==='1')&&(!f.has('bookmarked')||state[d.id]?.bookmarked)&&(!f.has('syllabus')||d.off!=='1')&&(!f.has('onemethod')||d.alt!=='1');};
 function render(){shown=cards.filter(c=>keep(c,filter));const pages=perPage?Math.max(1,Math.ceil(shown.length/perPage)):1;page=Math.min(Math.max(1,page),pages);
  const from=perPage?(page-1)*perPage:0,visible=new Set(shown.slice(from,perPage?from+perPage:shown.length));cards.forEach(c=>c.hidden=!visible.has(c));
  pagers.forEach((nav,top)=>{nav.replaceChildren();nav.hidden=pages<2;if(pages<2)return;
   const add=(label,n,current)=>{const b=document.createElement('button');b.type='button';b.textContent=label;if(current)b.setAttribute('aria-current','page');b.disabled=current||n<1||n>pages;b.addEventListener('click',()=>{page=n;render();pagers[0].scrollIntoView({block:'start'});});nav.append(b);};
   add('Previous',page-1);for(let n=1;n<=pages;n++)add(String(n),n,n===page);add('Next',page+1);});
  if(status)status.textContent=filter?shown.length+' matching question'+(shown.length===1?'':'s'):'';
  document.querySelectorAll('.year-jump a').forEach(a=>a.hidden=!shown.some(c=>c.dataset.year===a.dataset.year));}
 function reveal(id){let i=shown.findIndex(c=>c.id===id);
  if(i<0&&filter&&cards.some(c=>c.id===id)){filter=null;form?.reset();render();i=shown.findIndex(c=>c.id===id);}
  if(i<0)return;if(perPage&&Math.floor(i/perPage)+1!==page){page=Math.floor(i/perPage)+1;render();}document.getElementById(id)?.scrollIntoView();}
 document.querySelectorAll('.year-jump a').forEach(a=>a.addEventListener('click',e=>{const first=shown.find(c=>c.dataset.year===a.dataset.year);if(!first)return;e.preventDefault();history.pushState(null,'','#'+first.id);reveal(first.id);}));
 addEventListener('hashchange',()=>reveal(decodeURIComponent(location.hash.slice(1))));
 if(form){form.addEventListener('submit',e=>{e.preventDefault();filter=new FormData(form);page=1;render();});form.addEventListener('reset',()=>{filter=null;page=1;setTimeout(render);});}
 render();if(location.hash)reveal(decodeURIComponent(location.hash.slice(1)));}
const search=document.querySelector('#search');if(search){
 let data=null,pagefind=null,engineTried=false,revision=0;
 const facets=['subject','year','type'];
 async function performSearch(){const r=++revision,term=search.value.trim(),results=document.querySelector('#search-results'),status=document.querySelector('#search-status');if(!term){results.replaceChildren();status.textContent='';return;}
 const filters=Object.fromEntries(facets.map(name=>[name,document.querySelector('#search-'+name).value]).filter(([,v])=>v));
 try{
  if(!engineTried){engineTried=true;try{pagefind=await import(new URL('pagefind/pagefind.js',base).href);await pagefind.init();}catch{pagefind=null;}}
  let found,total,mode;
  if(pagefind){const response=await pagefind.search(term,{filters});total=response.results.length;found=await Promise.all(response.results.slice(0,50).map(async hit=>{const result=await hit.data();return {title:result.meta.title||result.meta.question_id,id:result.meta.question_id,subject:result.filters.subject?.join(', ')||'',year:result.filters.year?.join(', ')||'',type:result.filters.type?.join(', ')||'',url:'q/'+result.meta.question_id+'/'};}));mode='Indexed search';}
  else{if(!data){const response=await fetch(new URL('search.json',base));if(!response.ok)throw Error();data=await response.json();}const all=data.filter(q=>[q.title,q.text,q.year,q.subject,q.type].join(' ').toLowerCase().includes(term.toLowerCase())&&Object.entries(filters).every(([k,v])=>String(q[k])===v));total=all.length;found=all.slice(0,50);mode='Text search fallback (index unavailable)';}
  if(r!==revision)return;results.replaceChildren();status.textContent=total+' matches · '+mode+(total>50?' · first 50 shown; refine your search':'');
  for(const q of found){const div=document.createElement('div');div.className='search-hit';const a=document.createElement('a');a.href=new URL(q.url,base);a.textContent=q.title;const meta=document.createElement('small');meta.textContent=q.id+' · '+q.subject+' · '+q.type;div.append(a,meta);results.append(div);}
 }catch{if(r===revision)status.textContent='Search could not load. Browse the subject and paper pages instead.';}}
 search.addEventListener('input',performSearch);facets.forEach(f=>document.querySelector('#search-'+f).addEventListener('change',performSearch));
}
let remaining=10800,end=null,tick=null;const timer=document.querySelector('#timer-value');function showTime(){if(timer)timer.textContent=[Math.floor(remaining/3600),Math.floor(remaining%3600/60),remaining%60].map(n=>String(n).padStart(2,'0')).join(':');}
document.querySelector('#timer-start')?.addEventListener('click',()=>{if(tick)return;end=Date.now()+remaining*1000;tick=setInterval(()=>{remaining=Math.max(0,Math.ceil((end-Date.now())/1000));showTime();if(!remaining){clearInterval(tick);tick=null;timer.textContent='Time complete';}},250);});document.querySelector('#timer-pause')?.addEventListener('click',()=>{if(end)remaining=Math.max(0,Math.ceil((end-Date.now())/1000));clearInterval(tick);tick=null;end=null;showTime();});
let printDetails=[];addEventListener('beforeprint',()=>{printDetails=[...document.querySelectorAll('details.answer')].map(d=>[d,d.open]);printDetails.forEach(([d])=>d.open=true);});addEventListener('afterprint',()=>printDetails.forEach(([d,open])=>d.open=open));
// "Step through it" is always closed until a reader opens it; the player script loads on first use.
(()=>{let loading=null;
 const load=()=>loading||(loading=new Promise((ok,fail)=>{const s=document.createElement('script');s.src=new URL('assets/steps.js',base).href;s.onload=ok;s.onerror=fail;document.head.append(s);}));
 document.addEventListener('toggle',e=>{const d=e.target;if(!(d instanceof HTMLDetailsElement)||!d.matches('details.steps')||!d.open)return;
  load().then(()=>window.gateSteps(d.querySelector('.steps-player'))).catch(()=>{d.querySelector('.steps-player').textContent='The step-through could not load. Check your connection.';});},true);})();
// Install as an app: Chrome, Edge and Android offer a prompt; iPhone and iPad use Share → Add to Home Screen.
(()=>{const buttons=[...document.querySelectorAll('.install-app')],hints=[...document.querySelectorAll('.install-hint')];if(!buttons.length)return;
 if(matchMedia('(display-mode: standalone)').matches||navigator.standalone)return;
 let prompt=null;
 addEventListener('beforeinstallprompt',e=>{e.preventDefault();prompt=e;buttons.forEach(b=>b.hidden=false);hints.forEach(h=>h.hidden=true);});
 addEventListener('appinstalled',()=>{buttons.forEach(b=>b.hidden=true);hints.forEach(h=>h.hidden=true);});
 if(/iPhone|iPad|iPod/.test(navigator.userAgent))hints.forEach(h=>h.hidden=false);
 buttons.forEach(b=>b.addEventListener('click',async()=>{if(!prompt)return;prompt.prompt();await prompt.userChoice;prompt=null;buttons.forEach(x=>x.hidden=true);}));})();
