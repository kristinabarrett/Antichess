from Player import Player
from Piece import Piece, PieceIdentity


class Pawn(Piece):

    movedYet = False

    def __init__(self, player):
        self.player = player
        self.identity = PieceIdentity.PAWN

    def renderName(self):
        return "P"

    def isMoveValid(self, initialX, initialY, finalX, finalY):
        deltaX = finalX - initialX
        deltaY = finalY - initialY

        # White is on the bottom of the board.
        if self.player == Player.WHITE:
            if deltaY == -1 and abs(deltaX) <= 1:
                return True
            elif deltaY == -2 and deltaX == 0 and not self.movedYet:
                return True
            else:
                return False

        # Black is on top of the board.
        else:
            if deltaY == 1 and abs(deltaX) <= 1:
                return True
            elif deltaY == 2 and deltaX == 0 and not self.movedYet:
                return True
            else:
                return False

    @staticmethod
    def isDiagonal(initialX, initialY, finalX, finalY):
        deltaX = abs(initialX - finalX)
        deltaY = abs(initialY-finalY)
        return deltaX > 0 and deltaY > 0
