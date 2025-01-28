#!/usr/bin/python3

"""
Collection organizer and purchase suggester for Warcaster: NM
"""

import os

from steve_utils.output_utils import double_print
from steve_utils.sort_and_filter import sort_and_filter

GAME_NAME = "Warcaster: Neo-Mechanika"
COMPANY = "SFG"

VALID_FACTIONS = ['Aeternus Continuum', 'Marcher Worlds', 'Iron Star Alliance',
    'Empyreans', 'Wild Cards']

if os.getcwd().endswith('minis_games'):
    file_h = open('DB/WarcasterData.txt', 'r', encoding="UTF-8")
else:
    file_h = open('minis_games/DB/WarcasterData.txt', 'r', encoding="UTF-8")

lines = file_h.readlines()
file_h.close()
lines = [line.strip() for line in lines]

TOTAL_MAX = 0
TOTAL_OWN = 0
mini_lines = []
for line in lines:
    if line.startswith('#') or line == '':
        continue
    line = line.split('#')[0].strip()
    try:
        model_name, model_faction, model_type, model_max, model_own = line.split(';')
    except ValueError:
        print("Problem with line:")
        print(line)
        continue
    if model_faction not in VALID_FACTIONS:
        print(f"Invalid faction: {model_faction}")
        continue

    if model_type in ['Solo', 'Squad', 'Warjack']:
        META_TYPE = model_type
    elif model_type in ['Hero', 'Champion Solo']:
        META_TYPE = 'Solo'
    elif model_type in ['Squad Attachment', 'Hero Attachment']:
        META_TYPE = 'Squad'
    elif model_type in ['Champion Warjack']:
        META_TYPE = 'Warjack'
    elif model_type in ['Vehicle Hero', 'Mantlet', 'Vehicle', 'Champion Vehicle']:
        META_TYPE = 'Other'
    else:
        print(f"Unhandled meta-type: {model_type}")
        continue

    model_max = int(model_max)
    model_own = int(model_own)
    if model_own > model_max:
        model_own = model_max
    TOTAL_MAX += model_max
    TOTAL_OWN += model_own
    mini_lines.append((model_name, model_faction, model_type, META_TYPE, model_own, model_max))

faction_choice, filtered_list = sort_and_filter(mini_lines, 1)
_, filtered_list = sort_and_filter(filtered_list, 3)
type_choice, filtered_list = sort_and_filter(filtered_list, 2)
item_choice, filtered_list = sort_and_filter(filtered_list, 0)

filtered_list = filtered_list[0]

if __name__ == "__main__":
    if os.getcwd().endswith('minis_games'):
        out_file_h = open("output/WarcasterOutput.txt", 'w', encoding="UTF-8")
    else:
        out_file_h = open("minis_games/output/WarcasterOutput.txt", 'w', encoding="UTF-8")

    double_print("Inventory tracker and purchase suggestions for the Warcaster: Neo-Mechanika " + \
        "miniatures game.\n", out_file_h)
    own_pct = TOTAL_OWN / TOTAL_MAX * 100
    double_print(f"I own {TOTAL_OWN} out of {TOTAL_MAX} model choices for this game " + \
        f"({own_pct:.2f} percent)", out_file_h)
    double_print(f"Maybe purchase a(n) {item_choice} ({type_choice}) from {faction_choice} " + \
        f"(have {filtered_list[4]} out of {filtered_list[5]})", out_file_h)
