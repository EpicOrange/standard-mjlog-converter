#!/usr/bin/env zsh
set -euo pipefail
HERE="$(dirname "$(realpath -s $0)")"
cd "$HERE"

python main.py "https://mahjongsoul.game.yo-star.com/?paipu=220930-8a7c1e7f-2114-46f9-80d4-208067ef0385_a939260192"
# python main.py "https://tenhou.net/0/?log=2023121909gm-000b-18940-d853a264&tw=3"
# python main.py "cmon7d6ai08d9bi5k8l0@0"
