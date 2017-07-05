#NAME: 
#  Interface.py
#
#PURPOSE: 
#  To provide a graphical user interface to visually represent
#  the data and structure of the Sudoku board in an interactive window.
#
#INPUTS: 
#  In order to properly function, the Board class must be imported along
#  with Tkinter, ttk, tkMessageBox
#
#CALLING SEQUENCE: 
#  The interface class only needs to be imported to be used.  

from Board import Board
from Tkinter import *
from ttk import *
from tkMessageBox import *

class Interface():
   # Configure the parent root window, create a Board object, define styles and call 
   # functions to build the user interface. 
   def __init__(self, parent):
      self.parent = parent
      self.parent.title("Sudoku")
      self.parent.configure(borderwidth = 9)
      self.parent.bind_all("<Key>", self.keyboard)
      self.main = Board()
      self.row, self.col = 0, 0	
      self.difficulties = {"Easy": 45, "Medium": 63, "Hard": 81}
      Style().configure('peer.TEntry', background = '#edf7ff')
      Style().configure('deselect.TEntry', background = 'white')
      Style().configure('match.TEntry', background = '#f7f5bb')
      Style().configure('used.TEntry', background = '#f7f7f7') 
      Style().configure("frame.TFrame", borderwidth = 3, relief = 'ridge')
      Style().configure('box1.TEntry', background = '#d0d4d6')
      Style().configure('box2.TEntry', background = '#8bc1d3')
      self.make_panel()
      self.make_board()

   # Build a control panel, child of the parent window. Create buttons for the
   # user to interact with to perform various functions.
   def make_panel(self):
      # Create a frame to hold and organize the buttons. 
      panel = Frame(self.parent, padding = 9, style = 'frame.TFrame')
      panel.pack(pady = 9)

      # Create a drop down menu to select the difficulty. See the toggle function.
      self.difficulty_var = StringVar()
      self.difficulty = Combobox(panel, width = 10, textvariable = self.difficulty_var, state = 'readonly')
      self.difficulty.grid(row = 0, column = 0, padx = 3, pady = 3)
      self.difficulty['values'] = ("Difficulty", "Easy", "Medium", "Hard")
      self.difficulty.bind('<<ComboboxSelected>>', self.toggle)
      self.difficulty.current(0)

      # Create a button to start a new game. See newgame function.
      self.newgame = Button(panel, width = 9, text = "New Game", command = self.newgame, state = DISABLED)
      self.newgame.grid(row = 0, column = 1)

      # Create a button to solve the puzzle and display the solution. See solve function.
      self.solve = Button(panel, width = 9, text = "Solve", command = self.solve, state = DISABLED)
      self.solve.grid(row = 1, column = 0)

      # Create a button to clear the values input by the user. See erase function.
      self.clear = Button(panel, width = 9, text = 'Clear', command = self.erase, state = DISABLED)
      self.clear.grid(row = 1, column = 1, padx = 3, pady = 3)

   # Build the game board to display the cells and their contents. 
   def make_board(self):
      # Make a frame to hold and organize the game board and place it in the parent root window.
      board_window = Frame(self.parent, borderwidth = 0, relief = 'flat')
      board_window.pack()
      
      # Make and configure 9 frames to represent the 9 boxes on the game board.
      # Vary the color to make the boxes visually differentiable. Note that the indices
      # box / 3 and box % 3 yields (0, 0), (0, 1), (0, 2), (1, 0) ... (2, 2)
      boxes = [None] * 9
      for box in range(9):
	 boxes[box] = Frame(board_window, padding = 3, style = 'box1.TEntry' if box % 2 == 0 else 'box2.TEntry') 
	 boxes[box].grid(row = box / 3, column = box % 3)

      # Make and configure 81 entry widgets to display values and accept input. 
      # Save the entry widgets into a list so they can be easily referenced later.
      # Bind the mouse click to a cursor function and provide it with the row and column
      # of the widget in which the mouse click occurs. 
      self.entry_list = [None] * 81
      for row in range(9):
	 for col in range(9):
	    box = row - (row % 3) + (col - (col % 3)) / 3
	    entry = Entry(boxes[box], state = DISABLED)
	    entry.configure(width = 3, justify = 'center', textvariable = StringVar())
	    entry.grid(row = row, column = col, padx = 3, pady = 3, ipadx = 9, ipady = 9)
	    entry.bind('<Button-1>', lambda event, row = row, col = col: self.cursor(row, col))
	    self.entry_list[row * 9 + col] = entry

   # Toggle the states of the buttons and cells between disabled 
   # and normal depending on whether or not a difficulty has been selected.
   def toggle(self, event):
      if self.difficulty_var.get() == 'Difficulty': 
	 toggle_state = DISABLED
      else: 
	 toggle_state = NORMAL
      self.newgame.configure(state = toggle_state)
      self.solve.configure(state = toggle_state)
      self.clear.configure(state = toggle_state)
      for cell in self.entry_list:
	 cell.configure(state = toggle_state)

   # Save the row and column of the click and update the board so the 
   # appropriate highlighting can be put into effect. 		
   def cursor(self, row_click, col_click):
      self.row = row_click
      self.col = col_click
      self.update()
		
   # Validate user input, update the game board and display appropriate messages.
   def keyboard(self, event):
      target = self.main.cells[self.row][self.col]
      if self.difficulty_var.get() == 'Difficulty':
	 showinfo(title = 'No difficulty selected', message = 'Please select a difficulty.', icon = 'error')
      elif target.value == 0 and event.char in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
	 target.value = int(event.char)
      else: 
	 showinfo(title = 'Invalid input', message = 'Oops! Try again.', icon = 'warning')
      if self.main.is_complete(): 
	 showinfo(title = 'Sudoku Complete', message = 'Well Done!')
      self.update()

   # Call the board's solve method to fill out the board, save a master solution, 
   # erase values based on the user-selected difficulty, initialize the 
   # row and column and update the game board.
   def newgame(self):
      self.main.solve(0)
      self.solution = self.main.solution()
      self.main.conceal(self.difficulties[self.difficulty.get()])
      self.row, self.col = 0, 0
      self.update()
		
   # Verify the user wants to view the solution, call the solve function, and update the board.
   def solve(self):
      if askyesno(message = 'Are you sure?'):
	 self.erase()
	 self.main.solve(0)
	 self.update()

   # Erase all user-input values, leaving the original puzzle unchanged.
   def erase(self):
      for cell in self.main.cell_list:
	 if cell.fixed == False: 
	    cell.value = 0
      self.update()
				
   # Update the board so the widgets reflect the current state of the game board. 
   # Highlight the current cell's value-matched and peer cells. 
   def update(self):
      cell_click = self.main.cells[self.row][self.col]
      for row in range(9):
	 for col in range(9):
	    cell = self.main.cells[row][col]
	    self.entry_list[row * 9 + col].delete(0, END)
	    if cell.value != 0: 
	       self.entry_list[row * 9 + col].insert(0, cell.value)
	    if cell_click.value != 0 and cell_click.value == cell.value: 
	       shade = 'match.TEntry'
	    elif cell in cell_click.peers: 
	       shade = 'peer.TEntry'
	    elif cell.value > 0: 
	       shade = 'used.TEntry'	
	    else: 
	       shade = 'deselect.TEntry'
	    self.entry_list[row * 9 + col].configure(style = shade)
