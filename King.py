from Piece import Piece, PieceIdentity


class King(Piece):
    def __init__(self, player):
        self.player = player
        self.identity = PieceIdentity.KING

    def renderName(self):
        return "K"

    def isMoveValid(self, initialX, initialY, finalX, finalY):
        deltaX = finalX - initialX
        deltaY = finalY - initialY

        # Check if out of range
        if abs(deltaX) > 1 or abs(deltaY) > 1:
            return False

        # Check if on axes
        if abs(deltaX) == abs(deltaY) and deltaX != 0:
            return True
        elif initialX == finalX:
            return True
        elif initialY == finalY:
            return True
        else:
            return False
