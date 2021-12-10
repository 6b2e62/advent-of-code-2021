# advent-of-code-2021
https://adventofcode.com/2021

Solutions in Python and Erlang

## Lessons learned
- python passes lists by reference, use `copy.copy()` for shallow copy (or `[:]`) or `copy.deepcopy` for deep copy
- double check datatypes when comparing numbers - e.g. `"988" > "1000"` returns true
- drawing solution helps
- with big data set, recursion is evil, undebuggable
- explore and experiment with itertools more, they reduce the complexity of the code
- apart from list comprehension, python has dictionary comprehension as well, `{ i: j for ... }` and set `{ }`
- apart from comprehensions, python also supports generator expression, e.g. `tuple(i for i in (1, 2, 3))`
- python has meta-like programming similar to ruby, e.g. `locals()`, `globals()`, or `getattr()`
- python has nice built-in set operations
- Erlang's `[97]` will be converted to `["a"]`, and `hd("a")` to `97`, watch out when taking elements from list
