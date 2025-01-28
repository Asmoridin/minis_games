#!/usr/bin/python3

"""
Handler to identify the various WM armies
"""

class Army:
    """
    Just a helper class to keep track of an army
    """
    def __init__(self, army_name, faction, is_prime, is_mkiv, is_cadre):
        self.army_name = army_name
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

armies = [
    Army("Devourer's Host", "Circle Orboros", True, False, False),
    Army("MKIV Mercenary", "Mercenaries", True, True, True),
    Army("Secret Dominion", "Circle Orboros", True, False, False),
]
army_dict = {}
for army in armies:
    army_dict[army.army_name] = army
