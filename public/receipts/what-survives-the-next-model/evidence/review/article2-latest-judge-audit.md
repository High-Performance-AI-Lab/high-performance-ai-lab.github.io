# Latest judge-research addendum

11 September 2026. Read `/Users/sergio.soage/grc-agent1/outputs/eval-sota-scan-2026-09-07.md`; inspected the relevant primary full text for its two requested judge papers. Original article, research scan, and source documents were not edited.

**Recommendation:** AgentJudgeBench can strengthen the instrument section with a narrow validity example. Do not import the scan's scaling-ceiling rhetoric. Withhold CBC's claimed human-gold improvement: an audit of the authors' saved sample reproduces the entire improvement as floating-point tie handling.

## AgentJudgeBench: useful evidence, narrower than the scan

[AgentJudgeBench v1](https://arxiv.org/html/2608.26623v1), 27 August 2026. Checked methods, results, limitations, and Appendices B/G/H/I. No experimental reproduction or complete code audit.

Its strongest addition to article lines 85–91 is that agreement with a deterministic scorer can diverge from semantic validity. Appendix G's human check uses one annotator per record, shown the programmatic scores. The reported κ is agreement among LLM judges, not independent human-annotation reliability. The scan's “human-gold + κ” language obscures that distinction.

The 77–82% band is an observation on the tested prompts, scorers, generators, and judges. It does not prove a capacity-independent ceiling for future models. Appendix B explicitly describes prompt dependence and untested training-loop implications.

The scan also conflates two failure modes. Appendix H's over-anchoring cases miss completeness, dependency, or coverage defects when the reference is present. Appendix I separately illustrates disagreement about equivalent orderings. Mechanistic evidence is shown for Gemini, not independently established for GPT-5.4.

**Possible insertion:** “Even a deterministic reference can reward the wrong equivalence. AgentJudgeBench found disagreements over schema-valid arguments and interchangeable tool orderings. Repeatability tells us whether a reading recurs; validity asks whether the distinction deserves to count.”

## CBC: formal scope and an independently checked numerical problem

[CBC v2](https://arxiv.org/html/2608.22432v2), 6 September 2026. Checked §§3–4, Proposition 5, §5.5/Table 5, limitations, and Appendices C/D.

The algebra identifies a two-way interaction under balanced shared-item coverage. Proposition 5 cancels task–language effects that are common across backbones; it is not robustness to arbitrary misspecification. The paper excludes task–language–backbone effects, cannot correct a common language shift, and warns that an interaction may represent actual specialization rather than unwanted bias. Those are useful examples of a calibration claim carrying assumptions.

Table 5 reports a human-anchor gain from 68.7% to 76.6%, based on the sign of the unweighted evaluator-panel mean margin. The calibration input is chosen-minus-rejected margins. But the stated double-centering correction has zero mean across backbones, so it cannot change that panel mean in exact arithmetic on complete cells.

**Do not use the human-anchor gain as evidence of improved correctness.** The public code and saved sample permit the direct check below. This is a specific reproducibility finding, not a claim that every result in the paper is invalid.

## Reproduction of the reported gain

Author repository revision: [`37d500566b0b7a7701a1ca199fafc467f2612587`](https://github.com/KurbanIntelligenceLab/multilingual-judge-calibration/tree/37d500566b0b7a7701a1ca199fafc467f2612587).

- [External analysis script](https://github.com/KurbanIntelligenceLab/multilingual-judge-calibration/blob/37d500566b0b7a7701a1ca199fafc467f2612587/scripts/run_external_mrewardbench_analysis.py): lines 130–134 double-center; 413–419 subtract the correction and average margins; 442–443 threshold both means with strict `> 0.0`.
- [Saved human-anchor sample](https://github.com/KurbanIntelligenceLab/multilingual-judge-calibration/blob/37d500566b0b7a7701a1ca199fafc467f2612587/data/external_validation/mrewardbench_panel/analysis_1500_item/human_anchor_sample.csv) and [reported summary](https://github.com/KurbanIntelligenceLab/multilingual-judge-calibration/blob/37d500566b0b7a7701a1ca199fafc467f2612587/data/external_validation/mrewardbench_panel/analysis_1500_item/human_anchor_validation.json).

I recomputed the saved sample's correctness indicators independently with Python's standard CSV library:

| Check | Result |
| --- | ---: |
| Sample rows | 700 |
| Raw strict-positive agreement | 68.7142857% |
| Corrected strict-positive agreement | 76.5714286% |
| Changed correctness decisions | 55 |
| Changed decisions whose raw margin is exactly zero | 55 |
| Corrected margins in those 55 rows | approximately +1.11×10⁻¹⁷ to +8.88×10⁻¹⁷ |
| Corrected agreement treating margins ≤10⁻¹² as nonpositive | 68.7142857% |

Every reported improvement is a tied item receiving tiny positive floating-point residue and consequently being marked correct. The entire 7.857-point gain disappears at every tested tolerance from 10⁻¹⁶ to 10⁻¹⁰: both methods have 481 correct items. This is a sensitivity check for roundoff around exact zero, not a proposal to change the metric's substantive decision threshold; those magnitudes are far below the paper's 1–5 rating scale. Three other rows have larger raw/corrected margin differences, potentially reflecting incomplete item-level panels; none changes a correctness verdict. I have not audited their source collection records and do not claim that every row's mean is preserved by the actual saved pipeline.

The identity behind this check is:

`beta[l,b] = M[l,b] - mean_b M[l,b] - mean_l M[l,b] + mean M`

Hence `mean_b beta[l,b] = 0`, so `mean_b (margin[t,l,b] - beta[l,b]) = mean_b margin[t,l,b]` for a complete panel in exact arithmetic. This is my algebraic check of the published operation. It needs no statistical assumption.

Local reproduction files: `/Users/sergio.soage/code/research/nap/meeting-prep-2026-09-05/article-part-2-v3/review-2026-09-11/cbc-anchor-check.py`, `/Users/sergio.soage/code/research/nap/meeting-prep-2026-09-05/article-part-2-v3/review-2026-09-11/cbc-anchor-check.json`, `/Users/sergio.soage/code/research/nap/meeting-prep-2026-09-05/article-part-2-v3/review-2026-09-11/cbc-anchor-sample.csv`, `/Users/sergio.soage/code/research/nap/meeting-prep-2026-09-05/article-part-2-v3/review-2026-09-11/cbc-anchor-summary.json`, `/Users/sergio.soage/code/research/nap/meeting-prep-2026-09-05/article-part-2-v3/review-2026-09-11/cbc-external-analysis.py`, `/Users/sergio.soage/code/research/nap/meeting-prep-2026-09-05/article-part-2-v3/review-2026-09-11/cbc-beta.csv`. Run `python3 /Users/sergio.soage/code/research/nap/meeting-prep-2026-09-05/article-part-2-v3/review-2026-09-11/cbc-anchor-check.py` to verify the saved-data result. No provider calls or full experiment reruns were performed.

## What strengthens Article II

The useful new requirement is operational: **a changed evaluator must pass outcome-preservation checks before its statistical improvement can be admitted.** The article already calls for known-good work and counterfeits. Extend that to metamorphic controls: preserve valid alternative orderings; preserve ties under transformations that mathematically preserve the panel mean; vary task difficulty and reference exposure; test whether purportedly independent judges share the same mistake.

That is a proposal for the authors' programme, motivated by this audit. It adds a concrete test to the essay's argument without relying on an unproved model-scaling ceiling or presenting consistency as correctness.
