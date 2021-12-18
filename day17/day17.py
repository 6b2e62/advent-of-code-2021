# x increases by x
# y increases by y
# x changes by 1, +1 if > 0, -1 if < 0, 0 if 0
# y decreases by 1

INPUT_MSG_LEN = len('target area: ')
VAR_EQUALS_LEN = len('x=')
DOTS_SEPARATOR = '..'
MSG_SEPARATOR = ', '

def read_file():
  data = open('input', 'r').read().split('\n')[0]
  data = data[INPUT_MSG_LEN:]
  x, y = data.split(MSG_SEPARATOR)
  x = x[VAR_EQUALS_LEN:].split(DOTS_SEPARATOR)
  y = y[VAR_EQUALS_LEN:].split(DOTS_SEPARATOR)
  return (
    ( int(x[0]), int(x[1]) ),
    ( int(y[0]), int(y[1]) )
  )

exp_x_pos, exp_y_pos = read_file()
print(exp_x_pos, exp_y_pos)
# x is forward
# y is upward

def missed_target(pos, target):
  ((x1, x2), (y1, y2)) = target
  cur_x, cur_y = pos
  if cur_y < y1: return True
  if cur_x > x2: return True
  return False

def hit_target(pos, target):
  ((x1, x2), (y1, y2)) = target
  cur_x, cur_y = pos
  return x1 <= cur_x <= x2 and y1 <= cur_y <= y2

# Could be further optimised
# as x won't be bigger than x2
# and y won't be smaller than y2
# thus range can be:
# for x (0, max_x) 
# for y (-min_y, min_y)
# but heuristics ftw
TIMES = 500

target = (exp_x_pos, exp_y_pos)
max_y = 0
# it would have to be set() if results are not unique
hits = 0
for start_x_vel in range(0, TIMES, 1):
  for start_y_vel in range(-TIMES, TIMES, 1):
    pos_x = 0
    pos_y = 0
    x_vel = start_x_vel
    y_vel = start_y_vel
    max_y_reached = 0
    for i in range(0, TIMES):
      # 1. update position
      pos_x += x_vel
      pos_y += y_vel

      # 2. update velocity
      if x_vel > 0: x_vel -= 1
      if x_vel < 0: x_vel += 1
      y_vel -= 1

      # Part 1
      if pos_y > max_y_reached: max_y_reached = pos_y
      if hit_target((pos_x, pos_y), target):
        # Part 2
        hits += 1
        if (max_y < max_y_reached):
          max_y = max_y_reached
          print(f'New record, pos ({pos_x}, {pos_y}), vel ({start_x_vel}, {start_y_vel}), step {i}, heigth: {max_y}')
        break

      if missed_target((pos_x, pos_y), target):
        break

print(hits)