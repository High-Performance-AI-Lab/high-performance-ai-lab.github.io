# Evaluation Workbench explainer QA

Checked 16 September 2026 against the local Astro production build.

## Editorial and product review

- Separates implemented foundation, proposed M1, and later customer/research work throughout the page.
- Preserves the current evidence boundaries: recorded replay is not fresh execution; a worker transcript is not a provider signature or independent effect; a hash proves identity, not truth; native refusals/errors/unknowns are not translated into success.
- Uses the merged PR #1 code identity `222fadc`, merged PR #6 architecture identity `426ec91`, and PR #7 review head `e75be60` as the page snapshot.
- Includes the separate `lab-specs` layer at local head `94abbe3`: Workbench definition packets are distinguished from canonical JSON, eval receipts/diffs, ProofPack evidence bundles, Assay gates, grader protocol direction, and cross-language conformance.
- Labels the on-page receipt JSON as an abridged anatomy rather than a valid conformance fixture; the spec's exact-member and closed-vocabulary rules remain authoritative.
- Labels all made-up Edge/fx API code as illustrative and proposed.
- Retains the current PR #7 state: substantive scope accepted, exact-base/immutable-link correction still requested, and no live dispatch authorized.
- Adds critical recommendations rather than restating the plan: protect a five-minute honest-verdict path, measure total human/compute effort and false alarms, keep Edge optional for accepted packs, and show the exact egress envelope.

## Illustration review

- Inspected all three 1536 × 1024 sources at full resolution.
- All three use the HPAL paper/charcoal/cut-paper grammar and restrained oxide-red semantics.
- The hero leaves the evaluation loop visibly open; the fx image keeps a missing observation channel empty; the Edge image keeps keys, retained evidence, and the local evaluation loop on the customer side.
- Captions state the claim boundary and alt text describes the visible scene.
- Source PNGs, public WebP derivatives, prompts, reference hashes, dimensions, byte counts, and output hashes are recorded in `provenance.json`.

## Automated verification

- `git diff --check` passes.
- `npm run build` passes with zero Astro errors, warnings, or hints.
- Built HTML has one `h1`, three images with nonempty alt text, `noindex, nofollow`, and no broken internal fragment links, including the spec-format navigation target.
- Public illustration assets are exact 1536 × 1024 WebP files.
- The `/docs/eval-workbench/` page is intentionally absent from the public index and navigation.

## Visual QA limitation

The in-app browser had no available browser surface in this session. The composed desktop/mobile page therefore has not received screenshot-based visual QA. Responsive rules were reviewed at the 1180, 820, and 560-pixel breakpoints, but one browser pass remains required before any public navigation or deployment decision. The page remains unlinked and noindexed; this pull request is a review surface, not publication approval.
