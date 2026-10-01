from games.base import GameSpec, DisguisedPromptMissing
from games import vickrey, cournot, repeated_pd, public_goods

ALL_GAMES = {
    "vickrey": vickrey.SPEC,
    "cournot": cournot.SPEC,
    "repeated_pd": repeated_pd.SPEC,
    "public_goods": public_goods.SPEC,
}

# Stage 2B games live apart from the registered Stage 2A set, and importing them
# registers their probes. GAMES is what a trial looks a key up in.
from games.stress import STRESS_GAMES  # noqa: E402

GAMES = {**ALL_GAMES, **STRESS_GAMES}

__all__ = ["GameSpec", "DisguisedPromptMissing", "ALL_GAMES", "STRESS_GAMES", "GAMES"]
