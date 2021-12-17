import time
import math
import sys

sys.setrecursionlimit(5000)

def read_file():
  data = open('test_input', 'r').read().split('\n')
  return data

data = read_file()
arr2d = []
for line in data:
  numbers = [int(i) for i in line]
  arr2d.append(numbers)

visited = set()

x_boundary = len(data) - 1
y_boundary = len(data[0]) - 1

min_path_length = math.inf
min_path_every_n = {}
min_dist_every_n = {}

TOLERANCE = 4
DIST_ERROR = 8
SCORE_ERROR = 8
LOWEST_KNOWN = 700

for i in range(TOLERANCE, (x_boundary + 1) * (y_boundary + 1), TOLERANCE):
  min_path_every_n[i] = math.inf
  min_dist_every_n[i] = math.inf

begin = (0, 0)
end = (x_boundary, y_boundary)

def arr2d_at(arr2d, at):
  i, j = at
  if i < 0 or i > x_boundary:
    return None

  if j < 0 or j > y_boundary:
    return None

  return arr2d[i][j]

it = 0

def path(arr2d, i, j, visited, score, step):
  global it
  global min_path_length
  it += 1

  if (i, j) in visited:
    return
  
  visited.add((i, j))

  if i < 0 or i > x_boundary:
    return
  if j < 0 or j > y_boundary:
    return
  
  score += arr2d[i][j]

  if step % TOLERANCE == 0:
    distance = (x_boundary - i) + (y_boundary - j)
    if score > min_path_every_n[step] and distance > min_dist_every_n[step]:
      return

    if score > min_path_every_n[step] + SCORE_ERROR:
      return

    if distance > min_dist_every_n[step] + DIST_ERROR:
      return

    if distance < min_dist_every_n[step]:
      min_dist_every_n[step] = distance

    if score < min_path_every_n[step]:
      min_path_every_n[step] = score

  if score > min_path_length:
    return

  if score > LOWEST_KNOWN:
    return

  if (i, j) == end:
    if score < min_path_length:
      min_path_length = score
    return

  down = (i + 1, j)
  right = (i, j + 1)
  left = (i, j - 1)
  top = (i - 1, j)

  values = [(arr2d_at(arr2d, pos), pos) for pos in [down, right, left, top]]
  values = sorted([(val, pos) for (val, pos) in values if val != None and pos not in visited])
  values = values[0:2]

  # values = list(filter(None.__ne__, values))
  for _val, (x, y) in values:
    path(arr2d, x, y, visited.copy(), score, step + 1)

path(arr2d, 0, 0, visited.copy(), -1 * arr2d[0][0], 1)

# About this solution
# 1. it's too slow
# 2. it can be faster, but then it's very innacurate
# 3. execution time could take days if we want it to be extremely accurate
# 4. Tolerance and distance can be adjusted to a specific data set
# It's bad in general
print(min_path_every_n)
print(min_path_length)
print(it)
