#!/usr/bin/python3

"""
Tracker and army suggestion tool for games of Battleground
"""

import os

from steve_utils.output_utils import double_print
from steve_utils.get_h_index import get_h_index

armies = ['Dwarves of Runegard', 'Orcs & Goblins', 'The Risen Kingdom', 'Rome', 'Carthage',
    'Persia', 'Macedon', 'Men of Hawkshold', 'Lords of Vlachold', 'Elves of Ravenwood',
    'Lizardmen', 'Wuxing', 'Monsters and Mercenaries', 'High Elves', 'Dark Elves',
    'Umenzi Tribesmen']

army_games_map = {}
for army in armies:
    army_games_map[army] = 0

if os.getcwd().endswith('minis_games'):
    file_h = open('wl_data/BattlegroundData.txt', 'r', encoding="UTF-8")
    out_file_h = open("wl_output/BattlegroundOut.txt", 'w', encoding="UTF-8")
else:
    file_h = open('minis_games/wl_data/BattlegroundData.txt', 'r', encoding="UTF-8")
    out_file_h = open("minis_games/wl_output/BattlegroundOut.txt", 'w', encoding="UTF-8")

data_lines = file_h.readlines()
file_h.close()
data_lines = [line.strip() for line in data_lines]

my_army_wl = {}
my_opp_wl = {}
my_opp_army_wl = {}
total_wl = [0, 0]

for line in data_lines:
    if line == "":
        continue
    if line.startswith('#'):
        continue
    MY_ARMY, OPP_ARMY, opponent, w_l = line.split(';')
    if MY_ARMY not in armies:
        double_print(f"Invalid army: {MY_ARMY}", out_file_h)
    if OPP_ARMY not in armies:
        double_print(f"Invalid army: {OPP_ARMY}", out_file_h)
    army_games_map[MY_ARMY] += 1
    army_games_map[OPP_ARMY] += 1

    if w_l not in ['W', 'L']:
        double_print(f"Invalid W/L: {w_l}", out_file_h)

    if MY_ARMY not in my_army_wl:
        my_army_wl[MY_ARMY] = [0, 0]
    if opponent not in my_opp_wl:
        my_opp_wl[opponent] = [0, 0]
    if OPP_ARMY not in my_opp_army_wl:
        my_opp_army_wl[OPP_ARMY] = [0, 0]

    if w_l == 'W':
        my_army_wl[MY_ARMY][0] += 1
        my_opp_wl[opponent][0] += 1
        total_wl[0] += 1
        my_opp_army_wl[OPP_ARMY][0] += 1
    if w_l == 'L':
        my_army_wl[MY_ARMY][1] += 1
        my_opp_wl[opponent][1] += 1
        total_wl[1] += 1
        my_opp_army_wl[OPP_ARMY][1] += 1

double_print("Battleground Win-Loss Tracker and army suggestion tool\n", out_file_h)

double_print(f"My current record is {total_wl[0]}-{total_wl[1]}\n", out_file_h)
double_print("My record by army:", out_file_h)
for army in sorted(my_army_wl):
    double_print(f"{army}: {my_army_wl[army][0]}-{my_army_wl[army][1]}", out_file_h)

army_h_index = []
for army, a_w_l in my_army_wl.items():
    army_h_index.append((army, sum(a_w_l)))
army_h_index = sorted(army_h_index, key=lambda x:x[1], reverse=True)

double_print(f"\nMy H-Index is {get_h_index(army_h_index)}", out_file_h)

double_print("\nMy record against opponents:", out_file_h)
for opponent in sorted(my_opp_wl):
    double_print(f"{opponent}: {my_opp_wl[opponent][0]}-{my_opp_wl[opponent][1]}", out_file_h)

double_print("\nMy record against opposing armies:", out_file_h)
for opp_army in sorted(my_opp_army_wl):
    opp_army_string = f"{opp_army}: {my_opp_army_wl[opp_army][0]}-{my_opp_army_wl[opp_army][1]}"
    double_print(opp_army_string, out_file_h)

MIN_SEEN = 1000000
min_seen_armies = []
for army, army_games_played in army_games_map.items():
    if army_games_played < MIN_SEEN:
        MIN_SEEN = army_games_played
        min_seen_armies = [army]
    elif army_games_played == MIN_SEEN:
        min_seen_armies.append(army)
double_print(f"\nI've seen these armies on the table the least {MIN_SEEN} times: " + \
    f"{', '.join(sorted(min_seen_armies))}", out_file_h)

playable_army_list = []
for army in armies:
    if army not in my_army_wl:
        playable_army_list.append((army, 0))
    else:
        playable_army_list.append((army, sum(my_army_wl[army])))
playable_army_list = sorted(playable_army_list, key=lambda x:(x[1], x[0]))
least_army = playable_army_list[0][0]
least_army_games = playable_army_list[0][1]

sugg_string = f"\nI should play more games with {least_army}, as I only have " + \
    f"{least_army_games} game{('', 's')[least_army_games != 1]}"
double_print(sugg_string, out_file_h)
