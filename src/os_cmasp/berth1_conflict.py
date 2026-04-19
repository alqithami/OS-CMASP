"""Berth-1-Conflict: executable OS-CMASP separation scaffold.

Dependency-free preflight harness for the manuscript's process-semantics claim.
The solver is frozen; ablations change only claim-state semantics or named sanity
conditions. The core invariant is that latent readiness is excluded from the
controller-visible context chi_B1(x) and can enter ordinary decisions only via
claim records.

New in v22:
- preflight is the default; benchmark outputs require --mode run;
- synthetic results require --allow-synthetic-results;
- replay-schema and paired-bank checks are available before any local run;
- run manifests record solver, dominance, schema, conditions, and replay hash.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from random import Random
from typing import Dict, Iterable, List, Optional, Tuple
from collections import defaultdict
import argparse
import csv
import hashlib
import json
import math
from pathlib import Path

Action = str
REQUIRED_PROPS = ("ready", "craneOK", "etaOnTime", "weatherSafe")
CURRENT_SITUATION = "berth-admission/current"
PLANNING_SITUATION = "berth-admission/planning"
UNKNOWN_SITUATION = "unknown"

OBSERVER_RANK = {
    "ready": {"human_dispatcher": 6, "harbor_master": 5, "terminal_ops": 4, "ais_feed": 2, "strategic_plan": 1, "legacy_dashboard": 1, "unknown": 0},
    "craneOK": {"human_dispatcher": 6, "crane_maintenance": 5, "terminal_ops": 4, "strategic_plan": 1, "unknown": 0},
    "etaOnTime": {"human_dispatcher": 6, "harbor_master": 5, "ais_feed": 4, "carrier_schedule": 2, "strategic_plan": 1, "unknown": 0},
    "weatherSafe": {"human_dispatcher": 6, "port_safety": 5, "local_sensor": 4, "approved_weather_feed": 3, "strategic_plan": 1, "unknown": 0},
}
FRESHNESS_WINDOW = {"ready": 2, "craneOK": 4, "etaOnTime": 1, "weatherSafe": 2}
SOLVER_VERSION = "berth1-fixed-solver-v22"
DOMINANCE_TABLE_VERSION = "maritime-dominance-v22"
ABLATION_CONDITIONS = [
    "provenance_preserving",
    "provenance_erased",
    "random_label_placebo",
    "labels_without_gating",
    "oracle_visible_state",
    "benign_agreement",
]
REPLAY_REQUIRED_FIELDS = {"seed", "t", "ready", "scenario", "prop", "value", "observer", "situation"}
REPLAY_TEMPLATE_FIELDS = [
    "seed","t","ready","crane_ok","eta_on_time","weather_safe","scenario",
    "queue_state","weather_regime","disruption_family","vessel_class","operating_mode",
    "time_bucket","berth_slot","eta_bin","prop","value","observer","situation",
    "credibility","timestamp","provenance",
]

@dataclass(frozen=True)
class LatentState:
    ready: bool
    crane_ok: bool
    eta_on_time: bool
    weather_safe: bool
    queue_state: str = "normal"
    weather_regime: str = "clear"
    disruption_family: str = "none"
    vessel_class: str = "feeder"
    operating_mode: str = "nominal"
    time_bucket: str = "day"
    berth_slot: str = "slot-A"
    eta_bin: str = "on-window"

def chi_b1(x: LatentState) -> Dict[str, str]:
    """Controller-visible context. Hidden safety/precondition truth is excluded."""
    return {
        "queue_state": x.queue_state,
        "weather_regime": x.weather_regime,
        "disruption_family": x.disruption_family,
        "vessel_class": x.vessel_class,
        "operating_mode": x.operating_mode,
        "time_bucket": x.time_bucket,
        "berth_slot": x.berth_slot,
        "eta_bin": x.eta_bin,
    }

@dataclass(frozen=True)
class Claim:
    prop: str
    value: bool
    observer: str
    situation: str
    credibility: float = 1.0
    timestamp: int = 0
    provenance: str = "synthetic"

@dataclass(frozen=True)
class EpisodeStep:
    seed: int
    t: int
    scenario: str
    latent: LatentState
    claims: Tuple[Claim, ...]

def truth(x: LatentState, prop: str) -> bool:
    if prop == "ready": return x.ready
    if prop == "craneOK": return x.crane_ok
    if prop == "etaOnTime": return x.eta_on_time
    if prop == "weatherSafe": return x.weather_safe
    raise KeyError(prop)

def base_claims(x: LatentState, t: int) -> List[Claim]:
    return [
        Claim("ready", x.ready, "harbor_master", CURRENT_SITUATION, timestamp=t, provenance="base-ready"),
        Claim("craneOK", x.crane_ok, "crane_maintenance", CURRENT_SITUATION, timestamp=t, provenance="base-crane"),
        Claim("etaOnTime", x.eta_on_time, "ais_feed", CURRENT_SITUATION, timestamp=t, provenance="base-eta"),
        Claim("weatherSafe", x.weather_safe, "port_safety", CURRENT_SITUATION, timestamp=t, provenance="base-weather"),
    ]

def replace_prop(claims: List[Claim], prop: str, repl: Iterable[Claim]) -> List[Claim]:
    return [c for c in claims if c.prop != prop] + list(repl)

def make_claims(x: LatentState, scenario: str, t: int) -> List[Claim]:
    claims = base_claims(x, t)
    if scenario == "benign_agreement":
        return claims + [
            Claim("ready", x.ready, "strategic_plan", PLANNING_SITUATION, timestamp=t, provenance="agree-ready"),
            Claim("craneOK", x.crane_ok, "terminal_ops", CURRENT_SITUATION, timestamp=t, provenance="agree-crane"),
            Claim("etaOnTime", x.eta_on_time, "carrier_schedule", PLANNING_SITUATION, timestamp=t, provenance="agree-eta"),
            Claim("weatherSafe", x.weather_safe, "approved_weather_feed", CURRENT_SITUATION, timestamp=t, provenance="agree-weather"),
        ]
    if scenario == "authority_conflict":
        return replace_prop(claims, "ready", [
            Claim("ready", x.ready, "harbor_master", CURRENT_SITUATION, timestamp=t, provenance="authoritative-local"),
            Claim("ready", not x.ready, "strategic_plan", PLANNING_SITUATION, timestamp=t, provenance="lower-plan"),
        ])
    if scenario == "freshness_conflict":
        return replace_prop(claims, "etaOnTime", [
            Claim("etaOnTime", x.eta_on_time, "ais_feed", CURRENT_SITUATION, timestamp=t, provenance="fresh-ais"),
            Claim("etaOnTime", not x.eta_on_time, "ais_feed", CURRENT_SITUATION, timestamp=t - 5, provenance="stale-ais"),
        ])
    if scenario == "context_conflict":
        return replace_prop(claims, "ready", [
            Claim("ready", x.ready, "terminal_ops", CURRENT_SITUATION, timestamp=t, provenance="current-ops"),
            Claim("ready", not x.ready, "terminal_ops", PLANNING_SITUATION, timestamp=t + 1, provenance="planning-context"),
        ])
    if scenario == "human_override":
        return replace_prop(claims, "weatherSafe", [
            Claim("weatherSafe", x.weather_safe, "human_dispatcher", CURRENT_SITUATION, timestamp=t, provenance="human-override"),
            Claim("weatherSafe", not x.weather_safe, "approved_weather_feed", CURRENT_SITUATION, timestamp=t, provenance="feed-conflict"),
        ])
    raise ValueError(f"unknown scenario: {scenario}")

def sample_state(rng: Random, scenario: str, p_all_clear: float) -> LatentState:
    if scenario == "benign_agreement":
        return LatentState(True, True, True, True)
    focal = rng.random() < p_all_clear
    if scenario in ("authority_conflict", "context_conflict"):
        return LatentState(focal, True, True, True)
    if scenario == "freshness_conflict":
        return LatentState(True, True, focal, True)
    if scenario == "human_override":
        return LatentState(True, True, True, focal)
    raise ValueError(scenario)

def scenario_for_step(scenario: str, t: int) -> str:
    if scenario == "mixed":
        return ["authority_conflict", "freshness_conflict", "context_conflict", "human_override"][t % 4]
    return scenario

def generate_episode_bank(scenario: str, horizon: int, seeds: int, p_all_clear: float) -> List[EpisodeStep]:
    bank: List[EpisodeStep] = []
    for seed in range(seeds):
        rng = Random(seed)
        for t in range(horizon):
            scen = scenario_for_step(scenario, t)
            x = sample_state(rng, scen, p_all_clear)
            bank.append(EpisodeStep(seed, t, scen, x, tuple(make_claims(x, scen, t))))
    return bank

def parse_bool(x: str) -> bool:
    return str(x).strip().lower() in {"1", "true", "yes", "y"}

def load_replay_bank(path: str) -> List[EpisodeStep]:
    replay_path = Path(path)
    if not replay_path.exists():
        raise FileNotFoundError(f"Replay CSV not found: {path}")
    grouped: Dict[Tuple[int, int], List[Dict[str, str]]] = defaultdict(list)
    with open(replay_path, newline="") as f:
        reader = csv.DictReader(f)
        missing = REPLAY_REQUIRED_FIELDS - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"replay CSV missing columns: {sorted(missing)}")
        for row in reader:
            grouped[(int(row["seed"]), int(row["t"]))].append(row)
    bank: List[EpisodeStep] = []
    for (seed, t), rows in sorted(grouped.items()):
        r0 = rows[0]
        x = LatentState(
            ready=parse_bool(r0["ready"]),
            crane_ok=parse_bool(r0.get("crane_ok", "true")),
            eta_on_time=parse_bool(r0.get("eta_on_time", "true")),
            weather_safe=parse_bool(r0.get("weather_safe", "true")),
            queue_state=r0.get("queue_state", "normal"),
            weather_regime=r0.get("weather_regime", "clear"),
            disruption_family=r0.get("disruption_family", "none"),
            vessel_class=r0.get("vessel_class", "feeder"),
            operating_mode=r0.get("operating_mode", "nominal"),
            time_bucket=r0.get("time_bucket", "day"),
            berth_slot=r0.get("berth_slot", "slot-A"),
            eta_bin=r0.get("eta_bin", "on-window"),
        )
        claims = tuple(
            Claim(
                prop=r["prop"],
                value=parse_bool(r["value"]),
                observer=r["observer"],
                situation=r["situation"],
                credibility=float(r.get("credibility", 1.0) or 1.0),
                timestamp=int(float(r.get("timestamp", t) or t)),
                provenance=r.get("provenance", "replay"),
            )
            for r in rows
        )
        bank.append(EpisodeStep(seed, t, r0["scenario"], x, claims))
    return bank

def write_replay_template(path: str) -> None:
    fields = REPLAY_TEMPLATE_FIELDS
    rows = [
        {"seed":0,"t":0,"ready":"true","crane_ok":"true","eta_on_time":"true","weather_safe":"true","scenario":"authority_conflict","queue_state":"normal","weather_regime":"clear","disruption_family":"none","vessel_class":"feeder","operating_mode":"nominal","time_bucket":"day","berth_slot":"slot-A","eta_bin":"on-window","prop":"ready","value":"true","observer":"harbor_master","situation":CURRENT_SITUATION,"credibility":1.0,"timestamp":0,"provenance":"template-authority"},
        {"seed":0,"t":0,"ready":"true","crane_ok":"true","eta_on_time":"true","weather_safe":"true","scenario":"authority_conflict","queue_state":"normal","weather_regime":"clear","disruption_family":"none","vessel_class":"feeder","operating_mode":"nominal","time_bucket":"day","berth_slot":"slot-A","eta_bin":"on-window","prop":"ready","value":"false","observer":"strategic_plan","situation":PLANNING_SITUATION,"credibility":1.0,"timestamp":0,"provenance":"template-plan"},
    ]
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

def transform_claims(claims: Tuple[Claim, ...], condition: str, rng: Random) -> List[Claim]:
    if condition in {"provenance_preserving", "labels_without_gating", "oracle_visible_state"}:
        return list(claims)
    if condition == "benign_agreement":
        first_value: Dict[str, bool] = {}
        for c in claims:
            first_value.setdefault(c.prop, c.value)
        return [Claim(c.prop, first_value[c.prop], c.observer, c.situation, c.credibility, c.timestamp, "benign-agreement") for c in claims]
    if condition == "provenance_erased":
        return [Claim(c.prop, c.value, "unknown", UNKNOWN_SITUATION, c.credibility, c.timestamp, "erased") for c in claims]
    if condition == "random_label_placebo":
        by_prop: Dict[str, List[Tuple[str, str]]] = defaultdict(list)
        for c in claims:
            by_prop[c.prop].append((c.observer, c.situation))
        shuffled: Dict[str, List[Tuple[str, str]]] = {}
        for prop, labels in by_prop.items():
            labels2 = list(labels)
            rng.shuffle(labels2)
            shuffled[prop] = labels2
        counters: Dict[str, int] = defaultdict(int)
        out = []
        for c in claims:
            k = counters[c.prop]
            counters[c.prop] += 1
            observer, situation = shuffled[c.prop][k]
            out.append(Claim(c.prop, c.value, observer, situation, c.credibility, c.timestamp, "randomized"))
        return out
    raise ValueError(f"unknown condition: {condition}")

def situation_score(situation: str) -> int:
    if situation == CURRENT_SITUATION: return 2
    if situation == PLANNING_SITUATION: return 1
    return 0

def claim_score(c: Claim, t: int) -> Tuple[int, int, int, float]:
    rank = OBSERVER_RANK.get(c.prop, {}).get(c.observer, 0)
    fresh = int((t - c.timestamp) <= FRESHNESS_WINDOW.get(c.prop, 0))
    return (situation_score(c.situation), rank, fresh, c.credibility)

def dominant_value(claims: Iterable[Claim], prop: str, t: int) -> Tuple[Optional[bool], Tuple[int, int, int, float], bool]:
    rel = [c for c in claims if c.prop == prop]
    if not rel:
        return None, (-1, -1, -1, 0.0), False
    top_score = max(claim_score(c, t) for c in rel)
    values = {c.value for c in rel if claim_score(c, t) == top_score}
    if len(values) != 1:
        return None, top_score, True
    return next(iter(values)), top_score, False

def contradiction_count(claims: Iterable[Claim]) -> int:
    return sum(int(len({c.value for c in claims if c.prop == prop}) > 1) for prop in REQUIRED_PROPS)

def optimistic_base_proposal(claims: List[Claim]) -> Action:
    for prop in REQUIRED_PROPS:
        if not any(c.prop == prop and c.value for c in claims):
            return "hold"
    return "go"

def certify_go(claims: List[Claim], t: int) -> Tuple[bool, str]:
    bad = []
    for prop in REQUIRED_PROPS:
        value, score, tied = dominant_value(claims, prop, t)
        sit, rank, _fresh, _cred = score
        if value is not True or tied or sit < 1 or rank < 3:
            bad.append(prop)
    if bad:
        return False, "uncertified-dominance-failed:" + ";".join(bad)
    return True, "dominant-support-certificate"

def fixed_solver(visible: Dict[str, str], claims: List[Claim], condition: str, x: LatentState, t: int) -> Tuple[Action, str, int, int]:
    del visible
    if condition == "oracle_visible_state":
        should_go = all(truth(x, p) for p in REQUIRED_PROPS)
        return ("go" if should_go else "hold"), "oracle-visible-state", 0, 1
    proposal = optimistic_base_proposal(claims)
    if proposal == "hold":
        return "hold", "base-proposal-hold", 0, 0
    if condition == "labels_without_gating":
        return "go", "ungated-base-proposal", 0, 0
    ok, reason = certify_go(claims, t)
    if ok:
        return "go", reason, 1, 1
    return "hold", reason, 1, 0

@dataclass(frozen=True)
class StepResult:
    condition: str
    seed: int
    t: int
    scenario: str
    ready: bool
    crane_ok: bool
    eta_on_time: bool
    weather_safe: bool
    action: Action
    reason: str
    certified: int
    gate_used: int
    contradiction_count: int
    reward: float
    regret: float
    safety_violation: int
    waiting_cost: float
    idling_emission_proxy: float
    intervention_cost: float
    false_certification: int
    service_delay_proxy: float

def evaluate_step(x: LatentState, action: Action, reason: str, certified: int, gate_used: int) -> Tuple[float, float, int, float, float, float, int, float]:
    should_go = all(truth(x, p) for p in REQUIRED_PROPS)
    safety = int(action == "go" and not should_go)
    reward = 1.0 if ((action == "go" and should_go) or (action == "hold" and not should_go)) else 0.0
    regret = 1.0 - reward
    waiting = 1.0 if (action == "hold" and should_go) else 0.0
    idling = waiting
    intervention = 1.0 if gate_used and action == "hold" and reason.startswith("uncertified") else 0.0
    false_cert = int(certified and ((action == "go" and not should_go) or (action == "hold" and should_go)))
    return reward, regret, safety, waiting, idling, intervention, false_cert, waiting

def evaluate_bank(bank: List[EpisodeStep], conditions: Iterable[str]) -> List[StepResult]:
    rows: List[StepResult] = []
    for step in bank:
        for condition in conditions:
            ablation_rng = Random(step.seed * 1_000_003 + step.t * 9176 + sum(ord(c) for c in condition))
            claims = transform_claims(step.claims, condition, ablation_rng)
            action, reason, gate_used, certified = fixed_solver(chi_b1(step.latent), claims, condition, step.latent, step.t)
            kappa = contradiction_count(claims)
            reward, regret, violation, waiting, idle, intervention, false_cert, service_delay = evaluate_step(
                step.latent, action, reason, certified, gate_used
            )
            rows.append(StepResult(condition, step.seed, step.t, step.scenario, step.latent.ready, step.latent.crane_ok,
                                   step.latent.eta_on_time, step.latent.weather_safe, action, reason, certified,
                                   gate_used, kappa, reward, regret, violation, waiting, idle, intervention,
                                   false_cert, service_delay))
    return rows

def summarize(rows: List[StepResult]) -> Dict[str, float | str | int]:
    n = len(rows)
    return {
        "condition": rows[0].condition if rows else "NA",
        "n": n,
        "mean_reward": sum(r.reward for r in rows) / n,
        "mean_regret": sum(r.regret for r in rows) / n,
        "cumulative_regret": sum(r.regret for r in rows),
        "safety_violations": sum(r.safety_violation for r in rows),
        "zero_violation": int(sum(r.safety_violation for r in rows) == 0),
        "waiting_cost": sum(r.waiting_cost for r in rows),
        "idling_proxy": sum(r.idling_emission_proxy for r in rows),
        "intervention_cost": sum(r.intervention_cost for r in rows),
        "false_certifications": sum(r.false_certification for r in rows),
        "certification_rate": sum(r.certified for r in rows) / n,
        "gate_rate": sum(r.gate_used for r in rows) / n,
        "mean_contradiction_count": sum(r.contradiction_count for r in rows) / n,
    }

def by_condition(rows: List[StepResult]) -> List[Dict[str, float | str | int]]:
    groups: Dict[str, List[StepResult]] = defaultdict(list)
    for r in rows:
        groups[r.condition].append(r)
    return [summarize(groups[c]) for c in ABLATION_CONDITIONS if c in groups]

def seed_mean(rows: List[StepResult], condition: str, seed: int, metric: str) -> float:
    selected = [r for r in rows if r.condition == condition and r.seed == seed]
    return sum(float(getattr(r, metric)) for r in selected) / len(selected)

def paired_deltas(rows: List[StepResult], baseline: str = "provenance_preserving") -> List[Dict[str, float | str | int]]:
    seeds = sorted({r.seed for r in rows})
    conditions = sorted({r.condition for r in rows if r.condition != baseline})
    metrics = ["regret", "safety_violation", "waiting_cost", "intervention_cost", "false_certification"]
    report = []
    for condition in conditions:
        for metric in metrics:
            deltas = [seed_mean(rows, condition, s, metric) - seed_mean(rows, baseline, s, metric) for s in seeds]
            mean = sum(deltas) / len(deltas)
            sd = math.sqrt(sum((d - mean) ** 2 for d in deltas) / max(len(deltas) - 1, 1)) if len(deltas) > 1 else 0.0
            hw = 1.96 * sd / math.sqrt(len(deltas)) if deltas else math.nan
            report.append({"condition": condition, "metric": metric, "seeds": len(deltas),
                           "mean_delta_vs_provenance_preserving": mean, "ci95_low": mean - hw, "ci95_high": mean + hw})
    return report

def leakage_diagnostic() -> Dict[str, object]:
    x_plus = LatentState(True, True, True, True)
    x_minus = LatentState(False, True, True, True)
    return {
        "chi_equal_for_ready_pair": chi_b1(x_plus) == chi_b1(x_minus),
        "hidden_truth_differs": x_plus.ready != x_minus.ready,
        "visible_keys": sorted(chi_b1(x_plus).keys()),
        "excluded_hidden_keys": ["ready", "crane_ok", "eta_on_time", "weather_safe"],
    }

def go_no_go(summary: List[Dict[str, float | str | int]], paired: List[Dict[str, float | str | int]], horizon: int, seeds: int) -> Dict[str, object]:
    by = {str(s["condition"]): s for s in summary}
    def value(cond: str, key: str) -> float:
        return float(by.get(cond, {}).get(key, math.nan))
    def paired_low(cond: str, metric: str) -> float:
        for r in paired:
            if r["condition"] == cond and r["metric"] == metric:
                return float(r["ci95_low"])
        return math.nan
    checks = {
        "leakage_guard_passes": bool(leakage_diagnostic()["chi_equal_for_ready_pair"]),
        "preserving_low_regret": value("provenance_preserving", "mean_regret") <= 0.05,
        "oracle_closes_gap": value("oracle_visible_state", "mean_regret") <= 0.05,
        "erasure_regret_separates": paired_low("provenance_erased", "regret") >= 0.20,
        "erased_safe_but_burdensome": value("provenance_erased", "safety_violations") == 0 and value("provenance_erased", "mean_regret") > value("provenance_preserving", "mean_regret"),
        "ungated_exposes_safety_need": value("labels_without_gating", "safety_violations") > value("provenance_preserving", "safety_violations"),
        "benign_low_overhead": value("benign_agreement", "mean_regret") <= 0.02,
    }
    return {"horizon": horizon, "seeds": seeds, "n_per_condition": horizon * seeds, "leakage_diagnostic": leakage_diagnostic(),
            "checks": checks, "all_checks_pass": bool(all(checks.values())),
            "interpretation": "Passes locked active-regime criteria" if all(checks.values()) else "Inspect active-regime assumptions before scaling"}

def validate_bank(bank: List[EpisodeStep]) -> Dict[str, object]:
    if not bank:
        raise ValueError("episode bank is empty")
    keys = [(s.seed, s.t) for s in bank]
    if len(keys) != len(set(keys)):
        raise ValueError("episode bank has duplicate (seed,t) steps")
    missing_claim_steps = [(s.seed, s.t) for s in bank if not s.claims]
    unknown_props = sorted({c.prop for s in bank for c in s.claims if c.prop not in REQUIRED_PROPS})
    unknown_observers = sorted({c.observer for s in bank for c in s.claims
                                if c.observer not in OBSERVER_RANK.get(c.prop, {})})
    scenarios = sorted({s.scenario for s in bank})
    seeds = sorted({s.seed for s in bank})
    leakage = leakage_diagnostic()
    if not leakage["chi_equal_for_ready_pair"]:
        raise ValueError("visible-context leakage guard failed")
    return {
        "steps": len(bank),
        "seeds": len(seeds),
        "seed_min": min(seeds),
        "seed_max": max(seeds),
        "scenarios": scenarios,
        "missing_claim_steps": missing_claim_steps[:10],
        "unknown_props": unknown_props,
        "unknown_observers": unknown_observers,
        "leakage_guard": leakage,
        "conditions": ABLATION_CONDITIONS,
        "solver_version": SOLVER_VERSION,
        "dominance_table_version": DOMINANCE_TABLE_VERSION,
    }

def file_sha256(path: Optional[str]) -> Optional[str]:
    if not path:
        return None
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def build_manifest(args: argparse.Namespace, bank_report: Dict[str, object]) -> Dict[str, object]:
    return {
        "purpose": "OS-CMASP Berth-1-Conflict fixed-solver ablation manifest",
        "mode": args.mode,
        "solver_version": SOLVER_VERSION,
        "dominance_table_version": DOMINANCE_TABLE_VERSION,
        "conditions": ABLATION_CONDITIONS,
        "scenario": args.scenario,
        "horizon": args.horizon,
        "seeds": args.seeds,
        "p_all_clear": args.p_all_clear,
        "replay_csv": args.replay_csv,
        "replay_sha256": file_sha256(args.replay_csv),
        "out_prefix": args.out_prefix,
        "schema_required_fields": sorted(REPLAY_REQUIRED_FIELDS),
        "schema_template_fields": REPLAY_TEMPLATE_FIELDS,
        "bank_report": bank_report,
    }

def write_json(path: str, payload: Dict[str, object]) -> None:
    with open(path, "w") as f:
        json.dump(payload, f, indent=2, sort_keys=True)

def write_csv(path: str, rows: List[object]) -> None:
    if not rows:
        return
    with open(path, "w", newline="") as f:
        first = rows[0]
        if hasattr(first, "__dataclass_fields__"):
            fieldnames = list(first.__dataclass_fields__.keys())
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for row in rows:
                writer.writerow(asdict(row))
        else:
            fieldnames = list(rows[0].keys())
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for row in rows:
                writer.writerow(row)

def main() -> None:
    parser = argparse.ArgumentParser(description="Berth-1-Conflict fixed-solver ablation scaffold")
    parser.add_argument("--mode", choices=["preflight", "run"], default="preflight",
                        help="preflight validates the contract and writes no result CSVs; run evaluates ablations")
    parser.add_argument("--horizon", type=int, default=100)
    parser.add_argument("--seeds", type=int, default=10)
    parser.add_argument("--p-all-clear", type=float, default=0.5)
    parser.add_argument("--scenario", type=str, default="mixed", choices=["authority_conflict", "freshness_conflict", "context_conflict", "human_override", "benign_agreement", "mixed"])
    parser.add_argument("--replay-csv", type=str, default=None)
    parser.add_argument("--write-template", type=str, default=None)
    parser.add_argument("--out-prefix", type=str, default="berth1_results")
    parser.add_argument("--manifest", type=str, default=None,
                        help="optional JSON manifest path for preflight or run")
    parser.add_argument("--allow-synthetic-results", action="store_true",
                        help="required for --mode run without --replay-csv")
    args = parser.parse_args()

    if args.write_template:
        write_replay_template(args.write_template)
        print(f"wrote replay template: {args.write_template}")
        return

    if args.replay_csv:
        replay_path = Path(args.replay_csv)
        if not replay_path.exists():
            placeholder_hint = ""
            if "path/to" in args.replay_csv or "twin_replay_claims.csv" in args.replay_csv:
                placeholder_hint = (
                    "\nIt looks like you used the documentation placeholder. "
                    "Replace it with an actual replay CSV path, or create a template with:\n"
                    "  python -m os_cmasp.berth1_conflict --write-template data/replay/berth1_replay_template.csv"
                )
            raise SystemExit(
                f"Replay CSV not found: {args.replay_csv}{placeholder_hint}\n"
                "For a pipeline check without replay, run:\n"
                "  scripts/run_berth1_synthetic_smoke.sh outputs/berth1/synthetic_smoke"
            )
        bank = load_replay_bank(args.replay_csv)
    else:
        bank = generate_episode_bank(args.scenario, args.horizon, args.seeds, args.p_all_clear)
    bank_report = validate_bank(bank)
    manifest = build_manifest(args, bank_report)

    if args.manifest:
        write_json(args.manifest, manifest)

    if args.mode == "preflight":
        print(json.dumps({"preflight": bank_report, "manifest_path": args.manifest}, indent=2, sort_keys=True))
        return

    if not args.replay_csv and not args.allow_synthetic_results:
        raise SystemExit(
            "Refusing to write synthetic benchmark outputs without --allow-synthetic-results. "
            "Use --mode preflight for contract checks, or provide --replay-csv for replay evaluation."
        )

    rows = evaluate_bank(bank, ABLATION_CONDITIONS)
    summary = by_condition(rows)
    paired = paired_deltas(rows)
    diagnostics = go_no_go(summary, paired, args.horizon, args.seeds)
    write_csv(f"{args.out_prefix}.csv", rows)
    write_csv(f"{args.out_prefix}_summary.csv", summary)
    write_csv(f"{args.out_prefix}_paired.csv", paired)
    write_json(f"{args.out_prefix}_diagnostics.json", {"diagnostics": diagnostics, "summary": summary, "paired": paired, "manifest": manifest})
    print(json.dumps({"diagnostics": diagnostics, "summary": summary, "manifest_path": args.manifest}, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
