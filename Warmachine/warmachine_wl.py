#!/usr/bin/python3

"""
Win-Loss Tracker, and faction/army/leader suggestion tool for Warmachine MKIV
"""

import os

from steve_utils.output_utils import double_print
from steve_utils.get_h_index import get_h_index

if os.getcwd().endswith('minis_games'):
    out_file_h = open("wl_output/WarmachineOut.txt", 'w', encoding="UTF-8")
    in_file = open('wl_data/WarmachineResults.txt', 'r', encoding="UTF-8")
else:
    out_file_h = open("minis_games/wl_output/WarmachineOut.txt", 'w', encoding="UTF-8")
    in_file = open('minis_games/wl_data/WarmachineResults.txt', 'r', encoding="UTF-8")

double_print("Warmachine MKIV Win-Loss Tracker and army selector", out_file_h)

# This will eventually be replaced when Inventory System is up and running
VALID_ARMY_MAP = {'Orgoth':['Sea Raiders'], 'Mercenaries':['Blindwater Congregation', 'Rhul Guard'],
    'Circle Orboros':["Devourer's Host", 'Secret Dominion'], 'Khador':['Armored Korps']}
ARMY_TO_FAC = {}
for faction, armies in VALID_ARMY_MAP.items():
    for army in armies:
        ARMY_TO_FAC[army] = faction

SR_SCENARIOS = ['Recon MK4', 'Battle Lines', 'Wolves At Our Heels', 'Payload', 'Two Fronts',
    'Invasion']
BRAWL_SCENARIOS = ['Asteroids', 'Binary', 'Ignition 2', 'Orbits', 'Singualrity', 'Syzygy']
OLD_SCENARIOS = ['Recon II']
ALL_SCENARIOS = SR_SCENARIOS + BRAWL_SCENARIOS + OLD_SCENARIOS
sr_wl = {}
brawl_wl = {}
for scenario in SR_SCENARIOS:
    sr_wl[scenario] = [0, 0]
for scenario in BRAWL_SCENARIOS:
    brawl_wl[scenario] = [0, 0]

in_lines = in_file.readlines()
in_file.close()
in_lines = [line.strip() for line in in_lines]

total_wl = [0, 0] # My Win Loss Record
fac_wl = {} # Win-Loss by faction
my_faction_plays = {}
fac_army_wl = {} # Faction -> Army -> W-L
caster_wl = {} # Faction -> Army -> Caster -> W-L
my_army_plays = {}
my_caster_plays = {}
opp_wl = {}
opp_fac_wl = {} # Win-Loss by faction
opp_fac_army_wl = {} # Faction -> Army -> W-L
opp_caster_wl = {} # Faction -> Army -> Caster -> W-L
for line in in_lines:
    if line == "":
        continue
    my_army, my_caster, opponent, opp_army, opp_caster, game_result, game_pts, scenario \
        = line.split(';')
    if my_army not in ARMY_TO_FAC:
        print(f"My army is unknown: {my_army}")
        continue
    my_faction = ARMY_TO_FAC[my_army]
    if my_faction not in fac_wl:
        fac_wl[my_faction] = [0, 0]
        my_faction_plays[my_faction] = 0
        fac_army_wl[my_faction] = {}
        caster_wl[my_faction] = {}
    if my_army not in fac_army_wl[my_faction]:
        fac_army_wl[my_faction][my_army] = [0, 0]
        my_army_plays[my_army] = 0
        caster_wl[my_faction][my_army] = {}
    if my_caster not in caster_wl[my_faction][my_army]:
        caster_wl[my_faction][my_army][my_caster] = [0, 0]
    if my_caster not in my_caster_plays:
        my_caster_plays[my_caster] = 0

    if opponent not in opp_wl:
        opp_wl[opponent] = [0, 0]

    if opp_army not in ARMY_TO_FAC:
        print(f"Opponent's army is unknown: {opp_army}")
        continue
    opp_faction = ARMY_TO_FAC[opp_army]
    if opp_faction not in opp_fac_wl:
        opp_fac_wl[opp_faction] = [0, 0]
        opp_fac_army_wl[opp_faction] = {}
        opp_caster_wl[opp_faction] = {}
    if opp_army not in opp_fac_army_wl[opp_faction]:
        opp_fac_army_wl[opp_faction][opp_army] = [0, 0]
        opp_caster_wl[opp_faction][opp_army] = {}
    if opp_caster not in opp_caster_wl[opp_faction][opp_army]:
        opp_caster_wl[opp_faction][opp_army][opp_caster] = [0, 0]

    game_res_type, game_res = game_result.split(' ')
    if game_res_type not in ['Assassination', 'Concession', 'Scenario']:
        print(f"Unknown Result {game_res_type}")
        continue
    if game_res not in ['Win', 'Loss']:
        print(f"Win or Loss?: {game_result}")
        continue
    game_pts = int(game_pts)
    if game_pts not in [50, 75, 100]:
        print(f"Unknown game point level: {game_pts}")
        continue

    if scenario not in ALL_SCENARIOS:
        print(f"Unknown scenario: {scenario}")
        continue

    my_faction_plays[my_faction] += 1
    my_army_plays[my_army] += 1
    my_caster_plays[my_caster] += 1
    if game_res == 'Win':
        total_wl[0] += 1
        fac_wl[my_faction][0] += 1
        fac_army_wl[my_faction][my_army][0] += 1
        opp_wl[opponent][0] += 1
        caster_wl[my_faction][my_army][my_caster][0] += 1
        opp_fac_wl[opp_faction][0] += 1
        opp_fac_army_wl[opp_faction][opp_army][0] += 1
        opp_caster_wl[opp_faction][opp_army][opp_caster][0] += 1
        if scenario in SR_SCENARIOS:
            sr_wl[scenario][0] += 1
        if scenario in brawl_wl:
            brawl_wl[scenario][0] += 1
    else:
        total_wl[1] += 1
        fac_wl[my_faction][1] += 1
        fac_army_wl[my_faction][my_army][1] += 1
        opp_wl[opponent][1] += 1
        caster_wl[my_faction][my_army][my_caster][1] += 1
        opp_fac_wl[opp_faction][1] += 1
        opp_fac_army_wl[opp_faction][opp_army][1] += 1
        opp_caster_wl[opp_faction][opp_army][opp_caster][1] += 1
        if scenario in SR_SCENARIOS:
            sr_wl[scenario][1] += 1
        if scenario in brawl_wl:
            brawl_wl[scenario][1] += 1

