#!/usr/bin/python3

"""
Collection organizer and purchase suggester for A Song of Ice and Fire Miniatures Game
"""

import os

from steve_utils.output_utils import double_print
from steve_utils.sort_and_filter import sort_and_filter

GAME_NAME = "A Song of Ice and Fire"
COMPANY = "CMON"

VALID_FACTIONS = ['Lannister', 'Neutral', 'Stark', 'Free Folk', "Night's Watch", 'Baratheon',
    'Targaryen', 'Greyjoy', 'Martell', 'Bolton', 'Brotherhood Without Banners']
VALID_TYPES = ['Commander', 'Infantry', 'Cavalry', 'Infantry Attachment', 'Cavalry Attachment',
    'Monster', 'NCU', 'War Machine', 'Cards']

MY_CURRENT_ARMIES = ['Stark', 'Lannister', 'Targaryen']
MY_FUTURE_ARMIES = ['Neutral', 'Martell', 'Free Folk', 'Bolton', "Brotherhood Without Banners",
    "Night's Watch", 'Greyjoy', 'Baratheon']

if os.getcwd().endswith('minis_games'):
    file_h = open('DB/ASOIAFData.txt', 'r', encoding="UTF-8")
else:
    file_h = open('minis_games/DB/ASOIAFData.txt', 'r', encoding="UTF-8")

def validate_factions(in_factions):
    """
    Validate and cleanup the house/faction information
    """
    ret_list = []
    for in_faction in in_factions.split('/'):
        if in_faction in VALID_FACTIONS:
            ret_list.append(in_faction)
        else:
            print("Unknown faction: " + in_faction)
    return ret_list

lines = file_h.readlines()
file_h.close()
lines = [line.strip() for line in lines]

faction_points = {}
for faction in VALID_FACTIONS:
    faction_points[faction] = 0

TOTAL_MAX = 0
TOTAL_OWN = 0
COMMANDER_COUNT = 0
COMMANDER_OWN = 0
mini_lines = []
names = set()
for line in lines:
    if line.startswith('#') or line == '':
        continue
    line = line.split('#')[0].strip()
    try:
        model_name, model_factions, model_type, model_pts, model_max, model_own = line.split(';')
    except ValueError:
        print("Problem with line:")
        print(line)
        continue
    if model_name in names:
        print("Duplicate: " + model_name)
    names.add(model_name)
    model_factions = validate_factions(model_factions)
    m_types = []
    for m_type in model_type.split('/'):
        if m_type not in VALID_TYPES:
            print("Invalid model type: " + m_type)
        else:
            m_types.append(m_type)
    model_pts = int(model_pts)
    model_max = int(model_max)
    model_own = int(model_own)
    if 'Commander' in m_types:
        COMMANDER_COUNT += 1
        if model_own > 0:
            COMMANDER_OWN += 1
    if model_own > model_max:
        model_own = model_max

    for faction in model_factions:
        faction_points[faction] += model_pts * model_own
    TOTAL_MAX += model_max
    TOTAL_OWN += model_own
    mini_lines.append((model_name, model_factions, m_types, model_pts, model_own, model_max))

# Limiting myself to either the armies I play, or the next army in the list
faction_map = {}
for item_tuple in mini_lines:
    for army in item_tuple[1]:
        if army not in MY_CURRENT_ARMIES:
            continue
        if army not in faction_map:
            faction_map[army] = [0, 0]
        faction_map[army][0] += item_tuple[4]
        faction_map[army][1] += item_tuple[5]
fac_list = []
for map_fac, map_inv in faction_map.items():
    fac_list.append((map_fac, map_inv[0], map_inv[1]))
fac_list = sorted(fac_list, key=lambda x:(x[1]/x[2], x[0]))
FILTERED_FACTION = fac_list[0][0]
if (len(MY_CURRENT_ARMIES) / len(VALID_FACTIONS)) < (fac_list[0][1] / fac_list[0][2]):
    FILTERED_FACTION = MY_FUTURE_ARMIES[0]
filtered_list = []
for check_line in mini_lines:
    if FILTERED_FACTION in check_line[1]:
        filtered_list.append(check_line)

type_choice, filtered_list = sort_and_filter(filtered_list, 2)
item_choice, filtered_list = sort_and_filter(filtered_list, 0)

filtered_list = filtered_list[0]

if __name__ == "__main__":
    if os.getcwd().endswith('minis_games'):
        out_file_h = open("output/ASOIAFOutput.txt", 'w', encoding="UTF-8")
    else:
        out_file_h = open("minis_games/output/ASOIAFOutput.txt", 'w', encoding="UTF-8")

    double_print("Inventory tracker and purchase suggestions for the Song of Ice and Fire " + \
        "miniatures game.\n", out_file_h)
    own_pct = TOTAL_OWN / TOTAL_MAX * 100
    double_print(f"I own {TOTAL_OWN} out of {TOTAL_MAX} list items for this game " + \
        f"({own_pct:.2f} percent)", out_file_h)
    double_print(f"Maybe purchase a(n) {type_choice} from {FILTERED_FACTION} - perhaps a " + \
        f"{item_choice} (have {filtered_list[4]} out of {filtered_list[5]})", out_file_h)

    double_print(f"\nI own {COMMANDER_OWN} out of {COMMANDER_COUNT} Commanders", out_file_h)

    double_print("\nCurrent points by faction:", out_file_h)
    faction_tuples = sorted(faction_points.items(), key=lambda x:(-1 * x[1], x[0]))
    for faction_item in faction_tuples:
        double_print(f"- {faction_item[0]}: {faction_item[1]}", out_file_h)
