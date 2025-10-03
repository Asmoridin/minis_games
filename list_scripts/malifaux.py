#!/usr/bin/python3

"""
Collection organizer and purchase suggester for Malifaux
"""

import os

from steve_utils.output_utils import double_print
from steve_utils.sort_and_filter import sort_and_filter

GAME_NAME = "Malifaux"
COMPANY = "Wyrd"

VALID_FACTIONS = ['Guild', 'Neverborn', 'Resurrectionists', 'Outcasts', 'Bayou', 'Arcanists',
    "The Explorer's Society", 'Ten Thunders']
FACTION_CONVERT = {'Res':'Resurrectionists', 'Explorer':"The Explorer's Society",
    'Thunder':'Ten Thunders'}
VALID_STATIONS = ['Master', 'Minion', 'Henchman', 'Totem', 'Enforcer', 'Peon']

if os.getcwd().endswith('minis_games'):
    file_h = open('DB/Malifaux Data.txt', 'r', encoding="UTF-8")
else:
    file_h = open('minis_games/DB/Malifaux Data.txt', 'r', encoding="UTF-8")

lines = file_h.readlines()
file_h.close()
lines = [line.strip() for line in lines]

TOTAL_MAX = 0
TOTAL_OWN = 0
mini_lines = []
names = set()
keyword_counter = {}
for line in lines:
    if line.startswith('#') or line == "":
        continue
    line = line.split('#')[0].strip()
    try:
        model_name, model_faction, model_station, keywords, model_max, model_own = line.split(';')
    except ValueError:
        print("Issue with line:")
        print(line)
        continue
    if model_faction in FACTION_CONVERT:
        model_faction = FACTION_CONVERT[model_faction]
    if model_faction not in VALID_FACTIONS:
        print(f"Unknown faction {model_faction} for {model_name}")
    if model_station not in VALID_STATIONS:
        print(f"Unknown station {model_station} for {model_name}")
    keywords = keywords.split('/')
    for keyword in keywords:
        keyword = keyword.strip()
        if keyword not in keyword_counter:
            keyword_counter[keyword] = 0
        keyword_counter[keyword] += 1
    model_max = int(model_max)
    model_own = int(model_own)
    TOTAL_MAX += model_max
    TOTAL_OWN += model_own
    mini_lines.append([model_name, model_faction, model_station, keywords, model_own, model_max])

faction_choice, filtered_list = sort_and_filter(mini_lines, 1)
keyword_choice, filtered_list = sort_and_filter(filtered_list, 3)
item_choice, filtered_list = sort_and_filter(filtered_list, 0)
filtered_list = filtered_list[0]

if __name__ == "__main__":
    if os.getcwd().endswith('minis_games'):
        out_file_h = open("output/Malifaux Out.txt", 'w', encoding="UTF-8")
    else:
        out_file_h = open("minis_games/output/Malifaux Out.txt", 'w', encoding="UTF-8")

    double_print("Inventory tracker and purchase suggestions for the Malifaux " + \
        "miniatures game.\n", out_file_h)
    own_pct = TOTAL_OWN / TOTAL_MAX * 100
    double_print(f"I own {TOTAL_OWN} out of {TOTAL_MAX} minis for this game " + \
        f"({own_pct:.2f} percent)", out_file_h)
    double_print(f"Maybe purchase a(n) {item_choice} from {faction_choice} (have " + \
        f"{filtered_list[4]} out of {filtered_list[5]})", out_file_h)

    double_print("\nFive lowest keyword counts:", out_file_h)
    keyword_sorter = sorted(keyword_counter.items(),
        key=lambda x: x[1])
    for keyword, count in keyword_sorter[:5]:
        double_print(f"{keyword}: {count}", out_file_h)
    out_file_h.close()
