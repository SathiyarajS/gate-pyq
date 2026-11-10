#!/usr/bin/env python3
"""One-off repair: restore the space lost between an English word and a number
("costs7n" -> "costs 7n", "are13" -> "are 13") in solutions and question text.

Conservative by design:
- only prose words seen standalone at least 5 times in the corpus are split;
- identifier-like stems (log2, fun1, ptr1, x1, T2, ...) are never touched;
- text inside ``` fences or `inline code` is never touched;
- the same mapping is applied to data/questions.json and subjects/**/*.md.
Run with --dry-run to print a sample of changes.
"""
import collections, json, re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
FIELDS = ("solution", "question_text", "derived_answer")
# Stems that are routinely glued to digits on purpose (identifiers, functions, units, subscripts).
KEEP = set("""log ln lg exp mod fun func len ptr str expr tau sigma delta lambda alpha beta gamma theta phi pi mu rho omega epsilon
x y z u v w a b c d e f g h i j k l m n o p q r s t var val tmp temp arr node next prev buf addr reg sum0 ip mac sha md
http https ipv tcp udp inc dec add sub mul div jmp jz mov load store push pop call ret
abc xyz root left right child parent key data info item elem id num cnt count idx flag bit byte word line row col
fn proc thread lock sem mutex state q0 st op opd arg param f0 base int char float double long short void main
binary print argument source wants bucket courseno man test top age semaphore operation tree parameter return returns
cs gate set paper sec section page fig figure table option case step stage type level layer pass round phase part
""".split())
WORD_GLUE = re.compile(r"(?<![A-Za-z0-9_$\\])([a-z]{2,})(?=(\d))")
CODE = re.compile(r"(```.*?```|`[^`\n]*`)", re.S)

def standalone_counts(texts):
    c = collections.Counter()
    for t in texts:
        for w in re.findall(r"(?<![A-Za-z0-9_])([a-z]{2,})(?=[\s,.;:)])", CODE.sub(" ", t)):
            c[w] += 1
    return c

def make_fixer(counts):
    ok = {w for w, n in counts.items() if n >= 5 and w not in KEEP}
    def fix_prose(s):
        return WORD_GLUE.sub(lambda m: m.group(1) + " " if m.group(1) in ok else m.group(1), s)
    def fix(text):
        if not isinstance(text, str):
            return text
        parts = CODE.split(text)
        return "".join(p if CODE.fullmatch(p) else fix_prose(p) for p in parts)
    return fix

def main():
    dry = "--dry-run" in sys.argv
    qpath = ROOT / "data/questions.json"
    raw = qpath.read_text()
    recs = json.loads(raw)
    counts = standalone_counts(str(r.get(f) or "") for r in recs for f in FIELDS)
    fix = make_fixer(counts)
    changes = []
    for r in recs:
        for f in FIELDS:
            new = fix(r.get(f))
            if new != r.get(f):
                changes.append((r["question_id"], f, r[f], new))
                r[f] = new
    md_changed = 0
    for md in sorted((ROOT / "subjects").rglob("*.md")) + sorted((ROOT / "supplemental").rglob("*.md")):
        text = md.read_text()
        new = fix(text)
        if new != text:
            md_changed += 1
            if not dry:
                md.write_text(new)
    print(f"{len(changes)} field edits in {len({c[0] for c in changes})} questions; {md_changed} markdown files")
    if dry:
        import random
        random.seed(1)
        for qid, f, old, new in random.sample(changes, min(40, len(changes))):
            # show the first differing window
            i = next(i for i, (a, b) in enumerate(zip(old, new)) if a != b)
            print(f"{qid:18} {f:15} {old[max(0, i-30):i+15]!r} -> {new[max(0, i-30):i+16]!r}")
        return
    # Keep the file's original compact, single-line formatting.
    qpath.write_text(json.dumps(recs, ensure_ascii=False, separators=(",", ":")) + ("\n" if raw.endswith("\n") else ""))

if __name__ == "__main__":
    main()
