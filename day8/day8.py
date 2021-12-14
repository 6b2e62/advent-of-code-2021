from collections import defaultdict

def read_file():
  data = open('input', 'r').read().split('\n')
  data = list(map(str.strip, data))
  data_formatted = []

  for line in data:
    if not line:
      continue

    signals = line.split(' | ')
    data_formatted.append(signals)

  return data_formatted

def count_easy_digits(data):
  easy_digits_count = 0
  for (_, output_signal) in data:
    output_signal = output_signal.split(' ')

    for signal in output_signal:
      if digits_map[len(signal)] != 0:
        easy_digits_count += 1

  return easy_digits_count

def zero():
    return 0

digits_map = defaultdict(zero)
digits_map[2] = 1
digits_map[4] = 4
digits_map[3] = 7
digits_map[7] = 8

def easy_digits_map(digits_count):
  return digits_map[digits_count]

def are_letters_in_str(letters, string):
  for letter in letters:
    if not letter in string:
      return False

  return True

# Execution time oriented solution
def signal_decoder(digits_map, signal):
  #    0:      1:      2:      3:      4:
  #  aaaa    ....    aaaa    aaaa    ....
  # b    c  .    c  .    c  .    c  b    c
  # b    c  .    c  .    c  .    c  b    c
  #  ....    ....    dddd    dddd    dddd
  # e    f  .    f  e    .  .    f  .    f
  # e    f  .    f  e    .  .    f  .    f
  #  gggg    ....    gggg    gggg    ....
  # 
  #   5:      6:      7:      8:      9:
  #  aaaa    aaaa    aaaa    aaaa    aaaa
  # b    .  b    .  .    c  b    c  b    c
  # b    .  b    .  .    c  b    c  b    c
  #  dddd    dddd    ....    dddd    dddd
  # .    f  e    f  .    f  e    f  .    f
  # .    f  e    f  .    f  e    f  .    f
  #  gggg    gggg    ....    gggg    gggg

  # 0, 6, 9 -> len 6;
  # 2, 3, 5 -> len 5;
  # 1 -> len 2;
  # 4 -> len 4;
  # 7 -> len 3;
  # 8 -> len 7;

  ## Algorithm
  # Find "8" is unique length
  # Find "1" is unique length
  # Find "4" is unique length
  # Find "7" is unique length
  ## Then
  # Take "1"; "6" misses one letter => deduced "6", remove 6 from array
  # Take "1"; "7" has TOP letter => deduced "7"
  # Take "4"; ("0" and "9" are left), "0" misses one letter => deduced "0", remove 0 from array
  # Length 6 array "9" is left => deduced "9"
  # Take "1", "3" contains both letters => deduced "3"
  # Take "6", one letter difference from "5" => deduced "5"
  # The last one is "2"
  hard_digits_5 = signal[0:3]
  hard_digits_6 = signal[3:6]
  digit_1 = digits_map[1]
  digit_4 = digits_map[4]
  digit_7 = digits_map[7]
  digit_8 = digits_map[8]
  digit_6 = digit_0 = digit_9 = digit_5 = digit_2 = digit_3 = None

  for digit in hard_digits_6:
    if are_letters_in_str(list(digit_1), digit) == True:
      continue
    digit_6 = digit
  hard_digits_6.remove(digit_6)
      
  top = list(set(digit_1) & set(digit_7))[0]
 
  for digit in hard_digits_6:
    diff = list(set(digit_4) - set(digit))
    if len(diff) == 1:
      digit_0 = digit
    else:
      digit_9 = digit

  for digit in hard_digits_5:
    if are_letters_in_str(list(digit_1), digit) == True:
      digit_3 = digit
  hard_digits_5.remove(digit_3)

  for digit in hard_digits_5:
    diff = list(set(digit_6) - set(digit))
    if len(diff) == 1:
      digit_5 = digit
    else:
      digit_2 = digit

  digits_map = {}
  for i in range(0, 10):
    sorted_chars = sort_chars(locals()[f'digit_{i}'])
    digits_map[''.join(sorted_chars)] = i

  return digits_map

def sort_chars(chars):
  sorted_chars = list(chars)
  sorted_chars.sort(key = ord)
  return ''.join(sorted_chars)

def signal_sum(data):
  ouput_values = []
  for (input_signal, output_signal) in data:
    output_signal = list(filter(len, output_signal.split(' ')))
    input_signal = list(filter(len, input_signal.split(' '))) 
    input_signal.sort(key = len)
    
    digit_1 = input_signal[0]
    digit_7 = input_signal[1]
    digit_4 = input_signal[2]
    digit_8 = input_signal[9]

    easy_digits_map = { 1: digit_1, 4: digit_4, 7: digit_7, 8: digit_8 }
    hard_digits = input_signal[3:-1]

    signal_to_digit_map = signal_decoder(easy_digits_map, hard_digits)

    number = []
    for signal in output_signal:
      signal_sorted = sort_chars(signal)
      digit = signal_to_digit_map[signal_sorted]
      number.append(str(digit))
    ouput_values.append(''.join(number))
  return sum(map(int, ouput_values))

# Short solutions
def q1(line):
  s = 0
  _, right = line
  signals = right.split(' ')
  for signal in signals: 
    if len(signal) in [2, 3, 4, 7]:
      s += 1
  return s

from itertools import permutations
# 0, 1, ..., 9
iterate = ['abcefg', 'cf', 'acdeg', 'acdfg', 'bcdf', 'abdfg', 'abdefg', 'acf', 'abcdefg', 'abcdfg']

all_letters = 'abcdefg'
def q2(line):
  left, right = line
  iterate_set = set(iterate)
  for p in permutations(all_letters):
    letter_p = { i: j for i, j in zip(p, all_letters) }
    left_p = { ''.join(sorted(map(letter_p.get, signal_p))) for signal_p in left.split() }
    if left_p == iterate_set:
      right_p = [''.join(sorted(map(letter_p.get, output_p))) for output_p in right.split()]
      return int(''.join(str(iterate.index(i)) for i in right_p))
      

data = read_file()
print(count_easy_digits(data), signal_sum(data))

s1 = s2 = 0
for line in data:
  s1 += q1(line)
  s2 += q2(line)

print(s1, s2)
