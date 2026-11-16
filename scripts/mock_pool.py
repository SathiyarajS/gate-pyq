"""Question pool and weights for the GATE-style mock test (site page /mock/).

build_site.py calls write_mock(...) after preparing the questions. Everything is
computed at build time from the data, so the browser only samples:

- weights: marks per 100-mark paper by subject and by topic, averaged over the
  papers of the last ten years (the same method as the Weightage page), and the
  recent question-type mix (MCQ / MSQ / NAT) per section and marks;
- pool: every question that can be marked automatically and fairly:
  in the current syllabus (or borderline, flagged), MCQ/MSQ/NAT worth 1 or 2
  marks, with an original question image, an official key (or, without one, our
  independently derived answer) in a parseable form, no "marks to all", and no
  discrepancy other than a stated model qualification.

The pool is small JSON (one row per question); questions are shown as their
committed images, exactly as on the rest of the site.
"""
import collections, hashlib, json, re

GA = '11-general-aptitude'
EM = '13-other-topics'          # in-syllabus part is Engineering Mathematics
SAFE_DISCREPANCY_TYPES = {'Source/model qualification'}
RECENT_YEARS = 10               # weightage window
TYPE_MIX_YEARS = 6              # MSQ exists from 2021; use the papers since then for the type mix


def norm_key(qtype, key):
    """Canonical answer string, or None if the key cannot be marked automatically.

    MCQ: 'B' or 'C|D' (either accepted). MSQ: 'A;C'. NAT: 'lo..hi'.
    """
    if key is None:
        return None
    k = str(key).strip()
    if re.search(r'marks?\s*to\s*all|\bMTA\b', k, re.I):
        return None
    if qtype == 'MCQ':
        m = re.fullmatch(r'\(?([A-E])\)?(?::.*)?', k)
        if m:
            return m.group(1)
        m = re.fullmatch(r'([A-E])\s+OR\s+([A-E])', k, re.I)
        return f'{m.group(1).upper()}|{m.group(2).upper()}' if m else None
    if qtype == 'MSQ':
        letters = re.findall(r'[A-E]', k)
        return ';'.join(sorted(set(letters))) if re.fullmatch(r'[A-E](\s*[;,]\s*[A-E])*', k) else None
    if qtype == 'NAT':
        num = r'-?\d+(?:\.\d+)?'
        m = re.fullmatch(rf'({num})\s*(?:to|:|–|-)\s*({num})', k) if not re.fullmatch(num, k) else None
        if m:
            lo, hi = sorted((float(m.group(1)), float(m.group(2))))
            return f'{lo:g}..{hi:g}'
        return f'{float(k):g}..{float(k):g}' if re.fullmatch(num, k) else None
    return None


def _shares(questions, recent_papers):
    """Mean share of a 100-mark paper per subject and per (subject, topic) over the given papers."""
    total = collections.Counter()
    for q in questions:
        if q['paper_id'] in recent_papers and q.get('marks'):
            total[q['paper_id']] += q['marks']
    subj, topic = collections.Counter(), collections.Counter()
    for q in questions:
        p = q['paper_id']
        if p in recent_papers and q.get('marks') and total[p]:
            share = 100 * q['marks'] / total[p]
            subj[q['subject_dir']] += share
            topic[(q['subject_dir'], q['topic'])] += share
    n = len(recent_papers)
    return {s: v / n for s, v in subj.items()}, {k: v / n for k, v in topic.items()}


def _type_mix(questions, papers):
    """Average count per paper of each type, by section (GA/core) and marks."""
    mix = collections.Counter()
    for q in questions:
        if q['paper_id'] in papers and q['display_type'] in ('MCQ', 'MSQ', 'NAT') and q.get('marks') in (1, 2):
            sec = 'GA' if q['subject_dir'] == GA else 'CS'
            mix[(sec, q['marks'], q['display_type'])] += 1
    n = len(papers)
    return {f'{sec}{m}': {t: round(mix[(sec, m, t)] / n, 2) for t in ('MCQ', 'MSQ', 'NAT')} for sec in ('GA', 'CS') for m in (1, 2)}


