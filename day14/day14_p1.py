def read_file():
  data = open('test_input', 'r').read().split('\n')
  first_line = data[0]
  return (first_line, data[2:])

def get_polymer_pairs(polymer):
  return [(x, y) for x, y in zip(polymer, polymer[1:])]

def apply_template(polymer_pairs, polymer_template):
  new_polymer = []
  (x, _) = polymer_pairs[0]
  new_polymer.append(x)

  for (x, y) in polymer_pairs:
    new_polymer.append(polymer_template[x + y])
    new_polymer.append(y)

  return new_polymer

def min_max_elements(polymer):
  unique_letters = set(polymer)
  most_common_letter = None
  most_common_counter = 0
  least_common_letter = None
  least_common_counter = len(polymer)

  for letter in sorted(unique_letters):
    count = polymer.count(letter)
    
    if count > most_common_counter:
      most_common_letter = letter
      most_common_counter = count

    if count < least_common_counter:
      least_common_letter = letter
      least_common_counter = count

  max_elements = (most_common_letter, most_common_counter)
  min_elements = (least_common_letter, least_common_counter)
  return (min_elements, max_elements)

def build_polymer_template(pairs):
  polymer_template = {}
  for pair in pairs:
    left, right = pair.split(' -> ')
    polymer_template[left] = right
  return polymer_template

def part_1(new_polymer, new_polymer_pairs, polymer_template):
  for step in range(1, 10):
    print(step)
    new_polymer_pairs = get_polymer_pairs(new_polymer)
    new_polymer = apply_template(new_polymer_pairs, polymer_template)

  ((least_letter, least_number), (most_letter, most_number)) = min_max_elements(new_polymer)
  print(f'{most_letter}: {most_number}, {least_letter}: {least_number} = {most_number - least_number}')

# Read
polymer, pairs = read_file()

# Tasks
polymer = list(polymer)
polymer_template = build_polymer_template(pairs)
polymer_pairs = get_polymer_pairs(polymer)

# Task 1
part_1(polymer.copy(), polymer_pairs, polymer_template)

  


