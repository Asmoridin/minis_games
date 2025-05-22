#!/usr/bin/python3

"""
Handler to identify the various WM armies
"""

VALID_FACTIONS = ['Cryx', 'Cygnar', 'Circle Orboros', 'Mercenaries']

class Army:
    """
    Just a helper class to keep track of an army
    """
    def __init__(self, army_name:str, faction:str, is_prime:bool, is_mkiv:bool, is_cadre:bool):
        self.army_name = army_name
        if faction not in VALID_FACTIONS:
            print(f"Invalid faction: {faction}")
        self.army_faction = faction
        self.is_prime = is_prime
        self.is_mkiv = is_mkiv
        self.is_cadre = is_cadre

def is_valid(army_name):
    """
    Returns true if the army is in the system as all, otherwise false
    """
    for army_obj in armies:
        if army_obj.army_name == army_name:
            return True
    return False

def get_legality(in_armies):
    """
    Returns Prime is one of the armies is Prime legal, otherwise return Unlimited
    """
    for this_army in in_armies:
        if army_dict[this_army].is_prime:
            return "Prime"
    return "Unlimited"

def get_era(in_armies):
    """
    Returns MKIV if the armies are MKIV era, otherwise return Legacy
    """
    for this_army in in_armies:
        if army_dict[this_army].is_mkiv:
            return "MKIV"
    return "Legacy"

armies = []

with open("minis_games/DB/WMMKIV-Armies.txt", 'r', encoding="UTF-8") as army_fh:
    for army_line in army_fh:
        if army_line.startswith('#'):
            continue
        in_army_name, faction_name, IN_PRIME, IN_MKIV, IS_CADRE = army_line.strip().split(';')
        if IN_PRIME == "True":
            IN_PRIME = True
        elif IN_PRIME == "False":
            IN_PRIME = False
        else:
            print(f"Invalid value for is_prime {IN_PRIME}")
            continue
        if IN_MKIV == "True":
            IN_MKIV = True
        elif IN_MKIV == "False":
            IN_MKIV = False
        else:
            print(f"Invalid value for in_mkiv {IN_MKIV}")
            continue
        if IS_CADRE == "True":
            IS_CADRE = True
        elif IS_CADRE == "False":
            IS_CADRE = False
        else:
            print(f"Invalid value for in_mkiv {IS_CADRE}")
            continue
        armies.append(Army(in_army_name, faction_name, IN_PRIME, IN_MKIV, IS_CADRE))

army_dict = {}
for army in armies:
    army_dict[army.army_name] = army
