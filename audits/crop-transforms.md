# Optional source-preserving crop rotation

Legacy crop records remain unchanged: `bbox` is measured in original page PDF
points and MuPDF renders that source rectangle directly. Existing output bytes
remain unchanged.

A reviewed crop may explicitly opt into rigid full-page rotation:

```json
"transform": {"rotation_degrees": -2, "coordinate_space": "rotated_page"}
```

For such a record only, `bbox` is in PDF points in the rotated page's enclosing
axis-aligned rectangle, translated so its upper-left is (0, 0). Positive angles
are clockwise in downward-y PDF coordinates. Only finite angles within ±10°
are supported. Unknown transform fields or coordinate spaces fail preflight.
The renderer applies rotation and translation to the entire source page with
MuPDF at the requested scale, then extracts the integer pixel rectangle with
outward-rounded edges. It does not mask, erase, threshold, redraw, or retouch
any pixel. Source-file SHA-256 preflight still runs before rendering any job.
WEBP quality remains 80, at default 3× (216 DPI), with the existing PNG fallback.

Preparation can retain `original_source_quad` (TL, TR, BR, BL inverse-mapped
source points) and `original_source_bbox` (that quadrilateral's enclosing source
rectangle) as provenance. These are derived geometric coordinates, not a
claim that an earlier rejected rectangular crop is equivalent. Render geometry
comes exclusively from `bbox` and `transform`; provenance is not a second clip.
`scripts/render_crops.py:crop_source_polygon` exposes this inverse mapping.

Overlap checks must compare bboxes only within identical `(file, page,
transform)` groups. Missing transform means original source coordinates.
Canonicalize the transform object (for example JSON with sorted keys). If a
file/page has mixed transforms, fail for explicit review or compare the
inverse-mapped source polygons. Never silently ignore cross-transform pairs,
and never interpret overlap of enclosing source rectangles as polygon overlap.

CS-2008 p15 uses exactly six transformed records: Q71–Q73, parts 1 and 2.
The three shared-context parts have identical bounds; each own-question part
is separate. All six use −2°. No other record on this source page remains in
untransformed coordinates. Original source scan blur and show-through remain.
These geometry changes alone do not confer independent review or verification.

Run regression tests: `python -m unittest discover -s tests -v`.
An external proposal file can be rendered without changing repository records:
`python scripts/render_crops.py --allow-draft --crops PATH --output DIRECTORY`.
