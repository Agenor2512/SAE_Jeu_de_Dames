from typing import Final
import numpy as np 

gridSize: Final[int] = 10

grid = np.empty((gridSize, gridSize), dtype=str)
grid[:] = " "
i: int = 0
column: int = 0


def initGrid():
    grid[8][6] = "n"



def displayGrid():
    print("   1 2 3 4 5 6 7 8 9 10")
    for i in range(0, gridSize):
        if i < 9:
            print(i+1, end=" |")
        else:
            print(i+1, end="|")

        for j in range(0, gridSize):
                print(grid[i][j], end="|")
        print()


def movePawn(pawnRowPos, pawnColumnPos, cellRowPos, cellColumnPos):
    if cellRowPos != 0 and cellRowPos != gridSize-1:

        grid[cellRowPos][cellColumnPos] = grid[pawnRowPos][pawnColumnPos]
        grid[pawnRowPos][pawnColumnPos] = " "

    else:
        grid[cellRowPos][cellColumnPos] = str(grid[pawnRowPos][pawnColumnPos]).upper()
        grid[pawnRowPos][pawnColumnPos] = " "


initGrid()
displayGrid()
movePawn(8, 6, 9, 5)
displayGrid()
