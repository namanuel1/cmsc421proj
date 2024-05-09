from minesweeper import *
import random
import sys
from csp_minesweeper import *
import numpy as np
import wx

# for print the CSP
def print_board(csp):
    for y_pos in range(csp.grid_height):
        row = ""
        for x_pos in range(csp.grid_width):
            row += " " + str(csp.grid_description[y_pos][x_pos]) + " "
        print(row + "\n")



class MyFrame(wx.Frame):
    def __init__(self, parent, title, row_size, column_size, bombs):
        super(MyFrame, self).__init__(parent, title=title, size=(300, 300))
        self.minesweeper = Minesweeper(row_size, column_size, bombs) 
        self.minesweeper.set_board(row_size, column_size)  
        self.panel = wx.Panel(self)
        self.grid = wx.GridSizer(row_size, column_size, 0, 0) 
        self.row = row_size
        self.column = column_size
        self.bombs = bombs

        self.buttons = [[None for _ in range(row_size)] for _ in range(column_size)]
        for row in range(row_size):
            for col in range(column_size):
                button = wx.Button(self.panel, id=wx.ID_ANY, label='', size=(30, 30))
                self.grid.Add(button, 0, wx.EXPAND)
                self.buttons[row][col] = button
                button.Bind(wx.EVT_BUTTON, lambda event, r=row, c=col: self.on_button_click(event, r, c))

        self.panel.SetSizer(self.grid)
        self.Bind(wx.EVT_CLOSE, self.on_close)

    def on_button_click(self, event, row, col):
        self.minesweeper.input_cell(row, col)
        playing = self.minesweeper.playing
        winner = self.minesweeper.check_win()
        if playing and not winner: 
            self.update_display()
            csp_board = self.minesweeper.get_shown_board()
            csp_board = self.minesweeper.get_shown_board()
            csp = CSP(self.row, self.column, csp_board)
            csp.solve()
            print_board(csp)
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        elif not playing: 
            self.update_display()
            wx.MessageBox('Boom! You hit a bomb!', 'Game Over', wx.OK | wx.ICON_ERROR)
            self.Destroy()
        elif winner: 
            self.update_display()
            wx.MessageBox('Congratulations! You have won!', 'Game Won', wx.OK | wx.ICON_INFORMATION)
            self.Destroy()

                
  


    def update_display(self):
        csp_board = self.minesweeper.get_shown_board()
        csp = CSP(self.row, self.column, csp_board)
        csp.solve()
        playing = self.minesweeper.playing
        for row in range(self.row):
            for col in range(self.column):
                cell = self.minesweeper.get_shown_board()[row][col]
                button = self.buttons[row][col]
                if cell == 'U': 
                    cell_csp = str(csp.grid_description[row][col])
                    if cell_csp == 'X': 
                        button.SetLabel('!')
                    if cell_csp == 'O': 
                        button.SetLabel('')
                else:
                    button.SetLabel(str(cell))
                    button.Disable()


    def on_close(self, event):
        self.Destroy()




def print_constraints(csp):
    print("Constraints:")
    for pos in csp.constraints:
        print(csp.constraints[pos])


# make sure you put in correct values for inputs

def test_set_board():
    i = 0
    while i < 5:
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        test = Minesweeper(5,5,5)
        test.set_board(3,3)
        print(test.board)
        i = i + 1
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

def test_input_cell():
    test = Minesweeper(5,5,3)
    test.set_board(3,3)
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print(test.board)
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    row = 0
    col = 0
    while test.playing:
        print("Print Row as Int, then 'stop': ")
        for line in sys.stdin:
            if 'stop' == line.rstrip():
                break
            else:
                row = int(line.rstrip())
        print("Print Col as Int, then 'stop': ")
        for line in sys.stdin:
            if 'stop' == line.rstrip():
                break
            else:
                col = int(line.rstrip())

        #try:
        test.input_cell(row,col)
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print(test.board)
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        #except:
            #print("INVALID INPUT >:(")
            
    print("GAME OVER")

def test_get_shown_board():
    test = Minesweeper(5,5,3)
    test.set_board(3,3)
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print(test.board)
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print(test.get_shown_board())
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    test.input_cell(3,3)
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print(test.get_shown_board())
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

def test_game_csp():
    # get input for initializing game
    print("Gimme Width then Height then Bombs as int")
    print("Don't blame me if you put too many bombs in")
    getting_valid_input = True
    
    while getting_valid_input:
        try:
            height = int(input())
            getting_valid_input = False
        except:
            print("ERROR, give me the height fr (as an int)")
    getting_valid_input = True

    while getting_valid_input:
        try:
            width = int(input())
            getting_valid_input = False
        except:
            print("ERROR, the width is needed as an int")
    getting_valid_input = True

    while getting_valid_input:
        try:
            bombs = int(input())
            getting_valid_input = False
        except:
            print("ERROR, bomb time but as int this time")

    getting_valid_input = True
    app = wx.App(False)
    frame = MyFrame(None, "Minesweeper", height, width, bombs)
    frame.Show()
    app.MainLoop()


"""
    test = Minesweeper(height,width,bombs)
    print("~~~~~~~~~~~~~~~~~~~~~~~~")
    print("The Top is board and bottom is the csp")
    for row in test.get_shown_board():
        print(row)
    print("------------------------")
    csp_board = test.get_shown_board()
    csp = CSP(width, height, csp_board)
    csp.solve()
    print_board(csp)
    print("~~~~~~~~~~~~~~~~~~~~~~~~")

    # first move (need to set up board)
    print("gimme the row (top is 0, you can count for the bottom), then column (left is 0)")
    while getting_valid_input:
        try:
            row = int(input())
            col = int(input())
            getting_valid_input = False
            try:
                test.set_board(row,col)
                test.input_cell(row,col)
            except:
                getting_valid_input = True
                print("damn u did something wrong")
                print("try again")
        except:
            print("aight, just read the previous message, you got an ERROR")
    getting_valid_input = True
    
    for row in test.get_shown_board():
            print(row)
    print("------------------------")
    csp_board = test.get_shown_board()
    csp = CSP(width, height, csp_board)
    csp.solve()
    print_board(csp)
    print("~~~~~~~~~~~~~~~~~~~~~~~~")
    
    winner = test.check_win()

    # now we play fr
    while test.playing and not winner:
        # get valid input and insert into board
        while getting_valid_input:
            try:
                row = int(input())
                col = int(input())
                getting_valid_input = False
                try:
                    test.input_cell(row,col)
                except:
                    getting_valid_input = True
                    print("damn u did something wrong")
                    print("try again")
            except:
                print("gimme the row (top is 0, you can count for the bottom), then column (left is 0)")
        getting_valid_input = True

        print("~~~~~~~~~~~~~~~~~~~~~~~~")
        for row in test.get_shown_board():
            print(row)
        print("------------------------")
        csp_board = test.get_shown_board()
        csp_board = test.get_shown_board()
        csp = CSP(width, height, csp_board)
        csp.solve()
        print_board(csp)
        print("~~~~~~~~~~~~~~~~~~~~~~~~")

        winner = test.check_win()

    print(test.board)
    if winner: 
        print("YOU WINNNNN LETS GOOOO")
    else:
        print("GAMEOVER >:(")
"""
    
test_game_csp()

