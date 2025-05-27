#!/usr/bin/python3

"""
Collection organizer and purchase suggester for Bushido
"""

import os
import re

from steve_utils.output_utils import double_print
from steve_utils.sort_and_filter import sort_and_filter
from steve_utils.check_inventory import check_inventory

GAME_NAME = "Bushido"
COMPANY = "GCT"

VALID_FACTIONS = ['Jung Pirates', 'Prefecture of Ryu', 'Savage Wave', 'Ronin', 'Kinshi Temple',
    'The Awoken', 'Cult of Yurei', 'Minimoto Clan', 'Temple of Ro-Kan', 'Shadow Wind Clan',
    'Shiho Clan', 'The Descension', 'Silvermoon Syndicate', 'Ito Clan',]

MY_CURRENT_FACTIONS = ['Jung Pirates', 'Ronin']
MY_FUTURE_FACTIONS = ['Prefecture of Ryu', 'Savage Wave', 'Kinshi Temple', 'Ito Clan',
    'The Awoken', 'Cult of Yurei', 'Minimoto Clan', 'Temple of Ro-Kan', 'Shadow Wind Clan',
    'Shiho Clan', 'The Descension', 'Silvermoon Syndicate']

if os.getcwd().endswith('minis_games'):
    file_h = open('DB/BushidoData.txt', 'r', encoding="UTF-8")
    theme_file_h = open('DB/BushidoThemes.txt', 'r', encoding="UTF-8")
    card_file_h = open('DB/BushidoCards.txt', 'r', encoding="UTF-8")
    ignore_file_h = open('DB/BushidoIgnore.txt', 'r', encoding="UTF-8")
    LIST_DIR = 'Lists/Bushido'
else:
    file_h = open('minis_games/DB/BushidoData.txt', 'r', encoding="UTF-8")
    theme_file_h = open('minis_games/DB/BushidoThemes.txt', 'r', encoding="UTF-8")
    card_file_h = open('minis_games/DB/BushidoCards.txt', 'r', encoding="UTF-8")
    ignore_file_h = open('minis_games/DB/BushidoIgnore.txt', 'r', encoding="UTF-8")
    LIST_DIR = 'minis_games/Lists/Bushido'

lines = file_h.readlines()
file_h.close()
lines = [line.strip() for line in lines]

theme_lines = theme_file_h.readlines()
theme_file_h.close()
theme_lines = [line.strip() for line in theme_lines]
theme_lines = [line.split(' (')[0] for line in theme_lines]

card_lines = card_file_h.readlines()
card_file_h.close()
card_lines = [line.strip() for line in card_lines]

ignore_lines = ignore_file_h.readlines()
ignore_file_h.close()
ignore_lines = [line.strip() for line in ignore_lines]

def manual_fix(in_item):
    """
    Fix for oddities from newrecruit list builder
    """
    if in_item in ignore_lines:
        return "IGNORE"
    if in_item in ['• 1x Animated Militia B', '• 1x Animated Militia C']:
        return 'Animated Militia'
    if in_item in ['• 1x Gashodokuro Guard']:
        return 'Animated Warriors'
    if in_item in ['• 1x Horseshoe Crab', '• 1x Itsiro Crab Swarm']:
        return 'Crabs of the Eastern Sea'
    if in_item in ['• 1x Kohanin B']:
        return 'Kohanin'
    if in_item in ['• 1x Kami of Sapping Silt B']:
        return 'Kami of Sapping Silt'
    if in_item == 'Mother of Pearl':
        return 'Mother-of-Pearl'
    if in_item == '• 1x Ashigaru of the Peaks B':
        return 'Ashigaru of the Peaks'
    if in_item == 'Kami of Evening Flame':
        return 'Kami of the Evening Flame'
    if in_item == '• 1x Eddo Ashigaru B':
        return 'Eddo Ashigaru'
    if in_item == '• 1x Golden Sentinel B':
        return 'Golden Sentinel'
    if in_item in ['• 1x Lost Slave A', '• 1x Lost Slave B']:
        return 'Lost Slave'
    if in_item == '• 1x Bakemono Archer B':
        return 'Bakemono Archers'
    if in_item == '• 1x Bakemono Bushi B':
        return 'Bakemono Bushi'
    if in_item == '• 1x Rinsho B':
        return "Rinsho"
    if in_item == '• 1x Bakemono Boomer B':
        return 'Bakemono Boomers'
    if in_item in ['• 1x Tribal Brute B', 'Tribal Brutes']:
        return 'Tribal Brute'
    if in_item == '• 1x Wolf Spear B':
        return 'Wolf Spears'
    if in_item == 'Shiho Hiroto':
        return 'Shiho Hiroto, The Black Eagle'
    if in_item == 'Eagles of Jwar':
        return 'Eagles of the Jwar Isles'
    if in_item in ['• 1x Hawk', '• 1x Kite']:
        return "Tsuki's Pack"
    if in_item == '• 1x Kyoaku-Han B':
        return 'Kyoaku-Han'
    if in_item == '• 1x Village Militia B':
        return 'Village Militia'
    if in_item == '• 1x Rice Farmer':
        return 'Rice Farmer of Ro-Kan'
    if in_item == '• 1x Blue Gale Scout A':
        return 'Blue Gale Scout'
    if in_item in ['• 1x Haiatake Guard A', '• 1x Haiatake Guard B']:
        return 'Haiatake Guard'
    if in_item in ['• 1x Zephyr Guard B', '• 1x Zephyr Guard A']:
        return 'Zephyr Guard'
    if in_item in ['• 1x Joji', '• 1x Lita']:
        return "Koji's Pack"
    if in_item in ["• 1x Hilltribe Tracker A", "• 1x Hilltribe Tracker B"]:
        return "Hilltribe Tracker"
    return in_item

