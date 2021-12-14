import numpy as np

def read_file():
  data = open('input', 'r').read().split('\n')
  for i in range(0, len(data)):
    if len(data[i]) == 0:
      return data[0:i], data[i+1:]

def build_arr(dots):
  max_x = 0
  max_y = 0

  for dot in dots:
    y, x = dot.split(',')
    y = int(y)
    x = int(x)

    if x > max_x:
      max_x = x
    if y > max_y:
      max_y = y
  
  return np.zeros((max_x + 1, max_y + 1), dtype=int)

def fill_arr(dots, arr2d):
  for dot in dots:
    y, x = dot.split(',')
    y = int(y)
    x = int(x)
    arr2d[x, y] = 1

def fold_arr_along_x(fold, arr2d):
  rows, cols = arr2d.shape
  new_arr2d = np.zeros((fold, cols), dtype=int)

  for x in range(0, fold):
    for y in range(0, cols):
      new_arr2d[x, y] = arr2d[x, y]
  
  for x in range(fold + 1, rows):
    for y in range(0, cols):
      if arr2d[x, y] == 1:
        new_arr2d[rows - x - 1, y] = 1

  return new_arr2d

def fold_arr_along_y(fold, arr2d):
  rows, cols = arr2d.shape
  new_arr2d = np.zeros((rows, fold), dtype=int)

  for x in range(0, rows):
    for y in range(0, fold):
      new_arr2d[x, y] = arr2d[x, y]

  for x in range(0, rows):
    for y in range(fold + 1, cols):
      if arr2d[x, y] == 1:
        new_arr2d[x, cols - y - 1] = 1

  return new_arr2d

def fold_arr(folds, arr2d):
  for i, fold in enumerate(folds):
    fold_how, fold_val = fold.split("=")
    new_arr2d = fold_arr_once(fold, arr2d.copy(), fold_how, fold_val)
    arr2d = new_arr2d

    print(f'Fold {i}: {count_ones(arr2d)}')
  return arr2d

def fold_arr_once(fold, arr2d, fold_how, fold_val):
  if fold_how == "fold along y":
    return fold_arr_along_x(int(fold_val), arr2d)
  else:
    return fold_arr_along_y(int(fold_val), arr2d)

def count_ones(arr2d):
  counter = 0
  for x, y in np.ndindex(arr2d.shape):
    counter += arr2d[x, y]

  return counter

# Read
dots, folds = read_file()

# New matrix
arr2d = build_arr(dots)

# Changed via reference
fill_arr(dots, arr2d)
folded_arr2d = fold_arr(folds, arr2d)

# Print nicely
for x, y in np.ndindex(folded_arr2d.shape):
  if y == 0:
    print('')
  val = folded_arr2d[x, y]
  if val == 0:
    print(' ', end='')
  else:
    print('#', end='')

# Notes
## 1
# Couldn't make numpy's resize & reshape to work thus decided
# resize manipulated the data, reshape requires specific shape
# to create new arr, thus ended with n * 2(n^2) for readability

## 2
# the task description has x and y inverted
# thus "fold along y" is reflected in code as "fold along x"