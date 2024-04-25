from minesweeper import Minesweeper
import random
import sys

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

test_get_shown_board()