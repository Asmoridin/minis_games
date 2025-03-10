#!/usr/bin/python3

"""
Collection tracker, and purchase suggestion tool for Marvel Crisis Protocol
"""

import os

from steve_utils.output_utils import double_print
from steve_utils.sort_and_filter import sort_and_filter
from steve_utils.check_inventory import check_inventory

GAME_NAME = "Marvel Crisis Protocol"
COMPANY = "AMG"

if os.getcwd().endswith('minis_games'):
    file_h = open('DB/MCPData.txt', 'r', encoding="UTF-8")
    LIST_DIR = 'Lists/MCP'
else:
    file_h = open('minis_games/DB/MCPData.txt', 'r', encoding="UTF-8")
    LIST_DIR = 'minis_games/Lists/MCP'

lines = file_h.readlines()
file_h.close()
lines = [line.strip() for line in lines]

valid_affiliations = ['Avengers', 'Hydra', 'Cabal', 'A-Force', 'Inhumans', 'X-Force',
    'Black Order', 'Defenders', 'Web Warriors', 'Convocation', 'Uncanny X-Men', 'Winter Guard',
    'Criminal Syndicate', 'Weapon X', 'Guardians of the Galaxy', 'Sentinels', 'Spider-Foes', 
    'S.H.I.E.L.D.', 'Asgard', 'Midnight Sons', 'Brotherhood of Mutants', 'Wakanda',
    'Dark Dimension', 'Hellfire Club', 'New Mutants', 'Servants of the Apocalypse',
    'Thralls of Dracula', 'Legion of the Lost', 'UNAFFILIATED']

data = []
leaders = {}
affiliated_models = {}
affil_own = {}
owned_models = set()
for affiliation in valid_affiliations:
    leaders[affiliation] = []
    affiliated_models[affiliation] = []
    affil_own[affiliation] = [0, 0]
TOTAL_MAX = 0
TOTAL_OWN = 0
mini_dict = {}
for line in lines:
    if line == "":
        continue
    try:
        model_name, model_affils, model_own = line.split(';')
    except ValueError:
        print("Issue with line:")
        print(line)
        continue
    model_affils = model_affils.split(',')
    model_affils = [affiliation.strip() for affiliation in model_affils]
    actual_model_affils = []
    model_own = int(model_own)
    if model_name in ['Sentinel MK4 (1)', 'Sentinel MK4 (2)']:
        model_name = 'Sentinel MK4'
    mini_dict[model_name] = 0
    if model_own == 1:
        mini_dict[model_name] += 1
        owned_models.add(model_name)
    for affiliation in model_affils:
        cleaned_affil = affiliation.replace("/L", '')
        if cleaned_affil not in valid_affiliations:
            print(f"Invalid affiliation: {affiliation}")
            continue
        if "/L" in affiliation:
            leaders[cleaned_affil].append(model_name)
            affiliated_models[cleaned_affil].append(model_name)
            affil_own[cleaned_affil][0] += model_own
            affil_own[cleaned_affil][1] += 1
            actual_model_affils.append(cleaned_affil)
        else:
            affiliated_models[affiliation].append(model_name)
            affil_own[affiliation][0] += model_own
            affil_own[affiliation][1] += 1
            actual_model_affils.append(affiliation)
    TOTAL_MAX += 1
    TOTAL_OWN += model_own
    data.append([model_name, actual_model_affils, model_own, 1])

chosen_affil, filtered_list = sort_and_filter(data, 1)
# Grab a leader, if one exists that I don't have.
temp_list = []
for model_tuple in filtered_list:
    if model_tuple[0] in leaders[chosen_affil]:
        temp_list.append(model_tuple)
if len(temp_list) > 0:
    filtered_list = temp_list
chosen_model, filtered_list = sort_and_filter(filtered_list, 0)

army_lists = []
for sub_dir in os.listdir(LIST_DIR):
    if sub_dir == 'Status.txt':
        continue
    for fac_list_file in os.listdir(LIST_DIR + "/" + sub_dir):
        list_name = sub_dir + "/" + fac_list_file.replace('.txt', '')
        this_list = {}
        list_fh = open(LIST_DIR + "/" + sub_dir + "/" + fac_list_file, 'r', encoding="UTF-8")
        list_lines = list_fh.readlines()
        list_fh.close()
        list_lines = [lline.strip() for lline in list_lines]
        PAST_CHARS = False
        for line in list_lines:
            if PAST_CHARS:
                continue
            if line.startswith('#') or line == '':
                continue
            if line.startswith('Characters (') or line.startswith('Threat:'):
                continue
            if line.startswith('Tactics ('):
                PAST_CHARS = True
                continue
            if line.startswith('*'):
                line = line[1:]
            line = line.replace(' (2)', '').replace(' (3)', '').replace(' (4)', '')
            line = line.replace(' (5)', '').replace(' (6)', '').replace(' (7)', '')
            line = line.replace(' (8)', '').replace(' (Mind)', '').replace(' (Space)', '')
            line = line.replace(' (Reality)', '').replace(' (Power)', '').replace(' (Soul)', '')
            line = line.replace(' (Time)', '')
            line = line.replace(' (Reality, Space)', '').replace(' (Mind, Space)', '')
            if line not in this_list:
                this_list[line] = 0
            this_list[line] += 1
        army_lists.append({'name':list_name, 'list':this_list})
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
        out_file_h = open("output/MCPOutput.txt", 'w', encoding="UTF-8")
    else:
        out_file_h = open("minis_games/output/MCPOutput.txt", 'w', encoding="UTF-8")

    double_print("Marvel Crisis Protocol Inventory Tracker and purchase suggester\n", out_file_h)

    summary_str = f"I own {TOTAL_OWN} out of {TOTAL_MAX} - {100 * TOTAL_OWN/TOTAL_MAX:.2f} percent"
    double_print(summary_str, out_file_h)
    BUY_STRING = f"Buy a {chosen_model} from the {chosen_affil} affiliation"
    double_print(BUY_STRING, out_file_h)

    LOW_INDEX = 0
    completed_lists = []
    for print_list in lists_minus_inventory:
        if print_list[1] == 0:
            completed_lists.append(print_list[0])
            LOW_INDEX += 1
        else:
            break
    double_print(f"\nCompleted lists: {', '.join(sorted(completed_lists))}", out_file_h)
    double_print(f"Closest list to completion is {lists_minus_inventory[LOW_INDEX][0]} - " + \
        f"needs {lists_minus_inventory[LOW_INDEX][1]} items", out_file_h)
    for item_name, item_qty in lists_minus_inventory[LOW_INDEX][2].items():
        double_print(f"- {item_name}: {item_qty}", out_file_h)

    double_print("\nTen most needed minis: ", out_file_h)
    uo_item_list = unowned_items.items()
    uo_item_list = sorted(uo_item_list, key = lambda x: (-1 * x[1], x[0]))
    for uo_item in uo_item_list[:10]:
        double_print(f"{uo_item[0]}: {uo_item[1]}", out_file_h)
