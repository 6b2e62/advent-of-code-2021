def read_file():
  data = open('input', 'r').read().split('\n')
  data = list(map(str.strip, data))
  return data[:-1]

data = read_file()

matrix = []
for d in data:
  matrix.append(d)

col_len = len(matrix[0])
row_len = len(matrix)
print(f'Rows {row_len}, cols {col_len}')

to_check = [
  [0, -1],
  [-1, 0],
  [0, 1],
  [1, 0]
]
def is_lowest_point(matrix, i, j, row_len, col_len):
  for points in to_check:
    a, b = points
    if a + i < 0 or a + i > row_len:
      continue
    if b + j < 0 or b + j > col_len:
      continue
    if matrix[i][j] >= matrix[i + a][j + b]:
      return False
  return True

risk_level = 0
for i in range(0, row_len):
  for j in range(0, col_len):
    if is_lowest_point(matrix, i, j, row_len - 1, col_len - 1):
      risk_level += 1 + int(matrix[i][j])

# Part 1
print(risk_level)

visited = set()
blocked = set()
current_bassin = []
all_bassins_sums = []

def is_ok(matrix, i, j):
  if matrix[i][j] == '9':
    blocked.add((i, j))
    return False
  return True

def traverse_points(matrix, i, j, row_len, col_len):
  if not is_ok(matrix, i, j):
    return
  if (i, j) in blocked:
    return
  if (i, j) in visited:
    return

  visited.add((i, j))
  current_bassin.append(1)
  for points in to_check:   
    a, b = points
    if a + i < 0 or a + i > row_len:
      continue
    if b + j < 0 or b + j > col_len:
      continue

    if is_ok(matrix, a + i, b + j):
      if (a + i, b + j) in visited:
        continue
      traverse_points(matrix, a + i, b + j, row_len, col_len)
    
for i in range(0, row_len):
  for j in range(0, col_len):
    traverse_points(matrix, i, j, row_len - 1, col_len - 1)
    bassin_sum = sum(current_bassin)
    if bassin_sum != 0:
      all_bassins_sums.append(bassin_sum)
      
    current_bassin = []
     
# Part 2
sorted_bassin_sums = sorted(all_bassins_sums)
print(sorted_bassin_sums[-1] * sorted_bassin_sums[-2] * sorted_bassin_sums[-3])
