# advent-of-code-2021
https://adventofcode.com/2021

## Lessons learned
- python passes lists by reference, use `copy.copy()` for shallow copy (or `[:]`) or `copy.deepcopy` for deep copy
- double check datatypes when comparing numbers - e.g. `"988" > "1000"` returns true
- drawing solution helps
- with big data set, recursion is evil, undebuggable
