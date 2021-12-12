## Other ideas
## itertools.product
## itertools.permutations
## However implementation would be clunky
from collections import defaultdict

def read_file():
  data = open('test_input', 'r').read().split('\n')
  data = list(filter(len, data))
  return data

def add(paths, a, b):
  # dont go back to start
  if b == 'start':
    return

  # dont go anywhere from end
  if a == 'end':
    return

  paths[a].add(b)

def build_grpah(data):
  paths = {}
  for line in data:
    a, b = line.split('-')

    # build paths bidirectional
    if a in paths:
      add(paths, a, b)

    if b in paths:
      add(paths, b, a)

    if a not in paths:
      paths[a] = set()
      add(paths, a, b)

    if b not in paths:
      paths[b] = set()
      add(paths, b, a)

  return paths

# Globals
data = read_file()
paths = build_grpah(data)
unique_paths = []
print(paths)

# Part 1 - set tolerance to 1
# Part 2 - set tolerance to 2
def can_visit(key, visited, tolerance=2):
  if key not in visited:
    return True
  # it means start || end is in visited
  if key in ['start', 'end']:
    return False
  # is this cave visited already?
  if visited[key] < tolerance:
    # is any cave visited twice?
    if any(v > 1 for v in visited.values()):
      return False
    # if is not, we can visit small cave again
    return True
  return False

# Bruteforce
def brute():
  unique_path = ['start']
  start = paths['start']

  visited = defaultdict(int)
  visited['start'] += 1

  for p in start:
    visit_vertice(p, unique_path[:], visited.copy())

def visit_vertice(key, unique_path, visited):
  unique_path.append(key)

  if key == 'end':
    unique_paths.append(unique_path)
    return

  if key.islower():
    visited[key] += 1

  if key in paths:
    for p in paths[key]:
      if can_visit(p, visited):
        visit_vertice(p, unique_path[:], visited.copy())

brute()

print(len(unique_paths))
