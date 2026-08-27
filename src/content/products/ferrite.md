---
name: "Ferrite"
tagline: "A Rust + Metal inference server that makes local AI on Apple Silicon fast, measurable, and honest."
description: "Ferrite runs large language models on the hardware you already own. It is engineered for predictable latency, low energy per token, and a correctness gate before every published number — so a faster result is never a wrong one."
eyebrow: "01 — Inference Engine"
category: "Platform"
url: "https://github.com/High-Performance-AI-Lab/ferrite"
command: "ferrite serve model.gguf"
accent: "teal"
order: 1
featured: true
features:
  - code: "01"
    label: "Serve any GGUF model"
    detail: "Ollama- and OpenAI-compatible APIs. Drop in a model and call it from anything you already run."
  - code: "02"
    label: "Metal-first kernels"
    detail: "Tuned for Apple Silicon — low latency, sustained throughput, and low energy per token."
  - code: "03"
    label: "Correctness-gated"
    detail: "Every throughput claim is checked against a reference decode before timing begins."
metrics:
  - value: "75.6"
    label: "tok/s decode · Qwen 0.5B · A18 Pro"
  - value: "0.046"
    label: "J/token energy at the same point"
  - value: "100"
    label: "% outputs verified against reference"
---

Ferrite is the lab's flagship system. It is both the product we ship and the instrument we use to measure every other project in the stack.
