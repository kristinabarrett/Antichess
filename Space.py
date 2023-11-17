class Space:
    """Represents a space on the board"""

    x = 0
    y = 0
    piece = None

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def setPiece(self, piece):
        self.piece = piece

    def getCoords(self):
        return self.x, self.y

    def render(self):
        if self.piece is None:
            return "    "
        else:
            return self.piece.render()
