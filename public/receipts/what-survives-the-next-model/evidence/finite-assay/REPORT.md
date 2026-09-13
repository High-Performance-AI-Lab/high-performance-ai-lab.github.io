# Finite assay: what the formal theory means in executable form

Corrected and executed 7 September 2026. This is an authored, exact finite mechanics example. This note describes the run after execution; it is not a preregistration or a confirmatory study. The [original output and files](baseline-2026-09-07/manifest.json) were preserved before correction and the original script reproduced its saved output byte-identically in a temporary directory.

Reproduce from this directory with `python3 run.py`. It uses only the Python standard library and writes [result.json](result.json) beside the script. `--output PATH` permits an isolated rerun without overwriting the saved result.

## Claim boundary

These results establish properties of the authored finite mechanisms under their explicit assumptions. They do not establish AI evaluation efficacy, a learned investigator, a real refund provider's behavior, production safety, independently qualified business rules, or novel mathematics. Each result below carries its own narrower limitation. This example remains a supporting mechanics illustration; the planned research concerns learning useful investigations and testing their transfer in more demanding environments.

## What ran

The original four worlds cross committed/uncommitted refund state with idempotent/non-idempotent provider behavior. Every world now includes `pending_original_commit`. An additional fifth world has no visible effect, a non-idempotent provider and a pending original request. All five use the same `observe`, `transition`, `execute` and `effects` functions. An execution ends after the chosen stop/retry action and a `settle_pending` transition. A stop can therefore have a later effect from the outstanding original request. In this authored schedule, a read is followed by the chosen action before the pending request settles.

The probes actually queried are the common timeout, the cached ledger, the fresh authoritative ledger and the provider contract. The contract probe is now queried with both possible results. The original family assumes an authorized intent, exact authoritative observations, and no outstanding or concurrent operation that can commit this intent after the read within the outcome horizon. The fifth world explicitly violates the last assumption.

The tested policies are unconditional stop, unconditional retry, and `inspect_then_act`: read the authoritative ledger, then stop if one effect exists or retry if zero. This conditional policy is hand-authored. Investigation is part of the policy whose success is checked; no learner discovered it.

Decision results have three states: `eligible` when every compatible world satisfies the obligations, `refused` when every compatible world violates them, and `no_valid_decision` when outcomes are mixed (reason `undetermined`) or the compatible family is empty (reason `adequacy_failure`). Passing and failing world counts accompany each result. Qualification of the evidence source is separate: these checks are conditional on the authored observer and transition semantics. An eligible policy is not evidence that those assumptions hold in a real system.

A second component enumerates all 340 delivery sequences of lengths one through four over two intent identifiers and two authority states. Five authored worker variants process each sequence: correct, missing idempotency, ignoring authority, deduplicating by amount, and refusing everything. Three separately expressed obligations examine effects: authority, at most one effect per intent, and exactly one effect for every intent with an authorized delivery. The obligation function does not call the worker transition function, but both share authorship. This code separation does not provide independent specification or scientific custody.

## Results

