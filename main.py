import os
import sys
from time import sleep

from Board import Board
from Player import Player


def main():
    board = Board()
    board.initializeBoard()
    runGame(board)
    exit(0)


def testRooks():
    board = Board()
    from Rook import Rook
    board.spaces[0][0].setPiece(Rook(Player.BLACK))
    board.spaces[7][0].setPiece(Rook(Player.BLACK))
    board.spaces[0][7].setPiece(Rook(Player.WHITE))
    board.spaces[7][7].setPiece(Rook(Player.WHITE))
    runGame(board)


def runGame(board):
    currentPlayer = None
    victory = None
    while True:
        currentPlayer = Player.BLACK if currentPlayer == Player.WHITE else Player.WHITE
        victory = victoryCheck(board, currentPlayer)
        if victory is not None:
            break
        takeTurn(board, currentPlayer)
    print("Winner: {}!".format(showPlayer(victory)))


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def showPlayer(player):
    return "White" if player == Player.WHITE else "Black"


def takeTurn(board: Board, currentPlayer):
    """Allow a player to make a move using the logic specified in Board class."""
    showBoard(board)
    print("\nIt is {}'s turn".format(showPlayer(currentPlayer)))

    # Check for autocapture
    caps = board.checkForCaptures(currentPlayer)
    if len(caps) == 1:
        cap = caps[0]
        print("\nAutomatic capture: {} -> {}".format(Board.rowColFromCoords(cap[0]), Board.rowColFromCoords(cap[1])))
        sleep(1)
        board.movePiece(currentPlayer, cap[0], cap[1])
        return
    elif len(caps) > 0:
        print("Available captures:", Board.showCaptures(caps))

    moveX, moveY = readInput()
    result, reason = board.movePiece(currentPlayer, moveX, moveY)
    if not result:
        print(reason + ".")
        print("Please try again,", showPlayer(currentPlayer))
        sleep(3)
        takeTurn(board, currentPlayer)


def victoryCheck(board, currentPlayer) -> Player:
    """Returns enum of black, white, or None depending on if/who the winner is."""
    currentPlayerSpaces, enemySpaces = board.getAllOccupiedSpaces(currentPlayer)
    enemyPlayer = Player.BLACK if currentPlayer == Player.WHITE else Player.WHITE
    if len(currentPlayerSpaces) == 0:
        return currentPlayer
    if len(enemySpaces) == 0:
        return enemyPlayer
    return None


def readInput():
    """Requests and takes in a move from the player. Returns coordinates of initial and final spaces."""
    initialBoardCoord = input("Please select a piece to move: ")
    finalBoardCoord = input("Select destination: ")
    return Board.coordsFromRowCol(initialBoardCoord), Board.coordsFromRowCol(finalBoardCoord)


def showBoard(board):
    """Prints the board in ASCII format to the console."""
    # clear()
    print(board.render())


if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == "rooks":
            testRooks()
    else:
        main()
