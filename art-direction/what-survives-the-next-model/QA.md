# Article 2 illustration QA

Checked 13 September 2026 against the local Astro production build.

## Visual review

- Desktop: Google Chrome 152, 1440 CSS pixels. Reviewed the opening, premise, intervention, and successor sections from the production build.
- Mobile: Google Chrome 152 through DevTools device-metric emulation, 390 CSS pixels. This avoids Chrome headless's 500-pixel command-line minimum. Reviewed the same four sections with all lazy images decoded before capture.
- The article has no horizontal overflow at either width.
- All figures retain the full 3:2 composition. The social crop preserves the researcher and all three hidden provider states at 1200 × 630.
- Captions remain legible and visually subordinate. Alt text describes the visible scene; captions state the relationship.
- The generated series matches Part I's near-white paper, spare charcoal contour, flat stone shapes, dry texture, negative space, and restrained oxide-red semantics. It does not use the earlier Part II draft's sepia engraving treatment.

## Editorial review

- Preserved Sergio's thesis, refund narrative, falsifiers, and claim boundaries.
- Removed the manuscript-level duplicate title and deck because the site masthead supplies them.
- Split the dense model-continuity passage into shorter argumentative steps.
- Added one bounded bridge to findings, dependencies, frozen comparisons, and qualified packs; it explicitly says the integrated product and customer results do not yet exist.
- Used four figures as pacing breaks: opening ambiguity, premise status, attribution by intervention, and successor reconstruction.

## Automated verification

`npm run verify` passes and covers the Astro type/build checks, page-specific social metadata, image dimensions and hashes, illustration provenance, local links, captions, alt text, the responsive breakpoint, receipts-manifest integrity, and byte-identical reruns of the finite refund and judge-calibration checks.

The in-app browser surface was unavailable during this task. Visual QA therefore used the installed local Chrome against the production build; nothing was pushed, deployed, or published.
