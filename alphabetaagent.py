from exceptions import AgentException
from connect4 import Connect4
from copy import deepcopy


def basic_static_eval(connect4: Connect4, player: str) -> float:
    p_points = 0
    o_points = 0
    val = 0
    if player == 'x':
        opp = 'o'
    else:
        opp = 'x'
    for four in connect4.iter_fours():
        if four.count(player) == 3:
            p_points += 1
        if four.count(opp) == 3:
            o_points += 1
        if four.count(player) == 4:
            p_points = 0
            val = float('inf')
        if four.count(opp) == 4:
            o_points = 0
            val = float('-inf')
    if val != 0:
        val = p_points - o_points
    return val


def advanced_static_eval(connect4: Connect4, player: str) -> float:
    p_points = 0
    o_points = 0
    val = 0
    if player == 'x':
        opp = 'o'
    else:
        opp = 'x'
    for four in connect4.iter_fours():
        if four.count(player) == 3:
            p_points += 1
        if four.count(opp) == 3:
            o_points += 1
        if four.count(player) == 2:
            p_points += 0.2
        if four.count(opp) == 2:
            o_points += 0.2
        if four.count(player) == 4:
            p_points = 0
            val = float('inf')
        if four.count(opp) == 4:
            o_points = 0
            val = float('-inf')

    if val != 0:
        val = p_points - o_points
    return val


class AlphaBetaAgent:
    def __init__(self, my_token='o', eval_func=basic_static_eval, max_depth=4):
        self.my_token = my_token
        self.eval_func = eval_func
        self.max_depth = max_depth

    def decide(self, connect4: Connect4):
        if connect4.who_moves != self.my_token:
            raise AgentException('not my round')
        action, value = self._alphabeta(deepcopy(connect4), self.max_depth, float('-inf'), float('inf'), True)
        return action

    def _alphabeta(self, connect4: Connect4, depth, alpha, beta, is_maximizing_player):
        pos = None
        if depth == 0 or connect4.game_over:
            if connect4.wins == self.my_token:
                return pos, float('inf')
            elif connect4.wins == self._other_token():
                return pos, float("-inf")
            else:
                return pos, self.eval_func(connect4, self.my_token)
        if is_maximizing_player:
            val = float('-inf')
            for position in connect4.possible_drops():
                new_connect4 = deepcopy(connect4)
                new_connect4.drop_token(position)
                _, new_val = self._alphabeta(new_connect4, depth - 1, alpha, beta, False)
                if new_val > val:
                    pos, val = position, new_val
                alpha = max(alpha, val)
                if beta <= alpha:
                    break

        else:
            val = float('inf')
            for position in connect4.possible_drops():
                new_connect4 = deepcopy(connect4)
                new_connect4.drop_token(position)
                _, new_val = self._alphabeta(new_connect4, depth - 1, alpha, beta, True)
                if new_val < val:
                    pos, val = position, new_val
                beta = min(beta, val)
                if beta <= alpha:
                    break

        if pos is None:
            return None, 0.0
        return pos, val

    def _other_token(self):
        if self.my_token == 'x':
            return 'o'
        else:
            return 'x'


