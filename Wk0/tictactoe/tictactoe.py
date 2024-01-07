"""
Tic Tac Toe Player
"""
import copy
import math

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
    count_x = sum(row.count(X) for row in board)
    count_o = sum(row.count(O) for row in board)

    if count_x == 0 or count_x <= count_o:
        return X
    else:
        return O

    raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # create action set
    action = set()

    # loop through the board and add any empty cells into possible set of actions
    for i in range(0,3):
        for j in range(0,3):
            if board[i][j] == EMPTY:
                action.add((i, j))

    return action

    raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # deepcopy of board    
    new_board = copy.deepcopy(board)

    # check if action is possible
    if action not in actions(board):
        raise ValueError('This move is not allowed')

    # place move by player who has their turn 
    new_board[action[0]][action[1]] = player(new_board)

    return new_board

    raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # check row
    for i in range(3):
        row = board[i]
        # check that all values == first value of each row
        if all(cell == row[0] for cell in row) and row[0] != EMPTY:
            return row[0]

    # check col
    for j in range(3):
        col = [row[j] for row in board]
        # check that all values == first value of each col
        if all(cell == col[0] for cell in col) and col[0] != EMPTY:
            return col[0]
    
    # check diagonal
    if board[0][0] == board[1][1] == board[2][2] != EMPTY:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != EMPTY:
        return board[0][2]
    
    return None



    raise NotImplementedError

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    count_x = sum(row.count(X) for row in board)
    count_o = sum(row.count(O) for row in board)

    # if either player wins
    if winner(board) == X or winner(board) == O:
        return True
    # draw
    elif count_x + count_o == 9:
        return True 
    else:
        return False

    raise NotImplementedError


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

    raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board) is True:
        return None
    
    alpha = float("-inf")
    beta = float("inf")

    if player(board) == X:
        v, action = max_value(board, alpha, beta)
        return action
    elif player(board) == O:
        v, action = min_value(board, alpha, beta)
        return action


# Functions for alpha beta pruning
def max_value(board, alpha, beta):
    # the game has ended, there is nothing to maximize

    if terminal(board) is True:
        return [utility(board), None]
    
    v = float("-inf")
    
    # The alpha value represents the best (maximum) score found so far for the maximizing player on the current path.
    for action in actions(board):
        value = min_value(result(board, action), alpha, beta)[0]
        alpha = max(alpha, value)

        # save the best move
        if value > v:
            v = value
            move = action

        # prune
        if alpha >= beta:
            break
    return v, move


def min_value(board, alpha, beta):
    # the game has ended, there is nothing to maximize

    if terminal(board) is True:
        return [utility(board), None]

    v = float("inf")

    # The beta value represents the best (minimum) score found so far for the minimizing player on the current path.
    for action in actions(board):
        value = max_value(result(board, action), alpha, beta)[0]
        beta = min(beta, value)

        # save the best move
        if value < v:
            v = value
            move = action

        # prune
        if alpha >= beta:
            break
    return v, move
