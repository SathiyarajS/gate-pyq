"""Static eligibility, escaping, SVG and rendering tests; not visual certification."""
import copy
import datetime
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import transcription as t
import build_site
import build_pdfs
from jinja2 import Environment, FileSystemLoader, select_autoescape


def verified():
    return dict(stem='Exact $x<y$ wording.', options={'B':'Two', 'A':'One'}, figures=[], status='verified', checked_pages=[1,2], notes='Every symbol, options and solution compared independently.', verified_on='2026-01-01', verification=dict(method='independent-visual-comparison', transcriber='preparer', reviewer='reviewer', solution_checked=True, rendered_comparison_checked=True))


class TranscriptionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / 'figures').mkdir()
        self.q = dict(question_id='CS-X-Q1', source_page=1, source_pages=[1,2])
        self.entry = verified()

    def tearDown(self): self.tmp.cleanup()

    def resolve(self, entry=None, contexts=None):
        return t.resolve(self.root, self.q, {'CS-X-Q1': self.entry if entry is None else entry, '_contexts': contexts or {}})

    def test_valid_and_missing(self):
        self.assertTrue(self.resolve())
        self.assertIsNone(t.resolve(self.root, self.q, {}))

    def test_draft_or_incomplete_review_never_displayed(self):
        for field, value in [('status','draft'), ('notes',''), ('verified_on','bad'), ('verified_on','2999-01-01'), ('checked_pages',[1]), ('checked_pages',['1',2]), ('verification',{})]:
            with self.subTest(field=field):
                entry = verified(); entry[field] = value
                self.assertIsNone(self.resolve(entry))
        for field, value in [('reviewer','preparer'), ('reviewer',' '), ('solution_checked',False), ('rendered_comparison_checked', False), ('method','OCR')]:
            entry = verified(); entry['verification'][field] = value
            self.assertIsNone(self.resolve(entry))

    def test_missing_rendered_comparison_review_falls_back(self):
        self.entry['verification'].pop('rendered_comparison_checked')
        self.assertIsNone(self.resolve())

    def test_unverified_missing_and_nested_contexts_fall_back(self):
        self.entry['shared_context_refs'] = ['common']
        self.assertIsNone(self.resolve())
        context = verified(); context['status'] = 'draft'
        self.assertIsNone(self.resolve(contexts={'common':context}))
        context = verified(); context['shared_context_refs'] = ['nested']
        self.assertIsNone(self.resolve(contexts={'common':context}))
        context = verified(); context['checked_pages'] = []
        self.assertIsNone(self.resolve(contexts={'common':context}))

    def test_shared_context_rendered_and_searchable(self):
        self.entry['shared_context_refs'] = ['common']
        context = verified(); context['stem'] = 'Common data'
        result = self.resolve(contexts={'common':context})
        self.assertIn('Common data', result['search'])
        self.assertLess(result['html'].index('Common data'), result['html'].index('Exact'))

    def test_options_keep_source_order_and_escape(self):
        self.entry['options']['A'] = '<img src=x onerror=alert(1)>'
        result = self.resolve()['html']
        self.assertLess(result.index('(B)'),result.index('(A)'))
        self.assertIn('&lt;img', result)
        self.assertNotIn('<img', result)

    def test_unsafe_or_malformed_options_figures_fall_back(self):
        for field, value in [('options', {'<script>':'x'}), ('options',[]), ('figures','x'), ('figures',['../x.svg']), ('figures',['figures/missing.svg']), ('shared_context_refs','x'), ('stem','')]:
            entry = verified(); entry[field] = value
            self.assertIsNone(self.resolve(entry))

    def test_math_code_markdown_tables_and_xss(self):
        output = str(t.rich('**Bold** and *italic* $x<y$ `a$b$c`\n\n```c\n  <x> $y$\n```\n\n| A | B |\n| --- | :---: |\n| $x$ | <script> |\n\n1. Step one\n2. Step two\n\n$$\nx^2\n$$', True))
        for token in ('<strong>Bold</strong>', '<em>italic</em>', 'data-math="x&lt;y"', '<code>a$b$c</code>', '  &lt;x&gt; $y$', '<table>', '<ol start="1">', 'data-display="true"'):
            self.assertIn(token, output)
        self.assertNotIn('<script>', output)

    def test_table_pipes_inside_math_code_and_escaped_prose(self):
        result = str(t.rich('| Expression | Code | Prose |\n| --- | --- | --- |\n| $P(A|B)$ | `a|b` | a\\|b |', True))
        self.assertEqual(result.count('<td>'), 3)
        self.assertIn('data-math="P(A|B)"', result)
        self.assertIn('<code>a|b</code>', result)
        self.assertIn('<td>a|b</td>', result)

    def test_escaped_asterisks_are_literal(self):
        result = str(t.rich(r'C = (20\*, 22\*, 25\*) and *x* with $a\*b$', True))
        self.assertIn('C = (20*, 22*, 25*) and <em>x</em>', result)
        self.assertNotIn('<em>, 22', result)
        self.assertIn(r'data-math="a\*b"', result)

    def test_display_math_stays_inside_table_cells(self):
        for expression in ('$$x$$', r'\[x\]'):
            result = str(t.rich('| Expression |\n| --- |\n| ' + expression + ' |', True))
            self.assertEqual(result.count('<td>'), 1)
            self.assertIn('<td><span class="math-source" data-math="x" data-display="true">', result)
            self.assertTrue(result.endswith('</tbody></table></div>'))

    def test_nonconsecutive_ordered_list_numbers_preserved(self):
        result = str(t.rich('1. One\n3. Three\n7. Seven', True))
        for number in (1, 3, 7): self.assertIn('<li value="' + str(number) + '">', result)

    def test_source_shared_context_requires_reviewed_reference(self):
        for field in ('shared_context', 'shared_context_reference'):
            self.q[field] = 'Original common data'
            self.assertIsNone(self.resolve())
            self.entry['shared_context_refs'] = ['common']
            self.assertIsNone(self.resolve())
            self.assertTrue(self.resolve(contexts={'common':verified()}))
            self.entry.pop('shared_context_refs'); self.q.pop(field)

    def test_legacy_dollar_end_markers_unchanged(self):
        self.assertNotIn('math-source', str(build_site.rich('Input w$ and stack Z$')))
        self.assertIn('math-source', str(build_site.rich(r'\(x\)')))
        self.assertNotIn('math-source', str(t.rich(r'Unclosed \(x and $y', True)))

    def svg(self, content):
        path = self.root / 'figures/a.svg'; path.write_text(content)
        return t.safe_svg(self.root, 'figures/a.svg')

    def test_valid_inline_svg(self):
        result = self.svg('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><title>Graph</title><path d="M0 0 L10 10" stroke="currentColor"/><text x="20" y="20" font-size="12">A&lt;B</text></svg>')
        self.assertIn('<text', result)
        self.assertIn('currentColor', result)
        self.assertNotIn('<img', result)

    def test_svg_font_style_values(self):
        ok = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><title>T</title><text x="1" y="20" font-size="12" font-style="{}">a</text></svg>'
        self.assertIn('font-style="italic"', str(self.svg(ok.format('italic'))))
        with self.assertRaises(ValueError): self.svg(ok.format('expression(x)'))

    def test_svg_forbidden_elements_attributes_colors_and_sizes(self):
        bad = ['<script>alert(1)</script>', '<foreignObject/>', '<image href="https://example.org/x"/>', '<g onclick="x"/>', '<style>@import "x";</style>', '<g style="fill:url(x)"/>', '<path fill="red"/>', '<text font-size="8">x</text>', '<g font-size="2"><text>x</text></g>', '<use href="#x"/>', '<g><image href="data:image/png,x"/></g>', '<path marker-end="url(https://example.org/x)"/>', '<path stroke="url(#x)"/>', '<animate/>']
        for element in bad:
            with self.subTest(element=element), self.assertRaises(ValueError):
                self.svg('<svg viewBox="0 0 100 100"><title>Unsafe</title>'+element+'</svg>')

    def test_svg_viewbox_dimensions_labels_and_entities(self):
        for raw in ['<svg/>', '<svg viewBox="0 0 nan 1"><title>x</title></svg>', '<svg viewBox="0 0 -1 10"><title>x</title></svg>', '<svg viewBox="0 0 1 1" width="20"><title>x</title></svg>', '<svg viewBox="0 0 1 1"/>', '<!DOCTYPE svg><svg viewBox="0 0 1 1"><title>x</title></svg>']:
            with self.subTest(raw=raw), self.assertRaises(ValueError): self.svg(raw)

    def test_svg_path_and_symlink_guards(self):
        for name in ('../a.svg', '/tmp/a.svg', 'https://x/a.svg', 'figures/../a.svg', 'figures/a.svg?x', 'figures/sub/a.svg'):
            with self.assertRaises(ValueError): t.safe_svg(self.root, name)
        outside = self.root / 'outside.svg'; outside.write_text('<svg/>')
        (self.root/'figures/link.svg').symlink_to(outside)
        with self.assertRaises(ValueError): t.safe_svg(self.root,'figures/link.svg')

    def test_svg_local_markers_only(self):
        result = self.svg('<svg viewBox="0 0 100 100"><title>Arrow</title><defs><marker id="tip"><path d="M0 0 L1 1"/></marker></defs><path d="M0 0 L2 2" marker-end="url(#tip)"/></svg>')
        self.assertRegex(result, r'url\(#f[0-9a-f]+-tip\)')
        with self.assertRaises(ValueError): self.svg('<svg viewBox="0 0 1 1"><title>x</title><path marker-end="url(#missing)"/></svg>')

    def test_loader_and_paper_path_guard(self):
        self.assertEqual(t.load_paper(self.root,'CS-X'),{})
        with self.assertRaises(ValueError): t.load_paper(self.root,'../x')
        directory = self.root/'data/transcriptions'; directory.mkdir(parents=True)
        (directory/'CS-X.json').write_text('[]')
        with self.assertRaises(ValueError): t.load_paper(self.root,'CS-X')

    def test_verified_template_original_toggle_and_answer(self):
        env = Environment(loader=FileSystemLoader(ROOT/'templates/site'), autoescape=select_autoescape(['html']))
        env.filters['rich'] = build_site.rich; env.filters['solution'] = build_site.solution; env.filters['reader'] = build_site.reader; env.filters['answer'] = build_site.answer
        q = dict(self.q, transcription=self.resolve(), display_type='MCQ', practice_key='B', subject_dir='test', number='1', ordinal=1, year=2026, marks=1, discrepancy_ids=[], permalink='q/CS-X-Q1/', report='#', question_title='Title', topic_title='Topic', question_text='Paraphrase', official_answer='B', derived_answer='B', solution='Solution', discrepancies=[], original_crops=[], source_link='https://example.org/paper')
        result = env.get_template('question.html').render(q=q,prefix='../')
        self.assertIn('class="transcription"',result)
        self.assertIn('<summary>View original</summary>',result)
        self.assertNotIn("text-version", result); self.assertIn('class="paraphrase search-text"', result)
        self.assertIn('<details class="answer"',result)
        self.assertNotIn('Not a verbatim question.',result)
        self.assertNotIn('<details open',result)


