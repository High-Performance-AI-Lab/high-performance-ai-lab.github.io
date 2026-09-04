---
title: "What we mean by measured local AI"
description: "A short operating note on why correctness, machine context, and raw evidence belong beside every performance number."
publishedAt: 2026-07-27
kind: "field-note"
author: "High Performance AI Lab"
tags: ["Measurement", "Inference", "Method"]
readingTime: "3 min"
featured: true
homepageExcerpt:
  - "Local inference is full of numbers that look comparable and are not. Tokens per second can describe prefill or decode, a warm cache or a cold start, one token or a long run, a correct implementation or a subtly broken one."
  - "Our rule is simple: the conditions travel with the claim. Correctness, machine context, and raw evidence belong beside every performance number."
---

Local inference is full of numbers that look comparable and are not. Tokens per second can describe prefill or decode, a warm cache or a cold start, one token or a long run, a correct implementation or a subtly broken one.

Our rule is simple: the conditions travel with the claim.

## Correctness comes first

Before timing an optimization, we compare its output with a reference implementation. The exact gate depends on the work—tokens, logits, cache state, or a numerical tolerance—but it must be explicit. A faster wrong answer is not an optimization.

## The machine is part of the result

Every useful measurement names the hardware, model, quantization, runtime path, workload shape, warmup, and trial count. Those details are not appendix material. They define what the number means.

## Evidence should outlive the announcement

Summaries are useful; artifacts are better. We publish the traces, manifests, scripts, and limits that let another person inspect the result or reproduce it on a second machine.

That is what “measured” means here: not certainty, but a claim with enough structure to be challenged and improved.
