"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """

    n = 1
    for i in range(3):
        for j in range(3):
            if board[i][j] != EMPTY:
                n = n + 1
    if n%2 == 0:
        return O
    else:
        return X

    
def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    
    actions_set = set()

    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                actions_set.add((i,j))
                
    return actions_set


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    i = action[0]
    j = action[1]

    if board[i][j] != EMPTY:
        print(i,j,board)
        raise ActionNotValid
    else:
        new_board = deepcopy(board)
        new_board[i][j] = player(board)

    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    # checking if rows have same value
    for i in range(3):
        for j in range(1):
            if board[i][j] == board[i][j+1] and board[i][j+1] == board[i][j+2]:
                if board[i][j] == X:
                    return X
                elif board[i][j] == O:
                    return O

    # checking if columns have same value
    for i in range(1):
        for j in range(3):
            if board[i][j] == board[i+1][j] and board[i+1][j] == board[i+2][j]:
                if board[i][j] == X:
                    return X
                elif board[i][j] == O:
                    return O

    # checking if the NW-SE diagonal has same value
    if board[0][0] == board[1][1] and board[1][1] == board[2][2]:
        if board[0][0] == X:
            return X
        elif board[0][0] == O:
            return O
     
    # checking if SW-NE diagonal has same value
    if board[0][2] == board[1][1] and board[1][1] == board[2][0]:
        if board[1][1] == X:
            return X
        elif board[1][1] == O:
            return O

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    check_win = winner(board)

    if check_win is None:
        for i in range(3):
            for j in range(3):
                if board[i][j] == EMPTY:
                    return False
        return True
    else:
        return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    won = winner(board)

    if won == X:
        return 1
    elif won == O:
        return -1
    else: # as this function is called only if terminal(board) is True
        return 0

def maxvalue(board):

    if terminal(board):
        return utility(board)

    max_value = float("-inf")

    for action in actions(board):
        max_value = max(max_value, minvalue(result(board, action)))
        
    return max_value

def minvalue(board):

    min_value = float("inf")

    if terminal(board):
        return utility(board)
    
    for action in actions(board):
        min_value = min(min_value, maxvalue(result(board, action)))
        
    return min_value


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    if player(board) == X:
        opt_value = float("-inf")
    else:
        opt_value = float("inf")

    for action in actions(board):
        if player(board) == X:
            value = minvalue(result(board,action))
            if value > opt_value:
                opt_value = value
                opt_action = action
        else:
            value = maxvalue(result(board,action))
            if value < opt_value:
                opt_value = value
                opt_action = action
    
    return opt_action
