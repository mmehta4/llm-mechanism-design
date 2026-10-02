"""Stage 3.5 coding rules, pinned on hand-written examples."""
from analysis.reasoning import code
from games import GAMES


def row(game, framing, played, reasoning, verdict="STRATEGIC_GAP", seed=7):
    p = GAMES[game].sampler(seed=seed)
    eq = p["equilibrium_named"] if framing == "named" and "equilibrium_named" in p else p["equilibrium"]
    return {"game": game, "framing": framing, "seed": str(seed), "verdict": verdict,
            "observed_action": str(played), "equilibrium": str(eq),
            "play_reasoning": reasoning, "play_prompt": GAMES[game].prompt(framing, 0, **p)}, p


def test_fraction_slip_is_mismatch():
    """Nemotron: reasoning ends at 70/3 ≈ 23.33, the field says 70."""
    r, p = row("cournot", "named", 0, "")
    eq = float(r["equilibrium"])
    r["observed_action"] = str(3 * eq)
    r["play_reasoning"] = f"Solving gives q = {3 * eq:.1f}/3 ≈ {eq:.2f}"
    assert "MISMATCH" in code(r)


def test_derived_then_deviated_on_purpose():
    r, p = row("cournot", "disguised", 0, "")
    eq = float(r["equilibrium"])
    r["observed_action"] = str(round(eq - 7))
    r["play_reasoning"] = f"The Nash equilibrium is x≈{eq:.2f}, but total gain peaks at {round(eq - 7)} channels."
    c = code(r)
    assert "KNEW_AND_DEVIATED" in c and "MISMATCH" not in c


def test_naming_a_word_the_question_uses_does_not_count():
    r, _ = row("vickrey", "named", 50, "In this auction I bid my value.", verdict="AT_EQUILIBRIUM")
    assert "NAMES_GAME" not in code(r)          # the named question itself says "auction"


def test_naming_the_disguised_game_counts():
    r, _ = row("cournot", "disguised", 30, "This is a Cournot duopoly game.", verdict="AT_EQUILIBRIUM")
    assert "NAMES_GAME" in code(r)


def test_cooperation_norm_needs_both_the_move_and_the_words():
    r, _ = row("repeated_pd", "named", "C", "Cooperating builds trust and mutual benefit.")
    assert "COOPERATION_NORM" in code(r)
    r2, _ = row("repeated_pd", "named", "C", "I pick C.")
    assert code(r2) & {"COOPERATION_NORM"} == set() and "UNCODED" in code(r2)


def test_truthful_default_in_the_double_pay_trap():
    r, p = row("vickrey_trap", "named", 0, "I bid my value.")
    r["observed_action"] = str(p["value"])
    assert "TRUTHFUL_DEFAULT" in code(r)


def test_collusive_quantity():
    r, p = row("cournot", "disguised", 0, "Assuming both choose the same, maximise (a-2n)n.")
    r["observed_action"] = str((p["a"] - p["c"]) / 4)
    assert "COLLUSIVE" in code(r)


def test_vickrey_value_mention_is_not_a_mismatch():
    """Practice false alarm: the value IS the equilibrium in Vickrey; mentioning it proves nothing."""
    r, p = row("vickrey", "disguised", 0, "")
    r["observed_action"] = str(p["value"] + 0.7)
    r["play_reasoning"] = f"Bid a little above the value of {p['value']} to be sure to win."
    assert "MISMATCH" not in code(r) and "KNEW_AND_DEVIATED" not in code(r)


def test_codebook_is_locked():
    from analysis.reasoning import reasoning_locked
    assert reasoning_locked()


# --- codebook v2 ---------------------------------------------------------------------

def test_v2_label_swap_claims_the_chosen_cooperative_letter_dominates():
    from analysis.reasoning_v2 import main_code
    r, p = row("repeated_pd", "disguised", "", "")
    r["observed_action"] = p["coop"]
    r["play_reasoning"] = f"{p['coop']} strictly dominates {p['defect']}: it pays more either way."
    assert main_code(r) == "LABEL_SWAP"


def test_v2_dominated_is_not_a_label_swap():
    from analysis.reasoning_v2 import main_code
    r, p = row("repeated_pd", "named", "C", "C is dominated, but cooperating builds trust.")
    assert main_code(r) in {"KNEW_OVERRODE", "COOPERATION_NORM"}


def test_v2_knew_overrode_beats_cooperation_norm_in_the_order():
    from analysis.reasoning_v2 import main_code
    r, _ = row("repeated_pd", "named", "C",
               "Backward induction says defect, but cooperating builds mutual trust.")
    assert main_code(r) == "KNEW_OVERRODE"


def test_v2_claimed_nash_wrong_number():
    from analysis.reasoning_v2 import main_code
    r, p = row("cournot", "named", 0, "This is the Cournot-Nash equilibrium output.")
    r["observed_action"] = str(float(r["equilibrium"]) - 4.3)
    assert main_code(r) == "CLAIMED_NASH_WRONG"


def test_v2_only_offers_codes_for_the_right_game():
    from analysis.reasoning_v2 import ORDER
    assert "COLLUSIVE" not in ORDER["repeated_pd"] and "LABEL_SWAP" not in ORDER["cournot"]


def test_codebook_v2_is_locked():
    from analysis.reasoning_v2 import locked
    assert locked()
