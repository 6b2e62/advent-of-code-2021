from collections import defaultdict

def read_file():
  data = open('input', 'r').read().split('\n')
  first_line = data[0]
  return (first_line, data[2:])

def get_polymer_pairs(polymer):
  return [(x, y) for x, y in zip(polymer, polymer[1:])]

def build_polymer_template(pairs):
  polymer_template = {}
  for pair in pairs:
    left, right = pair.split(' -> ')
    l1, l2 = list(left)
    polymer_template[(l1, l2)] = right
  return polymer_template


polymer, pairs = read_file()
polymer = list(polymer)
polymer_template = build_polymer_template(pairs)

# Globals
letters_counter = defaultdict(int)
current_pairs = defaultdict(int)
next_pairs = defaultdict(int)

# Task 2
for letter in polymer:
  # Inc first letters of polymer - we will never use them again
  letters_counter[letter] += 1

polymer_pairs = get_polymer_pairs(polymer)
for pair in polymer_pairs:
  # Init pairs for the first loop
  current_pairs[pair] += 1

for i in range(0, 40):
  for pair, number in current_pairs.items():
    # Incr letters
    letter = polymer_template[pair]
    letters_counter[letter] += number

    # Prepare next loop
    p1, p2 = pair
    next_pairs[(p1, letter)] += number
    next_pairs[(letter, p2)] += number
  
  # Reset
  current_pairs = next_pairs
  next_pairs = defaultdict(int)

lowest = min(letters_counter.values())
highest = max(letters_counter.values())
  
print(letters_counter)
print(f'Difference: {highest - lowest}')