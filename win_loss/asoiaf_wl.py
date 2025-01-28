#!/usr/bin/python3

"""
Win-Loss tracker and Army suggestion tool for A Song of Ice and Fire Miniatures Game
"""

import os

from steve_utils.output_utils import double_print
from steve_utils.get_h_index import get_h_index

if os.getcwd().endswith('minis_games'):
    out_file_h = open("wl_output/ASOIAFWLOut.txt", 'w', encoding="UTF-8")
    in_file = open('wl_data/ASOIAFResults.txt', 'r', encoding="UTF-8")
    ARMY_DATA_F = 'DB/ASOIAFData.txt'
else:
    out_file_h = open("minis_games/wl_output/ASOIAFWLOut.txt", 'w', encoding="UTF-8")
    in_file = open('minis_games/wl_data/ASOIAFResults.txt', 'r', encoding="UTF-8")
    ARMY_DATA_F = 'minis_games/DB/ASOIAFData.txt'

double_print("A Song of Ice and Fire Win-Loss Tracker and army selector", out_file_h)

GAME_MODES = ['A Game of Thrones', 'A Clash of Kings', 'A Dance With Dragons', 'A Feast for Crows',
    'Dark Wings, Dark Words', 'Fire & Blood', 'Winds of Winter', 'Here We Stand', 'Honed and Ready']

# Let's read the Army/Commander Data, and parse it
army_fh = open(ARMY_DATA_F, 'r', encoding="UTF-8")
army_lines = army_fh.readlines()
army_fh.close()
army_lines = [line.strip() for line in army_lines]
all_armies_commanders = {}
my_armies_commanders = {}
seen_total = {}
for line in army_lines:
    if line.startswith('#') or line == "":
        continue
    line = line.split('#')[0].strip()
    line_vals = line.split(';')
    if 'Commander' in line_vals[2]:
        for faction in line_vals[1].split('/'):
            if faction not in all_armies_commanders:
                all_armies_commanders[faction] = []
            all_armies_commanders[faction].append(line_vals[0])
            if line_vals[5] == '1':
                if faction not in my_armies_commanders:
                    my_armies_commanders[faction] = []
                my_armies_commanders[faction].append(line_vals[0])
        seen_total[line_vals[0]] = 0

army_total_plays = {}
for army_name in all_armies_commanders:
    army_total_plays[army_name] = 0

# Let's start parsing the W-L data
commander_wl = {} # For each commander, the total win loss
army_wl = {} # For each army, its win-loss
opp_wl = {} # Win-Loss by opponent
opp_army_wl = {} # W-L against each army
total_wl = [0, 0]
in_lines = in_file.readlines()
in_file.close()
in_lines = [line.strip() for line in in_lines]
mode_wl = {}
for game_mode in GAME_MODES:
    mode_wl[game_mode] = [0, 0]
for line in in_lines:
    if line == '':
        continue
    try:
        my_army, my_comm, opp_army, opp_comm, result, opp_name, my_score, opp_score, \
            game_mode = line.split(';')
    except ValueError:
        print("Problem with line:")
        print(line)
        continue
    if my_army not in all_armies_commanders:
        print(f"My army not recognized: {my_army}")
        continue
    if my_comm not in all_armies_commanders[my_army]:
        print(f"Invalid Commander: {my_comm}")
        continue
    if opp_army not in all_armies_commanders:
        print(f"Opponent's army not recognized: {opp_army}")
        continue
    if opp_comm not in all_armies_commanders[opp_army]:
        print(f"Invalid Opponent Commander: {opp_comm}")
        continue
    if result not in ['W', 'L']:
        print("Invalid result in line:")
        print(line)
        continue

    if my_comm not in commander_wl:
        commander_wl[my_comm] = [0, 0]
    seen_total[my_comm] += 1
    seen_total[opp_comm] += 1
    army_total_plays[my_army] += 1
    if my_army not in army_wl:
        army_wl[my_army] = [0, 0]
    if opp_name not in opp_wl:
        opp_wl[opp_name] = [0, 0]
    if opp_army not in opp_army_wl:
        opp_army_wl[opp_army] = [0, 0]
    if result == 'W':
        total_wl[0] += 1
        commander_wl[my_comm][0] += 1
        army_wl[my_army][0] += 1
        opp_wl[opp_name][0] += 1
        opp_army_wl[opp_army][0] += 1
        mode_wl[game_mode][0] += 1
    if result == 'L':
        total_wl[1] += 1
        commander_wl[my_comm][1] += 1
        army_wl[my_army][1] += 1
        opp_wl[opp_name][1] += 1
        opp_army_wl[opp_army][1] += 1
        mode_wl[game_mode][1] += 1

