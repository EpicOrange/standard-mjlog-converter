from .classes import GameRules, GameMetadata
from .kyoku import Kyoku
from .wall import get_hidden_dead_wall

from typing import *

def convert_rules(rules: GameRules) -> Dict[str, Any]:
    return {}

recognized_events = {"draw", "discard", "riichi", "dora_flip"}
def convert_event(i: int, event: Tuple[Any, ...]) -> Dict[str, Any]:
    ret = {
        "index": i,
        "player": event[0],
        "type": event[1],
    }
    if event[1] == "draw" or event[1] == "discard" or event[1] == "riichi":
        ret["tile"] = event[2]
    if event[1] == "draw":
        ret["kan_draw"] = event[3]
    if event[1] == "discard":
        ret["tsumogiri"] = event[3]
        ret["riichi"] = False
    if event[1] == "riichi":
        ret["tsumogiri"] = event[3]
        ret["riichi"] = True

    return ret

def convert_kyoku(i: int, kyoku: Kyoku) -> Dict[str, Any]:
    dead_wall = get_hidden_dead_wall
    return {
        "index": i,
        "players": [{
                "points": None,
                "haipai": None,
            } for i in range(kyoku.num_players)],
        "kyoku": kyoku.round,
        "honba": kyoku.honba,
        "riichi_sticks": kyoku.riichi_sticks,
        "doras": None,
        "uras": None,
        "kan_tiles": None,
        "wall": kyoku.wall[52:122],
        "events": [convert_event(i, e) for i, e in enumerate([e for e in kyoku.events if e[1] in recognized_events])],
    }

def to_standard_format(link: str, kyokus: List[Kyoku], metadata: GameMetadata) -> Dict[str, Any]:
    return {
        "ref": link,
        "ver": "v1",
        "players": [{
                "name": metadata.name[i],
                "scores": metadata.game_score[i],
                "payout": metadata.final_score[i],
            } for i in range(metadata.num_players)],
        "rules": convert_rules(metadata.rules),
        "kyokus": [convert_kyoku(i, k) for i, k in enumerate(kyokus)],
    }
