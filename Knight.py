from Piece import Piece, PieceIdentity


class Knight(Piece):
    def __init__(self, player):
        self.player = player
        self.identity = PieceIdentity.KNIGHT

    def renderName(self):
        return "H"

    def isMoveValid(self, initialX, initialY, finalX, finalY):
        deltaX = finalX - initialX
        deltaY = finalY - initialY

        if abs(deltaX) == 2 and abs(deltaY) == 1:
            return True
        elif abs(deltaX) == 1 and abs(deltaY) == 2:
            return True
        else:
            return False
