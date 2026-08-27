---
title: "autoharness"
tagline: "Autonomously discover the best prompt harness for a small model."
eyebrow: "09 — Harness discovery"
description: "An overnight discovery loop that edits harness.py to maximize judge-verified eval accuracy on a frozen small model, collecting residual failures as a post-training corpus."
url: "https://github.com/High-Performance-AI-Lab/auto-harness"
category: "tools"
tags: ["Python", "Agents", "RL"]
order: 9
stackOrder: 9
stackAction: "Discover"
stackRole: "Autonomous harness search"
accent: "cyan"
icon: "trace"
status: "in the lab"
metric: "eval_accuracy"
metricLabel: "judge-verified, no training"
command: "python harness.py"
---

autoharness applies the autoresearch keep/revert loop to prompt engineering. Instead of editing model weights, it edits the prompt strategy — instructions, chain-of-thought, few-shot count, format — and keeps only changes that improve judge-verified accuracy.
