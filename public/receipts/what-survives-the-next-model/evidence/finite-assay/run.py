"""Exact, authored finite mechanics; no model run or empirical validation.

Exercises decision-relative identification, an invalid world quotient,
property pressure, shrinking, and an explicitly chosen counterfactual coupling.
"""
from dataclasses import asdict, dataclass, replace
from itertools import product
from pathlib import Path
import argparse
import json


@dataclass(frozen=True)
class World:
    committed: int
    idempotent: bool
    pending_original_commit: bool = False


WORLDS = [World(c, i) for c, i in product((0, 1), (False, True))]
DELAYED_WORLD = World(0, False, True)
EXTENDED_WORLDS = WORLDS + [DELAYED_WORLD]
POLICIES = ("stop", "retry", "inspect_then_act")
ASSUMPTION_BOUNDARY = (
    "Conditional on authored transitions, authorized intent, exact authoritative "
    "observations, and the represented outcome horizon; no empirical instrument qualification."
)


def observe(w, probe):
    # A stale observation is accurate about an earlier state, not the present one.
    return {"timeout": "timeout", "cached_ledger": 0,
            "fresh_ledger": w.committed,
            "provider_contract": w.idempotent}[probe]


def transition(w, action):
    """Both requests concern the same intent; settle ends this authored horizon.

    A fresh read does not cancel a pending original request. For an idempotent
    provider, both request completions use the same intent identity.
    """
    if action == "stop":
        return w
    if action == "retry" or (action == "settle_pending" and w.pending_original_commit):
        count = max(1, w.committed) if w.idempotent else w.committed + 1
        return replace(w, committed=count,
                       pending_original_commit=False if action == "settle_pending" else w.pending_original_commit)
    if action == "settle_pending":
        return w
    raise ValueError(action)


def execute(w, policy):
    if policy not in POLICIES:
        raise ValueError(policy)
    state = w
    trace = [{"event": "start", "state": asdict(state)}]
    action = policy
    if policy == "inspect_then_act":
        value = observe(state, "fresh_ledger")
        trace.append({"event": "fresh_ledger", "observation": value, "state": asdict(state)})
        action = "stop" if value else "retry"
    for event in (action, "settle_pending"):
        state = transition(state, event)
        trace.append({"event": event, "state": asdict(state)})
    return {"policy": policy, "initial_state": asdict(w), "trace": trace,
            "final_state": asdict(state), "effects": state.committed}


def effects(w, policy):
    return execute(w, policy)["effects"]


def decision_result(candidate_worlds, policy):
    """Decision status is distinct from the qualification of the evidence source."""
    outcomes = [effects(w, policy) for w in candidate_worlds]
    passing = sum(value == 1 for value in outcomes)
    failing = len(outcomes) - passing
    if not outcomes:
        status, reason = "no_valid_decision", "adequacy_failure"
    elif not failing:
        status, reason = "eligible", "all_compatible_worlds_satisfy"
    elif not passing:
        status, reason = "refused", "all_compatible_worlds_violate"
    else:
        status, reason = "no_valid_decision", "undetermined"
    return {"status": status, "reason": reason, "passing_worlds": passing,
            "failing_worlds": failing, "qualification": "conditional_on_authored_assumptions"}


def eligible(candidate_worlds, policy):
    return decision_result(candidate_worlds, policy)["status"] == "eligible"


def compatible(evidence, family=None):
    family = WORLDS if family is None else family
    return [w for w in family if all(observe(w, p) == o for p, o in evidence)]


SCENARIOS = {
    "timeout": [("timeout", "timeout")],
    "cached": [("timeout", "timeout"), ("cached_ledger", 0)],
    "fresh0": [("timeout", "timeout"), ("fresh_ledger", 0)],
    "fresh1": [("timeout", "timeout"), ("fresh_ledger", 1)],
    "contract0": [("timeout", "timeout"), ("provider_contract", False)],
    "contract1": [("timeout", "timeout"), ("provider_contract", True)],
    "empty": [("fresh_ledger", 2)],
    "late": [("timeout", "timeout"), ("fresh_ledger", observe(DELAYED_WORLD, "fresh_ledger"))],
}