| Check | Exact result | Limitation |
| --- | --- | --- |
| Initial timeout and successful investigation | Four compatible worlds. Of the three tested policies, only `inspect_then_act` succeeds in all four. Stop and retry have mixed outcomes. | Hand-authored policy; success is conditional on the original family's authoritative-read and no-pending/concurrent-commit assumptions. |
| Cached ledger read | Four compatible worlds remain; `inspect_then_act` still succeeds. | A correct historical reading provides no current-state discrimination here. |
| Fresh ledger read | Two worlds remain. At zero, retry and `inspect_then_act` succeed; stop is refused. At one, stop and `inspect_then_act` succeed; retry has mixed outcomes. | Exact observations and the original family only; the complete provider mechanism remains unidentified. |
| Queried provider contract | Either contract result leaves two worlds. If idempotent, retry and `inspect_then_act` succeed; otherwise only `inspect_then_act` succeeds. | An assumed exact contract probe; no provider contract was fetched or validated. |
| Empty compatibility set | A fresh reading of two produces `no_valid_decision`, reason `adequacy_failure`, for every policy. | Contradiction of this family is distinct from both mixed evidence and a known violation. |
| Coarse environment quotient | Merging committed and uncommitted non-idempotent worlds preserves their timeout but fails to preserve the fresh observation and retry consequence. | One explicit counterexample; it does not implement a general abstraction method. |
| Represented delayed commit | The shared observer returns zero in the fifth world. `inspect_then_act` records zero effects at read, one after retry, and two after `settle_pending`; unconditional retry also ends at two. Stop ends at one. The incomplete family still makes retry eligible. Adding the fifth world leaves three compatible worlds and mixed outcomes for all three policies. | One authored pending mechanism and one settlement schedule; no empirical provider evidence or exhaustive concurrency analysis. The result is computed by actual simulator transitions. |
| Correct worker | No property failures on the 340 enumerated traces. | Only the declared authority/intent rules and delivery horizon through length four. |
| Safety-only checker | Falsely accepts 440 of 1,700 variant–trace rows: 130 amount-deduplication rows and 310 refusal-only rows. The total and split are both recomputed and serialized. | Authored census, not an estimated field error rate; failure categories overlap. |
| Shrinking | A four-delivery duplicate-effect witness reduces to two deliveries of one intent; no single deletion retains the violation. | The shrinker accepts deletions only on target-violation retention. Reachability and oracle determinacy are trivial here; non-target obligations are not enforced. Along this path authority holds and useful completion fails both before and after. This is not causal attribution. |
| Counterfactual non-identification | Two equally weighted two-unit potential-outcome couplings have identical binary interventional marginals and zero average effect; their same-unit switch probabilities are zero and one. | Direct arithmetic for specified couplings, adapted from Pearl, *Causality*, second edition, §1.4.4. These are not fitted structural causal models or identified real-unit counterfactuals. The structural construction and argument are in [the foundations](../SCIENTIFIC-FOUNDATIONS.md#6-counterfactual-fidelity-is-stronger-than-reproducing-outcomes). |

Do not add the per-property counts as distinct failed executions. Exactly-one useful completion also fails when an implementation creates multiple effects.

## Verification evidence

The [executed Node check](../../qa/check_finite_explorer.mjs) reruns Python into a temporary output, requires byte equality with saved `result.json`, and compares all eight explorer scenarios and all fifteen five-world/policy execution traces against that fresh result. It separately recounts all property counts from sequence predicates, including the 130/310 split, and recomputes the two coupling marginals. Its minimal DOM harness executes all eight buttons and the actual render code, checking policy rows, selected buttons, descriptive text and the delayed trace.

The [retained source-check record](verification-2026-09-07/explorer-source.json) contains the command, execution time, source hashes, counts and limits. This checker was authored in the same correction pass; its separate execution is not independent scientific custody or independent specification. The earlier unsupported claim of an independent review has been removed. A separate read-only pass by the coordinating agent retained its [check script](verification-2026-09-07/root_readonly_check.py) and [passing result](verification-2026-09-07/root-readonly-result.json). It inspected the shared simulator, reproduced the saved JSON in isolation, compared all eight binary state combinations and three policies against an algebraic reference, checked the decision states and delayed trace, and recounted 130/310 from input predicates. That pass shares this task’s specification and collaboration context; it is not external replication or empirical semantic validation.

The library checker now invokes this executable check against the served module and requires it to match the source; a stale served copy fails. The Node harness does not perform visual browser rendering or establish browser accessibility.

## What this does not establish

The fixtures, policies, variants and properties are authored. No subject-model call, learned experiment selection, hidden outcome boundary, field observation or prospective memory experiment ran. The runtime generator is an explicit finite enumerator, and the oracle has no measurement noise.

The example supplies executable counterexamples to several invalid inferences: more observations imply more information; matching current output implies environment adequacy; a nonempty compatible set establishes model adequacy; avoiding duplicates implies useful correctness; and matching experimental marginals identifies individual counterfactuals. Its positive policy also shows that gathering information can be part of successful action without identifying the complete world. These logical distinctions are established ideas, not novel-theory claims.

## Next experiment

Use this fixture to check mechanics, then separately specify the reference, enforce a subject-facing information boundary and introduce held-out mechanism families. Vary qualification and retained knowledge independently in the planned controlled study, accounting for harmful acceptances, false refusals, ties, unresolved decisions, useful completion and total investigation cost. The [local audit](../LOCAL-ARCHITECTURE-AUDIT.md#smallest-meaningful-internal-falsification-experiment) defines the intended experiment; it has not been run by this fixture.
