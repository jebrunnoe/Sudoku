#NAME: 
#  Board.py
#
#PURPOSE: 
#  To organize and manage the data of a Sudoku game board. The Board class 
#  represents the Sudoku game board as a 9x9 array of Cell objects.
#
#INPUTS: 
#  In order to properly function, the Cell class must be imported, along with
#  copy and random packages.
#
#CALLING SEQUENCE: 
#  The Board class only needs to be imported to be used. 

from Cell import Cell
import copy, random

class Board():
   def __init__(self):
      self.cells = [[Cell() for row in range(9)] for col in range(9)]			  
      self.cell_list = []
      self.master = [None] * 81
      # Create the associations between each cell and it's peers
      for row in range(9):
	 for col in range(9):
	    self.cell_list.extend([self.cells[row][col]])
	    for index in range(9):
	       if index != row: 
		  self.cells[row][col].peers.extend([self.cells[index][col]])
	       if index != col: 
		  self.cells[row][col].peers.extend([self.cells[row][index]])    
	    for box_row in range(row - (row % 3), row - (row % 3) + 3):
	       for box_col in range(col - (col % 3), col - (col % 3) + 3):
		  if box_row != row and box_col != col: 
		     self.cells[row][col].peers.extend([self.cells[box_row][box_col]])

   # Fix designates cells containing nonzero values as fixed
   def fix(self):
      for row in range(9):
	 for col in range(9):
	    if self.cells[row][col].value > 0: 
	       self.cells[row][col].fixed = True

   # Use a depth-first recursive search algorithm to exhaustively try
   # every possible combination of possible solutions given the current arrangement
   # of fixed values on the game board.  
   def solve(self, depth):
      if depth == 81: 
	 self.master = self.solution()
	 return True
      cell = self.cell_list[depth]
      if cell.fixed: 
	 return self.solve(depth + 1)
      cell.revise()
      while cell.possible:
	 possible_value = random.choice(cell.possible)
	 cell.value = possible_value
	 cell.possible.remove(possible_value)
	 if self.solve(depth + 1): 
	    return True
      cell.value = 0
      return False

   # Erase a variable number of randomly selected cells, 
   # depending on the provided difficulty. Checke for uniqueness
   # prior to erasing the cell value
   def conceal(self, difficulty): 
      self.fix()
      for cell in random.sample(self.cell_list, difficulty):
	 if self.is_unique(cell): 
	    cell.value = 0
	    cell.fixed = False
   
   # Test whether or not erasing the provided cell will preserve the uniqueness 
   # of the solution to the remaining puzzle. 
   def is_unique(self, cell):
      cell.revise()
      for possible_value in cell.possible:
	 if possible_value != cell.value:
	    save = cell.value
	    cell.value = possible_value
	    result = copy.deepcopy(self).solve(depth = 0) 
	    cell.value = save
	    if result: 
	       return False
      return True
	
   # Make a master solution key from the completed board. 
   def solution(self):
      master = list()
      for cell in self.cell_list:
	 master.append(cell.value)
      return master

   # Check the current board against the master solution key. 
   def is_complete(self):
      for index in range(81):
	 if self.cell_list[index].value != self.master[index]:
	    return False
      return True