double_print(f"\nMy record is {total_wl[0]}-{total_wl[1]}\n", out_file_h)

double_print("My record by faction", out_file_h)
for faction_name, faction_record in sorted(fac_wl.items()):
    double_print(f"{faction_name}: {faction_record[0]}-{faction_record[1]}", out_file_h)
    for army_name, army_record in sorted(fac_army_wl[faction_name].items()):
        double_print(f"- {army_name}: {army_record[0]}-{army_record[1]}", out_file_h)
        for caster_name, caster_rec in caster_wl[faction_name][army_name].items():
            double_print(f"--- {caster_name}: {caster_rec[0]}-{caster_rec[1]}", out_file_h)


double_print(f"\nMy Faction H-Index is {get_h_index(my_faction_plays.items())}", out_file_h)
double_print(f"My Army H-Index is {get_h_index(my_army_plays.items())}", out_file_h)
double_print(f"My Caster H-Index is {get_h_index(my_caster_plays.items())}", out_file_h)

double_print("\nMy record against opponents:", out_file_h)
for opponent_name, opp_record in sorted(opp_wl.items()):
    double_print(f"{opponent_name}: {opp_record[0]}-{opp_record[1]}", out_file_h)

double_print("\nMy record against opposing factions, armies, and casters:", out_file_h)
for faction_name, faction_record in sorted(opp_fac_wl.items()):
    double_print(f"{faction_name}: {faction_record[0]}-{faction_record[1]}", out_file_h)
    for army_name, army_record in sorted(opp_fac_army_wl[faction_name].items()):
        double_print(f"- {army_name}: {army_record[0]}-{army_record[1]}", out_file_h)
        for caster_name, caster_rec in opp_caster_wl[faction_name][army_name].items():
            double_print(f"--- {caster_name}: {caster_rec[0]}-{caster_rec[1]}", out_file_h)

LOW_FACTION = "Cryx"
LOW_ARMY = "Dark Host"
LOW_COMBO = "Cryx/Dark"
LOW_PLAYS = 0
LOW_CASTER = "Bane Witch Agathia"
double_print(f"\nI should play more games with {LOW_COMBO} as I only have {LOW_PLAYS} games " + \
    f"(preferably use {LOW_CASTER})", out_file_h)

double_print("\nScenario Information:", out_file_h)
for scenario in sorted(SR_SCENARIOS):
    double_print(f"{scenario}: {sr_wl[scenario][0]}-{sr_wl[scenario][1]}", out_file_h)

double_print("\nBrawlmachine Scenarios:", out_file_h)
for scenario in sorted(BRAWL_SCENARIOS):
    double_print(f"{scenario}: {brawl_wl[scenario][0]}-{brawl_wl[scenario][1]}", out_file_h)
