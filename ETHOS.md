# High Performance AI Lab — ethos (draft)

> A faster wrong answer is not progress.\
> A cheaper black box is not a product.\
> A bigger model is not a system.

We build systems for local, inspectable, evidence-bound intelligence.

## Voice

Say what you measured. Name the machine. Show the receipt. Skip the adjectives. We write like engineers who expect a skeptical reader and a second machine.

## What we believe

1. **The machine is part of the result.**
   Every useful measurement names the hardware, model, quantization, runtime path, workload shape, warmup, and trial count. Those details are not appendix material. They define what the number means.

2. **Correctness comes first.**
   Before we time an optimization, we compare its output with a reference. A faster wrong answer is not an optimization. A cheaper wrong answer is not a saving.

3. **State should be explicit and identity-bound.**
   KV caches, recurrent state, agent traces, and proof artifacts are not implementation details. They are first-class objects with identities, checksums, and fail-closed boundaries.

4. **Source is a promise, not a deliverable.**
   Open source matters because it lets others inspect, reproduce, and challenge our methods. We publish the code, the conditions, and the evidence behind every claim.

5. **Hard-won knowledge should become a ladder.**
   We document the path from first principle to fast kernel — including the wrong turns — so the next person starts further ahead.

6. **Intelligence must fit the work.**
   The next leap will not come from one model doing everything. Understand the task, the machine, and the boundary well enough, and you can build the system the work actually needs.

## What we do

We work across the whole path from task to silicon:

- **Run** — Ferrite, a local inference engine for Apple Silicon.
- **Remember** — kvpack, a replay layer for reusable model state.
- **Observe** — gputrace, a profiler that turns Metal traces into evidence.
- **Optimize** — Crucible, a search loop for verified faster kernels.
- **Port** — The ANE Book, a field guide to deploying on the Neural Engine.
- **Teach** — Inference School, an open curriculum from first principles.
- **Prove** — fail-closed evaluation and proof artifacts for agents.
- **Bind** — workflow-level model binding with statistics.
- **Discover** — autoharness, autonomous harness discovery for small models.
- **Craft** — Handwerk, small-model tool calling learned through craft.

## What we are not

- We are not an AI research lab chasing scale.
- We are not a model company.
- We are not a cloud API vendor.
- We do not rent intelligence by the token.

We build systems. We make fast, private, inspectable intelligence reproducible.

## The standard

No borrowed claims.\
No performance without parity.\
No progress without a way back.\
No release without a receipt.
