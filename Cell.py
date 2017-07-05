#NAME: 
#  Cell.py
#
#PURPOSE: 
#  The Cell class represents one cell on the Sudoku game board. A cell contains
#  a value, a boolean to designate whether the cell is fixed or writable, a list
#  of peers (other cells which share the same row, column or box), and a list of possible values.
#
#CALLING SEQUENCE: 
#  Cell only needs to be imported to be used.

class Cell(): 
   # The cell's parameters are initialized when the cell is created.
   def __init__(self):
      self.value = 0    
      self.fixed = False
      self.peers = []
      self.possible = range(1, 10)

   # Check each of the cell's peers for the given value and return True a
   # match is found, otherwise False
   def in_peers(self, value):
      for cell in self.peers:
	 if value == cell.value: 
	    return True
      return False

   # Update the cell's list of possible values by iterating through
   # 1 - 9 and calling 'in_peers' to check for each value.
   def revise(self):
      del self.possible[:]
      for value in range(1, 10):
	 if not self.in_peers(value): 
	    self.possible.extend([value])
