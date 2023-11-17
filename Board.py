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
                    (result, reason) = self.canMovePiece(currentPlayer, currentSpace.getCoords(),
                                                         enemySpace.getCoords())
                    if result:
                        self.possibleCaptureCoords.append((currentSpace.getCoords(), enemySpace.getCoords()))
        return self.possibleCaptureCoords

    def movePiece(self, currentPlayer, initialCoord, finalCoord):
        """Parameters will be tuples of x,y coordinates"""
        (result, reason) = self.canMovePiece(currentPlayer, initialCoord, finalCoord)
        if len(self.checkForCaptures(currentPlayer)) > 0:
            captureCheck = False
            caps = self.checkForCaptures(currentPlayer)
            for coords in caps:
                if coords[0] == initialCoord and coords[1] == finalCoord:
                    captureCheck = True
                    break
            if not captureCheck:
                result = False
                capString = Board.showCaptures(caps)
                reason = "Possible capture(s) available: " + capString

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

        if initialCoord is None or len(initialCoord) != 2 or not isinstance(initialCoord[0], int) or not isinstance(
                initialCoord[1], int):
            return False, "Initial space is invalid"
        if finalCoord is None or len(finalCoord) != 2 or not isinstance(finalCoord[0], int) or not isinstance(
                finalCoord[1], int):
            return False, "Final space is invalid"
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
        if piece.identity == PieceIdentity.PAWN:
            diagonal = Pawn.isDiagonal(initialCoord[0], initialCoord[1], finalCoord[0], finalCoord[1])
            if (isACapture and not diagonal) or (not isACapture and diagonal):
                return False, "Pawns can only move diagonally for captures"
        return True, "Move is valid"

    @staticmethod
    def checkOutOfBounds(coord):
        """Parameter will be tuple of x,y coordinates. Returns False if move is on the board, True if not"""
        if coord is None or len(coord) != 2:
            return True
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
        xCoords = range(initialX, finalX, directionX)
        yCoords = range(initialY, finalY, directionY)

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
            if curX == initialX and curY == initialY:
                continue
            curSpace = self.getSpace((curX, curY))
            if curSpace.piece is not None:
                return True
        return False

    def checkDestination(self, currentPlayer, coord):
        """Returns SPACE_EMPTY if destination is empty, SPACE_ENEMY if enemy piece, SPACE_FRIEND if friendly"""
        target = self.getSpace(coord)
        if target.piece is None:
            return SPACE_EMPTY
        if target.piece.player == currentPlayer:
            return SPACE_FRIEND
        if target.piece.player != currentPlayer:
            return SPACE_ENEMY

    def getSpace(self, coord) -> Space:
        """Returns a space object from the specified tuple"""
        return self.spaces[coord[0]][coord[1]]

    @staticmethod
    def toChar(n: int):
        """Returns none if n is out of bounds"""
        return "hgfedcba"[n].capitalize() if n in range(8) else None

    @staticmethod
    def fromChar(c: str):
        """Returns none if c out of bounds"""
        if len(c) > 1:
            return None
        f = "hgfedcba".find(c.lower())
        return f if f != -1 else None

    @staticmethod
    def coordsFromRowCol(rowCol: str):
        """
        A rowCol is a string, example: "A3". Returns a tuple of 0-indexed (x,y) coords.
        If either is a bad input, the whole result is None
        """
        try:
            if len(rowCol) < 2:
                return None
            y = Board.fromChar(rowCol[0])
            x = int(rowCol[1]) - 1
            return (x, y) if x is not None and int(y) in range(8) else None
        except:
            return None

    @staticmethod
    def rowColFromCoords(coords):
        """
        Inverse of coordsFromRowCol
        If either is a bad input, the whole result is None
        """
        try:
            if len(coords) < 2:
                return None
            y = Board.toChar(coords[1])
            x = str(coords[0] + 1)
            return "{}{}".format(y, x) if y is not None and coords[0] in range(8) else None
        except:
            return None

    @staticmethod
    def showCaptures(caps):
        """Returns a string formatted to display the given list of captures (as from checkForCaptures())"""
        return ", ".join("({} -> {})".format(Board.rowColFromCoords(c[0]), Board.rowColFromCoords(c[1])) for c in caps)

    def render(self):
        res = " "

        for x in range(8):
            res += "   " + str(x + 1) + " "
        res += "\n"
        for x in range(8):

            res += "  "
            for y in range(8):
                res += "┼────"
            res += "┼\n" + Board.toChar(x) + " "
            for y in range(8):
                space = self.spaces[y][x]  # Render by row,column
                res += "│" + space.render()
            res += "│\n"

        res += "  "
        for y in range(8):
            res += "┴────"
        res += "┴\n  "
        return res
