#!/usr/bin/python3

"""
Win-Loss tracker and Fleet/Commander suggestion tool for Star Wars: Armada
"""

import os

from steve_utils.output_utils import double_print
from steve_utils.get_h_index import get_h_index

if os.getcwd().endswith('minis_games'):
    out_file_h = open("wl_output/SWArmadaOut.txt", 'w', encoding="UTF-8")
    in_file = open('wl_data/SWArmadaWL.txt', 'r', encoding="UTF-8")
    cmdr_data_file = open('wl_data/SWArmadaCommanders.txt', 'r', encoding="UTF-8")
else:
    out_file_h = open("minis_games/wl_output/SWArmadaOut.txt", 'w', encoding="UTF-8")
    in_file = open('minis_games/wl_data/SWArmadaWL.txt', 'r', encoding="UTF-8")
    cmdr_data_file = open('minis_games/wl_data/SWArmadaCommanders.txt', 'r', encoding="UTF-8")

VALID_FLEETS = ['Empire', 'Rebel', 'Republic', 'Separatist']

double_print("Star Wars: Armada Win-Loss Tracker and fleet selector", out_file_h)

# Let's read the commanders, and parse the commander data
cmdrs_by_fleet = {}
cmdr_to_fleet = {}
cmdr_total_plays = {}
seen_total = {}
cmdr_lines = cmdr_data_file.readlines()
cmdr_data_file.close()
cmdr_lines = [line.strip() for line in cmdr_lines]
for cmdr_line in cmdr_lines:
    if cmdr_line == '':
        continue
    try:
        fleet, cmdr_name = cmdr_line.split(';')
    except ValueError:
        print("Issue with commander line:")
        print(cmdr_line)
        continue
    if fleet not in VALID_FLEETS:
        print(f"Unknown fleet {fleet} for commander {cmdr_name}")
        continue
    if fleet not in cmdrs_by_fleet:
        cmdrs_by_fleet[fleet] = []
    cmdr_to_fleet[cmdr_name] = fleet
    cmdrs_by_fleet[fleet].append(cmdr_name)
    cmdr_total_plays[cmdr_name] = 0
    seen_total[cmdr_name] = 0

# Let's start parsing the W-L data
cmdr_wl = {} # For each commander, the total win loss tie
fleet_wl = {} # For each fleet, its win-loss-tie
opp_wl = {} # Win-Loss-Tie by opponent
opp_fleet_wl = {} # W-L-Ts each fleet
total_wl = [0, 0, 0]
in_lines = in_file.readlines()
in_file.close()
in_lines = [line.strip() for line in in_lines]
for line in in_lines:
    if line == '':
        continue
    try:
        my_fleet, my_cmdr, opp_fleet, opp_cmdr, opp_name, result = line.split(';')
    except ValueError:
        print("Problem with line:")
        print(line)
        continue
    if my_cmdr != "Unknown" and my_cmdr not in seen_total:
        print(f"My commander not recognized: {my_cmdr}")
        continue
    if opp_cmdr != "Unknown" and opp_cmdr not in seen_total:
        print(f"Opponent's commander not recognized: {opp_cmdr}")
        continue
    if result not in ['W', 'L', 'D']:
        print("Invalid response in line:")
        print(line)
        continue
    if my_cmdr != "Unknown":
        if my_cmdr not in cmdr_wl:
            cmdr_wl[my_cmdr] = [0, 0, 0]
        seen_total[my_cmdr] += 1
        cmdr_total_plays[my_cmdr] += 1

    if opp_cmdr != "Unknown":
        seen_total[opp_cmdr] += 1

    if my_fleet not in fleet_wl:
        fleet_wl[my_fleet] = [0, 0, 0]
    if opp_name not in opp_wl:
        opp_wl[opp_name] = [0, 0, 0]
    if opp_fleet not in opp_fleet_wl:
        opp_fleet_wl[opp_fleet] = [0, 0, 0]
    if result == 'W':
        total_wl[0] += 1
        if my_cmdr != "Unknown":
            cmdr_wl[my_cmdr][0] += 1
        fleet_wl[my_fleet][0] += 1
        opp_wl[opp_name][0] += 1
        opp_fleet_wl[opp_fleet][0] += 1
    elif result == 'L':
        total_wl[1] += 1
        if my_cmdr != "Unknown":
            cmdr_wl[my_cmdr][1] += 1
        fleet_wl[my_fleet][1] += 1
        opp_wl[opp_name][1] += 1
        opp_fleet_wl[opp_fleet][1] += 1
    else:
        total_wl[2] += 1
        if my_cmdr != "Unknown":
            cmdr_wl[my_cmdr][2] += 1
        fleet_wl[my_fleet][2] += 1
        opp_wl[opp_name][2] += 1
        opp_fleet_wl[opp_fleet][2] += 1

