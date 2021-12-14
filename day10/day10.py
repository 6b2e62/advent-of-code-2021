import statistics

def read_file():
  data = open('input', 'r').read().split('\n')
  data = list(filter(len, data))
  return data

data = read_file()

illegal_points = {
  ')': 3,
  ']': 57,
  '}': 1197,
  '>': 25137,
}

completion_points = {
  ')': 1,
  ']': 2,
  '}': 3,
  '>': 4
}

opening = '([{<'
closing = ')]}>'

def syntax_check(line):
  q = []
  for bracket in line:
    if bracket in opening:
      q.append(bracket)
    else:
      stored = q.pop()
      if opening.find(stored) != closing.find(bracket):
        return (bracket, illegal_points[bracket])

  return (None, 0)

def syntax_completion(line):
  q = []
  for bracket in line:
    if bracket in opening:
      q.append(bracket)
    else:
      stored = q.pop()

  closing_brackets = [closing[opening.find(bracket)] for bracket in q[::-1]]
  total_points = 0

  for bracket in closing_brackets:
    total_points *= 5
    total_points += completion_points[bracket]

  return (''.join(closing_brackets), total_points)

points_sum = 0
lines_to_complete = []
for line in data:
  _, points = syntax_check(line)
  points_sum += points

  if points == 0:
    lines_to_complete.append(line)
print(points_sum)

all_points = []
for line in lines_to_complete:
  _, points = syntax_completion(line)
  all_points.append(points)

print(statistics.median(all_points))
