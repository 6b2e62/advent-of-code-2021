# advent-of-code-2021
https://adventofcode.com/2021

## Solutions in Python and Erlang
By day:
- day 1
  - [day1.erl](day1/day1.erl)
  - [day1.py](day1/day1.py)
- day 2
  - [day2.erl](day2/day2.erl)
  - [day2.py](day2/day2.py)
- day 3
  - [day3.erl](day3/day3.erl)
  - [day3.py](day3/day3.py)
- day 4
  - [day4.erl](day4/day4.erl) - trying to work on arrays in erlang doesn't end up well
  - [day4_simplified.erl](day4/day4_simplified.erl) - simplified
  - [day4.py](day4/day4.py)
- day 5
  - Erlang - TBD
  - [day5.py](day5/day5.py)
- day 6
  - [day6.erl](day6/day6.erl)
  - [day6.py](day6/day6.py)
- day 7
  - [day7.erl](day7/day7.erl)
  - [day7.py](day7/day7.py)
- day 8
  - Erlang - TBD
  - [day8.py](day8/day8.py)
- day 9
  - Erlang - TBD
  - [day9.py](day9/day9.py)
- day 10
  - [day10.erl](day10/day10.erl)
  - [day10.py](day10/day10.py)
- day 11
  - Erlang - TBD
  - [day11.py](day11/day11.py)
- day 12
  - [day12.erl](day12/day12.erl)
  - [day12.py](day12/day12.py)
- day 13
  - Erlang - TBD
  - [day13.py](day13/day13.py) - heavy version, numpy array used
  - [day13_simplified.pyl](day13/day13_simplified.py) - lightweigth, set based
- day 14
  - Erlang - TBD
  - [day14_p1.py](day14/day14_p1.py) - part 1
  - [day14_p2.py](day14/day14_p2.py) - part 2
  - [day14_linkedlist.py](day14/day14_linkedlist.py) - attempt to use linked lists, it was a bad idea
- day 15
  - [day15_bruteforce.py](day15/day15_bruteforce.py)
  - [day15_optimal.py](day15/day_optimal.py)
- day 16
  - [day16_iterative.py](day16/day16_iterative.py) - only part 1, part 2 is hard, brackets have to match perfectly
  - [day16_recursive.py](day16/day16_recursive.py)
- day 17
  - [day17.py](day17/day17.py)
- day 18
  - [day18.py](day18/day18.py)
- day 19
- day 20
- day 21
- day 22
- day 23
- day 24


## Lessons learned
- Python: passes lists by reference, use `copy.copy()` for shallow copy (or `[:]`) or `copy.deepcopy` for deep copy
- General: double check datatypes when comparing numbers - e.g. `"988" > "1000"` returns true
- General: drawing solution helps
- General: with big data set, recursion is evil, undebuggable
- Python: explore and experiment with itertools more, they reduce the complexity of the code
- Python: apart from list comprehension, has dictionary comprehension as well, `{ i: j for ... }` and set `{ }`
- Python: apart from comprehensions, also supports generator expression, e.g. `tuple(i for i in (1, 2, 3))`
- Python: has meta-like programming similar to ruby, e.g. `locals()`, `globals()`, or `getattr()`
- Python: has nice built-in set operations
- Erlang: `[97]` will be converted to `["a"]`, and `hd("a")` to `97`, watch out when taking elements from list
- Python: nice shorthand for checking adjacent elements in 2d array
```python
for i in ...
  for j in ...
    for x, y in [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]:
```
- Erlang: has ETS (bult-in term storage), that can be used like a global variable (store)
- Erlang: Digraphs are based on ETS, thus there's no need to return updated object after modification
- Erlang: when program performance is dead slow analyze lists usage, copying big lists, appending list via ets:insert is extremely slow
- General: When task hints to "count", there's probably a fast way to do it, avoid storing data if not necessary. Copying or storing big chunks of data is slow and will most probably result in OOM. 
