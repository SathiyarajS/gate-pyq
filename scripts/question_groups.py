"""Reviewed study groups. Discovery output is deliberately not an input here."""
import json
import re


def load_patterns(root, questions):
    path = root / 'data/problem-patterns.json'
    if not path.exists():
        return []
    by_id = {q['question_id']: q for q in questions}
    result, seen, assigned = [], set(), set()
    for group in json.loads(path.read_text()).get('groups', []):
        gid = group.get('id', '')
        if not re.fullmatch(r'[a-z0-9-]+', gid) or gid in seen:
            raise ValueError('Invalid or duplicate pattern id: ' + gid)
        seen.add(gid)
        status = group.get('status')
        if status not in ('candidate', 'reviewed', 'rejected'):
            raise ValueError('Pattern needs explicit review status: ' + gid)
        members = group.get('members', [])
        if len(members) < 2 or len(set(members)) != len(members) or any(i not in by_id for i in members):
            raise ValueError('Invalid pattern members: ' + gid)
        if any(by_id[i].get('subject_dir', by_id[i].get('subject')) != group.get('subject') for i in members):
            raise ValueError('Pattern crosses subject boundaries: ' + gid)
        if group.get('representative') not in members:
            raise ValueError('Pattern representative must be a member: ' + gid)
        if status != 'reviewed':
            continue  # Even perfectly identical candidate text cannot hide a question.
        review = group.get('review', {})
        sources = review.get('sources', [])
        if (review.get('method') != 'source-page-comparison' or not review.get('reviewer')
                or not re.fullmatch(r'\d{4}-\d{2}-\d{2}', review.get('reviewed_on', ''))
                or {s.get('question_id') for s in sources} != set(members)
                or len({(s.get('question_id'), s.get('file'), s.get('page')) for s in sources}) != len(sources)
                or any(not s.get('file') or not s.get('page') or not s.get('notes')
                       or not re.fullmatch(r'[0-9a-f]{64}', s.get('sha256', '')) for s in sources)
                or not group.get('rationale') or not group.get('title')):
            raise ValueError('Reviewed pattern lacks source comparison evidence: ' + gid)
        if assigned.intersection(members):
            raise ValueError('Overlapping patterns must not duplicate or silently hide questions: ' + gid)
        assigned.update(members)
        result.append(group)
    return result


def study_units(questions, groups, sortkey):
    """Partition a subject into groups + singletons, with every question once.

    The representative is explicit for patterns, newest for known repeats.
    Only members in this subject are folded, even if repeat links cross subjects.
    """
    by_id = {q['question_id']: q for q in questions}
    units, used = [], set()
    for group in groups:
        members = sorted((by_id[i] for i in group['members'] if i in by_id), key=sortkey)
        if not members:
            continue
        ids = {q['question_id'] for q in members}
        if used.intersection(ids):
            raise ValueError('Overlapping study groups')
        used.update(ids)
        representative = by_id.get(group.get('representative'))
        if representative is None or representative['question_id'] not in ids:
            representative = members[0]
        units.append({'representative': representative,
                      'alternatives': [q for q in members if q is not representative],
                      'group': group if len(members) > 1 else None})
    units.extend({'representative': q, 'alternatives': [], 'group': None}
                 for q in questions if q['question_id'] not in used)
    return sorted(units, key=lambda unit: sortkey(unit['representative']))


def repeat_groups(repeats):
    seen, result = set(), []
    for info in repeats.values():
        members = tuple(info['group'])
        if members not in seen:
            seen.add(members)
            result.append({'members': members, 'title': 'Known repeat',
                           'rationale': 'Previously recorded repeat: same setup and requested answer, possibly with changed values. Review coverage is incomplete.'})
    return result
