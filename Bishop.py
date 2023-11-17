from Piece import Piece, PieceIdentity


class Bishop(Piece):
    def __init__(self, player):
        self.player = player
        self.identity = PieceIdentity.BISHOP

    def renderName(self):
        return "B"

    def isMoveValid(self, initialX, initialY, finalX, finalY):
        deltaX = finalX - initialX
        deltaY = finalY - initialY

        # Check if on diagonals
        if abs(deltaX) == abs(deltaY) and deltaX != 0:
            return True
        else:
            return False
