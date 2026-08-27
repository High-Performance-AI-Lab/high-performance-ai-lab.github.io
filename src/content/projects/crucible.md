---
title: "crucible"
tagline: "An auto-kernel loop that searches, benchmarks, and certifies faster GPU kernels."
eyebrow: "03 — Kernel synthesis"
description: "Generate and benchmark candidate GPU kernels, then certify the invariants that keep the winners correct."
category: "systems"
tags: ["Kernels", "TLA+", "Search"]
order: 3
stackOrder: 4
stackAction: "Optimize"
stackRole: "Search with invariants"
accent: "citron"
icon: "proof"
status: "in the lab"
metric: "optimize → certify"
metricLabel: "performance with invariants"
command: "crucible search kernel.toml"
---

Crucible brings measurement and specification together so optimization does not have to mean giving up a reasoned correctness story.
