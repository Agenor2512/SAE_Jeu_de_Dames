from Coordinates import Coordinates

class Move:
    def __init__(self, startRowIndex, startColIndex, endRowIndex, endColIndex):
        self.startMove = Coordinates(startRowIndex, startColIndex)
        self.endMove = Coordinates(endRowIndex, endColIndex)

    def calculateMidPos(self):
            midRowPos = (self.startMove.rowIndex + self.endMove.rowIndex)//2
            midColPos = (self.startMove.columnIndex + self.endMove.columnIndex)//2
            midPos = Coordinates(midRowPos, midColPos)

            return midPos