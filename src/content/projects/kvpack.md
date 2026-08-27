---
title: "kvpack"
tagline: "Resume exact model context without paying the prefill cost twice."
eyebrow: "02 — Cache infrastructure"
description: "A high-performance replay layer that checkpoints KV cache and recurrent state, then restores exact prefixes without repeating prefill."
url: "https://github.com/High-Performance-AI-Lab/kvpack"
category: "systems"
tags: ["Rust", "KV cache", "C ABI"]
order: 2
stackOrder: 2
stackAction: "Remember"
stackRole: "Reusable model state"
accent: "cobalt"
icon: "checkpoint"
status: "open source"
metric: "fail closed"
metricLabel: "identity + integrity verified"
command: "cargo add kvpack"
---

Crash-safe publication, content-addressed prefix lookup, bounded parallel restore, and optional authenticated encryption.
