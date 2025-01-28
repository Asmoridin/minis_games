#!/usr/bin/python3

"""
Collection tracker, and purchase suggestion tool for Marvel Crisis Protocol
"""

import os

from steve_utils.output_utils import double_print
from steve_utils.sort_and_filter import sort_and_filter

GAME_NAME = "Marvel Crisis Protocol"
COMPANY = "AMG"

if os.getcwd().endswith('minis_games'):
    file_h = open('DB/MCPData.txt', 'r', encoding="UTF-8")
else:
    file_h = open('minis_games/DB/MCPData.txt', 'r', encoding="UTF-8")

lines = file_h.readlines()
file_h.close()
lines = [line.strip() for line in lines]

valid_affiliations = ['Avengers', 'Hydra', 'Cabal', 'A-Force', 'Inhumans', 'X-Force',
    'Black Order', 'Defenders', 'Web Warriors', 'Convocation', 'Uncanny X-Men', 'Winter Guard',
    'Criminal Syndicate', 'Weapon X', 'Guardians of the Galaxy', 'Sentinels', 'Spider-Foes', 
    'S.H.I.E.L.D.', 'Asgard', 'Midnight Sons', 'Brotherhood of Mutants', 'Wakanda',
    'Dark Dimension', 'Hellfire Club', 'New Mutants', 'Servants of the Apocalypse',
    'Thralls of Dracula', 'Legion of the Lost']

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
for line in lines:
    if line == "":
        continue
    model_name, model_affils, model_own = line.split(';')
    model_affils = model_affils.split(',')
    model_affils = [affiliation.strip() for affiliation in model_affils]
    actual_model_affils = []
    model_own = int(model_own)
    if model_own == 1:
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

if __name__ == "__main__":
    if os.getcwd().endswith('minis_games'):
        out_file_h = open("output/MCPOutput.txt", 'w', encoding="UTF-8")
    else:
        out_file_h = open("minis_games/output/MCPOutput.txt", 'w', encoding="UTF-8")

    double_print("Marvel Crisis Protocol Inventory Tracker and purchase suggester\n", out_file_h)

    summary_str = f"I own {TOTAL_OWN} out of {TOTAL_MAX} - {100 * TOTAL_OWN/TOTAL_MAX:.2f} percent"
    double_print(summary_str, out_file_h)
    buy_string = f"Buy a {chosen_model} from the {chosen_affil} affiliation"
    double_print(buy_string, out_file_h)
