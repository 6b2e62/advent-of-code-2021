def test():
  depths = [199, 200, 208, 210, 200, 207, 240, 269, 260, 263]
  ver2(depths)
  ver3(depths)
  
def read_depths():
  depths = open('input', 'r').read().split('\n')
  # :-1 to get rid of empty string in the end
  return list(map(int, depths[:-1]))

def ver1():
  count = 0
  with open('input', 'r') as f:
    previous_line = f.readline().strip()
  
    while previous_line:
      current_line = f.readline().strip()
      
      if not current_line:
        break
  
      current_number = int(current_line)
      previous_number = int(previous_line)
  
      if current_number > previous_number:
        count = count + 1
  
      previous_line = current_line
  
  print(count)

def ver2(depths = read_depths()):
  previous_depth = depths[0]
  count = 0

  for current_depth in depths[1:]:
    if current_depth > previous_depth:
      count += 1

    previous_depth = current_depth

  print(count)

def ver3(depths = read_depths()):
  previous_sum = sum(depths[0:3])
  count = 0

  for i in range(len(depths[1:]) - 1):
    current_sum = sum(depths[i : i + 3])
    if current_sum > previous_sum:
      count += 1

    previous_sum = current_sum
  print(count)

test()
ver1() # Count depths while reading the file
ver2() # Load data, then load the files - iterate through object - challange 1
ver3() # Load data, then load the files - iterate with index - challange 2