def scenario_result(mode):
    evidence = SCENARIOS[mode]
    candidates = compatible(evidence)
    results = {p: decision_result(candidates, p) for p in POLICIES}
    result = {"mode": mode, "evidence": evidence,
              "compatible": [asdict(w) for w in candidates],
              "policy_results": results,
              "decisions": [p for p in POLICIES if eligible(candidates, p)],
              "omitted_mechanism": mode == "late", "limitation": ASSUMPTION_BOUNDARY}
    if mode == "late":
        extended = compatible(evidence, EXTENDED_WORLDS)
        result["extended_compatible"] = [asdict(w) for w in extended]
        result["extended_policy_results"] = {p: decision_result(extended, p) for p in POLICIES}
        result["delayed_executions"] = {p: execute(DELAYED_WORLD, p) for p in POLICIES}
    return result


def ledger_trace(commands, mutant):
    """Two equally priced, separately authorized intents; actor authority is input.

    `deliver` is repeatable transport delivery. Correct idempotency is by intent,
    not amount. The oracle checks effects against separately expressed obligations (shared authorship).
    """
    paid = {"A": 0, "B": 0}
    accepted = []
    for key, authorized in commands:
        if mutant == "refuse_all" or (not authorized and mutant != "ignore_authority"):
            continue
        if mutant == "dedupe_amount" and sum(paid.values()):
            continue
        if mutant != "no_idempotency" and paid[key]:
            continue
        paid[key] += 1
        accepted.append((key, authorized))
    return {"paid": paid, "accepted": accepted}


def obligations(commands, out):
    requested = {key for key, authorized in commands if authorized}
    return {
        "authority": all(authorized for _, authorized in out["accepted"]),
        "at_most_once_per_intent": all(v <= 1 for v in out["paid"].values()),
        "useful_completion": all(out["paid"][key] == 1 for key in requested),
    }


def same_failure(commands, mutant, property_name):
    return not obligations(commands, ledger_trace(commands, mutant))[property_name]


def shrink(commands, mutant, property_name):
    # Authored deletion operator; preserves this failure, not a claimed root cause.
    current = list(commands)
    changed = True
    while changed:
        changed = False
        for n in range(len(current)):
            trial = current[:n] + current[n + 1:]
            if same_failure(trial, mutant, property_name):
                current = trial
                changed = True
                break
    assert all(not same_failure(current[:n] + current[n+1:], mutant, property_name)
               for n in range(len(current)))
    return current


