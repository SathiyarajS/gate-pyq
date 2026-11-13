#!/usr/bin/env python3
"""Independent preview browser checks and screenshots; serve _site on port 8765 first."""
import asyncio,json
from pathlib import Path
from playwright.async_api import async_playwright
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'audits/screenshots';OUT.mkdir(exist_ok=True)
async def run():
 results=[]
 async with async_playwright() as p:
  browser=await p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
  for width in (360,1280):
   for theme in ('light','dark'):
    page=await browser.new_page(viewport={'width':width,'height':900},color_scheme=theme)
    for name,path in [('home',''),('subject','01-digital-logic/'),('answer','01-digital-logic/'),('paper','papers/CS-1991/')]:
     await page.goto('http://127.0.0.1:8765/'+path,wait_until='networkidle')
     if name=='answer':await page.locator('details.answer').first.evaluate('(e)=>e.open=true')
     overflow=await page.evaluate('document.documentElement.scrollWidth>innerWidth')
     results.append({'width':width,'theme':theme,'page':name,'horizontal_overflow':overflow})
     await page.screenshot(path=str(OUT/f'review-{name}-{width}-{theme}.png'),full_page=False)
    await page.close()
  page=await browser.new_page()
  await page.add_init_script("Object.defineProperty(window,'localStorage',{get(){throw new Error('blocked storage')}})")
  errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  await page.goto('http://127.0.0.1:8765/01-digital-logic/',wait_until='networkidle')
  await page.locator('button.bookmark').first.click();await page.locator('#theme').click()
  results.append({'blocked_storage_errors':errors})
  await browser.close()
 (ROOT/'audits/site-preview-review-browser.json').write_text(json.dumps(results,indent=2));print(json.dumps(results,indent=2))
asyncio.run(run())