class BuildIntegrationTests(unittest.TestCase):
    def test_verified_and_draft_build_search_counts_and_pdf(self):
        import contextlib
        import io
        import shutil
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root/'data/transcriptions').mkdir(parents=True)
            for name in ('templates', 'site-static'):
                shutil.copytree(ROOT/name, root/name)
            shutil.copy2(ROOT/'DISCREPANCIES.md', root/'DISCREPANCIES.md')
            q = json.loads((ROOT/'data/questions.json').read_text())[0]
            papers = [p for p in json.loads((ROOT/'data/papers.json').read_text()) if p['paper_id']==q['paper_id']]
            for name, data in [('questions.json',[q]), ('papers.json',papers)]:
                (root/'data'/name).write_text(json.dumps(data))
            shutil.copy2(ROOT/'data/topics.json',root/'data/topics.json')
            entry = verified(); entry['checked_pages'] = q.get('source_pages') or [q['source_page']]
            entry['stem'] = 'UniqueSearchNeedle $x^2$'
            transpath = root/'data/transcriptions'/(q['paper_id']+'.json')
            for state, expected in [('verified',1), ('draft',0)]:
                entry['status']=state; transpath.write_text(json.dumps({q['question_id']:entry}))
                with patch.object(build_site,'ROOT',root), patch.object(sys,'argv',['build_site.py','--preview','--output','out']), contextlib.redirect_stdout(io.StringIO()):
                    build_site.main()
                report = json.loads((root/'out/build-report.json').read_text())
                self.assertEqual(report['redrawn_questions'],expected)
                search = json.loads((root/'out/search.json').read_text())
                self.assertEqual('UniqueSearchNeedle' in search[0]['text'],bool(expected))
                subject = q['subject'] if q['subject']!='excluded' else '13-other-topics'
                records = json.loads((root/'out'/subject/'index.json').read_text())
                with patch.object(build_pdfs,'ROOT',root):
                    for questions_only in (True, False):
                        doc = build_pdfs.document(subject,records,questions_only)
                        self.assertEqual('UniqueSearchNeedle' in doc,bool(expected))
                        self.assertEqual('Answer &amp; detailed solution' in doc,False)
                        self.assertEqual('<details open class="answer"' in doc,not questions_only)
                        self.assertIn('../assets/vendor/katex/katex.min.js',doc)
                self.assertIn('paraphrase',records[0]['html'].lower())
            with patch.object(build_site,'ROOT',root), patch.object(sys,'argv',['build_site.py']):
                with self.assertRaisesRegex(SystemExit,'Release blocked'): build_site.main()

if __name__ == '__main__': unittest.main()
