---
title: "What Survives the Next Model"
description: "An eval should leave us with a better theory of when success holds, what would break it, and which experiment is worth running next—even when the model changes."
publishedAt: 2026-09-13
kind: "article"
author: "Sergio Soage"
tags: ["Evals", "Evidence", "Experimental Design", "AI Systems"]
readingTime: "18 min"
featured: false
unlisted: false
homepageExcerpt:
  - "The request has timed out. An agent is refunding forty euros to a customer. It sent the instruction to the payment provider and received no answer. Now it must choose: send the instruction again, or stop."
  - "One observation. Several worlds. Opposite right answers. A useful eval should expose the conditions its theory of success leaves out—and leave those discoveries useful to the next investigator."
socialImage:
  src: "/img/articles/what-survives-the-next-model/silent-provider-worlds-social.jpg"
  alt: "A researcher studies three silent provider boxes whose cutaways reveal a refund already settled, never started, or still in flight."
  width: 1200
  height: 630
  type: "image/jpeg"
---

<p class="article-series"><a href="/articles/evals-as-theory-building/">Evals as Theory Building</a> · Part II</p>

<blockquote class="article-epigraph">
  <p><em>“Now, here, you see, it takes all the running you can do, to keep in the same place.”</em></p>
  <footer>— <cite>Lewis Carroll, Through the Looking-Glass</cite></footer>
</blockquote>

The request has timed out.

An agent is refunding forty euros to a customer. It sent the instruction to the payment provider and received no answer. Now it must choose: send the instruction again, or stop.

Both choices are correct in some world and wrong in another. If the first refund went through, only the acknowledgment was lost, and the provider does not recognize a repeated instruction, a retry pays the customer twice. If nothing happened, stopping abandons a request the agent could have completed. If the provider is still working on it, either action may be premature.

One observation. Several worlds. Opposite right answers.

<figure class="article-illustration article-illustration--hero">
  <img src="/img/articles/what-survives-the-next-model/silent-provider-worlds.webp" width="1536" height="1024" alt="A researcher studies three identical silent provider boxes whose cutaways show a red refund token already settled, still untouched, or moving through a hidden channel." decoding="async" fetchpriority="high" />
  <figcaption>The same silence can hide a completed action, no action, or an action still in flight.</figcaption>
</figure>

This is the position an eval is in when different explanations fit the same score. The [first essay](/articles/evals-as-theory-building/) argued that an eval is a theory of success made operational. Its verdict needs rigor, proof and verification before it may change a system. What should compound across models is our understanding of the work, with receipts that let us question and rebuild it.

We want to take that argument further. An eval should help discover the conditions its theory of success leaves out, design experiments that test them, and make those discoveries useful to the next investigator. After the model, the tool or the evaluator changes, it should help us decide which earlier conclusions still apply and what we need to find out next.

Our bet is that this investigation can become a learned capability. That claim is untested.

<aside class="claim-ceiling" aria-label="The research hypothesis of Part II">
  <p class="claim-ceiling__label">The hypothesis</p>
  <p>An investigator can learn which conditions make an earlier conclusion reusable, including conditions nobody recorded, and choose the experiments that test them. After a system changes, it should preserve more valid conclusions at lower total cost than competent dependency checks, at the same limits on harmful reuse and unnecessary refusal. If explicit checks perform as well, the learning claim fails.</p>
</aside>

