import numpy as np

board = np.array([["_","_","_"],["_","_","_"],["_","_","_"]])

INFINITE = float("inf")

nodes_visited = 1

def utility(state):
    #Zeilenweise
    for row in state:
        if row[0] == row[1] == row[2] and row[0] != "_":
            return check_player(row[0])
    #Spaltenweise
    for col in state.T:
        if col[0] == col[1] == col[2] and col[0] != "_":
            return check_player(col[0])
    #Diagonal
    state_diag = np.diag(state)
    if state_diag[0] == state_diag[1] == state_diag[2] and state_diag[0] != "_":
        return check_player(state_diag[0])
    state_flip = np.diag(np.fliplr(state))
    if state_flip[0] == state_flip[1] == state_flip[2] and state_flip[0] != "_":
        return check_player(state_flip[0])
    return 0

def check_player(value):
    if value == "X":
        return 1
    if value == "O":
        return -1
    return 0

def terminal_test(state):
    if utility(state) != 0:
        return True
    for row in state:
        for col in row:
            if col == "_":
                return False
    return True

def successors(state, value):
    successors_list = []
    for i in range(3):
        for j in range(3):
            if state[i][j] == "_":
                new_state = np.copy(state)
                new_state[i][j] = value
                successors_list.append(((i, j), new_state))
    return successors_list

def max_value(state):
    global INFINITE
    global nodes_visited
    nodes_visited += 1

    if terminal_test(state):
        u = utility(state)
        return u

    v = -INFINITE
    for (a, s) in successors(state, "X"):
        v = max(v, min_value(s))
    return v

def min_value(state):
    global INFINITE
    global nodes_visited
    nodes_visited += 1

    if terminal_test(state):
        u = utility(state)
        return u

    v = +INFINITE
    for (a, s) in successors(state, "O"):
        v = min(v, max_value(s))
    return v

def minimax(state):
    global INFINITE
    (val, action) = (-INFINITE, None)
    for (a, s) in successors(state, "X"):
        v = min_value(s)
        if val <= v:
            val, action = v, a
    return action

def main():
    move = minimax(board)
    print("Start Bord:\n", board)
    print("Bester Zug für Max:", move)
    print("Anzahl besuchter Knoten:", nodes_visited)

if __name__ == '__main__':
    main()