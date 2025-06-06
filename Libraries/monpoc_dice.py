#!/usr/bin/python3

a_die = ['Miss', 'Miss', 'Miss', 'Strike', 'Strike', 'Super Strike']
b_die = ['Miss', 'Miss', 'Strike', 'Strike', 'Strike', 'Super Strike']
p_die = ['Miss', 'Strike', 'Strike', 'Strike', 'Strike', 'Super Strike']

def rollDice(a_die_num, b_die_num, p_die_num, num_times = 100000, target_def = ''):
  # Create a list to handle possible outputs (to map out later)
  possible_results = [0] * ((a_die_num + b_die_num + p_die_num) * 2)
  total_results = 0
  success_results = 0
  for x in range (0, num_tries):
    this_roll_success = 0
    for a in range(0, a_die_num):
this_res = random.choice(a_die)
Strike + 1
Super Strike + 2
for b in range
for p in range

toatal_results += this_roll_successes
if targetDef != '' and this roll success >= target_def:
  success_result += 1

if __name__ == "main":
  rollDice(2,2,3, target_def=5)

Output:
Rolled 2 Action Die, 2 Boost Die, and 3 Power Die
Overall average of the roll is 6.00
80.46 percent change to hit Defense 5

Distribution:
- 0: 0.01
- 1: 0.21
- 2: 1.44
- 3: 5.42
- 4: 12.46
- 5: 20.02
- 6: 22.53
etc

Cumulative distribution:
- 0: 100.00
- 1: 99.99
- 2: 99.78
etcetc
