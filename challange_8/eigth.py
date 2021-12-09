from collections import defaultdict

def read_file():
  data = open('input', 'r').read().split('\n')
  data = list(map(str.strip, data))

  data_formatted = []
  for line in data:
    if not line:
      continue
    [signals, sum_of_signals] = line.split(' | ')
    data_formatted.append((signals, sum_of_signals))
  return data_formatted

def count_easy_digits(data):
  easy_digits_count = 0
  for (signals, sum_of_signals) in data:
    sum_of_signals_digits = sum_of_signals.split(' ')
    for sum_of_signals_digit in sum_of_signals_digits:
      if digits_map[len(sum_of_signals_digit)] != 0:
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
def signal_decoder(easy_digits_map, signal_digits):
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
  # Take "1"; "6" misses one letter => "6"
  # Take "1"; "7" define TOP letter => "7"
  # Take "4"; ("0" and "9" are left), "0" misses one letter => "0"
  # Other length 6 is "9" => "9"
  # Take "1", "3" contains both letters => "3"
  # Take "6", one letter difference with "5" => "5"
  # The last one is "2"
  hard_digits_5_len = signal_digits[0:3]
  hard_digits_6_len = signal_digits[3:6]
  digit_1 = easy_digits_map[1]
  digit_4 = easy_digits_map[4]
  digit_7 = easy_digits_map[7]
  digit_8 = easy_digits_map[8]
  digit_6 = digit_0 = digit_9 = digit_5 = digit_2 = digit_3 = None

  for digit in hard_digits_6_len:
    if (are_letters_in_str(list(digit_1), digit) == True):
      continue
    digit_6 = digit
  hard_digits_6_len.remove(digit_6)
      
  top = list(set(digit_1) & set(digit_7))[0]
 
  for digit in hard_digits_6_len:
    diff = list(set(digit_4) - set(digit))
    if len(diff) == 1:
      digit_0 = digit
    else:
      digit_9 = digit

  for digit in hard_digits_5_len:
    if (are_letters_in_str(list(digit_1), digit) == True):
      digit_3 = digit
  hard_digits_5_len.remove(digit_3)

  for digit in hard_digits_5_len:
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

def sum_of_signals(data):
  ouput_values = []
  for (signals, sum_of_signals) in data:
    sum_of_signals_digits = list(filter(len, sum_of_signals.split(' ')))
    signal_digits = list(filter(len, signals.split(' '))) 
    signal_digits.sort(key = len)
    
    digit_1 = signal_digits[0]
    digit_7 = signal_digits[1]
    digit_4 = signal_digits[2]
    digit_8 = signal_digits[9]

    easy_digits_map = { 1: digit_1, 4: digit_4, 7: digit_7, 8: digit_8 }
    hard_digits = signal_digits[3:-1]

    signal_to_digit_map = signal_decoder(easy_digits_map, hard_digits)
    number = []
    for signal in sum_of_signals_digits:
      signal_sorted = sort_chars(signal)
      digit = signal_to_digit_map[signal_sorted]
      number.append(str(digit))
    ouput_values.append(''.join(number))
  return sum(map(int, ouput_values))

# Short solutions
def q1(data):
  counter = 0
  for line in data:
    _, right = line
    signals = right.split(' ')
    for i in signals: 
      if len(i) in [2, 3, 4, 7]:
        counter += 1
  return counter

from itertools import permutations
iterate = ['abcefg', 'cf', 'acdeg', 'acdfg', 'bcdf', 'abdfg', 'abdefg', 'acf', 'abcdefg', 'abcdfg']
# 0, 1, ..., 9

def q2(line):
  left, right = line
  all_letters = 'abcdefg'
  iterate_set = set(iterate)
  for p in permutations(all_letters):
    letter_p = { i: j for i, j in zip(p, all_letters) }
    left_p = { ''.join(sorted(map(letter_p.get, signal_p))) for signal_p in left.split() }
    if left_p == iterate_set:
      right_p = [''.join(sorted(map(letter_p.get, output_p))) for output_p in right.split()]
      return int(''.join(str(iterate.index(i)) for i in right_p))
      

data = read_file()
print(count_easy_digits(data))
print(q1(data))
print(sum_of_signals(data))

s = 0
for line in data:
  s += q2(line)

print(s)
