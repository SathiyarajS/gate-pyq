"""Crop display regression tests; no browser, asset rendering or network required."""
import importlib.util
import re
import unittest
from html.parser import HTMLParser
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('build_site', ROOT / 'scripts/build_site.py')
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class Elements(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.nodes = []
        self.stack = []
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        node = {'tag': tag, 'attrs': dict(attrs), 'parents': self.stack[:], 'text': ''}
        self.nodes.append(node)
        if tag not in ('img', 'input', 'br', 'hr', 'meta', 'link'):
            self.stack.append(node)

    def handle_endtag(self, tag):
        if self.stack and self.stack[-1]['tag'] == tag:
            self.stack.pop()

    def handle_data(self, data):
        for node in self.stack:
            node['text'] += data

    def find(self, tag=None, cls=None):
        return [n for n in self.nodes if (tag is None or n['tag'] == tag)
                and (cls is None or cls in n['attrs'].get('class', '').split())]


class QuestionTemplateTests(unittest.TestCase):
    def render(self, crops, prefix='../../'):
        env = Environment(loader=FileSystemLoader(ROOT / 'templates/site'),
                          autoescape=select_autoescape(['html']))
        env.filters['rich'] = builder.rich; env.filters['solution'] = builder.solution; env.filters['reader'] = builder.reader; env.filters['answer'] = builder.answer
        q = dict(question_id='CS-2026-Q1', display_type='MCQ', practice_key='B',
                 subject_dir='test', number='1', ordinal=1, year=2026, session='CS1',
                 marks=1, discrepancy_ids=[], permalink='q/CS-2026-Q1/', report='#',
                 question_title='Test question', topic_title='Test topic',
                 question_text='Compare "A" < B & C.\nExplain why.', original_crops=crops,
                 official_answer='B', derived_answer='B', solution='Answer explanation',
                 discrepancies=[])
        return Elements(env.get_template('question.html').render(q=q, prefix=prefix))

    def test_multipart_crops_have_native_full_size_links_and_safe_alt(self):
        crops = [dict(file=f'CS-2026-Q1-{i}.webp', width=1200, height=600, page=i)
                 for i in (1, 2)]
        for prefix in ('../../', '../../../../', '/gate-pyq/'):
            with self.subTest(prefix=prefix):
                doc = self.render(crops, prefix)
                images = doc.find('img')
                self.assertEqual(len(images), 2)
                for i, img in enumerate(images, 1):
                    attrs = img['attrs']
                    link = img['parents'][-1]
                    self.assertEqual(link['tag'], 'a')
                    self.assertEqual(link['attrs']['href'], attrs['src'])
                    self.assertEqual(attrs['src'], f'{prefix}assets/questions/CS-2026-Q1-{i}.webp')
                    self.assertIn(f'part {i} of 2', link['attrs']['aria-label'])
                    self.assertNotIn('tabindex', link['attrs'])
                    self.assertEqual((attrs['width'], attrs['height'], attrs['loading']), ('1200', '600', 'lazy'))
                    self.assertIn('GATE 2026: Compare "A" < B & C.', attrs['alt'])

    def test_crop_paraphrase_hidden_but_searchable_without_affecting_answers(self):
        doc = self.render([dict(file='q.webp', width=1200, height=600, page=1)])
        self.assertFalse(doc.find('details', 'text-version'))
        text, = doc.find('div', 'paraphrase')
        self.assertIn('search-text', text['attrs']['class'])
        self.assertEqual(text['attrs']['aria-hidden'], 'true')
        self.assertIn('data-pagefind-body', text['attrs'])
        self.assertFalse(any('data-pagefind-ignore' in n['attrs'] for n in text['parents']))
        self.assertLess(doc.nodes.index(doc.find('section', 'original-source')[0]), doc.nodes.index(text))
        answer, = doc.find('details', 'answer')
        self.assertNotIn('open', answer['attrs'])
        self.assertIn('data-pagefind-ignore', answer['attrs'])
        self.assertNotIn(text, answer['parents'])
        self.assertNotIn(text, doc.find('div', 'practice')[0]['parents'])
        self.assertRegex((ROOT / 'site-static/style.css').read_text(), r'\.search-text\{[^}]*clip')

    def test_no_crop_preview_remains_visible(self):
        doc = self.render([])
        self.assertFalse(doc.find('img'))
        self.assertFalse(doc.find('details', 'text-version'))
        text, = doc.find('div', 'paraphrase')
        self.assertIn('data-pagefind-body', text['attrs'])
        self.assertFalse(any(n['tag'] == 'details' for n in text['parents']))

    def test_crop_css_retains_white_card_and_responsive_dimensions(self):
        css = (ROOT / 'site-static/style.css').read_text()
        image_rule = re.search(r'\.original-source img\{([^}]+)\}', css).group(1)
        for declaration in ('width:100%', 'max-width:820px', 'height:auto', 'background:white'):
            self.assertIn(declaration, image_rule.split(';'))
        self.assertNotIn('invert(', css)
        self.assertIn('a:focus-visible', css)
        self.assertRegex(css, r'\.original-source \.original-crop-link\{[^}]*display:block;[^}]*max-width:820px')


if __name__ == '__main__':
    unittest.main()
