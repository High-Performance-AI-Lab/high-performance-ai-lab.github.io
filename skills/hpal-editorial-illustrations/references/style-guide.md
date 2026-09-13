# HPAL illustration style guide

## Canonical visual grammar

The reference series in `public/img/articles/evals-as-theory-building/` uses:

- a warm near-white paper field rather than a yellow or sepia ground;
- loose charcoal-black contours with visibly handmade edges;
- flat off-white, stone-grey, charcoal, and oxide-red paper or screenprint shapes;
- subtle grain and imperfect ink coverage, with almost no tonal modelling;
- naturally drawn adult researchers or operators at a physical task;
- one surreal but immediately readable material metaphor;
- large areas of unmarked paper and a low object count;
- oxide red as semantic emphasis, never ambient decoration;
- no embedded text, labels, logos, interfaces, robots, glow, or gradients.

The work should feel assembled from ink, dry pigment, and cut paper. It should not look like an antique engraving. Dense cross-hatching, uniformly beige paper, portrait realism, and elaborate apparatus are drift even if their palette is nominally correct.

## Reference roles

- `map-becomes-territory.webp`: best reference for line economy, negative space, and a red path becoming physical structure.
- `smoke-without-fire.webp`: best reference for a large semantic red mass and a hidden causal mechanism.
- `evaluator-under-evaluation.webp`: best reference for human scale, absurd-but-clear instruments, and central object hierarchy.
- `assay-fixed-gate.webp`: best reference for evidence represented as tactile, sealed matter.
- `eval-loop-retained-failures.webp`: best reference for process, retained paths, and a broad scene with two actors.

Use three references that cover composition, people, and the role of red. More references can blur the direction.

## Semantic test

Before generating, finish these sentences:

- The reader should see that **...**
- Red marks **...**
- The human action is **...**
- The image must leave **...** unresolved.

After generating, cover the caption. A reader should still recover the central relationship in a few seconds. If they can only describe an attractive laboratory scene, the image has failed.

## Web production

- Article asset: 1536 × 1024 WebP, 3:2, normally `loading="lazy" decoding="async"`.
- Opening hero: same dimensions, with `fetchpriority="high"` instead of lazy loading.
- Social asset: 1200 × 630 JPEG, composed or cropped so the focal action survives the narrower frame.
- Put public files under `public/img/articles/<article-slug>/`.
- Use a `<figure class="article-illustration">` and a nonempty `<figcaption>`.
- Alt text names the visible subject, action, and consequential red element. It does not repeat the caption or begin with “Image of”.
- Captions are concise interpretive sentences, not mini-paragraphs.

## Provenance minimum

For each selected asset record:

- stable asset name and role;
- exact final prompt;
- generation tool and mode;
- reference paths and SHA-256 hashes;
- generated source path and SHA-256 hash;
- public asset path, dimensions, media type, bytes, and SHA-256 hash;
- one short visual-QA note;
- a statement that the image is conceptual artwork, not evidence.
