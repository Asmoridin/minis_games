#!/usr/bin/python3

"""
Summarizes the current collection status of all tracked board games
"""

import os
import math
import sys

from board_games.General.Libraries.output_utils import double_print

FILE_PREFIX = "board_games/General"
if os.getcwd().endswith('board_games'):
    FILE_PREFIX = "General"

# Process Play Data

PLAY_DIR = os.path.join(FILE_PREFIX, "Data", "Plays")

# Fix for renamed games
GAME_NAME_FIX = {
    "Hordes: High Command": "Warmachine: High Command",
    "Shadowfist: Combat In Kowloon": "Shadowfist",
    "Spearpoint 1943: Eastern Front": "Spearpoint 1943",
    "Summoner Wars": "Summoner Wars (Second Edition)",
}

game_plays_total = {}
game_year_counter = {} # To track in how many years a game was playable
YEARS_PROCESSED = 0
prev_year_plays = {}
for play_file in sorted(os.listdir(PLAY_DIR))[:-1]:
    if not play_file.endswith(".txt"):
        continue
    YEARS_PROCESSED += 1
    prev_year_plays = {}
    with open(os.path.join(PLAY_DIR, play_file), encoding="UTF-8") as play_file_h:
        play_lines = play_file_h.readlines()
    play_lines = [line.strip() for line in play_lines]
    this_years_plays = []
    for play_line in play_lines:
        if play_line == "":
            continue
        play_game, play_count = play_line.split(';')
        play_game = play_game.strip()
        if play_game in GAME_NAME_FIX:
            play_game = GAME_NAME_FIX[play_game]
        play_count = int(play_count)
        this_years_plays.append((play_game, play_count))
        if play_game not in game_plays_total:
            game_year_counter[play_game] = 0
            game_plays_total[play_game] = 0
        game_plays_total[play_game] += play_count
        prev_year_plays[play_game] = play_count
    for game_name in game_year_counter:
        game_year_counter[game_name] += 1

    this_years_plays = sorted(this_years_plays, key=lambda x:x[1], reverse=True)

PREV_YEAR_PLAY_TOTAL = 0
for game_name, play_count in prev_year_plays.items():
    if game_name != "New Game":
        PREV_YEAR_PLAY_TOTAL += play_count

# Get current year data
THIS_YEAR_PLAYS = 0
current_year_file = sorted(os.listdir(PLAY_DIR))[-1]
with open(os.path.join(PLAY_DIR, current_year_file), encoding="UTF-8") as play_file_h:
    current_play_lines = play_file_h.readlines()
current_play_lines = [line.strip() for line in current_play_lines]
current_year_plays = {}
for play_line in current_play_lines:
    if play_line == "":
        continue
    play_game, play_count = play_line.split(';')
    play_count = int(play_count)
    current_year_plays[play_game] = play_count
    if play_game != "New Game":
        THIS_YEAR_PLAYS += play_count

if __name__ == "__main__":
    if os.getcwd().endswith('board_games'):
        out_file_h = open("General/BGSummaryOut.txt", 'w', encoding="UTF-8")
    else:
        out_file_h = open("board_games/General/BGSummaryOut.txt", 'w', encoding="UTF-8")

    game_goals = {}
    TOTAL_PLAYS_GOAL = 0
    for game_name, game_plays in game_plays_total.items():
        # Take the highest of last year's plays, or average plays per year
        avg_plays = math.ceil(game_plays / game_year_counter[game_name])
        last_year_plays = prev_year_plays.get(game_name, 0)
        goal_plays = max(avg_plays, last_year_plays + 1)
        game_goals[game_name] = goal_plays
        if game_name != "New Game":
            TOTAL_PLAYS_GOAL += goal_plays

    # Figure out today's date progress as a percentage of the year
    from datetime import datetime
    now = datetime.now()
    start_of_year = datetime(now.year, 1, 1)
    end_of_year = datetime(now.year + 1, 1, 1)
    year_progress = (now - start_of_year).total_seconds() / \
        (end_of_year - start_of_year).total_seconds()

    # Now, given our current year progress, determine how many plays we should have
    # And then print out the top 10 games by how far off that goal we are
    game_progress = []
    TOTAL_PLAYS = 0
    completed_games = []
    new_games = []
    for game_name, _ in current_year_plays.items():
        if game_name not in game_goals:
            # Game not played last year, so just make it a goal of 1
            game_goals[game_name] = 1
            TOTAL_PLAYS_GOAL += 1
            new_games.append(game_name)
    for game_name, goal_plays in game_goals.items():
        current_plays = current_year_plays.get(game_name, 0)
        if current_plays >= goal_plays:
            TOTAL_PLAYS += goal_plays
            if game_name in new_games:
                game_name += " (New Game)"
            completed_games.append(game_name)
            continue
        expected_plays = goal_plays * year_progress
        if game_name != "New Game":
            TOTAL_PLAYS += current_plays
        progress_diff = current_plays - expected_plays
        game_progress.append((game_name, current_plays, expected_plays, progress_diff))
    game_progress = sorted(game_progress, key=lambda x:x[3])
    double_print("\nTop 10 Games Behind Expected Play Count (based on " + \
        f"{year_progress*100:.2f}% of year):", out_file_h)
    for game_info in game_progress[:10]:
        info_n, info_c, info_e, _ = game_info
        info_g = game_goals.get(info_n, 0)
        info_diff = info_e - info_c
        if info_diff > 0:
            PT_STR = f"- {info_n}: {info_c} plays out of {info_g} ({info_diff:.2f} behind)"
        else:
            PT_STR = f"- {info_n}: {info_c} plays out of {info_g} ({info_diff:.2f} ahead)"
        double_print(PT_STR, out_file_h)

    # Figure out what percentage of the total plays goal we've achieved
    # And then print out how far off pace we are
    total_plays_percentage = TOTAL_PLAYS * 100 / TOTAL_PLAYS_GOAL
    expected_pace = year_progress * TOTAL_PLAYS_GOAL
    pace_diff = TOTAL_PLAYS - expected_pace
    total_plays_string = f"\nTotal Plays so far: {TOTAL_PLAYS} out of " + \
        f"{TOTAL_PLAYS_GOAL} ({total_plays_percentage:.2f} percent)"
    double_print(total_plays_string, out_file_h)
    pace_string = f"At {year_progress*100:.2f}% of the year, you should have " + \
        f"played {expected_pace:.2f} games. You are {'ahead' if pace_diff >= 0 else 'behind'} " + \
        f"pace by {abs(pace_diff):.2f} plays."
    double_print(pace_string, out_file_h)
    total_play_str = f"In total, you have played {THIS_YEAR_PLAYS} games this year, " + \
        f"compared to {PREV_YEAR_PLAY_TOTAL} last year."
    double_print(total_play_str, out_file_h)
    double_print(f"Completed Games List: ({len(completed_games)})", out_file_h)
    for comp_game in sorted(completed_games):
        double_print(f"- {comp_game}", out_file_h)

    out_file_h.close()
