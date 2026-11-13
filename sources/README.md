# Source papers

The original question papers and answer keys are **not stored in this repository**. What is stored:

- `site-assets/q/`: the cropped image of every question, rendered once from its source paper. The website and PDFs use only these images.
- `audits/crop-source-map.json`: for each source PDF, its URL (or the member name inside the official GATE 2026 `CS.zip` archive), page count and **sha256 fingerprint**.
- `sources/manifest.json`: the same URLs and fingerprints as recorded when the papers were first fetched.
- `data/crops.json`: the page and box each question image was cut from.

To get the PDFs on your machine (only needed to re-render an image or to transcribe a question), run:

```sh
python scripts/fetch_sources.py
```

It downloads each paper from its recorded link and keeps it only if its sha256 matches the recorded fingerprint. If a link no longer works, the committed images remain the record of that paper.

The question papers belong to their original setters (the organising IITs/IISc). This project claims no rights in them; see `LICENSE`.