Active evaluation already chooses informative tests. [Dynamic safety cases](https://arxiv.org/abs/2412.17618) already track claims and evidence as systems change, and benchmark maintainers already version tasks and rerun selectively. These are starting points for the learning problem we care about: choose the next experiment by what it can establish about the reuse of an earlier conclusion.

## Four worlds, then a fifth

Return to the timeout. We built a small executable model of it: four worlds, crossing whether the refund committed with whether the provider tolerates a repeated instruction, and three policies for the agent. Everything below about those worlds is an exact, reproducible result of that model. It is not evidence about any real provider.

Reading a cached copy of the ledger leaves all four worlds standing. It is a correct historical reading, and it changes nothing about the decision. Reading the authoritative ledger fresh leaves two worlds. Within these four deliberately restricted worlds, two is enough. If the fresh reading shows one refund, stop. If it shows none, one retry produces exactly one refund.

That last sentence rests on assumptions the model makes explicit: the reading is exact, the intent was authorized, the retry completes before the stated horizon, and no earlier, concurrent or other new request for the same intent commits after the reading. The policy that satisfies every world is “look, then act.” Nothing learned it. We wrote it, and the finite check confirms it under those assumptions.

Then we added a fifth world, in which the provider commits late. The ledger truthfully reads zero. The agent retries. The original request settles. Two refunds. The same policy, safe in all four original worlds, is unsafe in the fifth, and nothing in the original evidence was wrong. The family of worlds was too small.

That is the whole essay in miniature. The conclusion “one retry after a fresh zero is safe” was a true record of the four-world experiment. Carried into a world with an unstated mechanism, it became a false guide to action. What failed was not the observation. It was an assumption of the restricted model that had been left out of the shortened, reusable claim.

## The claim, and its open premise

Write the conclusion the way it should have been stored. Not “retry after a fresh zero,” but:

*For this authorized intent, an exact authoritative reading shows zero effects. If no earlier, concurrent or other new request for that intent can commit after the read, and one retry completes once before the stated horizon, exactly one refund occurs within that horizon.*

Every clause is a premise, and the one-effect-per-successful-retry clause is a rule of our authored model, not a promise any real provider has made. Change the provider and the clause excluding every other commit after the read is open. The conclusion has not been falsified. Its next use needs evidence about that open clause. The investigator's task is to find a sufficient check at the lowest expected total cost, and to say when the available experiments cannot settle it.

A build system offers the right picture. It reuses yesterday's compiled output only when every input the output depends on is unchanged. Scientific memory should make the same promise about a conclusion, with one honest complication: a hash proves identity, not understanding. If the dependency list is incomplete, a perfectly implemented cache preserves a false claim perfectly. The fifth world is exactly a missing entry in the dependency list.

So, for every retained conclusion facing a change, ask of each premise: is it *retained*, because an explicit argument says the change does not touch it; *re-established*, because a new check has discharged it under the new conditions; or *open*. An open premise interrupts the derivation that needs it. Another derivation may still support the conclusion, but no unrelated green check can stand in for the missing one.

<figure class="article-illustration">
  <img src="/img/articles/what-survives-the-next-model/premise-bridges.webp" width="1536" height="1024" alt="Three stone bridges carry red support lines: one remains intact, one is repaired by a researcher, and one ends at an open gap." loading="lazy" decoding="async" />
  <figcaption>A premise is retained, re-established, or left open. An open span cannot carry the claim.</figcaption>
</figure>

<aside class="evidence-roles" aria-label="Three questions before a stored result may influence a decision">
  <p class="evidence-roles__label">Admission asks three questions</p>
  <p><strong>Checked:</strong> does the derivation hold, from evidence through stated rules to this conclusion?</p>
  <p><strong>Permitted:</strong> does the conclusion's scope cover this use, or is “passed these cases” being promoted to “safe in every case”?</p>
  <p><strong>Current:</strong> has any premise it depends on changed since it was checked?</p>
</aside>

This is an admission policy, not a proof that the premises are true. Part I required verified evidence before a verdict could change a system. Reuse is another decision of that kind. Assay's expiry and revocation should govern it: a conclusion is admitted for a use, in a context, until an affected premise moves, and only the support that depended on that premise is reopened.

The hard part is the missing entries. An expert can write “the provider never commits late” into a dependency list after the fifth world has been found. The research question is whether an investigator can find that clause before the duplicate refund, from the trajectory it observes, without being told which mechanism to look for. Our finite example exposes the missing mechanism. It does not detect it; that is the first capability an investigator would need.

The test has to be fair: if two worlds produce the same history up to the retry, that history alone cannot tell them apart. What the investigator can do is flag the premise as unsupported and go looking, with a declared budget of extra observations, a contract query or a safe experiment. Proposing the missing assumption before the harm is the capability. Guessing which hidden world is true is not.

Part I treated dead ends as material for the next eval. The stronger demand is that a counterexample changes what the investigator knows to ask. The late refund exposes a distinction between “nothing has happened” and “nothing can still happen.” A useful memory would make that distinction available to investigate the next unfamiliar timeout.

## The next experiment

Suppose a new version of the agent resolves more refunds per hour. Several explanations fit. The agent is better. The agent is stopping earlier, and the evaluator counts a closed case as a resolved one. The agent has learned what the evaluator rewards. These do not exhaust the possibilities, and repeating the measurement will not choose among them, because each explanation predicts the same dashboard.

Repeating a measurement that makes identical predictions under the competing explanations cannot distinguish those explanations. Only a new observation or intervention on which their predictions differ can. A checker hypothesis might predict that a qualified second evaluator reverses premature closures previously counted as successes. A worker hypothesis must specify how its stopping rule responds to acknowledgment timing, then predict the result of a registered delay. Some explanations predict a change; others predict invariance. The useful experiment is one on which their predictions differ. Each explanation commits to that prediction before the intervention runs. An explanation fitted to a result is a hypothesis. A prediction on new evidence puts it at risk.

This is old science. Experimental design has selected informative tests for a century, and [active evaluation](https://arxiv.org/abs/2410.05952) already applies it to choosing which benchmark items to run. We want to make an earlier conclusion's premises the target: choose the experiment for what it can establish about them, and charge its cost against the value of keeping that conclusion. Memory then participates in experimental design. In a [science-sandbox study](https://arxiv.org/abs/2608.30165) of hidden-rule worlds, agents improved a numerical objective without stating the rule that produced it in their explanations. Whether a recovered rule transfers better under change than a score-optimized policy is not established by that study. A useful test of our view would have to measure that transfer.

There is a second decision the investigator has to make: when to stop. Every experiment costs something, and combinations of experiments can be informative where each alone is not. The eval we want would choose when to buy more evidence and state what remains unexamined when it stops. Judge-panel research has begun to [formalize whether another single call is justified](https://arxiv.org/html/2608.19802v1) under a fixed audit and cost model. That default does not rule out every useful combination; extending the choice to experiments the investigator generates is open.

## The instrument must earn its reading

None of this works if the instrument cannot resolve the difference it is asked to judge. A balance that drifts by more than the proposed gain cannot tell us whether the gain exists, however carefully we record its serial number.

A recent study, [Clean Engineering, Unstable Measurement](https://arxiv.org/abs/2609.04198), found this in its tested language-model evaluators: identical request bytes to a fixed model name did not produce stable readings, and the campaigns failed their own repeatability gates while their execution records were sound.

The setting is specific. The obligation travels. Before asking whether an improvement passes, ask whether the instrument can distinguish an improvement of that size from its own noise.

Repeatability is not validity. A reading can recur perfectly and still count the wrong thing. While checking sources for this essay we found a clean example. A [September 2026 paper on calibrating multilingual judges](https://arxiv.org/abs/2608.22432v2) reports that its correction raises agreement with human preferences on a 700-item sample from 68.7 to 76.6 percent. Its code and saved margins are public, and recounting the published margins reproduces the reported percentages.

It also reproduces the flaw. Every one of the 55 items that changed from wrong to right was a tie: a raw margin of exactly zero that the correction turned into a positive residue smaller than 10⁻¹⁶. For each item, the correction has zero mean across the complete evaluator panel, so it leaves the exact panel-mean margin unchanged and those items stay tied. The code counts anything above zero as correct. Treat the residues as ties and both methods score 481 of 700.

The tolerances tested and the pinned files are in the receipts. This says nothing about the paper's other results. It says that repeating a calculation does not validate its decision rule.

<aside class="map-warning" aria-label="Reproducibility versus validity">
  <p class="map-warning__label">Boundary condition</p>
  <h3 class="map-warning__title">Reproducibility does not establish validity.</h3>
  <p>An instrument earns its reading by surviving known-good work it must accept, counterfeits it must reject, and transformations that must leave its verdict unchanged. A tie that becomes a win under a correction that preserves that item's panel-mean margin has failed the third test.</p>
</aside>

The instrument can also be biased in a direction that flatters everyone. In the refund model we enumerated every delivery sequence of one to four steps, over two intents and two authorization states, against five workers: one correct and four defective. A checker that looked only for harm accepted the worker that refuses every refund and the one that deduplicates by amount and so drops the second of two legitimate requests for the same sum. Out of 1,700 authored rows, 440 passed a check they should have failed. These are not field incidents. They are an exact census showing that “did anything bad happen?” is a question the do-nothing agent always answers well. Safety and useful completion have to be examined together, and the evaluator has to be attacked with the same seriousness as the system. That was ProofPack's job in the first essay. It does not get smaller here.

## When the case fails, who failed?

When a case fails, the worker, the world and the instrument are all candidates. A person reading the trace may offer a diagnosis. That review is valuable and expensive, and once written down it can look more settled than the evidence warrants.

Interventions can narrow the field. Regrade the saved run with an independently written evaluator. Rerun the same task in a corrected world. Run a reference worker of known competence on the same case. Each swap holds the starting state and the exogenous conditions fixed as far as the design allows, knowing that a new world or worker changes the trajectory downstream, and the pattern of changed and unchanged outcomes is evidence about where the fault lies. It is evidence under assumptions: that the second evaluator does not share the first one's mistake, that correcting the world did not simply remove the hard part, that the reference worker does not carry the candidate's defect. Where the interventions cannot separate an individual fault from a shared one, the attribution stays joint or unresolved, and it says so.

<figure class="article-illustration article-illustration--hero">
  <img src="/img/articles/what-survives-the-next-model/intervention-stages.webp" width="1536" height="1024" alt="A worker, a miniature test world, and a dial instrument occupy separate stages while an investigator swaps only the instrument and a red path remains fixed." loading="lazy" decoding="async" />
  <figcaption>Change one component and watch what follows. Attribution comes from interventions, not a label on a trace.</figcaption>
</figure>

The attribution then travels with the record: not “the model failed” but “this failure is attributed to the evaluator, on these interventions, under these registered controls.” People qualify the controls, decide scope, audit cases that look settled, and adjudicate the disagreements. Their decisions are recorded and reused under their stated conditions. Such a panel should be tested on single faults, shared faults and interactions, with confident misattributions counted as failures.

Attribution matters because the loop is fast. An automated research loop can change the agent, the world and the evaluator in one afternoon. Without a defensible diagnosis, it risks repairing the wrong one. One investigation should be allowed to produce three separable kinds of progress, each with its own evidence: better work, a better instrument, and better knowledge for the next investigation. They do not move together. Repairing an evaluator that accepted premature completion can lower the scores of agents that exploited it, and the dashboard may call that regression.

The [Red Queen Gödel Machine](https://arxiv.org/abs/2606.26294v2) co-evolves agents and evaluators with a discipline worth borrowing: the criterion is frozen within an epoch, changed between epochs, and records that depended on the old criterion lose their standing when it changes. Its guarantees are epoch-local. Part I drew the same boundary against a loop grading its own progress. An investigator may propose a new experiment or a repair to its evaluator. The proposal still has to pass qualified controls and independent checking before its result may govern the next change.

The software form of this record can be modest. A **Finding** names its premises and dependencies. A frozen comparison records which worker, world and evaluator versions produced the contrast. A qualified evaluation pack says which uses the evidence earned. Those primitives exist separately in our work. The integrated product and customer results do not. The research claim begins only when using them improves a fresh decision.

## What a better eval should show

An eval that remembers earlier conclusions should have to earn that reuse. We would judge it by the valid conclusions it preserves, the harmful reuse and unnecessary refusal it causes, and the total cost of its investigations.

A fair comparison needs a fixed cohort of scoped conclusions and a registered stream of changes: model swaps, tool upgrades, workload shifts, evaluator repairs, and worlds with omitted mechanisms held out by family. Give each method the same model, tools, raw history and total resources. Audit what it keeps and what it refuses against a separately authored reference. Compare the learned investigator with full re-evaluation, reuse on unchanged identities, competent explicit dependency checks, ordinary retrieval over past runs, and an ordinary adaptive investigator that may propose experiments too. The point is to test what is gained by retaining learned investigation state across cases—not merely by permitting fresh model reasoning. Specify what persists, whether weights, a policy, structured memory or code, and ablate that state without removing the comparator's access to the underlying history. Charge each arm for preparation and training as well as generation, qualification, failed investigations, human review and reruns.

The output should be a claim-reuse profile: which conclusions remained supported without new evidence, which needed a new check, which were withdrawn, and which were wrongly reused or wrongly refused. Keep retention and re-establishment separate, and count errors in both. The reference records decision correctness and evidential support separately. An unsupported assurance remains unsupported when the conclusion happens to be true; unnecessary refusal is judged against the evidence and investigation budget the method was permitted to use. Measure harmful reuse among reused claims and wrongful refusal among valid claims. An investigator that reuses nothing has an unestimated reuse error rate, not zero risk.

Unresolved reference judgments must stay visible. Error limits need uncertainty bounds fixed in advance, and related changes must be grouped by lineage: a hundred correlated traces are not a hundred experiments. This accounting makes the claim inspectable. It asks whether the investigator has learned to preserve useful knowledge responsibly, including when the change reveals a condition nobody recorded.

<aside class="claim-ceiling" aria-label="How the hypothesis loses">
  <p class="claim-ceiling__label">How this loses</p>
  <p>If explicit dependency checks retain as much valid knowledge at the same cost, keep the checks and drop the learning claim. If the investigator wins only by refusing more or spending more, it has not won. If its advantage vanishes when the ordinary arm gets the same model and evidence, the advantage was never the method.</p>
</aside>

Uncontrolled adaptive reuse can invalidate ordinary guarantees. Dwork and colleagues showed a decade ago that [reusing a holdout adaptively](https://papers.nips.cc/paper_files/paper/2015/file/bad5f33780c42f2588878a9d07405083-Paper.pdf) degrades its guarantees even when the data are never seen, and they gave protocols that control the damage. Evidence for better investigation therefore needs fresh material or a protocol that controls what each method learns from feedback and accounts for it. Freshness is a premise like the others.

## Score the model by what survives it

Replacing a model changes two things at once: what the system can do, and what we are entitled to believe about it. We think evaluation should account for both.

Part I made the eval an operational theory of success. What should persist across models is that theory, the instruments that test it, and the evidence that establishes where its conclusions may be used. Treat each candidate model as a change applied to that body of work, exactly as the provider swap was a change applied to the refund claim. Which conclusions remain supported for the proposed use? Which need new evidence? What useful work becomes possible, and what does it cost to justify it?

Compare candidates against the same relevant claims, with the same investigator, the same evidence limits and the same admission rules. A higher benchmark score can come with a larger revalidation burden, and reopened support is not falsified knowledge: the old claim may still be true of the old system while its use to justify the new one needs fresh evidence. Admission should expose that burden beside the gains, and count the actual cost of the checks, since ten cheap re-establishments can cost less than one expensive one.

The bolder demand follows. Before the next model arrives, the eval should predict, under stated assumptions about the change, what it will require us to re-establish: which support should carry across, where a new check will be needed, and what evidence would defeat its own judgment. Then those predictions are tested, independently, against the same reference, error limits and coverage rules as everything else.

An omission earns no credit on its own. An eval that declares everything outside its coverage has predicted nothing and covered nothing, and the audit should count that as lost coverage. A model failure the eval correctly detects is evidence about the model. A false assurance is evidence against the eval. Keeping those two apart is the attribution discipline from earlier, applied to the eval's own forecasts.

<aside class="claim-ceiling" aria-label="Scoring a model by what survives it">
  <p class="claim-ceiling__label">Position</p>
  <p>A candidate model is judged on capability and on continuity: the conclusions that remain supported for their intended use, the support it reopens, and the measured cost of re-establishing it. The eval's predictions about that continuity must themselves survive independent audit. The position stands without the learning hypothesis. The hypothesis is about who makes those predictions well.</p>
</aside>

## What a successor can use

We expect stronger models to absorb some machinery we now build by hand. A planning routine, a separate critic, a curated memory: each may be unnecessary for the next model. A stronger worker with simpler scaffolding should be free to replace an elaborate arrangement if it meets the same standards. The obligation that carries across that replacement is to make the rules for concluding explicit: what counts as evidence, which inferences are sound, when a conclusion's support reopens, who may change the criterion and when. Those rules are versioned and reviewed like anything else.

A retained lesson earns credit when it improves decisions on fresh applicable problems. In [S3Gym](https://arxiv.org/abs/2608.31100), better self-judgment of past behavior was not reliably associated with better later behavior, which is a reminder that a lesson can look learned and change nothing. The test is a recipient. Hand a successor, human or model, the promising change, the experiment that challenged it and the premises it depends on. Then measure what the successor does: whether it chooses the right next experiment, notices the unsupported promotion, refuses the action that exceeds its authorization, and how long that takes compared with a successor given only the raw history. A handoff is evaluated by what the recipient does next, and whether the record makes that faster is a claim we have to earn.

Peter Naur [warned](https://pages.cs.wisc.edu/~remzi/Naur.pdf) that the theory of a program lives in the people who hold it and that no document carries it. The record is not the theory. It keeps the particulars, and the reasons for doubt beside them, from which the next investigator rebuilds the theory. Whether they rebuild it faster is our hypothesis, not his.

<figure class="article-illustration article-illustration--hero">
  <img src="/img/articles/what-survives-the-next-model/successor-notebook.webp" width="1536" height="1024" alt="Two researchers exchange an open notebook while an unbroken red thread runs from a completed apparatus, across its pages, to an unfinished apparatus." loading="lazy" decoding="async" />
  <figcaption>The record does not carry the theory. It gives the next investigator somewhere better to begin.</figcaption>
</figure>

The refund example leaves a concrete thing for a successor: the conditional claim written out above, with its premises listed and its open clause named. A provider change does not by itself falsify that conditional claim. It reopens the affected support. The next investigator inherits the obligation to re-establish it.

Part I argued that our understanding of the work should compound across models. In practice, that means discovering a condition nobody listed, recognizing when a conclusion's support changes, and choosing evidence that makes its next use justified. The successor should inherit defensible support—and know which open premise to investigate next.

<p class="article-coda"><strong>What survives is not the score.</strong> It is the support we can still defend—and the open premise we know to investigate next.</p>

<p class="article-receipts">The finite refund results and the judge-calibration check are reproducible from the <a href="/receipts/what-survives-the-next-model/RECEIPTS.html">receipts that accompany this essay</a>: pinned scripts, saved outputs, assumptions and rerun commands.</p>
