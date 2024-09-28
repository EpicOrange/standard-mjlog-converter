from py_mjlog_converter.fetch.tenhou import *
from py_mjlog_converter.fetch.majsoul import *
from py_mjlog_converter.fetch.riichicity import *
from py_mjlog_converter.kyoku import Kyoku
from py_mjlog_converter.classes import GameMetadata
from py_mjlog_converter.output import to_standard_format
from typing import *
import argparse
import asyncio
import json
import sys


async def parse_game_link(link: str) -> Tuple[List[Kyoku], GameMetadata, str]:
    """Given a game link, fetch and parse the game into kyokus"""
    if "tenhou.net/" in link:
        tenhou_log, metadata, player, identifier = fetch_tenhou(link)
        kyokus, parsed_metadata = parse_tenhou(tenhou_log, metadata)
    elif "mahjongsoul" in link or "maj-soul" in link or "majsoul" in link:
        # EN: `mahjongsoul.game.yo-star.com`; CN: `maj-soul.com`; JP: `mahjongsoul.com`
        # Old CN (?): http://majsoul.union-game.com/0/?paipu=190303-335e8b25-7f5c-4bd1-9ac0-249a68529e8d_a93025901
        majsoul_log, metadata, player, identifier = await fetch_majsoul(link)
        kyokus, parsed_metadata = parse_majsoul(majsoul_log, metadata)
    elif all(c in "0123456789abcdefghijklmnopqrstuv" for c in link[:20]): # riichi city log id
        riichicity_log, metadata, player, identifier = await fetch_riichicity(link)
        kyokus, parsed_metadata = parse_riichicity(riichicity_log, metadata)
    else:
        raise Exception("expected tenhou link similar to `tenhou.net/0/?log=`"
                        " or mahjong soul link similar to `mahjongsoul.game.yo-star.com/?paipu=`"
                        " or 20-character riichi city log id like `cjc3unuai08d9qvmstjg`")
    return kyokus, parsed_metadata, identifier

async def convert_link(link: str) -> str:
    kyokus, game_metadata, identifier = await parse_game_link(link)
    return json.dumps(to_standard_format(identifier, kyokus, game_metadata))


def main():
    parser = argparse.ArgumentParser(description='Analyzes your Mahjong Soul, tenhou.net, or Riichi City game to find instances of mahjong injustice.')
    parser.add_argument('link', type=str, help='Link to game log')
    args = parser.parse_args()
    link = args.link
    print(asyncio.run(convert_link(link)))












if __name__ == "__main__":
    main()
