import itertools

BOARD_SIZE = 10

def read_file():
  data = open('input', 'r').read().split('\n')
  data = [list(d) for d in data]
  for i in range(0, BOARD_SIZE):
    for j in range(0, BOARD_SIZE):
      data[i][j] = int(data[i][j])
  return data

data = read_file()

def incr_adjacent(data, x, y):
  new_to_flash = False
  for i in range(x - 1, x + 2):
    for j in range(y - 1, y + 2):
      if i > BOARD_SIZE - 1 or j > BOARD_SIZE - 1:
        continue
      if i < 0 or j < 0:
        continue
      if (i, j) == (x, y):
        continue

      if data[i][j] < 10:
        data[i][j] += 1
      if data[i][j] == 10:
        new_to_flash = True

  data[x][y] += 1
  return new_to_flash

steps = 0
flashes = 0
all_flashed_at = None
for step in range(0, 1000):
  # Incr first
  for i in range(0, BOARD_SIZE):
    for j in range(0, BOARD_SIZE):
      data[i][j] += 1

  # Adj
  flashing = True
  new_flashes = []
  while flashing:
    for i in range(0, BOARD_SIZE):
      for j in range(0, BOARD_SIZE):
        if data[i][j] == 10:
          new_to_flash = incr_adjacent(data, i, j)
          if new_to_flash:
            new_flashes.append(1)
    if len(new_flashes) == 0:
      flashing = False
    else:
      new_flashes.pop()

  # Prepare next round
  for i in range(0, BOARD_SIZE):
    for j in range(0, BOARD_SIZE):
      if data[i][j] >= 10:
        data[i][j] = 0

  # Count zeros on board
  flatten = list(itertools.chain(*data))
  zero_count = flatten.count(0)
  if zero_count == BOARD_SIZE * BOARD_SIZE and all_flashed_at == None:
    # When board is 0s only
    all_flashed_at = step + 1

  flashes += zero_count

print(flashes)
print(all_flashed_at)