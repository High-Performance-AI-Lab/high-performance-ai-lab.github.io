---
title: "handwerk"
tagline: "Small-model tool calling, learned through craft."
eyebrow: "10 — Small-model craft"
description: "A 46M controller benchmarked on choosing tools and emitting structurally valid, type-correct JSON calls, with improved abstention, at 1/65th the size of the 3B teacher."
url: "https://github.com/High-Performance-AI-Lab/handwerk"
category: "systems"
tags: ["Python", "Small models", "Tool calling"]
order: 10
stackOrder: 10
stackAction: "Craft"
stackRole: "Small-model controller"
accent: "amber"
icon: "neural-die"
status: "research release"
metric: "46M"
metricLabel: "vs 3B teacher · 1/65th size"
command: "python harness.py"
---

Handwerk studies how a small model's tool selection is bounded by demonstrated craft — verified, on-policy data — rather than raw capacity. The central finding: small amounts of the right data move a 46M model where bulk demonstrations cannot.
