"""Weightage tables, syllabus flags and offline packs for build_site.py."""
import collections, hashlib, json
from pathlib import Path

FIRST_MARKS_YEAR = 2003  # every question from 2003 on has its marks recorded
PERIODS = (3, 5, 10)


def load_syllabus(root, topics):
    """data/syllabus.json -> ({(subject, topic): note}, metadata). Unknown topic IDs are an error."""
    path = root / 'data/syllabus.json'
    if not path.exists():  # optional: without it nothing is flagged
        return {}, {'syllabus': 'current', 'source': '', 'source_url': '', 'accessed_on': '', 'method': ''}
    data = json.loads(path.read_text())
    off = {}
    for subject, entries in data['not_listed'].items():
        known = {t['id'] for t in topics.get(subject, {}).get('topics', [])}
        for topic, note in entries.items():
            if topic not in known:
                raise SystemExit(f'data/syllabus.json names an unknown topic: {subject}/{topic}')
            off[(subject, topic)] = note
    return off, {k: data[k] for k in ('syllabus', 'source', 'source_url', 'accessed_on', 'method')}


def _fmt(value):
    """One decimal, without a trailing .0 (9.0 -> 9, 0.04 -> 0)."""
    return ('%.1f' % value).removesuffix('.0') if round(value, 1) else ('0' if not value else '<0.1')


def _mb(size):
    return '%.1f MB' % (size / 1048576) if size < 10 * 1048576 else '%d MB' % round(size / 1048576)


def weightage(questions, titles, topic_titles, off):
    """Marks per 100-mark paper by subject and topic.

    Each paper counts once: a question's share is its marks over that paper's
    total (so the 150-mark papers of 2003-2008 and multi-set years compare
    fairly), and a period's figure is the mean over its papers.
    """
    paper_year, paper_total = {}, collections.Counter()
    for q in questions:
        if q['year'] >= FIRST_MARKS_YEAR:
            if q.get('marks') is None:
                raise SystemExit('Weightage needs marks for every question from %d: %s' % (FIRST_MARKS_YEAR, q['question_id']))
            paper_year[q['paper_id']] = q['year']; paper_total[q['paper_id']] += q['marks']
    if not paper_year: return None  # nothing from the years with recorded marks
    years = sorted(set(paper_year.values())); latest = years[-1]
    by_subject = collections.defaultdict(collections.Counter)   # subject -> paper -> share
    by_topic = collections.defaultdict(collections.Counter)     # (subject, topic) -> paper -> share
    asked = collections.defaultdict(list)                       # (subject, topic) -> [year, ...] for every year in the archive
    for q in questions:
        key = (q['subject_dir'], q['topic']); asked[key].append(q['year'])
        if q['paper_id'] in paper_total:
            share = 100 * q['marks'] / paper_total[q['paper_id']]
            by_subject[q['subject_dir']][q['paper_id']] += share; by_topic[key][q['paper_id']] += share

    def mean(shares, papers):
        return sum(shares[p] for p in papers) / len(papers)

    def papers_in(first, last=latest):
        return [p for p, y in paper_year.items() if first <= y <= last]

    periods = []
    for n in PERIODS:
        first = years[-min(n, len(years))]; papers = papers_in(first)
        subjects = sorted(({'slug': s, 'title': titles[s], 'value': mean(by_subject[s], papers)} for s in titles), key=lambda r: -r['value'])
        top = max(r['value'] for r in subjects)
        for r in subjects: r['pct'] = round(100 * r['value'] / top, 1); r['text'] = _fmt(r['value'])
        ranked = []
        for (s, t), shares in by_topic.items():
            if (s, t) in off or t in ('other', 'unreviewed'): continue
            value = mean(shares, papers)
            if value:
                ranked.append({'subject': s, 'subject_title': titles[s], 'topic': t, 'title': topic_titles[(s, t)], 'value': value,
                               'count': sum(first <= y <= latest for y in asked[(s, t)]), 'last': max(asked[(s, t)])})
        ranked.sort(key=lambda r: -r['value']); ranked = ranked[:25]
        for r in ranked: r['pct'] = round(100 * r['value'] / ranked[0]['value'], 1); r['text'] = _fmt(r['value'])
        periods.append({'n': n, 'first': first, 'last': latest, 'papers': len(papers), 'subjects': subjects, 'topics': ranked})

    grid = []
    for s in sorted(titles):
        grid.append({'slug': s, 'title': titles[s], 'cells': [mean(by_subject[s], papers_in(y, y)) for y in years]})
    peak = max(c for row in grid for c in row['cells'])
    for row in grid:
        row['cells'] = [{'value': c, 'text': _fmt(c), 'step': min(5, 1 + int(5 * c / peak))} for c in row['cells']]

    # Per-subject topic table: the last ten years, every topic, flagged ones included and marked.
    first10 = years[-min(10, len(years))]; papers10 = papers_in(first10); subject_topics = {}
    for s in titles:
        rows = []
        for (subject, t), title in topic_titles.items():
            if subject != s or not asked[(s, t)]: continue
            rows.append({'topic': t, 'title': title, 'value': mean(by_topic[(s, t)], papers10), 'off': (s, t) in off,
                         'count': sum(first10 <= y <= latest for y in asked[(s, t)]), 'total': len(asked[(s, t)]), 'last': max(asked[(s, t)])})
        rows.sort(key=lambda r: (-r['value'], -r['last']))
        top = max([r['value'] for r in rows] + [0.001])
        for r in rows: r['pct'] = round(100 * r['value'] / top, 1); r['text'] = _fmt(r['value'])
        subject_topics[s] = rows
    return {'years': years, 'periods': periods, 'grid': grid, 'subject_topics': subject_topics, 'first10': first10, 'latest': latest, 'papers10': len(papers10)}


