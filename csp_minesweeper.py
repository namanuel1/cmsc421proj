from itertools import product
import random
import copy
from minesweeper import *
import numpy as np

class Variable:
  def __init__(self, x_pos, y_pos):
    self.x_pos = x_pos
    self.y_pos = y_pos
    self.constraints = set()

  def add_constraint(self, x_pos, y_pos):
    self.constraints.add((x_pos, y_pos))

class Constraint:
  def __init__(self, x_pos, y_pos, sum):
    self.x_pos = x_pos
    self.y_pos = y_pos
    self.sum = sum
    self.variables = set()

  def add_variable(self, x_pos, y_pos):
    self.variables.add((x_pos, y_pos))

  def __str__(self):
    return "X: " + str(self.x_pos) + ", Y: " + str(self.y_pos) + ", Sum: " + str(self.sum) + ", Variables: " + str(self.variables)

#init fucntion takes in board dimensions and description
class CSP:
  def __init__(self, grid_width, grid_height, grid_description):
    self.grid_width = grid_width
    self.grid_height = grid_height
    self.grid_description = grid_description
    self.constraints = {}
    self.variables = {}

  # get position of valid surrounding tiles
  def neighbors(self, x_pos, y_pos):
    for i in range(-1, 2):
      if 0 <= x_pos-i < self.grid_width:
        for j in range(-1, 2):
          if 0 <= y_pos-j < self.grid_height:
            if not i == j == 0:
              yield (x_pos-i, y_pos-j)

  # returns list of unknown tile positions surrounding given position
  def find_constraints(self, x_pos, y_pos):
    return {n for n in self.neighbors(x_pos, y_pos) if self.grid_description[n[1]][n[0]] == "U"}

  # returns number of known mines surrounding given position
  def find_mine_neighbors(self, x_pos, y_pos):
    mines = 0
    for n in self.neighbors(x_pos, y_pos):
      if self.grid_description[n[1]][n[0]] == "X":
        mines = mines + 1
    return mines

  #adds constraint and associated variables
  def add_constraint(self, x_pos, y_pos):
    constraint_list = self.find_constraints(x_pos, y_pos)
    if constraint_list:
      new_constraint = Constraint(x_pos, y_pos, self.grid_description[y_pos][x_pos] - self.find_mine_neighbors(x_pos, y_pos))
      self.constraints[(x_pos, y_pos)] = new_constraint
      #initializing variables
      for v_pos in constraint_list:
        variable = self.variables.setdefault(v_pos, Variable(*v_pos))
        variable.add_constraint(x_pos, y_pos)
        new_constraint.add_variable(*v_pos)

  # creates constraint graph for the board
  def constraint_graph(self):
    for x_pos in range(self.grid_width):
      for y_pos in range(self.grid_height):
        if isinstance(self.grid_description[y_pos][x_pos], int):
          self.add_constraint(x_pos, y_pos)
    #print_constraints(self)

  # simpile filtering/proprocessing mechanism that assigns obvious safe spaces and mines
  def filter(self):
    solved = []
    for c in self.constraints.values():
      #if sum is 0, all surrounding cells must be safe
      if c.sum == 0:
        for v in c.variables:
          solved.append(("O", v))
      #if the sum is equal to the number of variables, then it is definately a mine
      elif c.sum == len(c.variables):
        for v in c.variables:
          solved.append(("X", v))
    return solved

  #this function updates redundant values in contstraints because we're working with sets
  def simplify(self):
    simplified = False
    for v1 in self.constraints.values():
      for v2 in self.constraints.values():
        #checking if they are supersets of eachother
        if not v1 is v2:
          if v1.variables > v2.variables:
            #removing redundant constraint
            v1.variables -= v2.variables
            v1.sum -= v2.sum
            simplified = True
    return simplified

  def backtracking_search(self):
    def rec_search(solutions, var_values, curr_vars, curr_cons):
      #if all variables have been solved, we can stop (base case)
      if not curr_vars:
        solutions.append(var_values)
        return solutions

      #not solved then pick a var with least amount of constraints
      var = min(curr_vars.values(), key=lambda x:len(x.constraints))
      #will store (0,) -> empty/no mine or (1,) -> cell contains a mine
      values = tuple()

      #search for whether this variable can have a mine
      for cons in var.constraints:
        #no mines adjacent to the cell, constraints satisfied
        if curr_cons[cons].sum == 0:
          break
        #otherwise the cell could be a mine!!
        else:
          values += (1,)

      #check whether the cell could have no mine (be 0)
      for cons in var.constraints:
        unassigned_vars = curr_cons[cons].variables
        if len(unassigned_vars) ==  curr_cons[cons].sum:
          break
        else:
          values += (0,)

      #this part is actually assigning the variable by removing it and determining if its
      #safe or a mine
      if values:
        #remove current var because it has already been assigned
        del curr_vars[(var.x_pos, var.y_pos)]
        #need to also remove constraints associated with variable
        #print("var constraints:")
        #print(var.constraints)
        for cons in var.constraints:
          if (var.x_pos, var.y_pos) in curr_cons[cons].variables:
            curr_cons[cons].variables.remove((var.x_pos, var.y_pos))
          #else:
            #print("a")
            #print(curr_cons[cons].variables)
            #print("b")
            #print((var.x_pos, var.y_pos))
        #if it's 0 or safe, make 0 assignment at position
        if 0 in values:
          curr_val = (((var.x_pos, var.y_pos), 0),)
          #recursive call with updated values, variables, and constraints
          rec_search(solutions, var_values+curr_val, curr_vars, curr_cons)

        #if 1 it could be a mine
        if 1 in values:
          #make 1 assingment to reflect that mine is at position
          curr_val = (((var.x_pos, var.y_pos), 1),)
          for cons in var.constraints:
            #decrementing to show that it's a mine
            curr_cons[cons].sum -= 1
          #recursive call with updated arguments
          rec_search(solutions, var_values+curr_val, curr_vars, curr_cons)

          #to properly backtrack we need to restore constraint sums in recursive calls
          for cons in var.constraints:
            curr_cons[cons].sum += 1

        #restoring variable and constraint information for backtracking after variable assignment
        curr_vars[(var.x_pos, var.y_pos)] = var
        for cons in var.constraints:
          curr_cons[cons].variables.add((var.x_pos, var.y_pos))
      #end of rec_search()

    #initialize
    values = tuple()
    curr_vars = self.variables
    curr_cons = self.constraints
    solutions = []
    #recursive call
    rec_search(solutions, values, curr_vars, curr_cons)

    #count the mines and return solutions
    mine_count=  {}
    #iterating through possible solutions
    for sol in solutions:
      #key is board and value is mine (1) no mine (0)
      for position,val in sol:
        #trying to count mines of all solutions, remember solutions look like ((x,y), value)
        #so if two solutions had a mine at (2,3) mine count = {(2,3):2}
        mine_count[position] = mine_count.setdefault(position,0) + val

    #the values found dictionary will store the positions of guaranteed mines "X"
    #or guaranteed safe spaces "O", it will look like ("X", (x,y))
    values_found = {
        ("X", position) if v else ("O", position) for position,v in mine_count.items() if v == len(solutions) or v == 0
        }

    #want a guaranteed solution:
    if values_found:
      return values_found
    #if there's a solution, want cells with least chance of being a mine
    elif mine_count:
      return [("O", min(mine_count, key=mine_count.get))]
    #else there are no solutions, return something random because hidden cells could be mine or safe cell
    #in this case
    else:
      cells = [cell for cell in product(range(self.grid_width), range(self.grid_height))
                      if self.grid_description[cell[1]][cell[0]] == "U"]
      if cells:
        return [("O", random.choice(cells))]


  #it updates the string board representation
  def update_board(self, constraints):
    #assume input constraints is a list (like returned by filtering) where ("X", (x,y))
    #if there are no constraints just return board
    if constraints == None:
      return
    #if not empty then iterate through constraints
    for state, pos in constraints:
      #updating string representation
      x,y = pos
      row = self.grid_description[y]
      #updating the row at position y
      self.grid_description[y] = row[:x]+[state]+row[x+1:]
    return self.grid_description


  #actually trying to solve a board now
  def solve_step(self):
    #generate constraint graph
    self.constraint_graph()
    #first want to filter out inconsistentcies
    while True:
      filtered = self.filter()
      if filtered:
        self.update_board(filtered)
      else:
        break
      #now we are checking redunancies with simplify()
      print("simplifying constriants")
      simplified = self.simplify()
      if simplified:
        filtered = self.filter()
        #after simplifying, do filtering
        if filtered:
          print("constraints after filtering")
          self.update_board(filtered)
        else:
          print('no cons after simplifying')
      else:
        print("no simplication")
      #after we have done preprocessing with simplify() and filter(), run backtracking
      print('now in backtracking')
      self.constraint_graph()
      search_result = self.backtracking_search()
      #update the board
      self.update_board(search_result)
      return

  def solve(self):
    while True:
        #old_grid = self.grid_description.copy()
        old_grid = copy.deepcopy(self.grid_description)
        self.solve_step()
        #print_board(csp)
        if old_grid == self.grid_description or not any("U" in sub for sub in self.grid_description):
          break

    return self.grid_description