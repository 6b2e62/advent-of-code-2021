def read_file():
  data = open('input', 'r').read().split('\n')
  for i in range(0, len(data)):
    if len(data[i]) == 0:
      return data[0:i], data[i+1:]

dots, folds = read_file()

def fold_x(x, dot):
  if dot[0] > x:
    diff = dot[0] - x
    return (x - diff, dot[1])
  return dot

def fold_y(y, dot):
  if dot[1] > y:
    diff = dot[1] - y
    return (dot[0], y - diff)
  return dot

## Alternative solution, hash based
dots = [dot.split(',') for dot in dots]
dots = { (int(x), int(y)) for x, y in dots }

for fold in folds:
  type, val = fold.split('=')
  val = int(val)

  if type == 'fold along x':
    dots = { fold_x(val, dot) for dot in dots }
  else:
    dots = { fold_y(val, dot) for dot in dots }

  print(len(dots))