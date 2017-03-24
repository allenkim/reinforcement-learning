from math import inf
from random import randint, gauss
from copy import deepcopy

bot_level = 0

def alphabeta_move(node, turn, strength):
    global bot_level
    bot_level = strength
    return alphabeta_bot(node, strength, -inf, inf, turn)

def heuristic(node):
    num_r_y = []
    for col in node.board:
        num_red = 0
        num_yellow = 0
        for elt in col:
            if elt == 'R':
                num_red += 1
            elif elt == 'Y':
                num_yellow += 1
        num_r_y.append(num_red - num_yellow)
    num_r_y[3] *= gauss(1.5,1)
    num_r_y[2] *= gauss(1,1)
    num_r_y[4] *= gauss(1,1)
    num_r_y[1] *= gauss(0.5,1)
    num_r_y[5] *= gauss(0.5,1)
    num_r_y[0] *= gauss(0,1)
    num_r_y[6] *= gauss(0,1)
    return sum(num_r_y)

# 'R' is max, 'Y' is min
def alphabeta_bot(node, depth, alpha, beta, player):
    """
    node: ConnectFourGame object
    depth: depth of alphabeta (higher the depth, stronger the bot)
    alpha: lower bound for max
    beta: upper bound for min
    player: either 'R' or 'Y'
    """
    winner = node.check_winner()
    if depth == 0 or winner != '.':
        if bot_level == 0:
            legal_c = node.legalColumns()
            if len(legal_c) > 0:
                rand_idx = randint(0, len(legal_c) - 1)
                return legal_c[rand_idx]

        # Simple Heuristic evaluation
        if winner == 'R':
            return 10000 + depth
        elif winner == 'Y':
            return -10000 - depth
        else:
            return heuristic(node)
    if player == 'R':
        best_v = -inf
        best_col = 3
        for col in range(node.cols):
            child_node = deepcopy(node)
            legal = child_node.insert(col, 'R')
            if legal:
                new_v = alphabeta_bot(child_node, depth - 1, alpha, beta, 'Y')
                if new_v > best_v:
                    best_v = new_v
                    best_col = col
                alpha = max(alpha, best_v)
                if beta <= alpha:
                    break
        if depth == bot_level:
            return best_col
        return best_v
    elif player == 'Y':
        best_v = inf
        best_col = 3
        for col in range(node.cols):
            child_node = deepcopy(node)
            legal = child_node.insert(col, 'Y')
            if legal:
                new_v = alphabeta_bot(child_node, depth - 1, alpha, beta, 'R')
                if new_v < best_v:
                    best_v = new_v
                    best_col = col
                beta = min(beta, best_v)
                if beta <= alpha:
                    break
        if depth == bot_level:
            return best_col
        return best_v
