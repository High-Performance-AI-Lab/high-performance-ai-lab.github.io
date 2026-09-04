---
title: "Evals as Theory Building"
description: "An eval is more than a score. It is a working theory of success—and it needs rigor, verification, and proof before its verdict is allowed to change a system."
publishedAt: 2026-09-04
kind: "article"
author: "High Performance AI Lab"
tags: ["Evals", "Evidence", "Verification", "AI Systems"]
readingTime: "8 min"
featured: false
---

Every organization has a sentence that can change the direction of its work: *The numbers look good.*

Behind that sentence there is usually an evaluation—an eval—whether anybody calls it one or not. A pilot has been compared with the process it might replace. A supplier has been tested against another. A sample of customer interactions has been turned into a rating. Some part of reality has been selected, observed, and given a verdict.

AI makes these verdicts unusually easy to produce. A different model, a revised instruction, or a new arrangement of tools can be tried in hours. An automated research loop can run a hundred variations while the people responsible for the work sleep.

But an eval is not merely a test at the end of that process. It defines what the process can recognize as improvement. It chooses the situations that count, the facts that will be observed, and the rule that turns those facts into a pass, a failure, or a score.

An eval is a theory of success made operational.

In Jorge Luis Borges’s one-paragraph story [“On Exactitude in Science”](https://www.public.asu.edu/~bdaniel6/cll/pdfs/Del_rigor_en_la_ciencia.pdf), an empire constructs a map as large as the empire itself, matching it point for point. It is perfectly faithful and entirely useless. Every useful map is a compromise, defined as much by what it leaves out as by what it contains.

<figure class="article-illustration article-illustration--hero">
  <img src="/img/articles/evals-as-theory-building/map-becomes-territory.webp" width="1536" height="1024" alt="A person draws a red labyrinth whose lines leave the page and become walls around them." decoding="async" fetchpriority="high" />
  <figcaption>The eval begins as a map. Once it directs the work, it becomes part of the territory.</figcaption>
</figure>

Two changes can improve the same score for opposite reasons. One may perform the work better. The other may have learned what the eval rewards. From the dashboard they look alike. Outside it, one is progress and the other is camouflage.

The important question is therefore not simply whether a system passed. It is what the passing result proves, how that proof can be checked, and what the result is now allowed to change.

<aside class="claim-ceiling" aria-label="The relationship between rigor, proof, and verification">
  <p class="claim-ceiling__label">Three different obligations</p>
  <p><strong>Rigor</strong> makes the claim precise and tries to break it. <strong>Proof</strong> is the inspectable record of what survived. <strong>Verification</strong> lets somebody else check that record without taking its author on faith.</p>
</aside>

## Every eval is a map

An eval makes the same bargain. Customer satisfaction becomes a rating. Risk becomes a category. A resolved problem becomes a closed ticket. Each reduction makes the activity legible by making it smaller.

But what becomes visible—and what disappears—matters.

Imagine a customer-support operation that measures resolution by whether a ticket has been closed. At first, the number is merely an imperfect description of the work. Then it becomes a target. Teams are rewarded for it. An AI assistant is tuned against it. Soon the organization becomes very good at closing tickets, including tickets attached to problems that remain unsolved.

The eval has stopped observing the work from a distance. It has begun organizing the work around itself.

This is the danger in confusing a map with the territory. The map does not need to be malicious or obviously wrong. It only needs to omit something consequential and then acquire authority. Once budgets, promotions, and releases depend on it, the abstraction can begin remaking the reality it was meant to describe.

<aside class="map-warning" aria-label="Warning about evals becoming instructions">
  <p class="map-warning__label">Failure mode</p>
  <h3 class="map-warning__title">When the eval becomes the instruction.</h3>
  <blockquote class="map-warning__quote" cite="https://stuff.mit.edu/~hauser/Papers/Hauser-Katz%20Measure%2004-98.pdf">
    <p>“You are what you measure.”</p>
    <footer>John R. Hauser and Gerald M. Katz · <cite><a href="https://stuff.mit.edu/~hauser/Papers/Hauser-Katz%20Measure%2004-98.pdf">Metrics: You Are What You Measure!</a></cite> · 1998</footer>
  </blockquote>
  <p>A score does not remain neutral once it selects models, funds projects, rewards teams, or authorizes a release. An error in the eval can move the whole organization in the wrong direction while every dashboard reports progress.</p>
</aside>

This is not an argument against evals. We need maps because we cannot carry the territory with us. It is an argument for keeping the map answerable to the journeys people actually take.

That requires more than adding another decimal place.

## The smoke is real. The fire is not.

Smoke rises behind a hill. We do not wait for the flames. We infer them. The inference works because the world has taught us to trust the connection: fire produces smoke.

A smoke machine preserves the signal and severs the cause. Nothing about the smoke is false. Only the conclusion is.

<figure class="article-illustration">
  <img src="/img/articles/evals-as-theory-building/smoke-without-fire.webp" width="1536" height="1024" alt="A red smoke plume rises from behind a hill while a hidden bellows, rather than a fire, produces it." loading="lazy" decoding="async" />
  <figcaption>The signal can be genuine even when the conclusion is false.</figcaption>
</figure>

An eval result works in much the same way. The number does not resemble good judgment, useful work, or a satisfied customer. We treat it as evidence of those things because we believe there is a dependable chain connecting the work to the cases, the cases to the evaluator, and the evaluator to the result.

A system that learns to satisfy the evaluator without completing the work breaks that chain. The score may still be calculated perfectly. It simply no longer points where we thought it did.

More test cases can produce more smoke. They do not establish that there is a fire.

An eval places a system under examination. Rigor begins when we place the eval under examination too. Can it reject behavior we know to be wrong? Can it continue to accept behavior we know to be honest? Does an irrelevant change alter the verdict? What happens at the edges of the situations somebody thought to include?

<figure class="article-illustration article-illustration--narrow">
  <img src="/img/articles/evals-as-theory-building/evaluator-under-evaluation.webp" width="1536" height="1024" alt="One person measures an irregular red object while another measures the ruler itself with an oversized caliper." loading="lazy" decoding="async" />
  <figcaption>The system is being measured. The instrument must be measured too.</figcaption>
</figure>

This is the role of **ProofPack**. It is an independent verification and evidence layer for evals. Known-good cases test whether the evaluator is merely refusing everything. Controlled counterfeits test whether it can recognize the failures it claims to detect. Generated variations test whether the apparent rule survives beyond the examples that made it look convincing.

We have applied that pressure to our own work. In one six-hour campaign, an automated adversary could see an entire benchmark harness and was asked to produce incorrect answers that the harness would accept. It found 89 escapes in 153 attempts. Those escapes became material for a stronger eval. The revised harness blocked all 89 on replay and detected all 49 defects we had deliberately planted.

The important result was not a claim that the new harness could never fail. It was a bounded claim with receipts: the attacks, cases, outputs, failures, repairs, and replay results were kept together so the conclusion could be checked instead of merely repeated.

For each run, ProofPack binds the claim to the exact cases, system versions, evaluator, outputs, traces, errors, and missing results that produced it. If a declared part is absent or altered, verification fails. A timeout cannot disappear into an average. A case that never ran cannot masquerade as a pass.

This is proof in the empirical sense: not certainty for all time, but a checkable chain between a stated claim and the evidence that survived an attempt to break it.

<aside class="claim-ceiling" aria-label="Definition of a qualified eval">
  <p class="claim-ceiling__label">Qualification threshold</p>
  <p>A qualified eval tells us which counterfeits it rejected, which honest controls it preserved, which conditions produced the result, where its claim ends, and how another person can verify the record.</p>
</aside>

ProofPack can establish those bounded facts. A further question remains: Are they sufficient for the decision at hand?

## What may the verdict change?

A trustworthy observation is not yet a decision.

Suppose a pilot appears to reduce cost. Is any reduction sufficient? Must quality remain unchanged? How much uncertainty will we tolerate? What happens if some cases never complete? Which existing process remains available if the replacement is refused?

If these questions are answered only after the results are visible, the rule can bend toward the result people already want.

**Assay** holds the decision boundary still. Before the eval runs, it records the claim being tested, what must be preserved, what would disqualify the change, how much evidence is required, and which fallback remains available. When ProofPack’s verified facts arrive, Assay applies the rule fixed in advance.

<figure class="article-illustration">
  <img src="/img/articles/evals-as-theory-building/assay-fixed-gate.webp" width="1536" height="1024" alt="A person fixes the opening of a balance-shaped gate before sealed and damaged evidence bundles arrive." loading="lazy" decoding="async" />
  <figcaption>Assay fixes the boundary before the evidence arrives.</figcaption>
</figure>

This produces three meaningfully different outcomes. Evidence can admit a bounded next step. It can refuse a proposed change. Or it can be invalid because the record is missing, inconsistent, or produced under the wrong conditions. A broken eval is not a failed model, and a tie is not an improvement. Keeping those states separate prevents the pressure to produce an answer from manufacturing one.

<aside class="evidence-roles" aria-label="The respective roles of ProofPack, Assay, and the responsible operator">
  <p class="evidence-roles__label">Three separate responsibilities</p>
  <p><strong>ProofPack</strong> makes the result checkable.</p>
  <p><strong>Assay</strong> holds it to the rule fixed before the result was known.</p>
  <p><strong>A person</strong> remains responsible for what happens next.</p>
</aside>

That separation is the evidence boundary. The process trying to improve a system does not get to decide, on its own, that it has succeeded.

## The eval enters the loop

Research rarely follows the line shown in its final chart. It has the shape of a [labyrinth](https://increment.com/documentation/notes-on-the-synthesis-of-labyrinths/): each answer opens another passage. A promising route reaches a wall. We return to an earlier junction carrying what the dead end taught us, then try again.

The straight path appears only afterward, when the work is written down.

An eval changes character when its result becomes feedback. It is no longer only observing a system. It is selecting what the next system will become.

This is why automated research can be both powerful and dangerous. A loop can try a variation, observe the result, keep what appears to help, and begin again. It turns time into search. But the loop is loyal to its eval. If the eval rewards a shortcut, automation will find and refine the shortcut with extraordinary patience.

We therefore work with two coupled loops. One improves the performer. The other improves the eval: its cases, counterexamples, properties, evaluator, and definitions of success.

<figure class="article-illustration article-illustration--hero">
  <img src="/img/articles/evals-as-theory-building/eval-loop-retained-failures.webp" width="1536" height="1024" alt="One person follows red thread through a labyrinth while another redraws a wall, leaving the failed paths visible." loading="lazy" decoding="async" />
  <figcaption>Dead ends are not discarded. They become material for the next eval.</figcaption>
</figure>

The loops inform each other without collapsing into one. A discovered failure can become a new case. A successful counterfeit can become permanent pressure. A repaired evaluator can become a stronger instrument. But each change creates a new claim. Yesterday’s proof cannot silently authorize today’s eval.

<aside class="map-warning" aria-label="The boundary around self-improving evals">
  <p class="map-warning__label">Boundary condition</p>
  <h3 class="map-warning__title">No self-certifying loop.</h3>
  <p>A system may help improve the performer or redraw the eval. It may not conceal which one changed, inherit authority from a previous version, or grade its own progress.</p>
</aside>

Before an eval can judge an activity, it must decide what the activity contains. What is a case? What counts as the same outcome? Which relationships matter? Which differences are errors, and which are legitimate exceptions?

Together, those choices form the eval’s ontology: not a vocabulary of technical nouns, but the distinctions the eval is capable of seeing. The lab designs ontologies and tools that expose those distinctions.

Once they are visible, disagreement has somewhere precise to land: on the definition, relationship, or boundary that produced the score. The disputed assumption can be tested against the work and revised without quietly giving an old result a new meaning.

No eval can reproduce the whole activity. If the map matched the territory in every detail, it would be another territory. The aim is not perfect representation. It is an approximation that can be pressured, corrected, and made more faithful over time.

Peter Naur used *theory* in a practical sense in [“Programming as Theory Building”](https://gist.github.com/onlurking/fc5c81d18cfce9ff81bc968a7f342fb1). It is the understanding that lets someone explain how a system corresponds to the work, why its boundaries were drawn where they were, and what should change when a new case does not fit. The theory is not the documentation. It is what makes intelligent change possible.

Theory building happens when each new case deepens that understanding instead of vanishing into a score. A counterexample exposes a missing distinction. A disagreement forces a definition into view. A dead end records why the next path must differ.

This is why the receipts matter. They cannot contain the complete understanding held by the people who do the work. A receipt cannot reproduce the dinner it records. It can tell us what was ordered, when the transaction happened, and where to begin if the charge is disputed.

Verification preserves a starting point from which that theory can be questioned and rebuilt. A failed case becomes more than an anecdote. A disagreement becomes a definition that can be examined. A claim acquires a boundary, a history, and a route back to the evidence.

This is theory building with receipts.

## What rigorous evals make possible

Most eval systems end with a score. Our lab begins with the question the score cannot answer by itself: *Why should this result be trusted, and how much authority should it receive?*

ProofPack pressures the eval and preserves the resulting facts in a form that can be independently verified. Assay turns workflow evidence into explicit eval environments, fixes the statistical and decision rules, and controls admission, expiry, and revocation. One makes the evidence difficult to fake or accidentally overstate. The other prevents qualified evidence from being used for a purpose it never earned.

<aside class="claim-ceiling" aria-label="The durable asset created by rigorous evaluation">
  <p class="claim-ceiling__label">What persists</p>
  <p>The model is replaceable. A tested, inspectable account of what success means—and the verified history of how that account changes—is the asset.</p>
</aside>

With that foundation, automated loops can improve a harness, refine an eval, and distill repeatable parts of a workflow into a model fitted to the organization. ProofPack keeps each apparent improvement attached to what actually happened. Assay controls which verified findings may teach the next iteration. The loop can learn without swallowing every available signal as truth.

The same evidence boundary can extend beyond the model. [**muser**](https://github.com/High-Performance-AI-Lab/muser) demonstrates our ability to design optimized inference paths for Apple hardware, NVIDIA hardware, or both. [**kvpack**](https://github.com/High-Performance-AI-Lab/kvpack) shows how performance and safety can support each other by preserving expensive model state while binding it to the conditions that give it meaning.

This matters because the place where AI runs is part of the decision. Cost, latency, privacy, and control shape which system is useful. A workflow involving sensitive knowledge should be able to remain inside infrastructure the organization owns. But faster or more private execution is valuable only if the system continues to do the work that justified it.

That brings us back to the eval.

A score still has a useful role. We need abstractions because reality cannot enter an AI system without becoming something else. But a score cannot contain the work, prove its own meaning, or decide how much authority it deserves.

It needs company: the definitions that shaped the eval, the counterexamples that pressured it, the evidence that survived, the rule that governed its use, the person who made the decision, and the conditions that will cause the conclusion to be examined again.

Models will come and go. What should compound is the organization’s understanding of the work: what success means, how to distinguish improvement from camouflage, and which evidence is strong enough to change the system.

<p class="article-coda"><strong>That is the theory.</strong> The receipts are how it survives the next model.</p>

<style>
  .claim-ceiling {
    margin: clamp(42px, 7vw, 64px) 0;
    padding: clamp(24px, 4vw, 34px);
    border: 1px solid var(--line-strong);
    border-left: 4px solid var(--accent);
    border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
    background: var(--surface-2);
  }

  .claim-ceiling__label,
  .map-warning__label,
  .evidence-roles__label {
    margin: 0;
    color: var(--accent);
    font: 700 9px/1 var(--mono);
    letter-spacing: 0.12em;
    text-transform: uppercase;
  }

  .claim-ceiling > p:last-child {
    margin: 18px 0 0;
    color: var(--ink);
    font-family: var(--display);
    font-size: 1.08rem;
    line-height: 1.55;
  }

  .map-warning {
    margin: clamp(42px, 7vw, 64px) 0;
    padding: clamp(24px, 4vw, 34px);
    border: 1px solid var(--line-strong);
    border-top: 4px solid var(--accent);
    border-radius: 0 0 var(--radius-sm) var(--radius-sm);
    background: linear-gradient(135deg, var(--accent-soft), transparent 58%), var(--surface);
  }

  .map-warning__title {
    margin: 16px 0 0;
    color: var(--ink);
    font-family: var(--display);
    font-size: clamp(1.45rem, 3.4vw, 2.25rem);
    font-weight: 620;
    letter-spacing: -0.025em;
    line-height: 1.08;
  }

  .map-warning__quote {
    margin: clamp(24px, 4vw, 34px) 0 0;
    padding: clamp(22px, 4vw, 32px) 0;
    border-top: 1px solid var(--line-strong);
    border-bottom: 1px solid var(--line-strong);
  }

  .map-warning__quote p {
    margin: 0;
    color: var(--ink);
    font-family: var(--display);
    font-size: clamp(2.25rem, 5.5vw, 4.2rem);
    font-weight: 620;
    letter-spacing: -0.04em;
    line-height: 1;
  }

  .map-warning__quote footer {
    margin-top: 18px;
    color: var(--faint);
    font: 600 9px/1.55 var(--mono);
    letter-spacing: 0.06em;
    text-transform: uppercase;
  }

  .map-warning__quote a {
    color: inherit;
    text-decoration-color: var(--line-strong);
    text-underline-offset: 3px;
  }

  .map-warning > p:last-child {
    margin: 22px 0 0;
    color: var(--ink);
    font-family: var(--display);
    font-size: clamp(1.08rem, 1.7vw, 1.25rem);
    font-weight: 520;
    letter-spacing: -0.01em;
    line-height: 1.52;
  }

  .evidence-roles {
    margin: clamp(42px, 7vw, 64px) 0;
    overflow: hidden;
    border: 1px solid var(--line-strong);
    border-top: 4px solid var(--accent);
    border-radius: 0 0 var(--radius-sm) var(--radius-sm);
    background: var(--surface);
  }

  .evidence-roles__label {
    padding: 22px clamp(24px, 4vw, 34px);
    border-bottom: 1px solid var(--line);
  }

  .evidence-roles > p:not(.evidence-roles__label) {
    margin: 0;
    padding: clamp(18px, 3vw, 24px) clamp(24px, 4vw, 34px);
    border-bottom: 1px solid var(--line);
    color: var(--ink);
    font-family: var(--display);
    font-size: clamp(1.15rem, 2.1vw, 1.45rem);
    letter-spacing: -0.015em;
    line-height: 1.35;
  }

  .evidence-roles > p:last-child {
    border-bottom: 0;
  }

  .evidence-roles strong {
    color: var(--accent);
    font-weight: 650;
  }

  .article-coda {
    margin: clamp(48px, 8vw, 76px) 0 0 !important;
    padding-top: clamp(26px, 4vw, 38px);
    border-top: 4px solid var(--accent);
    color: var(--ink);
    font-family: var(--display);
    font-size: clamp(1.55rem, 3.5vw, 2.5rem);
    font-weight: 520;
    letter-spacing: -0.025em;
    line-height: 1.2;
  }

  .article-coda strong {
    color: var(--accent);
    font-weight: 650;
  }

  .article-illustration {
    width: min(1000px, calc(100vw - 32px));
    margin: clamp(44px, 7vw, 76px) 50%;
    transform: translateX(-50%);
  }

  .article-illustration--hero {
    width: min(1120px, calc(100vw - 32px));
  }

  .article-illustration--narrow {
    width: min(900px, calc(100vw - 32px));
  }

  .article-illustration img {
    display: block;
    width: 100%;
    height: auto;
    background: #faf9f7;
  }

  .article-illustration figcaption {
    max-width: 740px;
    margin: 12px auto 0;
    color: var(--faint);
    font: 600 10px/1.55 var(--mono);
    letter-spacing: 0.08em;
    text-transform: uppercase;
  }

  @media (max-width: 640px) {
    .article-illustration,
    .article-illustration--hero,
    .article-illustration--narrow {
      width: calc(100vw - 24px);
      margin-top: 40px;
      margin-bottom: 48px;
    }

    .article-illustration figcaption {
      padding: 0 4px;
      font-size: 9px;
    }
  }
</style>
