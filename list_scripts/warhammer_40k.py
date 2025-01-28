#!/usr/bin/python3

"""
Collection tracker/manager for the Warhammer 40K minis game.
"""

import os

from steve_utils.output_utils import double_print

GAME_NAME = "Warhammer 40,000"
COMPANY = "Games Workshop"

def get_meta(army_name):
    """
    Conert an army into one of the grouping of armies, based on my own criteria
    """
    if army_name in ['Black Templars', 'Blood Angels', 'Adeptus Astartes', 'Ultramarines',
        'Imperial Fists', 'White Scars', 'Raven Guard', 'Salamanders', 'Iron Hands',
        'Space Wolves', 'Dark Angels', 'Grey Knights', 'Deathwatch']:
        return "Space Marines"
    elif army_name in ['Thousand Sons', 'Death Guard', 'World Eaters', 'Chaos Knights',
        'Heretic Astartes', 'Legiones Daemonica']:
        return "Chaos"
    elif army_name in ['Aeldari', 'Drukhari']:
        return "Aeldari"
    elif army_name in ['Tyranids', 'Necrons', 'Genestealer Cults', 'Orks', "T'au Empire",
        'Leagues of Votann', ]:
        return "Xenos"
    elif army_name in ['Adeptus Custodes', 'Adeptus Mechanicus', 'Agents of the Imperium',
        'Astra Militarum', 'Adepta Sororitas', 'Imperial Knights', ]:
        return "Imperium"
    else:
        print(f"Army {army_name} not given a meta type")
        return None

my_armies = ['Adeptus Astartes', 'Necrons', 'Adepta Sororitas', 'Drukhari', 'World Eaters', ]

if os.getcwd().endswith('minis_games'):
    file_h = open('DB/WH40KData.txt', 'r', encoding="UTF-8")
else:
    file_h = open('minis_games/DB/WH40KData.txt', 'r', encoding="UTF-8")

lines = file_h.readlines()
file_h.close()
lines = [line.strip() for line in lines]

TOTAL_MAX = 0
TOTAL_OWN = 0
errors = []
item_names = set()
army_points = {}
filter_lines = []
for line in lines:
    line = line.split('//')[0].strip()
    if line == '':
        continue
    try:
        item_name, factions, keywords, points, item_own = line.split(';')
    except ValueError:
        print("Issue with line: " + line)
        continue
    item_names.add(item_name)
    factions = factions.split(',')
    factions = [faction.strip() for faction in factions]
    if len(factions) == 2 and 'Adeptus Astartes' in factions:
        factions.remove('Adeptus Astartes')
    keywords = keywords.split(',')
    keywords = [kw.strip() for kw in keywords]
    points = int(points)
    try:
        item_own = float(item_own)
    except:
        item_own = int(item_own.split('/')[0])/int(item_own.split('/')[1])
    ITEM_MAX = 3
    if 'Epic Hero' in keywords:
        ITEM_MAX = 1
    elif 'Battleline' in keywords or 'Dedicated Transport' in keywords:
        ITEM_MAX = 6
    TOTAL_MAX += ITEM_MAX
    TOTAL_OWN += item_own

    for army in factions:
        if army not in army_points:
            army_points[army] = 0
        army_points[army] += points * item_own
    filter_lines.append((item_name, factions, keywords, points, item_own, ITEM_MAX))

# Filter by meta_faction
meta_faction = {}
for line in filter_lines:
    this_meta = get_meta(line[1][0])
    if this_meta not in meta_faction:
        meta_faction[this_meta] = [0, 0]
    meta_faction[this_meta][1] += line[4]
    meta_faction[this_meta][0] += line[5]
meta_sorter = []
for meta_item in meta_faction:
    meta_sorter.append((meta_item, meta_faction[meta_item][1]/meta_faction[meta_item][0], meta_faction[meta_item][0] - meta_faction[meta_item][1]))
meta_sorter = sorted(meta_sorter, key=lambda x:(x[1], -x[2], x[0]))

# Filter by army
armies = {}
for line in filter_lines:
    if get_meta(line[1][0]) != meta_sorter[0][0]:
        continue
    for army in line[1]:
        if army not in my_armies:
            continue
        if army not in armies:
            armies[army] = [0, 0]
        armies[army][1] += line[4]
        armies[army][0] += line[5]
army_sorter = []
for army in armies:
    army_sorter.append((army, armies[army][1]/armies[army][0], armies[army][0] - armies[army][1]))
army_sorter = sorted(army_sorter, key=lambda x:(x[1], -x[2], x[0]))

# Filter by keyword
keywords = {}
new_filter_lines = []
for line in filter_lines:
    if army_sorter[0][0] not in line[1]:
        continue
    for keyword in line[2]:
        if keyword not in item_names:
            if keyword not in keywords:
                keywords[keyword] = [0, 0]
            keywords[keyword][1] += line[4]
            keywords[keyword][0] += line[5]
    new_filter_lines.append(line)
filter_lines = new_filter_lines
keyword_sorter = []
for keyword in keywords:
    keyword_sorter.append((keyword, keywords[keyword][1]/keywords[keyword][0], keywords[keyword][0] - keywords[keyword][1]))
keyword_sorter = sorted(keyword_sorter, key=lambda x:(x[1], -x[2], x[0]))

# Sort by name
names = []
for line in filter_lines:
    if keyword_sorter[0][0] in line[2]:
        names.append((line[0], line[4]/line[5], line[5] - line[4]))
names = sorted(names, key=lambda x:(x[1], -x[2], x[0]))

if __name__ == "__main__":
    if os.getcwd().endswith('minis_games'):
        out_file_h = open("output/Warhammer40K.txt", 'w', encoding="UTF-8")
    else:
        out_file_h = open("minis_games/output/Warhammer40K.txt", 'w', encoding="UTF-8")
    for error in errors:
        double_print(error, out_file_h)
    double_print("I own %.2f out of %d - %.2f percent" % (TOTAL_OWN, TOTAL_MAX, 100 * TOTAL_OWN/TOTAL_MAX), out_file_h)

    status_string = "Buy a %s unit from the %s army, perhaps a %s" % (keyword_sorter[0][0], army_sorter[0][0], names[0][0])
    double_print(status_string, out_file_h)

    double_print("\nArmy points summary:", out_file_h)
    for army in sorted(army_points):
        if army_points[army] > 0:
            double_print(f" - {army}: {army_points[army]}", out_file_h)
