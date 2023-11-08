from enum import Enum

from Player import Player


class Piece:
    """Parent class for all pieces"""

    player = None
    identity = None

    def render(self):
        return ("B" if self.player == Player.BLACK else "W") + self.renderName()

    def renderName(self) -> str:
        pass


class PieceIdentity(Enum):
    KING = 0
    QUEEN = 1
    BISHOP = 2
    KNIGHT = 3
    ROOK = 4
    PAWN = 5



