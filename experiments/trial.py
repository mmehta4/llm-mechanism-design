"""One trial = one play decision + one competence probe, in the same framing.

The two calls are deliberately INDEPENDENT -- separate requests, no shared context.
If the probe were appended to the play conversation it would contaminate the play
decision, and on a disguised trial it would hand over the very vocabulary the
disguise exists to withhold.

The verdict column is the point of the whole paired design:

    COMPETENCE_GAP  cannot compute the payoff mechanics. Deviation is not strategic.
                    EXCLUDE from behavioural fits.
    PROBE_FORMAT_FAIL  answered the probe in prose instead of the bare label. Usually
                    CORRECT but unusable. Kept separate because folding it into
                    COMPETENCE_GAP would silently delete correct trials from the fits.
    STRATEGIC_GAP   computes them correctly, plays something else. The object of study.
    AT_EQUILIBRIUM  computes them and plays accordingly.
    PARSE_FAIL      the model answered, but not in a usable form. A fact about the
                    model; reported as a rate, never dropped.
    INFRA_FAIL      the request never reached the model -- quota, overload, network.
                    NOT a fact about the model. Excluded from every model-level
                    rate, and re-run in a later pass rather than recorded as data.
"""
from __future__ import annotations

import datetime as dt
import json

from agents.llm import LLMAgent
from games import GAMES
from games.probes import probe_for, probe_passed, is_malformed

COMPETENCE_GAP = "COMPETENCE_GAP"
PROBE_FORMAT_FAIL = "PROBE_FORMAT_FAIL"
STRATEGIC_GAP = "STRATEGIC_GAP"
AT_EQUILIBRIUM = "AT_EQUILIBRIUM"
PARSE_FAIL = "PARSE_FAIL"
INFRA_FAIL = "INFRA_FAIL"

# how close counts as "played the equilibrium"
NUMERIC_TOLERANCE = 0.5


def extract_action(action_obj, game_key: str):
    """Pull the decision out of the game's action schema."""
    for attr in ("bid", "quantity", "contribution", "action", "number"):
        if hasattr(action_obj, attr):
            return getattr(action_obj, attr)
    raise AttributeError(f"no recognised action field on {game_key} response")


def deviation_of(observed, equilibrium):
    """Signed distance for numeric games; 0/1 mismatch for discrete ones."""
    if isinstance(equilibrium, str):
        return 0.0 if str(observed).strip().upper() == equilibrium.upper() else 1.0
    try:
        return float(observed) - float(equilibrium)
    except (TypeError, ValueError):
        return None


def at_equilibrium(deviation, equilibrium) -> bool:
    if deviation is None:
        return False
    if isinstance(equilibrium, str):
        return deviation == 0.0
    return abs(deviation) <= NUMERIC_TOLERANCE


def equilibrium_for(params: dict, framing: str):
    """The equilibrium action IN THE LABELS OF THIS FRAMING.

    For most games the two framings share one answer (a bid, a quantity). The PD
    does not: the named prompt says C/D, the disguised one says X/Y with the letters
    counterbalanced. Scoring a named answer against the disguised label marked every
    named PD trial wrong -- found 2026-09-30, after the practice runs had reported
    named-PD equilibrium play as 0% when the models had in fact defected 15/20 times.
    """
    if framing == "named" and "equilibrium_named" in params:
        return params["equilibrium_named"]
    return params.get("equilibrium")


def verdict_of(row: dict, equilibrium) -> str:
    """Verdict from a row's recorded fields -- shared by live trials and rescoring."""
    # infrastructure first: a request the model never received says nothing about
    # the model, whichever of the two calls it hit
    if row.get("infra"):
        return INFRA_FAIL
    if not row.get("play_parse_ok"):
        return PARSE_FAIL
    if row.get("probe_malformed"):
        return PROBE_FORMAT_FAIL
    if row.get("probe_passed") is not True:
        return COMPETENCE_GAP
    if at_equilibrium(row["deviation"], equilibrium):
        return AT_EQUILIBRIUM
    return STRATEGIC_GAP


def run_trial(game_key: str, framing: str, model_key: str, seed: int,
              paraphrase_idx: int = 0) -> dict:
    spec = GAMES[game_key]
    params = spec.sampler(seed=seed)
    eq = equilibrium_for(params, framing)
    agent = LLMAgent(model_key)

    play_prompt = spec.prompt(framing, paraphrase_idx, **params)
    play = agent.act(play_prompt, spec.action_model)

    probe_prompt, probe_schema, probe_correct = probe_for(game_key, framing, **params)
    probe = agent.act(probe_prompt, probe_schema)

    row = {
        "timestamp": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "game": game_key,
        "framing": framing,
        "model_key": model_key,
        "model_api_id": play.model_api_id,
        "seed": seed,
        "paraphrase_idx": paraphrase_idx,
        "params": json.dumps({k: v for k, v in params.items() if not k.startswith("_")}),
        "equilibrium": eq,
        "play_prompt": play_prompt,
        "play_raw": play.raw,
        "play_parse_ok": play.parse_ok,
        "play_error": play.error,
        "play_latency_s": round(play.latency_s, 3),
        "probe_prompt": probe_prompt,
        "probe_correct_answer": probe_correct,
        "probe_parse_ok": probe.parse_ok,
        "probe_latency_s": round(probe.latency_s, 3),
        "total_latency_s": round(play.latency_s + probe.latency_s, 3),
        "cost_usd": round(agent.cost_usd(play) + agent.cost_usd(probe), 6),
        # how many HTTP attempts the two calls needed between them; >2 means
        # backoff engaged, which is rate limiting rather than model behaviour
        "attempts": play.extra.get("attempts", 1) + probe.extra.get("attempts", 1),
    }

    if play.parse_ok:
        observed = extract_action(play.action, game_key)
        dev = deviation_of(observed, eq)
        row.update({
            "observed_action": observed,
            "deviation": dev,
            "play_reasoning": play.reasoning,
        })
    else:
        row.update({"observed_action": None, "deviation": None, "play_reasoning": ""})

    if probe.parse_ok:
        given = getattr(probe.action, "answer", None)
        row.update({
            "probe_answer": given,
            "probe_passed": probe_passed(given, probe_correct),
            "probe_malformed": is_malformed(given, probe_correct),
            "probe_reasoning": probe.reasoning,
        })
    else:
        row.update({"probe_answer": None, "probe_passed": None,
                    "probe_malformed": True, "probe_reasoning": ""})

    row["infra"] = play.extra.get("infra") or probe.extra.get("infra")
    row["verdict"] = verdict_of(row, eq)
    return row
