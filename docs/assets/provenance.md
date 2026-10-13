# Asset provenance and inspection

All dates below use 2026-10-13, America/New_York. These are original AI-generated design assets created for this request with the built-in `image_gen.imagegen` tool. No image or source asset was copied from the previous Mental Health project, a stock library, a social-media dataset, or an existing brand. The underlying image model identifier is not exposed by the tool; it is unknown.

## Final assets

| Asset | Project file | Material | Dimensions | Bytes | Generation result |
| --- | --- | --- | --- | --- | --- |
| Satin bow | [bow.png](../../frontend/public/assets/bow.png) | Folded light ballet-pink satin fabric | 1024 × 670 RGBA | 828,279 | `exec-53a67695-e007-4bfd-ab10-d231922ada19.png` |
| Balloon | [balloon.png](../../frontend/public/assets/balloon.png) | Glossy light ballet-pink latex rubber | 745 × 1024 RGBA | 545,265 | `exec-503a2930-19ce-4c4f-8878-18d87fc65722.png` |

The [exact prompts](generation-prompts.md) and [machine-readable dimensions, crop boxes, alpha checks and SHA-256 hashes](asset-metadata.json) are retained. The original built-in outputs remain in the tool's generated-image directory; the project is self-contained because the selected web outputs are committed inside `frontend/public/assets/`.

## CHECK → TAKE ACTION → VERIFY

**CHECK:** Read the full master brief and new-project AGENTS.md; verified the independent intended project path; inspected the empty asset directory; located bundled Python/Pillow. Generation and processing commands were recorded before use in [generation-prompts.md](generation-prompts.md).

**TAKE ACTION:** Issued one built-in transparent generation per object. Used Pillow only to find meaningful alpha bounds, crop with an eight-pixel source margin, reduce the longest edge to 1024 pixels, and optimize lossless PNG storage. The threshold of alpha >5 was used only to find the crop rectangle; pixel alpha within the selected rectangle was preserved. No content retouching, recoloring, background removal, or synthetic drawing was performed with Python.

**VERIFY:** Opened both actual generated PNG files with `view_image`. Inspected both final assets composited on white for QA, also with `view_image`. The bow visibly retains two folded loops, central gathered knot, fabric thickness, fine weave, satin sheen and two ribbon tails. The balloon visibly retains broad studio highlights, rounded latex volume, tapered neck and a tied knot. They share a light pink family but visibly differ in material. No text, watermark, string, or additional object appears. Final PNGs have nonconstant alpha spanning 0–255; 314,992 bow pixels and 257,498 balloon pixels are fully transparent. White QA previews showed no broad background halo.

The white composites ([bow preview](bow-white-preview.png), [balloon preview](balloon-white-preview.png)) are documentation inspection artifacts, not the transparent runtime assets. Material evaluation is visual judgment, not a measured optical test.

## Presentation and extension limits

The decorative bow belongs in the asset/object registry and reusable presentation component, with decorative status, placement, dimensions, material, reduced-motion behavior and this provenance reference. It has no pacing or interaction authority.

The balloon is an exercise timing metaphor. The generated source is a single **full-inflation** photograph-like cutout. Low and mid states implemented by continuous scale/deformation are a **material approximation** that reuses the same source highlights and knot; they are not separate generated or photographed physical inflation states. An alternative pacing object must accept normalized progress only and cannot change breathing timing, instructions or safety controls.

Any color variants implemented through frontend filters are visual recoloring approximations. They preserve the source shading pattern rather than simulate physical changes in colored latex. Pink is the generated original; optional red is a prototype visual preference. Visual consistency of low/mid/full states and recolors must be checked in actual browser screenshots.

## Rights and public-release limitation

These are original generated outputs for the user's request, with no intentionally copied third-party artwork or logos. No source asset license was required from a stock provider. The tool did not return a specific output license or commercial clearance certificate, and this record does not establish copyright protectability, exclusive ownership, noninfringement or commercial rights. Use remains subject to the user's applicable tool/service terms. A future public product still needs an asset/content rights review; public source publication of this coursework design is not a commercial-readiness claim.
