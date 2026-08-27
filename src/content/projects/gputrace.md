---
title: "gputrace"
tagline: "Turn opaque Metal traces into performance evidence you can query, diff, and share."
eyebrow: "06 — Profiler toolkit"
description: "A command-line profiling toolkit for inspecting, comparing, and explaining Apple Metal GPU traces, with exports to pprof, Perfetto, JSON, and Markdown."
url: "https://github.com/High-Performance-AI-Lab/gputrace"
category: "tools"
tags: ["Go", "Metal", "Profiling"]
order: 6
stackOrder: 3
stackAction: "Observe"
stackRole: "Query and compare traces"
accent: "violet"
icon: "trace"
status: "in the lab"
metric: "trace → evidence"
metricLabel: "replay, diff, attribute"
command: "gputrace diff A.gputrace B.gputrace"
---

The toolkit extracts structural and timing evidence from GPU traces, supports repeatable comparisons, and turns profiler artifacts into reviewable reports.
