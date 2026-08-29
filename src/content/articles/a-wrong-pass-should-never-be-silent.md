---
title: "A wrong pass should never be silent"
description: "Benchmark verifiers are the least-measured part of AI evaluation. Why we red-team our own graders, and what we will publish."
publishedAt: 2026-08-29
kind: "article"
author: "High Performance AI Lab"
tags: ["Evaluation", "Verifiers", "Method"]
readingTime: "4 min"
featured: true
---

Every benchmark score is two claims. The model did something. A program judged it correctly.

The first claim gets leaderboards, error bars, and a news cycle. The second usually ships unexamined. And when a grader is wrong, it is wrong silently: a false pass looks exactly like a true one. Same green check, same reward, same row in the table.

We measure inference obsessively — the machine, the quantization, the warmup, the trial count. The judge deserves the same treatment.

## The public record

This is not a hypothetical concern, and the field's best projects already act on it.

Terminal-Bench 4.0 [fixed 19 tasks](https://www.tbench.ai/news/terminal-bench-4-0), updating instructions, environments, and verifiers "to address flakiness or misspecification," and removed 8 more — for saturation, refusals, public solutions, and unresolved quality issues. That is what healthy maintenance looks like. It is also direct evidence that graders drift and break in the wild, at the highest-profile agent benchmark there is.

Harbor, the runtime Terminal-Bench runs on, makes a quieter choice worth naming: in its pass-at-k computation, [a trial without a recorded reward counts as a failure](https://github.com/harbor-framework/harbor/blob/d0b584772b835a882ddec31812459eb0c8d70a75/src/harbor/utils/pass_at_k.py#L32-L45). Conservative, defensible — and it folds infrastructure errors into the headline number, where they are indistinguishable from model failures. Harbor already has the right machinery for verifier accountability: [separate verifier environments](https://www.harborframework.com/docs/tasks) and a [regrade workflow](https://www.harborframework.com/docs/run-jobs/regrade) that re-scores recorded runs under a new verifier without re-running the model. What is missing, there and everywhere, is the evidence contract on top: error-aware accounting, and a verdict that carries its own receipt.

## The failure you cannot rotate away

The structural weakness is always the same. A verifier probes a slice of the behavior it is supposed to pin down. An implementation that is correct exactly where probed — and wrong everywhere else — passes. At every seed. Rotating seeds varies the draws, not the domain.

This failure mode is invisible from inside the benchmark. The only way to see it is to attack your own grader and check its verdicts against ground truth it does not control.

## Graders became reward functions

There was a time when a weak verifier just misranked a leaderboard. That time is over. Verifiable rewards now drive reinforcement learning and agentic training loops. A gameable grader does not merely misjudge — it teaches models to game. The verifier is the least-audited component in the most consequential position.

## Our rule

In our storage work the rule is that a wrong restore must fail closed, never succeed silently — kvpack verifies identity and integrity before it hands back a byte of state. Evaluation deserves the same rule. A verdict is a claim. Claims travel with receipts.

## What we are doing about it

We red-teamed our own property-based benchmark harness — white-box, with a frontier model given the grader's full source and the explicit goal of getting wrong code certified as correct. It found real escapes. We used every one of them to harden the graders. The corpus, the counts, and the taxonomy publish with receipts, not before.

Then we measure the fix the honest way: a preregistered before/after experiment. Two environments identical to the byte except the hidden verifier. Same model, same prompts, same call budget. Outcome categories, analysis, and invalidation rules frozen and registered before the first call. Sessions as the unit of analysis, because adaptive attempts are not independent. Negative results publish unchanged.

All of it runs on hardware we own, with hash-chained ledgers and one reproduction command.

What will ship, in order:

- The escape corpus and its taxonomy, with the captured exploits replayable.
- The frozen preregistration, published before the run.
- The result — whatever it is.
- The tooling and receipts, so the claims can be checked without trusting us.

"Measured, or it doesn't ship" applies to our own graders first.
