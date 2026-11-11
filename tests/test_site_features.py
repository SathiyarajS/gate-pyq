import json, sys, tempfile, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import site_features


def question(qid, paper, year, subject, topic, marks):
    return {'question_id': qid, 'paper_id': paper, 'year': year, 'subject_dir': subject, 'topic': topic, 'marks': marks}


class WeightageTest(unittest.TestCase):
    def setUp(self):
        self.titles = {'a': 'A', 'b': 'B'}
        self.topic_titles = {('a', 'x'): 'X', ('a', 'y'): 'Y', ('b', 'z'): 'Z'}
        qs = []
        for year in range(2015, 2027):
            # One 100-mark paper a year, except 2026, which has two sets with different splits.
            for n, split in enumerate([(60, 20, 20)] if year < 2026 else [(60, 20, 20), (20, 20, 60)], 1):
                paper = f'P-{year}-{n}'
                qs += [question(paper + 'x', paper, year, 'a', 'x', split[0]), question(paper + 'y', paper, year, 'a', 'y', split[1]),
                       question(paper + 'z', paper, year, 'b', 'z', split[2])]
        self.questions = qs + [question('old', 'P-1995', 1995, 'a', 'x', None)]

    def test_each_paper_counts_once_and_shares_sum_to_100(self):
        w = site_features.weightage(self.questions, self.titles, self.topic_titles, {})
        for period in w['periods']:
            self.assertAlmostEqual(sum(r['value'] for r in period['subjects']), 100)
        three = next(p for p in w['periods'] if p['n'] == 3)   # 2024, 2025 and the two 2026 sets: four papers
        self.assertEqual(three['papers'], 4)
        self.assertAlmostEqual({r['slug']: r['value'] for r in three['subjects']}['b'], (20 + 20 + 20 + 60) / 4)
        # The year grid averages the two 2026 sets rather than adding them.
        self.assertAlmostEqual(w['grid'][1]['cells'][-1]['value'], 40)

    def test_flagged_topics_are_left_out_of_the_ranking_but_kept_on_the_subject(self):
        w = site_features.weightage(self.questions, self.titles, self.topic_titles, {('a', 'y'): 'not named'})
        self.assertNotIn('y', [r['topic'] for r in w['periods'][0]['topics']])
        self.assertTrue(next(r for r in w['subject_topics']['a'] if r['topic'] == 'y')['off'])

    def test_missing_marks_in_a_counted_year_is_an_error(self):
        self.questions.append(question('bad', 'P-2020-1', 2020, 'a', 'x', None))
        with self.assertRaises(SystemExit):
            site_features.weightage(self.questions, self.titles, self.topic_titles, {})


class SyllabusTest(unittest.TestCase):
    def test_repository_file_names_only_known_topics(self):
        topics = json.loads((ROOT / 'data/topics.json').read_text())
        off, meta = site_features.load_syllabus(ROOT, topics)
        self.assertTrue(off)
        self.assertTrue(meta['source_url'].startswith('https://'))

    def test_unknown_topic_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / 'data').mkdir()
            data = json.loads((ROOT / 'data/syllabus.json').read_text()); data['not_listed'] = {'a': {'nope': 'x'}}
            (Path(tmp) / 'data/syllabus.json').write_text(json.dumps(data))
            with self.assertRaises(SystemExit):
                site_features.load_syllabus(Path(tmp), {'a': {'topics': [{'id': 'x', 'title': 'X'}]}})


class OfflineTest(unittest.TestCase):
    def test_pack_version_follows_content(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp); (out / 's').mkdir(); (out / 's/index.html').write_text('one'); (out / 'a.webp').write_text('img')
            packs = [{'id': 's', 'title': 'S', 'group': 'subject', 'note': '', 'urls': ['s/', 'a.webp', 'a.webp']}]
            first, _, _ = site_features.write_offline(out, packs, ['s/'])
            self.assertEqual(first[0]['count'], 2)
            (out / 's/index.html').write_text('two')
            second, _, _ = site_features.write_offline(out, packs, ['s/'])
            self.assertNotEqual(first[0]['version'], second[0]['version'])
            packs[0]['urls'].append('missing.webp')
            with self.assertRaises(SystemExit):
                site_features.write_offline(out, packs, ['s/'])


if __name__ == '__main__':
    unittest.main()


class RepeatsTest(unittest.TestCase):
    def build(self, pairs):
        qs = [{'question_id': i, 'paper_id': 'P' + i, 'year': y, 'source_question_number': '1'} for i, y in (('a', 2000), ('b', 2010), ('c', 2020), ('d', 2015))]
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / 'data').mkdir()
            (Path(tmp) / 'data/repeats.json').write_text(json.dumps({'pairs': [{'a': a, 'b': b, 'kind': k} for a, b, k in pairs]}))
            return site_features.load_repeats(Path(tmp), qs)

    def test_groups_newest_first_with_relations(self):
        r = self.build([('a', 'b', 'same'), ('b', 'c', 'numbers')])
        self.assertEqual(r['a']['group'], ['c', 'b', 'a'])
        self.assertEqual(dict(r['a']['others']), {'b': 'same', 'c': 'numbers'})
        self.assertNotIn('d', r)

    def test_same_only_through_same_links(self):
        r = self.build([('a', 'b', 'same'), ('b', 'c', 'same')])
        self.assertEqual(dict(r['a']['others']), {'b': 'same', 'c': 'same'})

    def test_bad_pairs_are_rejected(self):
        for pairs in ([('a', 'zz', 'same')], [('a', 'b', 'topic')], [('a', 'b', 'same'), ('b', 'a', 'numbers')]):
            with self.assertRaises(SystemExit):
                self.build(pairs)

    def test_repository_file_is_valid(self):
        qs = json.loads((ROOT / 'data/questions.json').read_text())
        years = {p['paper_id']: p['year'] for p in json.loads((ROOT / 'data/papers.json').read_text())}
        for q in qs: q['year'] = years[q['paper_id']]
        self.assertTrue(site_features.load_repeats(ROOT, qs))
