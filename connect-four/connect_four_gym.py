from random import randint, random
import math

from connect_four import ConnectFourGame
from bots_connect_four import alphabeta_move

def invert_colors(board):
    for col in range(len(board)):
        for row in range(len(board[col])):
            if board[col][row] == 'R':
                board[col][row] = 'Y'
            elif board[col][row] == 'Y':
                board[col][row] = 'R'

class ConnectFourGym:
    def reset(self):
        # AI is always RED and yellow or red goes first randomly
        self.first_player = 'R' if random() < 0.5 else 'Y'
        self.max_level = 4
        self.opp_level = randint(0,self.max_level) # the AI that will face the bot
        self.game = ConnectFourGame()
        if self.first_player == 'Y':
            move = alphabeta_move(self.game, 'Y', self.opp_level)
            self.game.insert(move, 'Y')
        return self.game.board

    def render(self):
        self.game.print_board()

    def step(self, action):
        """
        action: column number to insert
        """
        legal = self.game.insert(action, 'R')

        # RED will always refer to oneself (the bot in training)
        # YELLOW - the opponent of the bot in training
        observation = None
        reward = 0.0
        done = False
        info = {} # debugging info

        if not legal:
            reward = -1.0
            done = True
            return (observation, reward, done, info)

        winner = self.game.check_winner()
        if winner == 'D':
            reward = 0.0
            done = True
            return (observation, reward, done, info)
        if winner != '.':
            if winner == 'R':
                reward = math.sqrt(self.opp_level/self.max_level + 0.1)
            else:
                reward = -1.0
            done = True
        else:
            move = alphabeta_move(self.game, 'Y', self.opp_level)
            self.game.insert(move, 'Y')
            winner = self.game.check_winner()
            if winner != '.': 
                reward = -1.0
                done = True
        
        observation = self.game.board

        return (observation, reward, done, info)

