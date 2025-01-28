#!/usr/bin/python3

"""
Tracker and army suggestion tool for Star Wars: X-Wing
"""

import os

from steve_utils.output_utils import double_print
from steve_utils.get_h_index import get_h_index

if os.getcwd().endswith('minis_games'):
    out_file_h = open("wl_output/XWingOut.txt", 'w', encoding="UTF-8")
    in_file = open('wl_data/XWingWL.txt', 'r', encoding="UTF-8")
else:
    out_file_h = open("minis_games/wl_output/XWingOut.txt", 'w', encoding="UTF-8")
    in_file = open('minis_games/wl_data/XWingWL.txt', 'r', encoding="UTF-8")

all_factions = ['First Order', 'Galactic Empire', 'Galactic Republic', 'Rebellion',
    'Resistance', 'Scum and Villainy', 'Separatist Alliance',]

double_print("Star Wars: X-Wing Win-Loss Tracker and faction selector\n", out_file_h)

data_lines = in_file.readlines()
in_file.close()
data_lines = [line.strip() for line in data_lines]

my_fac_wl = {}
my_opp_wl = {}
my_opp_fac_wl = {}
total_wl = [0, 0]
fac_games_map = {}
for faction in all_factions:
    fac_games_map[faction] = 0

for line in data_lines:
    if line == "":
        continue
    if line.startswith('#'):
        continue
    my_faction, opp_faction, opponent, w_l = line.split(';')

    if my_faction not in all_factions:
        double_print(f"Invalid faction: {my_faction}", out_file_h)
        continue
    if opp_faction not in all_factions:
        double_print(f"Invalid faction: {opp_faction}", out_file_h)
        continue

    fac_games_map[my_faction] += 1
    fac_games_map[opp_faction] += 1

    if w_l not in ['W', 'L']:
        double_print(f"Invalid W/L: {w_l}", out_file_h)

    if my_faction not in my_fac_wl:
        my_fac_wl[my_faction] = [0, 0]
    if opponent not in my_opp_wl:
        my_opp_wl[opponent] = [0, 0]
    if opp_faction not in my_opp_fac_wl:
        my_opp_fac_wl[opp_faction] = [0, 0]

    if w_l == 'W':
        my_fac_wl[my_faction][0] += 1
        my_opp_wl[opponent][0] += 1
        total_wl[0] += 1
        my_opp_fac_wl[opp_faction][0] += 1
    if w_l == 'L':
        my_fac_wl[my_faction][1] += 1
        my_opp_wl[opponent][1] += 1
        total_wl[1] += 1
        my_opp_fac_wl[opp_faction][1] += 1

double_print(f"My current record is {total_wl[0]}-{total_wl[1]}\n", out_file_h)
double_print(f"My record by faction ({len(all_factions)} total factions):", out_file_h)
for faction in sorted(my_fac_wl):
    double_print(f"{faction}: {my_fac_wl[faction][0]}-{my_fac_wl[faction][1]}", out_file_h)

faction_h_index = []
for faction, l_w_l in my_fac_wl.items():
    faction_h_index.append((faction, sum(l_w_l)))
faction_h_index = sorted(faction_h_index, key=lambda x:x[1], reverse=True)

double_print(f"\nMy H-Index is {get_h_index(faction_h_index)}", out_file_h)

double_print("\nMy record against opponents:", out_file_h)
for opponent in sorted(my_opp_wl):
    double_print(f"{opponent}: {my_opp_wl[opponent][0]}-{my_opp_wl[opponent][1]}", out_file_h)

double_print("\nMy record against opposing factions:", out_file_h)
for opp_faction in sorted(my_opp_fac_wl):
    faction_str = f"{opp_faction}: {my_opp_fac_wl[opp_faction][0]}-{my_opp_fac_wl[opp_faction][1]}"
    double_print(faction_str, out_file_h)

MIN_SEEN = 1000000
min_seen_factions = []
for faction, faction_games in fac_games_map.items():
    if faction_games < MIN_SEEN:
        MIN_SEEN = faction_games
        min_seen_factions = [faction]
    elif faction_games == MIN_SEEN:
        min_seen_factions.append(faction)
double_print(f"\nI've seen these factions on the table the least ({MIN_SEEN} times): " + \
    f"{'; '.join(sorted(min_seen_factions))}", out_file_h)

playable_faction_list = []
for faction in all_factions:
    if faction not in my_fac_wl:
        playable_faction_list.append((faction, 0))
    else:
        playable_faction_list.append((faction, sum(my_fac_wl[faction])))
playable_faction_list = sorted(playable_faction_list, key=lambda x:(x[1], x[0]))
least_faction = playable_faction_list[0][0]
least_faction_games = playable_faction_list[0][1]

sugg_string = f"\nI should play more games with the {least_faction}, as I only have " + \
    f"{least_faction_games} game{('', 's')[least_faction_games != 1]}"
double_print(sugg_string, out_file_h)