double_print(f"My current record is {total_wl[0]}-{total_wl[1]}", out_file_h)

double_print("\nMy record by commander:", out_file_h)
for army_name, army_comms in sorted(all_armies_commanders.items()):
    ARMY_WL_STR = ""
    if army_name in army_wl:
        ARMY_WL_STR = f"{army_name}: {army_wl[army_name][0]}-{army_wl[army_name][1]}"
    if ARMY_WL_STR != "":
        double_print(ARMY_WL_STR, out_file_h)
        for comm_name in army_comms:
            if comm_name in commander_wl:
                c_str = f" - {comm_name}: {commander_wl[comm_name][0]}-{commander_wl[comm_name][1]}"
                double_print(c_str, out_file_h)

# H-Index
h_indexer = []
for comm_name, comm_plays in commander_wl.items():
    h_indexer.append((comm_name, sum(comm_plays)))
h_indexer = sorted(h_indexer, key=lambda x:x[1], reverse=True)

double_print(f"\nMy H-Index is {get_h_index(h_indexer)}", out_file_h)

double_print("\nMy record against opponents:", out_file_h)
for opponent, this_opp_wl in sorted(opp_wl.items()):
    opp_wl_str = f"- {opponent}: {this_opp_wl[0]}-{this_opp_wl[1]}"
    double_print(opp_wl_str, out_file_h)

double_print("\nMy record against opposing armies:", out_file_h)
for opp_army, army_wl in sorted(opp_army_wl.items()):
    army_wl_str = f"- {opp_army}: {army_wl[0]}-{army_wl[1]}"
    double_print(army_wl_str, out_file_h)

double_print("\nRecord by game mode (most played first):", out_file_h)
game_mode_sorted = sorted(mode_wl.items(), key = lambda x:(-1 * sum(x[1]), x[0]))
for g_m in game_mode_sorted:
    double_print(f"- {g_m[0]} : {g_m[1][0]}-{g_m[1][1]}", out_file_h)

# Least seen commanders
LEAST_PLAYED_QTY = 100
least_played_commanders = []
for comm_name, comm_played in seen_total.items():
    if comm_played < LEAST_PLAYED_QTY:
        LEAST_PLAYED_QTY = comm_played
        least_played_commanders = [comm_name]
    elif comm_played == LEAST_PLAYED_QTY:
        least_played_commanders.append(comm_name)

see_str = f"\nI've seen the following commanders on the table the least ({LEAST_PLAYED_QTY} times)"
double_print(see_str, out_file_h)
double_print("; ".join(least_played_commanders), out_file_h)

# Figure out least played relevant army
for army_name in all_armies_commanders:
    if army_name not in my_armies_commanders:
        del army_total_plays[army_name]
LOWEST_ARMY = sorted(army_total_plays.items(), key= lambda x:(x[1], x[0]))[0]
filtered_comms = []
for commander in my_armies_commanders[LOWEST_ARMY[0]]:
    filtered_comms.append((commander, seen_total[commander]))
filtered_comms = sorted(filtered_comms, key = lambda x: (x[1], x[0]))
lowest_comm = filtered_comms[0]

LOW_A_STR = f"\nI should play more games with {LOWEST_ARMY[0]}, where I only have " + \
    f"{int(LOWEST_ARMY[1])} games. Suggested Commander - {lowest_comm[0]} ({lowest_comm[1]} " + \
    "total plays)"
double_print(LOW_A_STR, out_file_h)
