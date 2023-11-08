from Piece import Piece, PieceIdentity


class Queen(Piece):
    def __init__(self, player):
        self.player = player
        self.identity = PieceIdentity.QUEEN

    def isMoveValid(self, initialX, initialY, finalX, finalY):
        deltaX = finalX - initialX
        deltaY = finalY - initialY

        # Check if on axes
        if abs(deltaX) == abs(deltaY) and deltaX != 0:
            return True
        elif deltaX == 0 and deltaY != 0:
            return True
        elif deltaY == 0 and deltaX != 0:
            return True
        else:
            return False
