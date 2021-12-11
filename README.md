# advent-of-code-2021
https://adventofcode.com/2021

Solutions in Python and Erlang

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

