#!/usr/bin/python3

"""
Win-Loss Tracker and play suggester for Marvel: Crisis Protocol
"""

import os

from steve_utils.output_utils import double_print
from steve_utils.get_h_index import get_h_index
from minis_games.list_scripts import marvel_crisis_protocol

if os.getcwd().endswith('minis_games'):
    out_file_h = open("wl_output/MCPWLOut.txt", 'w', encoding="UTF-8")
    in_file = open('wl_data/MCPResults.txt', 'r', encoding="UTF-8")
else:
    out_file_h = open("minis_games/wl_output/MCPWLOut.txt", 'w', encoding="UTF-8")
    in_file = open('minis_games/wl_data/MCPResults.txt', 'r', encoding="UTF-8")

double_print("Marvel: Crisis Protocol Win-Loss Tracker and army selector\n", out_file_h)
VALID_EXTRACTS = ['Alien Ship Crashes in Downtown!', 'Deadly Legacy Virus Cured?',
    'Fear Grips World As "Worthy" Terrorize Cities', 'Mutant Extremists Target U.S. Senators!',
    'Paranoia Pummels Populace!', 'Research Station Attacked!', 'Struggle for the Cube Continues',
    'Skrulls Infiltrate World Leadership', 'Spider-Infected Invade Manhattan',
    'The Montesi Formula Found']
VALID_SECURES = ['Cosmic Invasion! Black Order Descends on Earth', 'Riots Spark Over Extremis 3.0',
    'Infinity Formula Goes Missing!', 'Intrusions Open Across City as Seals Collapse',
    'Gamma Wave Sweeps Across Midwest', 'Mayor Fisk Vows to Find Missing Witnesses',
    'Deadly Meteors Mutate Civilians', 'Demons Downtown! Has Our Comeuppance Come Due?',
    'Mutant Madman Turns City Center Into Lethal Amusement Park',
    'Portals Overrun City With Spider-People!', 'Super-Powered Scoundrels Form Sinister Syndicate!',
    'SWORD Establishes Base On Moons Blue Area']

extract_wl = {}
for extract in VALID_EXTRACTS:
    extract_wl[extract] = [0,0]
secure_wl = {}
for secure in VALID_SECURES:
    secure_wl[secure] = [0,0]

all_affil_leaders = marvel_crisis_protocol.leaders
my_affil_leaders = {}
all_affil_games = {}
for affil, affil_members in all_affil_leaders.items():
    all_affil_games[affil] = 0
    for affil_member in affil_members:
        if affil_member in marvel_crisis_protocol.owned_models:
            if affil not in my_affil_leaders:
                my_affil_leaders[affil] = []
            my_affil_leaders[affil].append(affil_member)
# Handling affiliations with no actual leaders
my_affil_leaders['Convocation'] = []
my_affil_leaders['Weapon X'] = []

# Read in the play data.
game_lines = in_file.readlines()
in_file.close()
game_lines = [line.strip() for line in game_lines]
my_wl = [0,0]
my_affil_w_l = {}
my_affil_ldr_w_l = {}
opp_affil_w_l = {}
opp_affil_ldr_w_l = {}
affil_games = {}
opp_wl = {}
for game_line in game_lines:
    if game_line == "":
        continue
    try:
        my_affil, my_leader, opp_affil, opp_leader, result, opponent, extract, secure = \
            game_line.split(';')
    except ValueError:
        print("Issue with line:")
        print(game_line)
        continue
    if my_affil not in all_affil_leaders:
        print(f"I played an unknown affiliation: {my_affil}")
        continue
    if my_affil not in my_affil_w_l:
        my_affil_w_l[my_affil] = [0,0]
        my_affil_ldr_w_l[my_affil] = {}
        affil_games[my_affil] = 0
    if opp_affil not in all_affil_leaders and opp_affil != 'Unaffiliated':
        print(f"Opponent played an unknown affiliation: {opp_affil}")
        continue
    if opp_affil not in opp_affil_w_l and opp_affil != 'Unaffiliated':
        opp_affil_w_l[opp_affil] = [0,0]
        opp_affil_ldr_w_l[opp_affil] = {}
    LEADERLESS_AFFILS = ['Weapon X', 'Convocation']
    if my_affil not in LEADERLESS_AFFILS and my_leader not in all_affil_leaders[my_affil]:
        print(f"Unknown leader {my_leader} for affiliation {my_affil}")
        continue
    if my_leader not in my_affil_ldr_w_l[my_affil]:
        my_affil_ldr_w_l[my_affil][my_leader] = [0,0]
    if opp_affil != 'Unaffiliated':
        if opp_affil not in LEADERLESS_AFFILS and opp_leader not in all_affil_leaders[opp_affil]:
            print(f"Unknown leader {opp_leader} for affiliation {opp_affil}")
            continue
    if opp_affil != 'Unaffiliated' and opp_leader not in opp_affil_ldr_w_l[opp_affil]:
        opp_affil_ldr_w_l[opp_affil][opp_leader] = [0,0]
    if result not in ['W', 'L']:
        print(f"Invalid result: {result}")
        continue
    if extract != "" and extract not in VALID_EXTRACTS:
        print(f"Invalid Extract: {extract}")
        continue
    if secure != "" and secure not in VALID_SECURES:
        print(f"Invalid Secure: {secure}")
        continue
    affil_games[my_affil] += 1
    all_affil_games[my_affil] += 1
    if opp_affil != 'Unaffiliated':
        all_affil_games[opp_affil] += 1
    if opponent not in opp_wl:
        opp_wl[opponent] = [0,0]
    if result == 'W':
        my_wl[0] += 1
        my_affil_w_l[my_affil][0] += 1
        my_affil_ldr_w_l[my_affil][my_leader][0] += 1
        opp_wl[opponent][0] += 1
        if extract != '':
            extract_wl[extract][0] += 1
        if secure != '':
            secure_wl[secure][0] += 1
        if  opp_affil != 'Unaffiliated':
            opp_affil_w_l[opp_affil][0] += 1
            opp_affil_ldr_w_l[opp_affil][opp_leader][0] += 1
    else:
        my_wl[1] += 1
        my_affil_w_l[my_affil][1] += 1
        my_affil_ldr_w_l[my_affil][my_leader][1] += 1
        opp_wl[opponent][1] += 1
        if extract != '':
            extract_wl[extract][1] += 1
        if secure != '':
            secure_wl[secure][1] += 1
        if  opp_affil != 'Unaffiliated':
            opp_affil_w_l[opp_affil][1] += 1
            opp_affil_ldr_w_l[opp_affil][opp_leader][1] += 1