def clean_list(in_list):
    """
    Handling accidental duplication in lists
    """
    for c_item in ['Animated Warrior', 'Crabs of the Eastern Sea', "Tsuki's Pack",
        'Rice Farmer of Ro-Kan', "Koji's Pack"]:
        if c_item in in_list:
            in_list[c_item] -= 1
    return in_list

TOTAL_MAX = 0
TOTAL_OWN = 0
mini_lines = []
mini_dict = {}
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
    if model_name in names:
        print("Duplicate: " + model_name)
    names.add(model_name)
    model_max = int(model_max)
    model_own = int(model_own)
    if model_own > model_max:
        model_own = model_max
    TOTAL_MAX += model_max
    TOTAL_OWN += model_own
    mini_dict[model_name] = model_own
    mini_lines.append((model_name, model_faction, model_own, model_max))

# Limiting myself to either the factions I play, or the next faction in the list
faction_map = {}
for item_tuple in mini_lines:
    faction = item_tuple[1]
    if faction not in MY_CURRENT_FACTIONS:
        continue
    if faction not in faction_map:
        faction_map[faction] = [0, 0]
    faction_map[faction][0] += item_tuple[2]
    faction_map[faction][1] += item_tuple[3]
fac_list = []
for map_fac, map_inv in faction_map.items():
    fac_list.append((map_fac, map_inv[0], map_inv[1]))
fac_list = sorted(fac_list, key=lambda x:(x[1]/x[2], x[0]))
FILTERED_FACTION = fac_list[0][0]
if (len(MY_CURRENT_FACTIONS) / len(VALID_FACTIONS)) < (fac_list[0][1] / fac_list[0][2]):
    FILTERED_FACTION = MY_FUTURE_FACTIONS[0]
filtered_list = []
for check_line in mini_lines:
    if FILTERED_FACTION in check_line[1]:
        filtered_list.append(check_line)

item_choice, filtered_list = sort_and_filter(filtered_list, 0)

filtered_list = filtered_list[0]

# Begin reading in army lists
army_lists = []
for sub_dir in os.listdir(LIST_DIR):
    if sub_dir == 'Unused Themes.txt':
        continue
    for fac_list_file in os.listdir(LIST_DIR + "/" + sub_dir):
        list_name = sub_dir + "/" + fac_list_file.replace('.txt', '')
        this_list = {}
        list_fh = open(LIST_DIR + "/" + sub_dir + "/" + fac_list_file, 'r', encoding="UTF-8")
        list_lines = list_fh.readlines()
        list_fh.close()
        list_lines = [lline.strip() for lline in list_lines]
        for line in list_lines:
            if line.startswith('#') or line == '':
                continue
            if '[100Rice]' in line or '[100 Rice]' in line:
                continue
            if line in theme_lines:
                continue
            line = line.split(':')[0]
            line = re.sub(r" \[\d+ Rice]", '', line)
            line = re.sub(r" \[-\d+ Rice]", '', line)
            line = line.replace(' - Human Form', '')
            line = line.replace(' - Fox Form', '')
            if line in card_lines:
                continue
            line = manual_fix(line)
            if line == "IGNORE":
                continue
            if line not in this_list:
                this_list[line] = 0
            this_list[line] += 1
        cleanup_list = clean_list(this_list)
        army_lists.append({'name':list_name, 'list':cleanup_list})
unowned_items = {}
lists_minus_inventory = check_inventory(army_lists, mini_dict)
lists_minus_inventory = sorted(lists_minus_inventory, key=lambda x:x[1])
for army_list in lists_minus_inventory:
    army_items = army_list[2]
    for list_item, list_item_qty in army_items.items():
        if list_item not in unowned_items:
            unowned_items[list_item] = 0
        unowned_items[list_item] += list_item_qty

if __name__ == "__main__":
    if os.getcwd().endswith('minis_games'):
        out_file_h = open("output/BushidoOutput.txt", 'w', encoding="UTF-8")
    else:
        out_file_h = open("minis_games/output/BushidoOutput.txt", 'w', encoding="UTF-8")

    double_print("Inventory tracker and purchase suggestions for the Bushido " + \
        "miniatures game.\n", out_file_h)
    own_pct = TOTAL_OWN / TOTAL_MAX * 100
    double_print(f"I own {TOTAL_OWN} out of {TOTAL_MAX} models for this game " + \
        f"({own_pct:.2f} percent)", out_file_h)
    double_print(f"Maybe purchase a(n) {item_choice} from {FILTERED_FACTION} (have " + \
        f"{filtered_list[2]} out of {filtered_list[3]})", out_file_h)

    double_print(f"\nClosest list to completion is {lists_minus_inventory[0][0]} - " + \
        f"needs {lists_minus_inventory[0][1]} items", out_file_h)
    for item_name, item_qty in lists_minus_inventory[0][2].items():
        double_print(f"- {item_name}: {item_qty}", out_file_h)

    double_print("\nTen most needed minis: ", out_file_h)
    uo_item_list = unowned_items.items()
    uo_item_list = sorted(uo_item_list, key = lambda x: (-1 * x[1], x[0]))
    for uo_item in uo_item_list[:10]:
        double_print(f"{uo_item[0]}: {uo_item[1]}", out_file_h)
