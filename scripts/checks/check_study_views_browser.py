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
                context=browser.new_context(viewport={'width':width,'height':height},service_workers='block')
                page=context.new_page();errors=[]
                page.on('pageerror',lambda e:errors.append(str(e)))
                visible="[...document.querySelectorAll('#questions>article')].filter(a=>!a.hidden)"
                page.goto(base+'/08-operating-systems/');total=page.locator('#questions>article').count()
                assert total>50 and page.evaluate(visible+'.length')==50  # 50 per page by default
                page.check('input[name=per-page][value="all"]');assert page.evaluate(visible+'.length')==total
                years=page.evaluate(visible+".map(a=>+a.dataset.year)");assert years==sorted(years,reverse=True)
                page.reload();assert page.is_checked('input[name=per-page][value="all"]')  # the choice is remembered
                page.check('input[name=per-page][value="50"]');assert page.evaluate(visible+'.length')==50
                page.locator('.list-pages').first.get_by_role('button',name='2').click()
                second=page.evaluate(visible+'[0].id');assert second==page.evaluate("[...document.querySelectorAll('#questions>article')][50].id")
                page.reload();assert page.is_checked('input[name=per-page][value="50"]')
                # Year jump and a link to a question on another page switch to that page.
                oldest=years[-1];page.click(f'.year-jump a[data-year="{oldest}"]')
                assert page.evaluate("!document.getElementById(location.hash.slice(1)).hidden")
                # One per method keeps one card per group; reset restores everything.
                page.check('input[name=onemethod]');page.click('#filters button[type=submit]')
                kept=page.evaluate(visible+".filter(a=>a.dataset.alt==='1').length");assert kept==0
                page.click('#filters button[type=reset]');page.check('input[name=per-page][value="all"]')
                assert page.evaluate(visible+'.length')==total
                # Answers stay per question.
                card=page.locator('#questions>article[data-type="MCQ"]').first;card.scroll_into_view_if_needed()
                card.locator('.choices button').first.click();assert card.locator('.attempt-result').inner_text().strip()
                # Similar questions page and Back.
                link=page.locator('#questions .similar-link a').first;qid=link.evaluate("a=>a.closest('article').id")
                link.click();page.wait_for_load_state();assert '/similar/' in page.url
                assert page.locator(f'#questions>article#{qid}').count()==1
                page.go_back();page.wait_for_load_state();assert page.url.endswith('/08-operating-systems/') or '#' in page.url
                # Old addresses redirect.
                page.goto(base+'/08-operating-systems/patterns/');page.wait_for_url('**/08-operating-systems/')
                assert page.evaluate('document.documentElement.scrollWidth-document.documentElement.clientWidth')<=1
                assert not errors,errors
                context.close()
            browser.close()
    finally:
        server.shutdown();server.server_close()
    print('Study-view Chromium checks passed: desktop/mobile, newest-first list, 50 per page, year jump, one per method, answers, similar page and Back, redirects, no JS errors or horizontal overflow.')


if __name__=='__main__':main()
