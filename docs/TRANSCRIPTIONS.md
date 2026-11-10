# Phase 5 transcription contract

`data/transcriptions/<paper_id>.json` maps known question IDs to entries. Missing,
draft, incomplete-review or unsafe entries never replace the existing fallback.
The site remains a private preview and the release gate is unchanged. Rendering a
comparison page is **not** an independent review or a verification certificate.

Minimal draft:

```json
{"CS-2026-S2-Q1": {
  "stem": "Exact source wording with $x$ or $$x^2$$.",
  "options": {"A": "First", "B": "Second"},
  "figures": [], "status": "draft", "checked_pages": [1], "notes": ""
}}
```

Use the actual corpus question ID and physical source pages. Options preserve
stored order, never inferred or sorted. The renderer supports escaped text,
inline/display LaTeX, fenced code, inline code, bold/italic, simple lists, and
Markdown tables. In prose, `\|` is a literal pipe inside a table cell and `\*`
is a literal asterisk (for example `20\*` for a starred key), so neither is read
as markup. Figure SVGs may use `font-style="italic"` for labels the source
prints in italics. Raw HTML, including HTML tables, is displayed literally;
merged-cell tables must be safely represented in a figure or kept draft pending
a structured-table extension. Legacy paraphrases/solutions retain their existing
math handling, including literal single-dollar end-markers. Only explicit
transcription content enables `$...$` inline math.

An entry is eligible for site display only with `status: "verified"`, a valid
non-future ISO `verified_on` date, nonempty `notes` describing what was checked,
and `checked_pages` covering every recorded source page, plus:

```json
"verification": {
  "method": "independent-visual-comparison",
  "transcriber": "stable preparer identity",
  "reviewer": "different stable reviewer identity",
  "solution_checked": true,
  "rendered_comparison_checked": true
}
```

Only enter these fields after a separate pass comparing **every** symbol,
number, option, figure label and edge against the rendered originals, and
checking the existing solution still matches. `rendered_comparison_checked`
requires reviewing the actual production-rendered comparison for every question,
including typeset math, tables, options and inline vector figures. JSON/source
checks and SVG structural inspection alone do not satisfy it. If browser review
is blocked, retain draft status even after source-level review. The production-rendered
comparison can be reviewed from screenshots: `python scripts/screenshot_comparisons.py <paper>`
writes `audits/compare-shots/<paper>/<id>-desktop.jpg` and `-mobile-dark.jpg` (original crop
beside the rendered entry), and `.github/workflows/review-shots.yml` publishes the same images
to the `review-shots` branch. Inspecting every screenshot for every question satisfies
`rendered_comparison_checked`; see HANDOFF.md §3.3. Structural validation cannot
establish that this review actually happened. Review metadata and notes remain
auditable in the comparison page. Unknown metadata fields are retained in the
source but do not grant display approval.

## Shared context

Store context once under the paper's reserved `_contexts` mapping. A question
uses `"shared_context_refs": ["common-1"]`. Each context has the same stem,
figures, status and independent-review fields as an entry, with its own nonempty
physical `checked_pages`. All referenced contexts must independently pass the
review gate before a verified question displays. Nested context references are
not supported. If the original record declares shared context or a context
reference, reviewed shared_context_refs are required; a verified stem alone
cannot silently hide that original context. Contexts are rendered before the stem and included in search.

## Figures

Only local `figures/<safe-name>.svg` paths are accepted. SVGs are parsed and
allowlisted, then serialized as **inline SVG**, so `currentColor` follows the
host light/dark theme. Keep the editable source next to the SVG as required by
CODEX_INSTRUCTIONS.md (a hand-authored SVG is itself its editable source).

Use a finite positive viewBox, no root fixed width/height, a meaningful `<title>`
or aria-label, real text at least 12px, and only `currentColor` or `none` fills
and strokes. Check the effective text size on mobile in the eventual visual QA.
Scripts, event handlers, foreignObject, images, animation, styles/CSS, hrefs,
external resources, declarations/entities and unsafe paths are rejected. Only
local marker URL references are supported. Unsupported/invalid figures make the
whole entry fall back safely; figures are never silently omitted from a
verified entry. Keep complex unsupported figures in draft until redrawn safely.

## Reviewing and building

- `python scripts/compare_transcription.py <paper_id>` creates a private ignored
  HTML aid using the same safe renderer, showing drafts as well as verified
  entries beside existing crop assets. Missing crops remain explicit blockers.
- With `npm ci`, math uses pinned local KaTeX. Without it, original LaTeX remains
  readable and typeset review is pending. No CDN or untrusted HTML is used.
- `python scripts/build_site.py --preview` uses eligible transcriptions and
  retains no-crop fallback. `--with-reviewed-crops` includes originals behind
  “View original” for verified transcriptions, and as primary fallback otherwise.
- Print HTML drafts reuse the site's rendered fragments and local math assets.
  HTML generation does not constitute PDF rendering or visual verification.
- `build-report.json` contains `redrawn_questions` and `redrawn_by_paper`, counting
  only entries accepted by this loader. `python scripts/update_redrawn_coverage.py`
  updates only the Redrawn column of COVERAGE.md from the same eligibility rules.

Browser/PDF visual checks, source-content review and publication authorization
remain separate gates. No automatic command may manufacture review metadata.