def _digest(path):
    return hashlib.sha1(path.read_bytes()).hexdigest()[:10]


def write_offline(out, packs, core):
    """Write offline/<id>.json for each pack, offline/core.json, and sw.js.

    A pack maps every URL it needs (relative to the site root) to a short content
    hash, so a saved pack can be refreshed by fetching only what changed.
    """
    target = out / 'offline'; target.mkdir(exist_ok=True)
    index = []
    for pack in packs:
        files, size = {}, 0
        for url in sorted(set(pack['urls'])):
            path = out / url / 'index.html' if url == '' or url.endswith('/') else out / url
            if not path.is_file(): raise SystemExit('Offline pack lists a missing file: ' + url)
            files[url] = _digest(path); size += path.stat().st_size
        version = hashlib.sha1(json.dumps(files, sort_keys=True).encode()).hexdigest()[:12]
        (target / (pack['id'] + '.json')).write_text(json.dumps({'id': pack['id'], 'title': pack['title'], 'version': version, 'bytes': size, 'files': files}))
        index.append({'id': pack['id'], 'title': pack['title'], 'group': pack['group'], 'note': pack['note'], 'version': version, 'bytes': size, 'size': _mb(size), 'count': len(files)})
    core_files = {}
    for url in sorted(set(core)):
        path = out / url / 'index.html' if url == '' or url.endswith('/') else out / url
        if not path.is_file(): raise SystemExit('Offline core lists a missing file: ' + url)
        core_files[url] = _digest(path)
    union = {}
    for pack in packs:
        if pack['group'] == 'subject':
            for url in pack['urls']: union[url] = (out / url / 'index.html' if url.endswith('/') else out / url).stat().st_size
    # The offline page is part of the core but embeds this index, so finish_offline() hashes it after it is rendered.
    return index, core_files, _mb(sum(union.values()))


def finish_offline(out, core_files, sw_source):
    for url in ('offline/',):
        core_files[url] = _digest(out / url / 'index.html')
    version = hashlib.sha1(json.dumps(core_files, sort_keys=True).encode()).hexdigest()[:12]
    (out / 'offline/core.json').write_text(json.dumps({'version': version, 'files': core_files}))
    (out / 'sw.js').write_text(sw_source.replace('__CORE_VERSION__', version))
    return version


def load_repeats(root, questions):
    """data/repeats.json -> {question_id: {'group': [ids, newest first], 'others': [(id, kind), ...]}}.

    Pairs are joined into groups. A question's relation to another member is the
    recorded pair's kind when the two were paired directly; otherwise "same" only
    if every link between them is "same", else "numbers".
    """
    path = root / 'data/repeats.json'
    if not path.exists():
        return {}
    by_id = {q['question_id']: q for q in questions}
    links = collections.defaultdict(dict)
    for pair in json.loads(path.read_text())['pairs']:
        a, b, kind = pair['a'], pair['b'], pair['kind']
        if a not in by_id or b not in by_id: raise SystemExit(f'data/repeats.json names an unknown question: {a} / {b}')
        if kind not in ('same', 'numbers'): raise SystemExit(f'data/repeats.json: unknown kind {kind!r}')
        if by_id[a]['paper_id'] == by_id[b]['paper_id']: raise SystemExit(f'data/repeats.json pairs two questions from one paper: {a} / {b}')
        if b in links[a]: raise SystemExit(f'data/repeats.json lists a pair twice: {a} / {b}')
        links[a][b] = links[b][a] = kind

    def relation(start, target):
        # Breadth-first; prefer an all-"same" path.
        best = {start: 'same'}; queue = [start]
        while queue:
            node = queue.pop(0)
            for nxt, kind in links[node].items():
                rel = 'same' if best[node] == 'same' and kind == 'same' else 'numbers'
                if nxt not in best or (best[nxt] == 'numbers' and rel == 'same'):
                    best[nxt] = rel; queue.append(nxt)
        return best[target]

    def newest_first(ids):
        def key(qid):
            q = by_id[qid]
            return (-q['year'], q['paper_id'], [int(n) for n in __import__('re').findall(r'\d+', q['source_question_number'])])
        return sorted(ids, key=key)

    result, seen = {}, set()
    for start in links:
        if start in seen: continue
        group, stack = set(), [start]
        while stack:
            node = stack.pop()
            if node in group: continue
            group.add(node); stack.extend(links[node])
        seen |= group; ordered = newest_first(group)
        for qid in ordered:
            result[qid] = {'group': ordered, 'others': [(o, links[qid].get(o) or relation(qid, o)) for o in ordered if o != qid]}
    return result
