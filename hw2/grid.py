# -*- coding: utf-8 -*-
"""
Created on Fri Sep 12 14:06:43 2014

@author: Cyprien Guillemot
"""

#Print top right corner
def printCorner():
    print "+"

#Print right side of cell
def printSide():
    print "|"

#Print top cell (or bottom)
def printTopCell():
    print "+ - - - -",
    
#Print border of cell
def printBordercell():
    print "|        ",

#Print top of the grid (or bottom)
def printTopLine():
    doFour(printTopCell)
    printCorner()
    
#Print border line of the grid
def printBorderLine():
    doFour(printBordercell)
    printSide()
    
#Print a cell row
def printRow():
    printTopLine()
    doFour(printBorderLine)
    
#Run 4 times f
def doFour(f):
    for num in range(0,4):
        f()

#Print the grid
def printGrid():
    doFour(printRow)
    printTopLine()
    
printGrid()