from Piece import Piece, PieceIdentity


class Rook(Piece):
    def __init__(self, player):
        self.player = player
        self.identity = PieceIdentity.ROOK

    def isMoveValid(self, initialX, initialY, finalX, finalY):

        # Check for zero movement
        if initialX == finalX and initialY == finalY:
            return False

        # Check if on axes
        if initialX == finalX:
            return True
        elif initialY == finalY:
            return True
        else:
            return False
