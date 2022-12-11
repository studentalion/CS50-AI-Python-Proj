"""
Tic Tac Toe Player
"""

import math
import copy

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
    cntx = 0
    cnto = 0
    for i in range(3):
        for j in range(3):
            if board[i][j]==X:
                cntx+=1
            elif board[i][j]==O:
                cnto+=1
    if cntx > cnto:
        return O
    else:
        return X

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    action = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                action.add((i,j))
    return action

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    newboard = copy.deepcopy(board)

    if player(board) == X:
        flag = X
    else:
        flag = O
    
    i = action[0]
    j = action[1]

    if newboard[i][j] == EMPTY:
        newboard[i][j] = flag
    else:
        raise ValueError

    return newboard

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2]:
            if board[i][0] == X:
                return X
            elif board[i][0] == O:
                return O
        if board[0][i] == board[1][i] == board[2][i]:
            if board[0][i] == X:
                return X
            elif board[0][i] == O:
                return O
    
    if board[0][0] == board[1][1] == board[2][2]:
        if board[0][0] == X:
            return X
        elif board[0][0] == O:
            return O
        
    if board[0][2] == board[1][1] == board[2][0]:
        if board[0][2] == X:
            return X
        elif board[0][2] == O:
            return O


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board)==X or winner(board)==O:
        return True
    else:
        for i in range(3):
            for j in range(3):
                if board[i][j] == EMPTY:
                    return False
    return True

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    best_action = ()

    if player(board) is X:
        curr_score = float('-inf')
        for action in actions(board):
            score = Minval(result(board,action))
            if score > curr_score:
                curr_score = score
                best_action = action
    elif player(board) is O:
        curr_score = float('inf')
        for action in actions(board):
            score = Maxval(result(board,action))
            if score < curr_score:
                curr_score = score
                best_action = action
    return best_action

def Maxval(board):
    v = float('-inf')
    if terminal(board):
        return utility(board)
    
    for action in actions(board):
        v = max(v,Minval(result(board,action)))
        return v

def Minval(board):
    v = float('inf')
    if terminal(board):
        return utility(board)
    
    for action in actions(board):
        v = min(v,Maxval(result(board,action)))
        return v

def Maxval_ab(board,a,b):
    raise NotImplementedError

def Minval_ab(board,a,b):
    raise NotImplementedError


    
    
