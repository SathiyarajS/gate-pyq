# Enhanced private preview review

This checkpoint adds pinned, locally served KaTeX 0.16.22 and Pagefind 1.4.0. No external runtime CDN is used and no deployment is authorized by these tests.

## Independent checks

- Production math formatting tested for explicit LaTeX delimiters, preservation of legacy single-dollar end markers, escaped HTML/attribute content, and code-block isolation.
- The actual pinned KaTeX parser passes ordinary math. External/HTML-producing and unknown commands preserve the original text rather than execute or silently discard it. `trust: false`, strict errors and expansion/size limits are set.
- Production practice logic passes twelve official-key/conditional-answer cases, blocked-storage initialization and nested base-link checks.
- The actual generated Pagefind WASM index is exercised through a local file-backed fetch adapter. All 3,406 unique question records are indexed; a cache search returns 88 results, and filtering to 2026 returns four, with correct metadata and nested-base paths. This adapter tests index behavior, not a browser or network server.
- Search documents contain only question context and metadata, not detailed solutions or answer keys. Search hits link to canonical question pages.
- Clean static site and print-HTML checks are recorded separately in `site-preview-review.json` and the reproducible audit scripts.

## Limits

No interactive browser, responsive screenshots, screen-reader inspection or actual PDF rendering is claimed. Chromium launch is blocked by runtime socket restrictions. Mathematical layout is not visually certified by parser tests. Original transcription/redraw, remaining crop reviews, historical completeness and redistribution rights remain separate gates. The default release build remains fail-closed; only explicitly labelled private previews are generated.
