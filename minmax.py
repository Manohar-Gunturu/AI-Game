from Util import state_conv1, card_number
import operator
from math import inf

def calc_en1(child):
    return calc_en(child)


def calc_en(child):
    if len(child.children) != 0:
        return child.value
    sum_w_o = 0.0
    sum_w_d = 0.0
    sum_r_o = 0.0
    sum_r_d = 0.0
    for i in range(12):
        for j in range(8):
            cellval = (12 - i) * 10 + j + 1
            val = state_conv1(i, j, child.state)
            sum_w_o += cellval if val % 100 == 1 else 0.0
            sum_w_d += cellval if val % 100 == 3 else 0.0
            sum_r_o += cellval if val % 100 == 2 else 0.0
            sum_w_d += cellval if val % 100 == 4 else 0.0
    en = sum_w_o + (3.0 * sum_w_d) - (2.0 * sum_r_d) - (1.5 * sum_r_o)
    return en


def calc_en_for_children(node, min_or_max):
    # for each child calculate
    ens = []
    for child in node.children:
        en = calc_en1(child)
        child.set_value(en)
        ens.append(en)
    if min_or_max == "min":
        (min_index, min_value) = min(enumerate(ens), key=operator.itemgetter(1))
        return min_index, min_value
    else:
        (max_index, max_value) = max(enumerate(ens), key=operator.itemgetter(1))
        return max_index, max_value


"""
   3 levels - including root as prf said, so 
     N
    / \ 
   N   N - apply max here and return
  /     \
  N      N  - apply - min here 
"""


def run_minmax(node):

    if len(node.children[0].children) == 0:
        # calculate e(n) on each state
        min_or_max = "max" if node.level % 2 == 0 else "min"
        # print("applied ", min_or_max)
        best_index, best_en = calc_en_for_children(node, min_or_max)
        node.set_value(best_en)
        return best_index

    for child in node.children:
        run_minmax(child)

    min_or_max = "max" if node.level % 2 == 0 else "min"
    # print("applied ", min_or_max)
    best_index, best_en = calc_en_for_children(node, min_or_max)
    node.set_value(best_en)
    return best_index


def run_alphabeta(node, alpha, beta, ismaximizing):
    if len(node.children) == 0:
        return ( calc_en(node), 0 )

    if ismaximizing:
        maxEval = -inf
        maxIndex = 0
        for i in range(len(node.children)):
            eval = run_alphabeta(node.children[i], alpha, beta, False)
            if max(maxEval, eval[0]) != maxEval:
                maxEval = eval[0]
                maxIndex = i
            alpha = max(alpha, eval[0])
            if beta <= alpha:
                break
        return ( maxEval, maxIndex )
    else:
        minEval = inf
        minIndex = 0
        for i in range(len(node.children)):
            eval = run_alphabeta(node.children[i], alpha, beta, True)
            if min(minEval, eval[0]) != minEval:
                minEval = eval[0]
                minIndex = i
            beta = min(beta, eval[0])
            if beta <= alpha:
                break
        return ( minEval, minIndex )