temp_affil_games = affil_games

double_print(f"My current record is {my_wl[0]}-{my_wl[1]}\n", out_file_h)

double_print("Record by affiliation:", out_file_h)
for affiliation, affil_record in sorted(my_affil_w_l.items()):
    double_print(f"{affiliation}: {affil_record[0]}-{affil_record[1]}", out_file_h)
    if affiliation not in LEADERLESS_AFFILS:
        for affil_leader, leader_wl in sorted(my_affil_ldr_w_l[affiliation].items()):
            double_print(f"- {affil_leader}: {leader_wl[0]}-{leader_wl[1]}", out_file_h)

affil_games = sorted(affil_games.items(), key=lambda x:x[1], reverse=True)
double_print(f"\nMy H-Index is {get_h_index(affil_games)}", out_file_h)

#Record against opponent
double_print("\nRecord against opponents:", out_file_h)
for opp_name, opp_record in sorted(opp_wl.items()):
    double_print(f"{opp_name}: {opp_record[0]}-{opp_record[1]}", out_file_h)

#Record against affiliation
double_print("\nRecord against opposing affiliation:", out_file_h)
for affiliation, affil_record in sorted(opp_affil_w_l.items()):
    double_print(f"{affiliation}: {affil_record[0]}-{affil_record[1]}", out_file_h)
    if affiliation not in LEADERLESS_AFFILS:
        for affil_leader, leader_wl in sorted(opp_affil_ldr_w_l[affiliation].items()):
            double_print(f"- {affil_leader}: {leader_wl[0]}-{leader_wl[1]}", out_file_h)

# Lowest seen affiliation
all_affil_games = sorted(all_affil_games.items(), key=lambda x:(x[1], x[0]))
lowest_played_games = all_affil_games[0][1]
lowest_played_affils = []
for affil, affil_plays in all_affil_games:
    if affil_plays == lowest_played_games:
        lowest_played_affils.append(affil)
least_str = f"\nI've seen these affiliations played the least ({lowest_played_games} times): " + \
    f"{', '.join(lowest_played_affils)}"
double_print(least_str, out_file_h)

#Recommend an affiliation/leader
PLAY_AFFIL = ''
for affiliation in all_affil_leaders:
    if affiliation not in temp_affil_games:
        temp_affil_games[affiliation] = 0
temp_affil_games = sorted(temp_affil_games.items(), key=lambda x:(x[1], x[0]))
for find_affil in temp_affil_games:
    if find_affil[0] in my_affil_leaders:
        PLAY_AFFIL = find_affil[0]
        break
USING_STR = ""
if len(my_affil_leaders[PLAY_AFFIL]) > 0:
    if PLAY_AFFIL not in my_affil_ldr_w_l:
        USING_STR = f", using {my_affil_leaders[PLAY_AFFIL][0]}, who I have played 0 times"
    else:
        valid_leaders = []
        for p_ldr in my_affil_leaders[PLAY_AFFIL]:
            if p_ldr in my_affil_ldr_w_l[PLAY_AFFIL]:
                valid_leaders.append((p_ldr, sum(my_affil_ldr_w_l[PLAY_AFFIL][p_ldr])))
            else:
                valid_leaders.append((p_ldr, 0))
        valid_leaders = sorted(valid_leaders, key=lambda x:(x[1], x[0]))
        USING_STR = f", using {valid_leaders[0][0]}, who I have played {valid_leaders[0][1]} times"
else:
    if PLAY_AFFIL not in my_affil_ldr_w_l:
        USING_STR = ", who I have played 0 times"
    else:
        USING_STR = f", who I have played {sum(my_affil_w_l[PLAY_AFFIL])} times"
double_print(f"\nMaybe play more games as {PLAY_AFFIL}{USING_STR}", out_file_h)

double_print("\n*** Scenario Information ***", out_file_h)
#Extracts
extract_wl = sorted(extract_wl.items(), key = lambda x:(-1 * sum(x[1]), \
    -1 * x[1][0]/(x[1][0] + x[1][1]), x[0]))
double_print("Extract information (from most played to least):", out_file_h)
for extract, extract_record in extract_wl:
    double_print(f"{extract}: {extract_record[0]}-{extract_record[1]}", out_file_h)

#Secures
secure_wl = sorted(secure_wl.items(), key = lambda x:(-1 * sum(x[1]), \
    -1 * x[1][0]/(x[1][0] + x[1][1]), x[0]))
double_print("\nSecure information (from most played to least):", out_file_h)
for secure, secure_record in secure_wl:
    double_print(f"{secure}: {secure_record[0]}-{secure_record[1]}", out_file_h)
