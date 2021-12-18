import math

def read_file():
  data = open('input', 'r').read().split('\n')
  return data[0]

hex_data = read_file()
# without leading 0s
# bin_int = bin(int(hex_data, 16))[2:]

# with leading 0s
bin_int = ''.join(bin(int(char, 16))[2:].zfill(4) for char in hex_data)

limit = math.inf
index = 0
version_sum = 0
stack = []

to_drop = []
while index < len(bin_int) or index < limit:
  # It needs at least (6) + (1 or 5) to start next iteration
  if index >= len(bin_int) - 7: break

  dropped = len(to_drop)
  if dropped:
    stack.append(to_drop.pop())

  p_ver = int(bin_int[index : index + 3], 2)
  version_sum += p_ver
  index += 3

  p_id = int(bin_int[index: index + 3], 2)
  index += 3

  # Operator packet
  if p_id != 4:
    can_close_bracket = False
    p_id_len = int(bin_int[index : index + 1], 2)
    index += 1

    if p_id_len == 1:
      p_sub_p_count = int(bin_int[index : index + 11], 2)
      index += 11
    else:
      p_sub_len = int(bin_int[index : index + 15], 2)
      index += 15
      limit = index + p_sub_len
  else:
    end_of_literal_group = False
    bin_number = ''
    while not end_of_literal_group:
      five_bits = bin_int[index : index + 5]
      index += 5
      bin_number += five_bits[1 : 1 + 4]
      if five_bits[0] == '0':
        end_of_literal_group = True
    to_drop.append(int(bin_number, 2))

print("Version sum is", version_sum)