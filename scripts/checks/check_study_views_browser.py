#!/usr/bin/env python3
"""Exercise the built study views in Chromium; CI owns this review, not the user."""
import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import os
from pathlib import Path
import threading
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[2]


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--site',type=Path,default=ROOT/'_site')
    args=ap.parse_args()
    class QuietHandler(SimpleHTTPRequestHandler):
        def log_message(self, *_args): pass
    server=ThreadingHTTPServer(('127.0.0.1',0),partial(QuietHandler,directory=str(args.site.resolve())))
    threading.Thread(target=server.serve_forever,daemon=True).start()
    base=f'http://127.0.0.1:{server.server_port}'
    try:
        with sync_playwright() as p:
            launch={'headless':True}
            if os.environ.get('GATE_BROWSER_EXECUTABLE'):launch['executable_path']=os.environ['GATE_BROWSER_EXECUTABLE']
            browser=p.chromium.launch(**launch)
            for width,height in [(1440,1000),(390,844)]:
                context=browser.new_context(viewport={'width':width,'height':height})
                page=context.new_page();errors=[]
                page.on('pageerror',lambda error:errors.append(str(error)))
                page.goto(base+'/08-operating-systems/patterns/')
                page.locator('.pattern-index a[href$="#group-srtf-schedule-metrics"]').click()
                group=page.locator('#group-srtf-schedule-metrics')
                alt=group.locator('.group-alternatives')
                assert not alt.evaluate('(el)=>el.open')
                alt.locator(':scope > summary').click()
                q=page.locator('#CS-2024-S2-Q37')
                assert q.is_visible()
                q.locator('.bookmark').click()
                assert q.locator('.bookmark').get_attribute('aria-pressed')=='true'
                q.locator('.answer > summary').click()
                assert q.locator('.answer').evaluate('(el)=>el.open')
                assert not page.locator('#CS-2025-S2-Q26 .answer').evaluate('(el)=>el.open')
                alt.locator(':scope > summary').click();assert not q.is_visible()
                alt.locator(':scope > summary').click()
                assert q.locator('.bookmark').get_attribute('aria-pressed')=='true'
                page.get_by_role('link',name='All questions',exact=True).click()
                page.locator('input[name=bookmarked]').check()
                page.get_by_role('button',name='Apply filters',exact=True).click()
                page.wait_for_function("document.querySelector('#filter-status').textContent.includes('1 matching')")
                assert page.locator('#CS-2024-S2-Q37').count()==1
                page.get_by_role('button',name='Reset',exact=True).click()
                assert page.locator('#questions .question').count()==10
                page.go_back();assert '/patterns/' in page.url
                page.get_by_role('link',name='Known repeats folded',exact=True).click()
                assert 'unique questions' not in page.locator('main').inner_text().lower()
                repeat_page=next(path for path in (args.site/'08-operating-systems/unique').rglob('index.html')
                                 if 'id="CS-1998-Q31"' in path.read_text())
                page.goto(base+'/'+repeat_page.relative_to(args.site).as_posix().removesuffix('index.html'))
                repeat=page.locator('.study-unit').filter(has=page.locator('#CS-1998-Q31'))
                alternatives=repeat.locator('.group-alternatives')
                alternatives.locator(':scope > summary').click()
                assert page.locator('#CS-1992-Q20').is_visible()
                alternatives.locator(':scope > summary').click()
                assert not page.locator('#CS-1992-Q20').is_visible()
                page.get_by_role('link',name='All questions',exact=True).click()
                first_id=page.locator('#questions .question').first.get_attribute('id')
                page.get_by_role('link',name='Next',exact=True).first.click()
                assert '/page/2/' in page.url
                assert page.locator('#questions .question').first.get_attribute('id')!=first_id
                page.get_by_role('link',name='Previous',exact=True).first.click()
                assert page.locator('#questions .question').first.get_attribute('id')==first_id
                page.get_by_role('link',name='Problem patterns',exact=True).click()
                assert not page.evaluate('document.documentElement.scrollWidth > innerWidth'), 'horizontal overflow'
                assert not errors, errors
                context.close()
            browser.close()
    finally:
        server.shutdown();server.server_close()
    print('Study-view Chromium checks passed: desktop/mobile, pattern/repeat variants, answer isolation, bookmarks, filters/reset, pagination, Back, no JS errors or horizontal overflow.')


if __name__=='__main__':main()
