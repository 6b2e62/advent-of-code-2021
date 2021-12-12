# advent-of-code-2021
https://adventofcode.com/2021

## Solutions in Python and Erlang

| Day | Erlang                              | Python                                 |
| --- | ----------------------------------- | -------------------------------------- |
| 1   | [day1.erl](challange_1/first.erl)   | [day1.py](challange_1/first.py)       |
| 2   | [day2.erl](challange_2/second.erl)  | [day2.py](challange_2/second.py)      |
| 3   | [day3.erl](challange_3/third.erl)   | [day3.py](challange_3/third.py)       |
| 4   | [day4.erl](challange_4/fourth.erl)  | [day4.py](challange_4/fourth.py)      |
| 5   | ---                                 | [day5.py](challange_5/fifth.py)       |
| 6   | [day6.erl](challange_6/sixth.erl)   | [day6.py](challange_6/sixth.py)       |
| 7   | [day7.erl](challange_7/seventh.erl) | [day7.py](challange_7/seventh.py)     |
| 8   | ---                                 | [day8.py](challange_8/eigth.py)       |
| 9   | ---                                 | [day9.py](challange_9/ninth.py)       |
| 10  | ---                                 | [day10.py](challange_10/tenth.py)     |
| 11  | ---                                 | [day11.py](challange_11/eleventh.py)  |
| 12  | ---                                 | ---                                   |

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