double_print(f"My current record (W-L-T) is {total_wl[0]}-{total_wl[1]}-{total_wl[2]}", out_file_h)

double_print(f"\nMy record by commander: ({len(seen_total)} total commander in game)", out_file_h)
cmdr_play_tuples = []
for fleet, fleet_ids in sorted(cmdrs_by_fleet.items()):
    fleet_wl_str = f"{fleet}:"
    if fleet in fleet_wl:
        fleet_wl_str = f"{fleet}: {fleet_wl[fleet][0]}-{fleet_wl[fleet][1]}-{fleet_wl[fleet][2]}"
    double_print(fleet_wl_str, out_file_h)
    for cmdr_name in fleet_ids:
        if cmdr_name in cmdr_wl:
            cmdr_play_tuples.append((cmdr_name, sum(cmdr_wl[cmdr_name])))
            out_str = f" - {cmdr_name}: {cmdr_wl[cmdr_name][0]}-{cmdr_wl[cmdr_name][1]}-" + \
                f"{cmdr_wl[cmdr_name][2]}"
            double_print(out_str, out_file_h)

cmdr_play_tuples = sorted(cmdr_play_tuples, key=lambda x: (-1 * x[1], x[0]))
double_print(f"\nMy H-Index is {get_h_index(cmdr_play_tuples)}", out_file_h)

double_print("\nMy record against opponents:", out_file_h)
for opponent, this_opp_wl in sorted(opp_wl.items()):
    opp_wl_str = f"- {opponent}: {this_opp_wl[0]}-{this_opp_wl[1]}-{this_opp_wl[2]}"
    double_print(opp_wl_str, out_file_h)

double_print("\nMy record against opposing fleets:", out_file_h)
for opp_fleet, fleet_wl in sorted(opp_fleet_wl.items()):
    fleet_wl_str = f"- {opp_fleet}: {fleet_wl[0]}-{fleet_wl[1]}"
    double_print(fleet_wl_str, out_file_h)

# Least seen Commander
LEAST_PLAYED_QTY = 100
least_played_ids = []
for cmdr_name, id_played in seen_total.items():
    if id_played < LEAST_PLAYED_QTY:
        LEAST_PLAYED_QTY = id_played
        least_played_ids = [cmdr_name]
    elif id_played == LEAST_PLAYED_QTY:
        least_played_ids.append(cmdr_name)

double_print("\nI've seen the following commanders on the table the least " + \
        f"({LEAST_PLAYED_QTY} times)", out_file_h)
double_print(", ".join(least_played_ids), out_file_h)

# Figure out least played relevant commander
fleet_plays = {}
filtered_cmdr_plays = []
for check_id, cmdr_plays in cmdr_total_plays.items():
    this_fleet = cmdr_to_fleet[check_id]
    filtered_cmdr_plays.append((check_id, cmdr_plays))
    if this_fleet not in fleet_plays:
        fleet_plays[this_fleet] = 0
    fleet_plays[this_fleet] += cmdr_plays
fleet_play_sorter = []
for this_fleet, fleet_plays in fleet_plays.items():
    fleet_play_sorter.append((this_fleet, fleet_plays))
fleet_play_sorter = sorted(fleet_play_sorter, key=lambda x:(x[1], x[0]))

LOWEST_FLEET = fleet_play_sorter[0]
relevant_cmdr_plays = []

for cmdr_name, cmdr_plays in filtered_cmdr_plays:
    if cmdr_to_fleet[cmdr_name] == LOWEST_FLEET[0]:
        relevant_cmdr_plays.append((cmdr_name, cmdr_plays))
relevant_cmdr_plays = sorted(relevant_cmdr_plays, key=lambda x:(x[1], x[0]))

low_cmdr = relevant_cmdr_plays[0]
LOW_O_STR = f"\nI should play more games with {LOWEST_FLEET[0]}, where I only have " + \
    f"{int(LOWEST_FLEET[1])} games. Suggested commander - {low_cmdr[0]} ({low_cmdr[1]} " + \
    "total plays)"
double_print(LOW_O_STR, out_file_h)
