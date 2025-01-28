#!/usr/bin/python3

"""
Collection organizer and purchase suggester for Runewars
"""

import os

from steve_utils.output_utils import double_print
from steve_utils.sort_and_filter import sort_and_filter

GAME_NAME = "Runewars"
COMPANY = "FFG"

VALID_FACTIONS = ['Daqan Lords', 'Waiqar the Undying', 'Latari Elves', "Uthuk Y'llan"]

if os.getcwd().endswith('minis_games'):
    file_h = open('DB/RunewarsData.txt', 'r', encoding="UTF-8")
else:
    file_h = open('minis_games/DB/RunewarsData.txt', 'r', encoding="UTF-8")

lines = file_h.readlines()
file_h.close()
lines = [line.strip() for line in lines]

TOTAL_MAX = 0
TOTAL_OWN = 0
mini_lines = []
names = set()
for line in lines:
    if line.startswith('#') or line == '':
        continue
    line = line.split('#')[0].strip()
    try:
        model_name, model_faction, model_max, model_own = line.split(';')
    except ValueError:
        print("Problem with line:")
        print(line)
        continue
    if model_faction not in VALID_FACTIONS:
        print("Invalid army in line:")
        print(line)
        continue
    if model_name in names:
        print("Duplicate: " + model_name)
    names.add(model_name)
    model_max = int(model_max)
    model_own = int(model_own)
    if model_own > model_max:
        model_own = model_max
    TOTAL_MAX += model_max
    TOTAL_OWN += model_own
    mini_lines.append((model_name, model_faction, model_own, model_max))

army_choice, filtered_list = sort_and_filter(mini_lines, 1)
item_choice, filtered_list = sort_and_filter(filtered_list, 0)

filtered_list = filtered_list[0]

if __name__ == "__main__":
    if os.getcwd().endswith('minis_games'):
        out_file_h = open("output/RunewarsOutput.txt", 'w', encoding="UTF-8")
    else:
        out_file_h = open("minis_games/output/RunewarsOutput.txt", 'w', encoding="UTF-8")

    double_print("Inventory tracker and purchase suggestions for the Runewars " + \
        "miniatures game.\n", out_file_h)
    own_pct = TOTAL_OWN / TOTAL_MAX * 100
    double_print(f"I own {TOTAL_OWN} out of {TOTAL_MAX} trays for this game " + \
        f"({own_pct:.2f} percent)", out_file_h)
    double_print(f"Maybe purchase a(n) {item_choice} from {army_choice} (have " + \
        f"{filtered_list[2]} out of {filtered_list[3]})", out_file_h)
