class Coordinates:
    def __init__(self, rowIndex, columnIndex):
        self.rowIndex = rowIndex
        self.columnIndex = columnIndex
    
    def coord(self):
        return self.rowIndex, self.columnIndex

    def isCoordValid(self):
        if self.rowIndex > 9 or self.columnIndex > 9:
            return False