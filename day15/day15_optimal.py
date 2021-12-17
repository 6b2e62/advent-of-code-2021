def read_file():
  data = open('input', 'r').read().split('\n')
  return data

data = read_file()

# = 1 - Part 1
# = 5 - Part 2
MULTIPLY_GRID  = 5

arr2d = [list(map(int, line)) * MULTIPLY_GRID for line in data * MULTIPLY_GRID]
bound_x = len(arr2d) - 1
bound_y = len(arr2d[0]) - 1

end = (bound_x, bound_y)
init = (0, 0, 0)
visited = [[0] * len(row) * MULTIPLY_GRID for row in arr2d * MULTIPLY_GRID]

# Instead using list
# heapq structure would be better, as it will automatically sort the data for us 
# heapq.heappush
# heapq.heappop
to_visit = [init]

tile_size = int(len(arr2d) / MULTIPLY_GRID)
for i in range(0, len(arr2d)):
  for j in range(0, len(arr2d[0])):
    if i < tile_size and j < tile_size: continue
    inc = (i // tile_size) + (j // tile_size)
    new_val = (arr2d[i][j] + inc)
    add_one = 1 if new_val >= 10 else 0
    arr2d[i][j] = new_val % 10 + add_one
    if arr2d[i][j] == 10:
      print(arr2d[i][j])

# sanity check
print(arr2d[tile_size - 1][tile_size - 1])
print(arr2d[2 * tile_size - 1][2 * tile_size - 1])
print(arr2d[3 * tile_size - 1][3 * tile_size - 1])
print(arr2d[4 * tile_size - 1][4 * tile_size - 1])
print(arr2d[5 * tile_size - 1][5 * tile_size - 1])

# lesson learned
# it doesn't update to_visit via reference
# sorted(to_visit, reverse=True).pop()

while True:
  to_visit.sort(reverse = True)
  val, x, y = to_visit.pop()

  if visited[x][y]: continue
  if (x, y) == end:
    print(f'x {x}, y {y} = {val}')
    break

  visited[x][y] = 1

  for xi, yj in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
    if xi < 0 or yj < 0 or xi > bound_x or yj > bound_y: continue
    if visited[xi][yj]: continue

    to_visit.append((val + arr2d[xi][yj], xi, yj))