def build(questions, titles, topic_titles, ds):
    years = sorted({q['year'] for q in questions})
    latest = years[-1]
    recent = {q['paper_id'] for q in questions if q['year'] > latest - RECENT_YEARS}
    mix_papers = {q['paper_id'] for q in questions if q['year'] > latest - TYPE_MIX_YEARS}
    subj_share, topic_share = _shares(questions, recent)

    # Linked ("common data") questions share their context text within a paper.
    group_of = {}
    for q in questions:
        if q.get('shared_context'):
            group_of[q['question_id']] = q['paper_id'] + ':' + hashlib.sha1(str(q['shared_context']).encode()).hexdigest()[:8]

    pool, skipped = [], collections.Counter()
    for q in questions:
        t = q['display_type']
        why = None
        if q.get('syllabus_status') == 'out': why = 'not in syllabus'
        elif t not in ('MCQ', 'MSQ', 'NAT'): why = 'not auto-gradable type'
        elif q.get('marks') not in (1, 2): why = 'marks not 1 or 2'
        elif not q.get('original_crops'): why = 'no question image'
        if not why:
            official = norm_key(t, q.get('official_answer'))
            derived = norm_key(t, q.get('derived_answer'))
            if q.get('official_answer') is not None:
                key, src = official, 'o'
                if official is None: why = 'official key not machine-gradable (or marks to all)'
                elif derived and derived != official and not _nat_agrees(official, derived):
                    why = 'our answer disagrees with the official key'
            else:
                key, src = (derived, 'd') if q.get('key_source') == 'derived' else (None, '')
                if key is None: why = 'no gradable key'
        if not why:
            kinds = {ds[d]['type'] for d in q['discrepancy_ids'] if d in ds}
            if kinds - SAFE_DISCREPANCY_TYPES: why = 'answer-affecting discrepancy'
        if why:
            skipped[why] += 1
            continue
        choices = max(['D'] + re.findall(r'[A-E]', key if t != 'NAT' else '')) if t != 'NAT' else ''
        pool.append({
            'i': q['question_id'], 's': q['subject_dir'], 't': q['topic'], 'y': q['year'], 'm': q['marks'], 'ty': t,
            'k': key, 'ks': src, 'n': ord(choices) - 64 if choices else 0,
            'b': 1 if q.get('syllabus_status') == 'borderline' else 0,
            'g': group_of.get(q['question_id'], ''),
            'img': [[c['file'], c['width'], c['height']] for c in q['original_crops']],
            'l': 'GATE ' + str(q['year']) + (' ' + q['session'] if q.get('session') else '') + ', Q' + str(q['number']),
            'tt': topic_titles.get((q['subject_dir'], q['topic']), q['topic']),
        })
    # A linked group is usable only if all its members made it into the pool.
    members = collections.Counter(p['g'] for p in pool if p['g'])
    expected = collections.Counter(group_of.values())
    for p in pool:
        if p['g'] and members[p['g']] != expected[p['g']]:
            p['g'] = ''  # partner missing: treat as a standalone question only if it reads standalone
            p['x'] = 1   # ...but mark it so the sampler skips it (its text relies on shared data)
    pool = [p for p in pool if not p.get('x')]

    subjects = [s for s in sorted(titles) if s != GA]
    names = {s: ('Engineering Mathematics' if s == EM else titles[s]) for s in titles}
    weights = {
        'subjects': {s: round(subj_share.get(s, 0), 3) for s in subjects},
        'topics': {s: {t: round(v, 4) for (ss, t), v in topic_share.items() if ss == s} for s in subjects + [GA]},
        'type_mix': _type_mix(questions, mix_papers),
    }
    return {
        'version': 1, 'latest': latest, 'recent_from': latest - RECENT_YEARS + 1, 'recent_papers': len(recent),
        'mix_from': latest - TYPE_MIX_YEARS + 1,
        'ga': GA, 'names': names, 'weights': weights, 'pool': pool,
        'skipped': dict(skipped.most_common()),
    }


def _nat_agrees(official, derived):
    """For NAT, a derived single value inside the official range agrees."""
    if '..' not in official or '..' not in derived:
        return False
    lo, hi = map(float, official.split('..'))
    dlo, dhi = map(float, derived.split('..'))
    return lo - 1e-9 <= dlo and dhi <= hi + 1e-9


def write_mock(out, questions, titles, topic_titles, ds):
    data = build(questions, titles, topic_titles, ds)
    (out / 'mock').mkdir(parents=True, exist_ok=True)
    (out / 'mock/pool.json').write_text(json.dumps(data, ensure_ascii=False, separators=(',', ':')))
    return data
