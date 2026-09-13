---
name: hpal-editorial-illustrations
description: "Create, art-direct, place, and verify conceptual raster illustrations for High Performance AI Lab essays. Use when an HPAL article needs a hero, inline editorial figure, social crop, alt text, caption, or a new image that must match the established Evals as Theory Building visual language."
---

# HPAL Editorial Illustrations

Create one readable metaphor at a time in HPAL's established print-editorial visual system. Preserve the author's argument; the illustration should reveal a relationship already present in the prose, not add a new claim.

## Workflow

1. Locate the website repository. The canonical reference set is `public/img/articles/evals-as-theory-building/`, especially `map-becomes-territory.webp`, `evaluator-under-evaluation.webp`, and `eval-loop-retained-failures.webp`.
2. Read the target passage and the paragraphs on both sides. Write a one-sentence visual thesis and a one-sentence claim boundary before prompting.
3. Inspect at least three canonical images with the image-viewing tool. Treat them as style references, not edit targets.
4. Read [references/style-guide.md](references/style-guide.md). Select a scene that makes the passage's causal structure visible without labels.
5. Use the built-in image-generation workflow for raster art. Label each input as a style reference. Generate one distinct asset per call; do not ask for a contact sheet.
6. Inspect the result at full size. Reject it if the metaphor is ambiguous, the red accent has become decoration, the people or hands are implausible, or it has drifted into sepia engraving, glossy 3D, photorealism, or generic corporate vector art.
7. Preserve the generated source outside `public/`. Convert the selected site asset to WebP at exactly 1536 × 1024 without changing its composition. Keep a 1200 × 630 JPEG social crop only when the article uses it in frontmatter.
8. Place the image after the passage that creates the question it answers. Add a factual alt description and a short interpretive caption. The alt describes the visible scene; the caption states the relationship.
9. Record the prompt, reference files, output hashes, dimensions, generated-source path, site path, tool, and visual QA in a repository-tracked provenance file. Never call generated artwork experimental evidence.
10. Build the site and inspect the article at desktop and mobile widths. Check pacing, crop, caption wrapping, loading behavior, alt text, and social metadata.

## Prompt skeleton

```text
Use case: illustration-story
Asset type: conceptual editorial illustration for an HPAL essay
Primary request: <one physical scene expressing one relationship>
Input images: Image 1, Image 2, Image 3 are style references only
Style/medium: spare mixed-media editorial collage on warm off-white paper; loose charcoal-black contour drawing; flat cut-paper shapes; dry, imperfect screenprint texture; natural adult figures; generous untouched paper
Color palette: warm off-white, charcoal, stone grey, and one restrained oxide red-orange accent
Composition/framing: landscape 3:2, one legible focal action, broad negative space, no border
Claim boundary: conceptual metaphor only; not research evidence
Constraints: no words, letters, numbers, equations, logos, UI, watermark, robot, glossy 3D, photorealism, dense cross-hatching, sepia wash, gradient, or decorative clutter
```

Name assets by idea, not section number: `open-premise.webp`, not `figure-02.webp`.

## Editorial rules

- Use a human-scale physical action: drawing, measuring, carrying, repairing, exchanging, opening, or tracing.
- Use red only for the consequential object, path, intervention, or state change.
- Prefer a single scene over a literal flowchart. When exact labels are essential, build a native SVG or HTML diagram instead of asking a raster model to typeset them.
- Do not depict a named author unless the author explicitly requests a likeness and supplies or approves a reference portrait.
- Do not reuse a Part I composition. Match its visual grammar while making a new scene.
- Use no more figures than the article's rhythm needs. A long essay typically supports a hero and two or three inline figures.
- Keep uncertainty visible. Open, unresolved, or missing support must not look complete.

## Handoff

Report the final asset paths, exact prompts, built-in generation mode, reference set, any rejected or unresolved visual issues, and the verification commands that passed. If the website repository is dirty, preserve unrelated changes and identify them explicitly.
