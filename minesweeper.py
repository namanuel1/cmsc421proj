from constants import *
import random
import numpy as np

class Minesweeper:

    def __init__(self, height, width, bombs):
        self.bombs = bombs
        self.discovered = 0
        self.playing = True
        self.height = height
        self.width = width

        # create np array of tuples
        cell = np.empty((), dtype=object)
        cell[()] = (EMPTY,HIDDEN)
        self.board = np.full((height, width), cell, dtype=object)

    # set the board after the first input (assumes first input is valid)
    # this ensures that the user doesn't instantly lose the game
    def set_board(self, row, col):
        # fill with random bombs
        i = 0
        while i < self.bombs:
            bomb_row = random.randint(0, self.height - 1)
            bomb_col = random.randint(0, self.width - 1)
            bomb_val, board_shown = self.board[bomb_row][bomb_col]
            # if the cordinate isn't a bomb and it isn't
            # the first user input, make that a bomb 
            if bomb_val > BOMB and \
                (row,col) != (bomb_row, bomb_col):
                    
                self.board[bomb_row][bomb_col] = (BOMB, board_shown)
                i = i + 1

        # increment neighboring cells if the current cell is a bomb
        for index_row, board_row in enumerate(self.board):
            for index_col, board_cell in enumerate(board_row):
                curr_cell_val, curr_cell_shown = self.board[index_row][index_col]
                # if the current cell is a bomb
                if curr_cell_val == BOMB:
                    row_pos = -1
                    # increment by row
                    while row_pos < 2:
                        # checks if row is valid
                        if 0 <= index_row + row_pos < self.height:
                            col_pos = -1
                            # go by cols
                            while col_pos < 2:
                                # checks if surrounding values are valid
                                if 0 <= index_col + col_pos < self.width:
                                    curr_val, curr_shown = \
                                        self.board[index_row + row_pos][index_col + col_pos]
                                    if curr_val != BOMB:
                                        self.board[index_row + row_pos][index_col + col_pos] = \
                                              (curr_val + 1, curr_shown)
                                col_pos = col_pos + 1
                        row_pos = row_pos + 1

    # if bomb then end game, if a cell with a bomb nearby then show that value, 
    # and if empty, then run recursive show cell function
    # NOTE: doesn't account for pressing already shown values 
    def input_cell(self, row, col):
        cell_val,cell_shown = self.board[row][col]
        if cell_val == BOMB:
            self.playing = False
        elif cell_val == EMPTY:
            self.rec_input_cell(row,col)
        else: 
            self.board[row][col] = (cell_val, SHOWN)

    # checks adjacent and diagonal values for empty values and makes the 
    # current and around into shown values if they aren't already
    def rec_input_cell(self, row, col):
        # valid row and col, pass if invalid
        if 0 <= row < self.height and \
            0 <= col < self.width:

            cell_val,cell_shown = self.board[row][col]
            self.board[row][col] = (cell_val, SHOWN)

            # change values in current cell
            self.board[row][col] = (cell_val, SHOWN)

            row_pos = -1
            # iterate through all surrounding cells
            # increment by row
            while row_pos < 2:
                col_pos = -1
                # go by cols
                while col_pos < 2:
                    # show current cell if valid 
                    if 0 <= row + row_pos < self.height and \
                        0 <= col + col_pos < self.width:
                        curr_val, curr_shown = self.board[row + row_pos][col + col_pos]
                        # if the current is EMPTY and HIDDEN, recursively iterate, else pass
                        if curr_val == EMPTY and curr_shown == HIDDEN:
                            self.board[row + row_pos][col + col_pos] = (curr_val, SHOWN)
                            self.rec_input_cell(row + row_pos, col + col_pos)   
                        self.board[row + row_pos][col + col_pos] = (curr_val, SHOWN)    
                    col_pos = col_pos + 1
                row_pos = row_pos + 1

    def get_shown_board(self):
        shown_board = np.copy(self.board)
        for index_row, board_row in enumerate(self.board):
            for index_col, board_cell in enumerate(board_row):
                if board_cell:
                    cell_val,cell_shown = self.board[index_row][index_col]

                    if cell_shown == HIDDEN:
                        shown_board[index_row][index_col] = 'U'
                    elif cell_val == EMPTY:
                        shown_board[index_row][index_col] = 'E'
                    else: 
                        shown_board[index_row][index_col] = cell_val
        return shown_board