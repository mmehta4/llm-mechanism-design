from games.base import GameSpec, DisguisedPromptMissing
from games import vickrey, cournot, repeated_pd, public_goods

ALL_GAMES = {
    "vickrey": vickrey.SPEC,
    "cournot": cournot.SPEC,
    "repeated_pd": repeated_pd.SPEC,
    "public_goods": public_goods.SPEC,
}

__all__ = ["GameSpec", "DisguisedPromptMissing", "ALL_GAMES"]
