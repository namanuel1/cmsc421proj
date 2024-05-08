from minesweeper import *
import random
import sys
from csp_minesweeper import *
import numpy as np

# for print the CSP
def print_board(csp):
    for y_pos in range(csp.grid_height):
        row = ""
        for x_pos in range(csp.grid_width):
            row += " " + str(csp.grid_description[y_pos][x_pos]) + " "
        print(row + "\n")


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
    
test_game_csp()