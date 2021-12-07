import copy

def read_file(): 
    data = open('input', 'r').read().split(',')
    data = list(map(str.strip, data))
    data = list(map(int, data))
    return data

def estimate_population_slow(initial_state, n):
    current_state = copy.copy(initial_state)
    current_length = len(current_state)

    for i in range(1, n + 1):
        for s_i in range(current_length):
            if current_state[s_i] == 0:
                current_state.append(8)
                current_state[s_i] = 6
                current_length += 1
            else:
                current_state[s_i] -= 1
    print(len(current_state))


def estimate_population_fast(initial_state, n):
    estimates = {
        8: 0,
        7: 0,
        6: 0,
        5: 0,
        4: 0,
        3: 0,
        2: 0,
        1: 0,
        0: 0
    }

    for state in initial_state:
        estimates[state] += 1

    for i in range(1, n + 1):
        estimates_copy = copy.copy(estimates)
        for key in estimates.keys():
            if key == 0:
                estimates[8] = estimates_copy[0]
                estimates[6] += estimates_copy[0]
            else:
                estimates[key - 1] = estimates_copy[key]
    print(sum(estimates.values()))

initial_state = read_file()
estimate_population_slow(initial_state, 80)
estimate_population_fast(initial_state, 256)


