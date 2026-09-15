# Evaluation Workbench field guide

This is the maintainer note for the internal Evaluation Workbench product
explainer. The page gives reviewers both a ten-foot orientation and a detailed
view of the current foundation, the short-term fx milestone, and the longer-term
customer and research direction.

## Review locally

```bash
npm install
npm run dev
```

Open <http://localhost:4321/docs/eval-workbench/>. The page is intentionally
absent from the public homepage and navigation and emits `noindex, nofollow`.
Opening a pull request makes the source reviewable; it does not approve a public
link or deployment.

## Files

- Page: `src/pages/docs/eval-workbench.astro`
- Styles: `src/styles/eval-workbench.css`
- Web assets: `public/img/explainers/eval-workbench/`
- Source art, prompts, provenance, and QA: `art-direction/eval-workbench-explainer/`

## Source snapshot and claim boundaries

The synthesis was prepared from these exact local identities:

- Evaluation Workbench corrected foundation: `222fadc`
- Product architecture: `426ec91`
- fx execution plan under review: `e75be60`
- Portable lab-specs suite: `94abbe3`

The page deliberately separates three kinds of statement:

- **Current** means implemented and reproducibly verified in the recorded,
  offline foundation. A recorded replay is not a fresh agent run.
- **Proposed** means specified for the fx milestone but not yet demonstrated.
- **Later** means gated by independent customer evidence and product decisions.

The spec section also keeps two layers distinct. Workbench definition packets
describe projects, lanes, scenarios, scorer bindings, and frozen attempt plans.
The portable `lab-specs` layer defines canonical JSON, receipts and diffs,
ProofPack evidence, Assay decision gates, and cross-language conformance. The
abridged JSON on the page is explanatory anatomy, not a valid conformance
fixture.

All Edge and fx API snippets are explicitly illustrative. Native errors,
refusals, unsupported controls, and unresolved evidence must retain their native
meaning rather than being converted into success.

## Verification

Run the repository gate before review:

```bash
npm run verify
```

The generated page should have one `h1`, nonempty image alt text, no broken
internal fragment links, and a `noindex, nofollow` robots directive. Illustration
hashes and dimensions are recorded in `provenance.json`.

Static and build checks have passed. A composed desktop/mobile browser review is
still required before any public navigation or deployment decision; the current
environment did not expose a browser surface for screenshot-based visual QA.
