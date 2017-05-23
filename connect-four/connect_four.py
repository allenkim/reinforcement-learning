# Credit to https://gist.github.com/poke/6934842 for the clean win checks
from itertools import groupby, chain
from random import randint

from bots_connect_four import alphabeta_move, pg_move

def diagonals_pos (matrix, cols, rows):
    """Get positive diagonals, going from bottom-left to top-right."""
    for di in ([(j, i - j) for j in range(cols)] for i in range(cols + rows -1)):
        yield [matrix[i][j] for i, j in di if i >= 0 and j >= 0 and i < cols and j < rows]

def diagonals_neg (matrix, cols, rows):
    """Get negative diagonals, going from top-left to bottom-right."""
    for di in ([(j, i - cols + j + 1) for j in range(cols)] for i in range(cols + rows - 1)):
        yield [matrix[i][j] for i, j in di if i >= 0 and j >= 0 and i < cols and j < rows]

class ConnectFourGame:
    def __init__ (self, cols = 7, rows = 6, required_to_win = 4):
        """Create a new game."""
        self.cols = cols
        self.rows = rows
        self.win = required_to_win
        self.board = [['.'] * rows for _ in range(cols)]

    def legal_columns(self):
        return [c_idx for c_idx, c in enumerate(self.board) if c[0] == '.']

    def random_move(self, color):
        """Insert a random (legal) move"""
        legal_c = self.legal_columns()
        if len(legal_c) > 0:
            rand_idx = randint(0, len(legal_c) - 1)
            self.insert(legal_c[rand_idx], color)

    def next_avail_row(self, col):
        """Returns the row to be placed if inserted in col, -1 if NA"""
        c = self.board[col]
        if c[0] != '.':
            return -1
        i = self.rows - 1
        while c[i] != '.':
            i -= 1
        return i

    def insert(self, column, color):
        """Insert the color in the given column."""
        row = self.next_avail_row(column)
        if row == -1:
            self.random_move(color)
            return False # Was an illegal move, so random move chosen instead

        self.board[column][row] = color
        return True # Legal move

    def check_winner (self):
        """Get the winner on the current board."""
        legal_cols = self.legal_columns()
        if len(legal_cols) <= 0:
            return 'D'

        lines = (
            self.board, # columns
            zip(*self.board), # rows
            diagonals_pos(self.board, self.cols, self.rows), # positive diagonals
            diagonals_neg(self.board, self.cols, self.rows) # negative diagonals
        )

        for line in chain(*lines):
            for color, group in groupby(line):
                if color != '.' and len(list(group)) >= self.win:
                    return color

        return '.'

    def print_board (self):
        """Print the board."""
        print('  '.join(map(str, range(self.cols))))
        for y in range(self.rows):
            print('  '.join((self.board[x][y]) for x in range(self.cols)))
            print()

if __name__ == '__main__':
    g = ConnectFourGame()
    turn = None
    bot_level = None
    while True:
        t_in = input('First or second player? (1 or 2): ')
        try:
            if 1 <= int(t_in) <= 2:
                turn = 'Y' if t_in == '1' else 'R'
                print()
                break
        except Exception as e:
            continue

    while True:
        bot_level = input('Bot Level (-1 to 5): ')
        try:
            if -1 <= int(bot_level) <= 5:
                bot_level = int(bot_level)
                print()
                break
        except Exception as e:
            continue

    while True:
        g.print_board()
        if turn == 'Y':
            while True:
                col = input('{}\'s turn: '.format('Red' if turn == 'R' else 'Yellow'))
                try:
                    if 0 <= int(col) < g.cols:
                        col = int(col)
                        break
                except Exception as e:
                    continue

            g.insert(col, turn)
        else:
            col = pg_move(g) if bot_level == -1 else alphabeta_move(g, turn, bot_level)
            g.insert(col, turn)

        winner = g.check_winner()
        if winner != '.':
            g.print_board()
            if winner == turn:
                print(turn + " wins!")
            else:
                print("Draw!")
            break

        turn = 'Y' if turn == 'R' else 'R'
