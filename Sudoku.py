#NAME: 
#  Sudoku
#
#PURPOSE: 
#  To run the GUI using Tkinter and the Interface class. 
#
#INPUTS:
#  In order to funtion properly Tkinter and the Interface class must be imported
#
#CALLING SEQUENCE: 
#  python Sudoku.py  

from Tkinter import *
from Interface import Interface

# Create a root window and pass it into a object of the Interface class, 
# then enter into the mainloop until the window is closed. 
root = Tk()			
GUI = Interface(root)				
root.mainloop()