def run(output_path=None):
    initial = compatible([("timeout", "timeout")])
    assert len(initial) == 4
    assert not eligible(initial, "stop") and not eligible(initial, "retry")
    assert eligible(initial, "inspect_then_act")
    cached = compatible([("timeout", "timeout"), ("cached_ledger", 0)])
    assert cached == initial  # More observations need not add information.
    fresh = {str(value): compatible([("fresh_ledger", value)]) for value in (0, 1)}
    assert eligible(fresh["0"], "retry") and eligible(fresh["1"], "stop")
    assert all(len(v) == 2 for v in fresh.values())  # Decision known; full world unknown.
    assert not compatible([("fresh_ledger", 2)])
    assert not eligible([], "retry")

    # A quotient that collapses commit/no-commit preserves the timeout but not
    # fresh-ledger observations, nor the consequence of retry for a non-idempotent API.
    alias_pair = [World(0, False), World(1, False)]
    assert observe(alias_pair[0], "timeout") == observe(alias_pair[1], "timeout")
    assert observe(alias_pair[0], "fresh_ledger") != observe(alias_pair[1], "fresh_ledger")
    assert effects(alias_pair[0], "retry") != effects(alias_pair[1], "retry")

    # The fifth world runs through the same observer, transitions and horizon.
    # Stop permits the original to settle once; retry races and creates two effects.
    late_observation = observe(DELAYED_WORLD, "fresh_ledger")
    inferred = compatible([("fresh_ledger", late_observation)])
    extended = compatible([("fresh_ledger", late_observation)], EXTENDED_WORLDS)
    delayed_executions = {p: execute(DELAYED_WORLD, p) for p in POLICIES}
    assert eligible(inferred, "retry")
    assert delayed_executions["stop"]["effects"] == 1
    assert delayed_executions["retry"]["effects"] == 2
    assert delayed_executions["inspect_then_act"]["effects"] == 2
    assert len(extended) == 3 and not any(eligible(extended, p) for p in POLICIES)
    assert decision_result([], "retry")["reason"] == "adequacy_failure"
    assert decision_result(initial, "retry")["reason"] == "undetermined"
    assert decision_result(fresh["0"], "stop")["status"] == "refused"
    contracts = {str(value).lower(): compatible([("provider_contract", value)])
                 for value in (False, True)}
    assert all(len(v) == 2 for v in contracts.values())
    assert eligible(contracts["true"], "retry") and not eligible(contracts["false"], "retry")

    alphabet = [(key, auth) for key, auth in product(("A", "B"), (False, True))]
    cases = [commands for n in range(1, 5) for commands in product(alphabet, repeat=n)]
    mutants = ["correct", "no_idempotency", "ignore_authority", "dedupe_amount", "refuse_all"]
    census = {}
    rows = []
    for mutant in mutants:
        failing = {name: 0 for name in ("authority", "at_most_once_per_intent", "useful_completion")}
        for case in cases:
            props = obligations(case, ledger_trace(case, mutant))
            for name, value in props.items():
                failing[name] += not value
            rows.append((mutant, case, props))
        census[mutant] = failing
    assert not any(census["correct"].values())
    assert census["no_idempotency"]["at_most_once_per_intent"] > 0
    assert census["ignore_authority"]["authority"] > 0
    assert census["dedupe_amount"]["useful_completion"] > 0
    assert census["refuse_all"]["useful_completion"] > 0

    # Safety-only scoring accepts useless refusal. Single trace-shape scoring
    # can reject valid alternatives; actual effects are the declared construct.
    safety_false_accepts = sum(p["authority"] and p["at_most_once_per_intent"] and not all(p.values())
                               for _, _, p in rows)
    safety_by_variant = {
        m: sum(p["authority"] and p["at_most_once_per_intent"] and not all(p.values())
               for mm, _, p in rows if mm == m) for m in mutants
    }
    assert sum(safety_by_variant.values()) == safety_false_accepts == 440
    assert safety_by_variant == {"correct": 0, "no_idempotency": 0, "ignore_authority": 0,
                                 "dedupe_amount": 130, "refuse_all": 310}
    example = [("A", True), ("B", True), ("A", True), ("B", True)]
    shrunk = shrink(example, "no_idempotency", "at_most_once_per_intent")
    assert len(shrunk) == 2 and shrunk[0][0] == shrunk[1][0]

    # Same observed marginals and randomized mean effect; different same-unit
    # counterfactual couplings. An SCM/coupling adds information beyond the marginals.
    worlds_same = [(0, 0), (1, 1)]
    worlds_flip = [(0, 1), (1, 0)]
    marginal = lambda a: [sum(y[j] for y in a) / len(a) for j in (0, 1)]
    assert marginal(worlds_same) == marginal(worlds_flip) == [0.5, 0.5]
    cf_switch = lambda a: sum(y0 != y1 for y0, y1 in a) / len(a)
    assert cf_switch(worlds_same) == 0 and cf_switch(worlds_flip) == 1

    result = {
        "status": "exact authored finite checks passed",
        "claim_boundary": "Mechanics demonstration, not AI evaluation efficacy, real refund validation, production safety or novel-theory proof.",
        "worlds": [asdict(w) for w in WORLDS],
        "extended_worlds": [asdict(w) for w in EXTENDED_WORLDS],
        "identification": {
            "initial_compatible_worlds": len(initial), "after_cached_read": len(cached),
            "after_fresh_read": {k: len(v) for k, v in fresh.items()},
            "safe_complete_before_read": [p for p in POLICIES if eligible(initial, p)],
            "after_read_decision": {k: [p for p in POLICIES if eligible(v, p)] for k, v in fresh.items()},
            "after_provider_contract": {
                k: {"worlds": len(v), "policy_results": {p: decision_result(v, p) for p in POLICIES}}
                for k, v in contracts.items()},
            "empty_set_result": decision_result([], "retry"),
            "queried_probes": sorted({probe for evidence in SCENARIOS.values() for probe, _ in evidence}),
            "proof_status": "Exact enumeration of this authored finite model, conditional on its semantics.",
            "limitation": "The original four worlds exclude pending or concurrent commits; the policy is hand-authored, not learned. " + ASSUMPTION_BOUNDARY,
        },
        "invalid_abstraction": {
            "same_timeout": observe(alias_pair[0], "timeout") == observe(alias_pair[1], "timeout"),
            "preserves_fresh_observation": observe(alias_pair[0], "fresh_ledger") == observe(alias_pair[1], "fresh_ledger"),
            "preserves_retry_effect": effects(alias_pair[0], "retry") == effects(alias_pair[1], "retry"),
            "limitation": "One explicit counterexample to this quotient; not a general abstraction construction or validation method."},
        "outside_model_witness": {
            "omitted_mechanism": "Pending original commit occurs after authoritative ledger read and retry.",
            "represented_state": asdict(DELAYED_WORLD),
            "fresh_observation": late_observation,
            "compatible_worlds_in_incomplete_family": len(inferred),
            "retry_result_within_incomplete_family": decision_result(inferred, "retry"),
            "compatible_worlds_in_extended_family": len(extended),
            "policy_results_within_extended_family": {p: decision_result(extended, p) for p in POLICIES},
            "executions": delayed_executions,
            "actual_effects_in_extended_witness": delayed_executions["retry"]["effects"],
            "proof_status": "Computed by the same observe, transition, execute and effects functions as the original family.",
            "limitation": "One authored delayed non-idempotent mechanism and one settle-after-action schedule; no real-provider validation or exhaustive concurrency exploration.",
            "conclusion": "A nonempty compatible set does not establish model adequacy. Fresh observation alone is insufficient when commits can race."
        },
        "property_census": {"case_count": len(cases), "max_delivery_horizon": 4,
                            "subject_variants": len(mutants), "outcomes": census,
                            "safety_only_false_accepts": safety_false_accepts,
                            "safety_only_false_accepts_by_variant": safety_by_variant,
                            "limitation": "Authored 1,700-row census, not a field error rate; failure categories overlap; subject and oracle share authorship."},
        "shrink": {"original": example, "reduced": shrunk,
                   "guarantee": "Deletion-one-minimal for duplicate-effect property in this finite trace; not causal attribution.",
                   "original_obligations": obligations(example, ledger_trace(example, "no_idempotency")),
                   "reduced_obligations": obligations(shrunk, ledger_trace(shrunk, "no_idempotency")),
                   "limitation": "Only target-violation retention is checked when accepting a deletion. Reachability and determinacy are trivial here; non-target obligations are not enforced."},
        "counterfactual_nonidentification": {
            "coupling_1": worlds_same, "coupling_2": worlds_flip,
            "both_interventional_marginals": marginal(worlds_same),
            "both_average_effects": marginal(worlds_same)[1] - marginal(worlds_same)[0],
            "switch_probability_under_coupling_1": cf_switch(worlds_same),
            "switch_probability_under_coupling_2": cf_switch(worlds_flip),
            "source": "Adaptation in potential-outcome notation of Pearl, Causality, 2nd ed., section 1.4.4; structural construction is in SCIENTIFIC-FOUNDATIONS.md section 6.",
            "proof_status": "Direct arithmetic for two specified equally weighted two-unit couplings; a constructive non-identification example, not a novel theorem.",
            "limitation": "These are potential-outcome tables, not fitted structural causal models, identified real-unit counterfactuals or an intervention-based attribution implementation."},
        "explorer_scenarios": {mode: scenario_result(mode) for mode in SCENARIOS},
        "policy_executions": [execute(w, p) for w in EXTENDED_WORLDS for p in POLICIES],
        "limitations": ["Worlds, properties, variants and oracle are manually authored by one implementation team.",
                        "Decision status is separate from instrument qualification: exact authored assumptions supply the finite check's conditional boundary, not empirical adequacy evidence.",
                        "No independent custody, generated natural-language policy, model calls or prospective learning.",
                        "Enumeration covers the four-world family, one additional delayed state under its declared schedule, and delivery traces through length four.",
                        "Static membership tests assume exact observations; no noise or probabilistic coverage guarantee."]
    }
    dest = Path(output_path) if output_path else Path(__file__).with_name("result.json")
    dest.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, help="Write results here instead of beside the script")
    run(parser.parse_args().output)
