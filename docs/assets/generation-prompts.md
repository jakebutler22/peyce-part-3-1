# Original raster asset generation

2026-10-13. Workflow: CHECK → TAKE ACTION → VERIFY. The new project and AGENTS.md were inspected before changes. No previous-project assets were copied.

## Planned commands and environment

- Built-in `image_gen.imagegen`, one independent transparent generation per asset. No CLI, API key, or downloaded third-party asset.
- Built-in `view_image` to inspect the actual returned pixels.
- Bundled Python 3 with Pillow at `/Users/jakebutler/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3` for alpha-aware crop, resize and PNG compression only. No image content is painted, synthesized or retouched with Python.
- Project output: `frontend/public/assets/bow.png` and `frontend/public/assets/balloon.png`.

## Bow prompt (exact)

```text
Use case: product-mockup
Asset type: original decorative cutout for the Peyce clickable design prototype
Primary request: one elegant soft ballet-pink satin ribbon bow, photographed as a real physical satin fabric object.
Subject: exactly one tied bow with two generous folded ribbon loops, a compact gathered center knot, visible fabric thickness along folded edges, and two graceful short ribbon tails with angled ends.
Style/medium: hyperrealistic premium studio product photography. The material is satin fabric, with fine woven texture, subtle creases, soft luminous satin sheen and believable self-shadowing, never plastic or latex.
Composition/framing: frontal view with a slight natural asymmetry, horizontally wide bow, all tails and loops fully visible, tightly but safely framed. The bow is isolated with genuinely transparent surrounding pixels, no floor, no room and no backdrop.
Lighting/mood: broad soft studio light from upper left; highlights follow the folds and convey fabric thickness; subtle shaded undersides and contact shading inside the knot.
Color palette: light ballet pink closely related to #F4D4E1; soft pink shadows, no vivid magenta.
Text: no text.
Constraints: original unbranded object, no watermark, no people, no hands, no box, no additional objects, no external cast floor shadow, no checkerboard painted into image, no border. Transparent background.
```

## Balloon prompt (exact)

```text
Use case: product-mockup
Asset type: original exercise pacing cutout for the Peyce clickable design prototype
Primary request: exactly one fully inflated soft ballet-pink LATEX balloon, photographed as a real physical balloon.
Subject: one smooth pear-shaped inflated latex balloon with a small pinched neck and clearly visible tied knot at the bottom. Slight natural taper toward the neck; round upper volume. No string.
Style/medium: hyperrealistic premium studio product photography. Clearly latex rubber, with believable smooth glossy latex surface, broad soft highlights, subtle specular highlight and rounded shaded volume; no fabric weave, metallic foil, satin, glass, ceramic or cartoon look.
Composition/framing: frontal upright view, isolated single balloon, the entire balloon and bottom knot fully visible, generous small safety margin, tightly but safely framed. Genuinely transparent surrounding pixels, no floor, no scene and no backdrop.
Lighting/mood: soft upper-left studio illumination, a broad white highlight near upper left, smaller subtle reflections and soft pink shade toward lower right. Keep the pink volume believable and the knot dimensional.
Color palette: light ballet pink in the same family as #F4D4E1, slightly warmer rich pink rubber color to retain material depth, no vivid magenta.
Text: no text.
Constraints: original unbranded object, no watermark, no symbols, no people, no hands, no extra balloons or objects, no external floor shadow, no checkerboard painted into image, no border. Transparent background.
```

## Tool and model disclosure

Built-in `image_gen.imagegen` is the intended tool. Its underlying image model identifier is not exposed by the callable tool metadata and will be recorded as unknown. The asset prompts were shaped by an AI coding assistant; no claim is made that these images were photographed or hand made.


## Observed generation and processing results

Both built-in generation calls completed successfully in one generation cycle. No image-content repair was needed.

- Bow source: `exec-53a67695-e007-4bfd-ab10-d231922ada19.png`, 1536 × 1024 RGBA.
- Balloon source: `exec-503a2930-19ce-4c4f-8878-18d87fc65722.png`, 1024 × 1536 RGBA.
- Both sources were inspected with built-in `view_image`.
- Alpha-aware crop (meaningful alpha threshold 5, eight-pixel source padding), LANCZOS downscale to longest edge 1024, and optimized PNG storage used bundled Pillow.
- Final selected runtime files are `frontend/public/assets/bow.png` and `frontend/public/assets/balloon.png`. They retain an RGBA alpha channel with fully transparent pixels.
- White-composite QA previews were generated only to inspect alpha edges and material appearance. They are kept in `docs/assets/` as inspection evidence and are not used by the frontend.

See [provenance.md](provenance.md) for actual pixel checks, rights limitations and single-source inflation/recolor approximation.
