---
title: "ferrite"
tagline: "Sustain high-throughput local inference on the Apple hardware people already own."
eyebrow: "01 — Inference engine"
description: "A Rust and Metal LLM server engineered for predictable latency, low energy per token, and rigorous performance measurement on Apple hardware."
url: "https://github.com/High-Performance-AI-Lab/ferrite"
category: "systems"
tags: ["Rust", "Metal", "GGUF"]
order: 1
stackOrder: 1
stackAction: "Run"
stackRole: "Inference runtime"
accent: "oxide"
icon: "lattice"
status: "active research"
metric: "0.0463 J/token"
metricLabel: "Qwen 0.5B · A18 Pro"
command: "ferrite serve model.gguf"
featured: true
---

Ferrite exposes Ollama-compatible and OpenAI-compatible APIs. Every published throughput number passes a correctness gate against a reference implementation first.
