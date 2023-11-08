from Bishop import Bishop
from King import King
from Knight import Knight
from Pawn import Pawn
from Piece import PieceIdentity
from Queen import Queen
from Rook import Rook
from Space import Space
from Player import Player

SPACE_EMPTY = 0
SPACE_ENEMY = 1
SPACE_FRIEND = 2


class Board:
    """Board class holds all spaces"""

    spaces = []
    # Variables holding caches, do not access internally.
    currentPlayerSpaces = None
    enemyPlayerSpaces = None
    possibleCaptureCoords = None

    def __init__(self):

        for x in range(8):
            self.spaces.append([])
            for y in range(8):
                self.spaces[x].append(Space(x, y))

    def initializeBoard(self):
        self.spaces[0][0].setPiece(Rook(Player.BLACK))
        self.spaces[1][0].setPiece(Knight(Player.BLACK))
        self.spaces[2][0].setPiece(Bishop(Player.BLACK))
        self.spaces[3][0].setPiece(Queen(Player.BLACK))
        self.spaces[4][0].setPiece(King(Player.BLACK))
        self.spaces[5][0].setPiece(Bishop(Player.BLACK))
        self.spaces[6][0].setPiece(Knight(Player.BLACK))
        self.spaces[7][0].setPiece(Rook(Player.BLACK))

        self.spaces[0][7].setPiece(Rook(Player.WHITE))
        self.spaces[1][7].setPiece(Knight(Player.WHITE))
        self.spaces[2][7].setPiece(Bishop(Player.WHITE))
        self.spaces[3][7].setPiece(Queen(Player.WHITE))
        self.spaces[4][7].setPiece(King(Player.WHITE))
        self.spaces[5][7].setPiece(Bishop(Player.WHITE))
        self.spaces[6][7].setPiece(Knight(Player.WHITE))
        self.spaces[7][7].setPiece(Rook(Player.WHITE))

        for i in range(8):
            self.spaces[i][1].setPiece(Pawn(Player.BLACK))
            self.spaces[i][6].setPiece(Pawn(Player.WHITE))

    def getAllOccupiedSpaces(self, currentPlayer):
        """Returns a tuple of two lists containing all spaces occupied by each player.
        The first list is the current player"""
        if self.enemyPlayerSpaces is None or self.currentPlayerSpaces is None:
            self.enemyPlayerSpaces = []
            self.currentPlayerSpaces = []
            for x in range(8):
                for y in range(8):
                    currentSpace = self.getSpace((x, y))
                    destinationType = self.checkDestination(currentPlayer, (x, y))
                    if destinationType == SPACE_EMPTY:
                        continue
                    if destinationType == SPACE_ENEMY:
                        self.enemyPlayerSpaces.append(currentSpace)
                    if destinationType == SPACE_FRIEND:
                        self.currentPlayerSpaces.append(currentSpace)
        return self.currentPlayerSpaces, self.enemyPlayerSpaces

    def clearCaches(self):
        """Clears the cache of occupied spaces."""
        self.enemyPlayerSpaces = None
        self.currentPlayerSpaces = None
        self.possibleCaptureCoords = None

    def checkForCaptures(self, currentPlayer):
        """Find all possible captures for the current player.
        Returns a list of tuples of initial and final coordinates"""
        if self.possibleCaptureCoords is None:
            (currentPlayerSpaces, enemyPlayerSpaces) = self.getAllOccupiedSpaces(currentPlayer)
            self.possibleCaptureCoords = []

            for currentSpace in currentPlayerSpaces:
                for enemySpace in enemyPlayerSpaces:
                    (result, reason) = self.canMovePiece(currentPlayer, currentSpace.getCoords(), enemySpace.getCoords())
                    if result:
                        self.possibleCaptureCoords.append((currentSpace.getCoords(), enemySpace.getCoords()))
        return self.possibleCaptureCoords

    def movePiece(self, currentPlayer, initialCoord, finalCoord):
        """Parameters will be tuples of x,y coordinates"""
        (result, reason) = self.canMovePiece(currentPlayer, initialCoord, finalCoord)
        if len(self.checkForCaptures(currentPlayer)) > 0:
            captureCheck = False
            for coords in self.checkForCaptures(currentPlayer):
                if coords[0] == initialCoord and coords[1] == finalCoord:
                    captureCheck = True
                    break
            if not captureCheck:
                result = False
                reason = "Possible Capture available"

        if result:
            initialSpace = self.getSpace(initialCoord)
            finalSpace = self.getSpace(finalCoord)
            finalSpace.setPiece(initialSpace.piece)
            initialSpace.setPiece(None)
            if finalSpace.piece.identity == PieceIdentity.PAWN:
                finalSpace.piece.movedYet = True
            self.clearCaches()
        return result, reason

    def canMovePiece(self, currentPlayer, initialCoord, finalCoord):
        """Parameters will be tuples of x,y coordinates. Returns bool indicating legality of move"""

        if Board.checkOutOfBounds(initialCoord):
            return False, "Initial space is out of bounds"
        if Board.checkOutOfBounds(finalCoord):
            return False, "Destination space is out of bounds"

        initialSpace = self.getSpace(initialCoord)
        destinationType = self.checkDestination(currentPlayer, finalCoord)
        isACapture = destinationType == SPACE_ENEMY

        piece = initialSpace.piece
        if piece is None:
            return False, "There is no piece to move on that space"
        if piece.player != currentPlayer:
            return False, "That's not your piece to move"
        if not piece.isMoveValid(initialCoord[0], initialCoord[1], finalCoord[0], finalCoord[1]):
            return False, "That piece can't move like that"
        if piece.identity != PieceIdentity.KNIGHT and self.searchPiecesInPath(initialCoord, finalCoord):
            return False, "Another piece is in the way"
        if destinationType == SPACE_FRIEND:
            return False, "You can't capture your own piece"
        if piece.identity == PieceIdentity.PAWN and not isACapture and Pawn.isDiagonal(initialCoord[0], initialCoord[1], finalCoord[0], finalCoord[1]):
            return False, "Pawns can only move diagonally for captures"
        return True, "Move is valid"

    @staticmethod
    def checkOutOfBounds(coord):
        """Parameter will be tuple of x,y coordinates. Returns False if move is on the board, True if not"""
        if coord[0] < 0 or coord[0] > 7:
            return True
        if coord[1] < 0 or coord[1] > 7:
            return True
        return False

    def searchPiecesInPath(self, initialCoord, finalCoord):
        """Parameters will be tuples of x,y coordinates
        Returns True if something is in the way, False if the way is clear"""
        initialX = initialCoord[0]
        initialY = initialCoord[1]
        finalX = finalCoord[0]
        finalY = finalCoord[1]

        # get direction of step on each axis
        directionX = -1 if initialX > finalX else 1
        directionY = -1 if initialY > finalY else 1

        # Lists of space indices between initial and final destinations
        xCoords = range(initialX, finalX - directionX, directionX)
        yCoords = range(initialY, finalY - directionY, directionY)

        # Check if either list is empty. If so, fill with initial/final value (they will be the same).
        if len(xCoords) == 0:
            xCoords = []
            for i in yCoords:
                xCoords.append(initialX)
        if len(yCoords) == 0:
            yCoords = []
            for i in xCoords:
                yCoords.append(initialY)

        # Walk from the starting x to the ending x.
        for index, curX in enumerate(xCoords):
            curY = yCoords[index]
            curSpace = self.getSpace((curX, curY))
            if curSpace.piece is not None:
                return True
        return False

    def checkDestination(self, currentPlayer, coord):
        """Returns SPACE_EMPTY if destination is empty, SPACE_ENEMY if enemy piece, SPACE_FRIEND if friendly"""
        target = self.getSpace(coord)
        if target.piece is None:
            return SPACE_EMPTY
        if target.piece.player != currentPlayer:
            return SPACE_ENEMY
        if target.piece.player == currentPlayer:
            return SPACE_FRIEND

    def getSpace(self, coord) -> Space:
        """Returns a space object from the specified tuple"""
        return self.spaces[coord[0]][coord[1]]

    def render(self):
        res = ""
        for xColumn in self.spaces:
            res += "+--"
            for space in xColumn:
                res += "|" + space.render() + "|"
            res += "\n"
        return res
