from exceptions import GameplayException
from connect4 import Connect4
from randomagent import RandomAgent
from minmaxagent import MinMaxAgent

connect4 = Connect4(width=7, height=6)
agent = MinMaxAgent('x')
while not connect4.game_over:
    connect4.draw()

    if connect4.who_moves == agent.my_token:
        n_column = agent.decide(connect4)
        if n_column is None:
            n_column = connect4.possible_drops()[0]
    else:
        n_column = int(input(':'))
    connect4.drop_token(n_column)

connect4.draw()
