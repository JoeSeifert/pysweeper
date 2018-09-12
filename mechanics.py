import random


class Square:

    def __init__(self, row, col, game):
        self.is_mine = False
        self.is_revealed = False
        self.is_flagged = False
        self.neighboring_mines = 0
        self.row = row
        self.col = col
        self.game = game
        self.neighbors = []

    def find_neighbors(self):
        """
        Calculates how many neighboring squares contain mines
        Adjusts class variable self.neighboring_mines to reflect this
        :return: None
        """
        if self.is_mine:
            return
        row_inds = (self.row - 1, self.row, self.row + 1)
        col_inds = (self.col - 1, self.col, self.col + 1)
        for r in row_inds:
            for c in col_inds:
                if r < 0 or c < 0:
                    continue
                try:
                    if self.game[r][c].is_mine:
                        self.neighboring_mines += 1
                    if not (r == self.row and c == self.col):
                        self.neighbors.append(self.game[r][c])
                except IndexError:
                    continue

    def reveal(self):
        """
        Reveals the square
        Will not reveal a flagged square
        Will not reveal an already revealed square
        Ends game if the square is a mine
        If square contains no neighboring mines (i.e. square is blank), reveals neighbors
        :return: None
        """
        if self.is_flagged or self.is_revealed:
            return
        elif self.is_mine:
            self.is_revealed = True
            self.game.end_condition = True
            self.game.win = False  # to be explicit that this is a loss
            return
        elif not self.neighboring_mines:
            # must reveal other squares as well
            self.is_revealed = True
            self.game.num_revealed += 1
            self.game.updated_squares.append(self)
            for sq in self.neighbors:
                if not sq.is_revealed:
                    sq.reveal()
        else:
            # no extra squares to be revealed
            self.is_revealed = True
            self.game.num_revealed += 1
            self.game.updated_squares.append(self)

    def flag(self):
        """
        Flags a square if it is not flagged, un-flags a square if it is flagged
        :return: None
        """
        if not self.is_revealed and self.is_flagged:
            # Sqaure is alread flagged
            self.is_flagged = False
            self.game.num_flagged -= 1
            self.game.updated_squares.append(self)
        elif not self.is_revealed and not self.is_flagged and (self.game.num_flagged < self.game.n_mines):
            # last condition in above --> make sure you have at least one flag left to give!
            self.is_flagged = True
            self.game.num_flagged += 1
            self.game.updated_squares.append(self)

    def __str__(self):
        """
        For printing the board properly in cmd
        :return: square's appropriate symbol
        """
        if self.is_mine and self.is_revealed:
            return 'x'
        elif self.is_revealed:
            return str(self.neighboring_mines)
        elif self.is_flagged:
            return '^'
        else:
            return '@'


class Game:

    def __init__(self, difficulty, nrows=None, ncols=None, n_mines=None):
        self.difficulties = {'beginner': (9, 9, 10), 'intermediate': (16, 16, 40), 'expert': (16, 30, 99),
                             'custom': (nrows, ncols, n_mines)}
        self.nrows, self.ncols, self.n_mines = self.difficulties[difficulty]
        self.board = []
        self.num_revealed = 0
        self.num_flagged = 0
        self.updated_squares = []
        self.end_condition = False
        self.win = False

    def make_game(self, row, col):
        self.create_board()
        self.place_mines(row, col)

    def create_board(self):
        """
        Creates board of empty Square() objects in self.board
        self.board is an array of arrays, indexed by self.board[row][col]
        :return: nothing
        """
        # will go as O(n^2) always
        for i in range(self.nrows):
            temp_row = []
            for j in range(self.ncols):
                temp_row.append(Square(i, j, self))
            self.board.append(temp_row)

    def place_mines(self, row, col):
        """
        Randomly selects indices to place the n_mines mines, then places them. Also calculates square.neighboring_mines
        for each Square() in self.board.

        To ensure a mine is not clicked from the start and that the player has something to work with, the starting
        click and all neighbors are removed from the possible mine locations

        :param row: Initially-clicked square row
        :param col: Initially-clicked square column
        :return:
        """
        rows = (row - 1, row, row + 1)
        cols = (col - 1, col, col + 1)
        no_mine_locs = ()
        for i in rows:
            for j in cols:
                if not (i < 0 or j < 0):
                    no_mine_locs += (i * self.ncols + j),
        sample_list = list(range(self.nrows * self.ncols))
        for loc in no_mine_locs:
            try:
                sample_list.remove(loc)
            except ValueError:
                continue
        mine_locations = random.sample(sample_list, self.n_mines)
        for loc in mine_locations:
            row = loc // self.ncols
            col = loc % self.ncols
            self.board[row][col].is_mine = True
        for i in range(self.nrows):
            for j in range(self.ncols):
                self.board[i][j].find_neighbors()

    def check_win(self):
        """
        Checks if a player has won
        :return: True if win, False else
        """
        if (self.num_revealed == (self.nrows * self.ncols) - self.n_mines) and not self.end_condition:
            # second condition in case player has two squares left and clicks on the mine instead of the blank
            self.end_condition = True
            self.win = True
        if self.end_condition and self.win:
            return True
        else:
            return False

    def check_lose(self):
        """
        Checks if a player has lost
        Note: this is necessary because it is possible to have neither won nor lost
        :return: True if loss, False else
        """
        if self.end_condition and not self.win:
            return True
        else:
            return False

    def reveal(self, row, col):
        # alternatively, for Game obj x, could call x[row][col].reveal()...
        # UPDATE: apparently I did that a while ago and never commented about it!
        self.board[row][col].reveal(row, col)

    def __getitem__(self, key):
        return self.board[key]

    def __str__(self):
        final = ''
        for row in self.board:
            for sq in row:
                final += str(sq) + ' '
            final += '\n'
        return final


if __name__ == '__main__':
    print('~~~This is not the code you are looking for~~~')
