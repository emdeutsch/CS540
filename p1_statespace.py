# Evan Deutsch
# CS540
# September 15, 2020
def fill(state, max, which):
    state[which] = max[which]
    return state
def empty(state, max, which):
    state[which] = 0
    return state;
def xfer(state, max, source, dest):
    tempState = [state[0], state[1]]
    tempMax = [max[0], max[1]];
    state[dest] = min(tempState[dest] + tempState[source], tempMax[dest])
    state[source] = -min(-(tempState[source] - (tempMax[dest] - tempState[dest])), 0)
    return state;
def succ(state, max):
    tempState = [state[0], state[1]]
    tempMax = [max[0], max[1]];
    print(fill(state, max, 0))
    state = [tempState[0], tempState[1]]
    max = [tempMax[0], tempMax[1]]
    print(fill(state, max, 1))
    state = [tempState[0], tempState[1]]
    max = [tempMax[0], tempMax[1]]
    print(empty(state, max, 0))
    state = [tempState[0], tempState[1]]
    max = [tempMax[0], tempMax[1]]
    print(empty(state, max, 1))
    state = [tempState[0], tempState[1]]
    max = [tempMax[0], tempMax[1]]
    print(xfer(state, max, 0, 1))
    state = [tempState[0], tempState[1]]
    max = [tempMax[0], tempMax[1]]
    print(xfer(state, max, 1, 0))