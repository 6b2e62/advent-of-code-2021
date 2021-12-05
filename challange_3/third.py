def read_file():
  data = open('input', 'r').read().split('\n')
  return data[:-1]

def power_consumption(data, lines_count):
  position_counter = [0 for x in data[0]]
 
  for bitstring in data:
    for i, bit in enumerate(bitstring):
      position_counter[i] += int(bit)
 
  msb = lambda n, count: '1' if (n / (count / 2) >= 1.0) else '0'
  m = [msb(n, lines_count) for n in position_counter]
 
  bitstring_msb = ''.join(m)
  bitstring_lsb = ''.join('1' if x == '0' else '0' for x in m)
  # print(bitstring_msb)
  # print(bitstring_lsb)
  msb_int = int(bitstring_msb, 2)
  lsb_int = int(bitstring_lsb, 2)
  return msb_int * lsb_int
 
def sb(data, rows_count, col, bit_type):
  bits_count = len(data[0])

  sum = 0
  for i in range(rows_count):
    sum += int(data[i][col])
  
  is_msb = sum / (rows_count / 2) >= 1.0
  if bit_type == 'msb':
    return is_msb
  else:
    return not is_msb

def filter_data(data, lines_count, col, is_msb):
  filtered = []
  for i in range(lines_count):
    if int(data[i][col]) == int(is_msb):
      filtered.append(data[i])
  return filtered

def rating(data, lines_count, rating_type):
  cols = len(data[0])
  new_data = data
  new_lines_count = lines_count
  bit_type = 'msb' if rating_type == 'oxygen' else 'lsb'
  cols = range(0, cols)
  for col in cols:
    expected_bit = sb(new_data, new_lines_count, col, bit_type)
    new_data = filter_data(new_data, new_lines_count, col, expected_bit)
    new_lines_count = len(new_data)

    if new_lines_count == 1:
      return int(new_data[0], 2)
  return int(new_data[0], 2)

  
data = read_file()
lines_count = len(data)
 
power = power_consumption(data, lines_count)
print(f'Power: {power}')

oxygen = rating(data, lines_count, 'oxygen')
scrubber = rating(data, lines_count, 'scrubber')  
print(f'Scrubber {scrubber}, Oxygen {oxygen}, result: {scrubber * oxygen}')
