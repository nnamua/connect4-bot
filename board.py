from stones import Stone, Yellow, Red, Empty

class Board:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self._array = []

        # Generate the starting board
        for x in range(width):
            column = []
            for y in range(height):
                column.append(Empty)
            self._array.append(column)

    # Returns a single column of the board
    def column(self, x: int):
        return self._array[x]

    # Returns a single row of the board
    def row(self, y: int):
        return [ self._array[x][y] for x in range(self.width) ]

    # Returns a copy of this board object
    def copy(self):
        copy = Board(self.width, self.height)
        for x in range(self.width):
            for y in range(self.height):
                copy[x][y] = self._array[x][y]
        return copy

    # Returns a flat (1D) array of the board stones
    def flatten(self):
        flatArray = []
        for x in range(self.width):
            for y in range(self.height):
                flatArray.append(self._array[x][y])
        return flatArray

    def __getitem__(self, index: int):
        return self._array[index]

    def __setitem__(self, index: int, item: Stone):
        self._array[index] = item

    def __str__(self):
        string = ""
        for y in range(self.height):
            string += "|"
            for x in range(self.width):
                string += str(self._array[x][y]) + "|"
            string += "\n"
        return string