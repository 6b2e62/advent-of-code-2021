import statistics

def read_file():
  data = open('input', 'r').read().split(',')
  data = list(map(str.strip, data))
  data = list(map(int, data))
  return data

def fuel_1(values, med):
  fuel_sum = 0
  for val in values:
    fuel_sum += abs(val - med)
  return fuel_sum

def fuel_2(values, med):
  fuel_sum = 0
  for val in values:
    fuel_sum += triangle_number(abs(val - med))
  return fuel_sum

def triangle_number(n):
  sum = 0
  for i in range(1, n + 1):
    sum += i
  return sum

input_data = read_file()

med = int(statistics.median(input_data))
avg = int(sum(input_data) / len(input_data))

lowest_fuel_1 = min([fuel_1(input_data, med), fuel_1(input_data, med - 1), fuel_1(input_data, med + 1)])
lowest_fuel_2 = min([fuel_2(input_data, avg), fuel_2(input_data, avg - 1), fuel_2(input_data, avg + 1)])

print(lowest_fuel_1, lowest_fuel_2)
