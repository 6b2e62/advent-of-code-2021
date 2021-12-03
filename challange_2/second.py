def read_file():
  data = open('input', 'r').read().split('\n')
  # :-1 to get rid of empty string in the end
  data = [d.split() for d in data[:-1]]
  return data

def ver1(data):
  current_position = {
    'depth': 0,
    'horizontal': 0
  }
  for key, value in data:
    value = int(value)
  
    direction, depth = {
      'forward': lambda val: ['horizontal', val],
      'up': lambda val: ['depth', -val],
      'down': lambda val: ['depth', val]
    }[key](value)
  
    current_position[direction] += depth
  
  result = current_position['depth'] * current_position['horizontal']
  print(result)

def ver2(data):
  current_position = {
    'depth': 0,
    'horizontal': 0,
    'aim': 0
  }
  for key, value in data:
    value = int(value)

    if key == 'forward':
      current_position['horizontal'] += value
      current_position['depth'] += (value * current_position['aim'])
    elif key == 'up':
      current_position['aim'] -= value
    elif key == 'down':
      current_position['aim'] += value

  result = current_position['depth'] * current_position['horizontal']
  print(result)

def ver3(data) -> int:
  F: str = 'forward'
  U: str = 'up'
  D: str = 'down'
  d: int = 0
  h: int = 0
  a: int = 0
  for key, value in data:
    v = int(value)
    h, d, a = {
      F: lambda v, h, d, a: [h + v, d + (v * a), a    ],
      U: lambda v, h, d, a: [h    , d          , a - v],
      D: lambda v, h, d, a: [h    , d          , a + v]
    }[key](v, h, d, a)
  r = h * d
  print(r)
  return r

data = read_file()
ver1(data)
ver2(data)
ver3(data) # look how they massacred my boy
