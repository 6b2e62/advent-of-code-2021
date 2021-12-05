import numpy

def read_file():
  data = open('input', 'r').read().split('\n')
  return data[:-1]

def load_data(data):
  lines = []
  size = 0
  
  for line in data:
    point_from, point_to = line.split(' -> ')
    x1, y1 = map(int, point_from.split(','))
    x2, y2 = map(int, point_to.split(','))
    size = max(x1, x2, y1, y2, size)
    lines.append([(x1, y1), (x2, y2)])

  return lines, size + 1

lines, size = load_data(read_file())
matrix = numpy.zeros((size, size), dtype=int)

for line in lines:
  (x1, y1), (x2, y2) = cord_from, cord_to = line

  x_smaller, x_bigger = min(x1, x2), max(x1, x2)
  y_smaller, y_bigger = min(y1, y2), max(y1, y2)
 
  # horizontal
  if y1 == y2:
    for i in range(x_smaller, x_bigger + 1):
      matrix[y1, i] += 1
  
  # vertical
  if x1 == x2:
    for i in range(y_smaller, y_bigger + 1):
      matrix[i, x1] += 1
  
  # diagonal
  if abs(x1 - x2) == abs(y1 - y2):
    x = y = y_sign = x_sign = None

    if x1 < x2:
      x_sign = 1
    else:
      x_sign = -1

    if y1 < y2:
      y_sign = 1
    else:
      y_sign = -1
    
    diff = abs(x1 - x2)
    for i in range(diff + 1):
      matrix[y1 + (i * y_sign), x1 + (i * x_sign)] += 1

print(matrix)
more_than_two_counter = 0
for i in range(size):
  for j in range(size):
    if matrix[i, j] >= 2:
      more_than_two_counter += 1
print(more_than_two_counter)

