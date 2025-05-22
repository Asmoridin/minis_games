#!/usr/bin/python3

"""
Collection manager, points summary for Warmachine MKIV.
"""

import os

from steve_utils.output_utils import double_print
from steve_utils.sort_and_filter import sort_and_filter
import minis_games.Libraries.wm_armies as wm_armies

# Devourer's Host is 366 points

GAME_NAME = "Warmachine MKIV"
COMPANY = "Privateer Press"

if os.getcwd().endswith('minis_games'):
    file_h = open('DB/WMMKIVData.txt', 'r', encoding="UTF-8")
else:
    file_h = open('minis_games/DB/WMMKIVData.txt', 'r', encoding="UTF-8")

def validate_armies(army_string):
    """
    Take an army string, and return a list of armies that are valid strings
    """
    armies = []
    for army in army_string.split('/'):
        if wm_armies.is_valid(army):
            armies.append(army)
        else:
            print("Invalid army: " + army)
    return armies

def validate_model_types(in_model_type):
    """
    Return a more generic model type
    """
    if in_model_type in ['Solo', 'Unit', 'Battle Engine']:
        return in_model_type
    elif in_model_type in ['Warlock', 'Warcaster']:
        return "Leader"
    elif in_model_type in ['Heavy Warbeast', 'Light Warbeast', 'Gargantuan Warbeast',
        'Heavy Warjack', 'Light Warjack']:
        return "Battlegroup"
    elif in_model_type in ['Command Attachment']:
        return "Unit"
    elif in_model_type in ['Structure']:
        return "Battle Engine"
    else:
        print("Unknown model type: " + in_model_type)

lines = file_h.readlines()
file_h.close()
lines = [line.strip() for line in lines]

data = []
leaders = []
TOTAL_MAX = 0
TOTAL_OWN = 0
model_names = set()
for line in lines:
    if line == '' or line.startswith('#'):
        continue
    try:
        model_name, model_armies, model_type, paint_points, dollar_cost, points, max_fa, \
            own_amount, built_amount, painted_amount = line.split(';')
    except ValueError:
        print(f"Issue with line for {line.split(';')[0]}")
        continue
    if model_name in model_names:
        print("Duplicate: " + model_name)
    model_names.add(model_name)
    model_armies = validate_armies(model_armies)
    MODEL_LEGALITY = wm_armies.get_legality(model_armies)
    MODEL_ERA = wm_armies.get_era(model_armies)
    model_type = validate_model_types(model_type)
    paint_points = int(paint_points)
    #TODO: Figure out dollar_cost
    points = int(points)
    max_fa = int(max_fa)
    own_amount = int(own_amount)
    built_amount = int(built_amount)
    painted_amount = int(painted_amount)
    if painted_amount > built_amount or built_amount > own_amount:
        print(f"May have an inventory issue with {model_name}")
