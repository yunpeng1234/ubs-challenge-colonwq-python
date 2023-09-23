from queue import PriorityQueue
import sys

### IMPORTANT: Remove any print() functions or rename any print functions/variables/string when submitting on CodePost
### The autograder will not run if it detects any print function.
from flask import Blueprint, jsonify, request

minichess = Blueprint("minichess", __name__)


# Helper functions to aid in your implementation. Can edit/remove
#############################################################################
######## Piece
#############################################################################
class Piece:
    horiVert = [(-1, 0), (0, -1), (1, 0), (0, 1)]
    diag = [(1, 1), (-1, -1), (1, -1), (-1, 1)]
    knight = [(1, 2), (-1, 2), (1, -2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1)]

    def __init__(self, position, color):
        self.position = position
        self.color = color

    def moves(self):
        pass


class King(Piece):
    def __init__(self, position, color):
        super().__init__(position, color)
        self.name = "King"
        self.value = 300

    def moves(self, board):
        res = []
        maxWidth = len(board[0])
        maxHeight = len(board)
        for x, y in self.horiVert:
            tempX = x + self.position[0]
            tempY = y + self.position[1]
            if (
                tempX >= 0
                and tempX < maxHeight
                and tempY >= 0
                and tempY < maxWidth
                and board[tempX][tempY] != self.color
            ):
                res.append((tempX, tempY))
        for x, y in self.diag:
            tempX = x + self.position[0]
            tempY = y + self.position[1]
            if (
                tempX >= 0
                and tempX < maxHeight
                and tempY >= 0
                and tempY < maxWidth
                and board[tempX][tempY] != self.color
            ):
                res.append((tempX, tempY))
        return res


class Rook(Piece):
    def __init__(self, position, color):
        super().__init__(position, color)
        self.name = "Rook"
        self.value = 5

    def moves(self, board):
        res = []
        maxWidth = len(board[0])
        maxHeight = len(board)
        maxDist = max(maxWidth, maxHeight)
        for x, y in self.horiVert:
            for dist in range(1, maxDist):
                tempX = x * dist + self.position[0]
                tempY = y * dist + self.position[1]
                if tempX >= 0 and tempX < maxHeight and tempY >= 0 and tempY < maxWidth:
                    if board[tempX][tempY] != self.color:
                        if board[tempX][tempY] == opponentColor(self.color):
                            res.append((tempX, tempY))
                            break
                        else:
                            res.append((tempX, tempY))
                    elif board[tempX][tempY] == self.color:
                        break
        return res


class Knight(Piece):
    def __init__(self, position, color):
        super().__init__(position, color)
        self.name = "Knight"
        self.value = 3

    def moves(self, board):
        res = []
        maxWidth = len(board[0])
        maxHeight = len(board)
        for x, y in self.knight:
            tempX = x + self.position[0]
            tempY = y + self.position[1]
            if (
                tempX >= 0
                and tempX < maxHeight
                and tempY >= 0
                and tempY < maxWidth
                and board[tempX][tempY] != self.color
            ):
                res.append((tempX, tempY))

        return res


class Bishop(Piece):
    def __init__(self, position, color):
        super().__init__(position, color)
        self.name = "Bishop"
        self.value = 3

    def moves(self, board):
        res = []
        maxWidth = len(board[0])
        maxHeight = len(board)
        maxDist = max(maxWidth, maxHeight)
        for x, y in self.diag:
            for dist in range(1, maxDist):
                tempX = x * dist + self.position[0]
                tempY = y * dist + self.position[1]
                if tempX >= 0 and tempX < maxHeight and tempY >= 0 and tempY < maxWidth:
                    if board[tempX][tempY] != self.color:
                        if board[tempX][tempY] == opponentColor(self.color):
                            res.append((tempX, tempY))
                            break
                        else:
                            res.append((tempX, tempY))
                    elif board[tempX][tempY] == self.color:
                        break
        return res


class Queen(Piece):
    def __init__(self, position, color):
        super().__init__(position, color)
        self.name = "Queen"
        self.value = 9

    def moves(self, board):
        res = []
        maxWidth = len(board[0])
        maxHeight = len(board)
        maxDist = max(maxWidth, maxHeight)
        for x, y in self.horiVert:
            for dist in range(1, maxDist):
                tempX = x * dist + self.position[0]
                tempY = y * dist + self.position[1]
                if tempX >= 0 and tempX < maxHeight and tempY >= 0 and tempY < maxWidth:
                    if board[tempX][tempY] != self.color:
                        if board[tempX][tempY] == opponentColor(self.color):
                            res.append((tempX, tempY))
                            break
                        else:
                            res.append((tempX, tempY))
                    elif board[tempX][tempY] == self.color:
                        break
        for x, y in self.diag:
            for dist in range(1, maxDist):
                tempX = x * dist + self.position[0]
                tempY = y * dist + self.position[1]
                if tempX >= 0 and tempX < maxHeight and tempY >= 0 and tempY < maxWidth:
                    if board[tempX][tempY] != self.color:
                        if board[tempX][tempY] == opponentColor(self.color):
                            res.append((tempX, tempY))
                            break
                        else:
                            res.append((tempX, tempY))
                    elif board[tempX][tempY] == self.color:
                        break
        return res

    pass


class Ferz(Piece):
    def __init__(self, position, color):
        super().__init__(position, color)
        self.name = "Ferz"
        self.value = 2

    def moves(self, board):
        res = []
        maxWidth = len(board[0])
        maxHeight = len(board)
        for x, y in self.diag:
            tempX = x + self.position[0]
            tempY = y + self.position[1]
            if (
                tempX >= 0
                and tempX < maxHeight
                and tempY >= 0
                and tempY < maxWidth
                and board[tempX][tempY] != self.color
            ):
                res.append((tempX, tempY))
        return res


class Princess(Piece):
    def __init__(self, position, color):
        super().__init__(position, color)
        self.name = "Princess"
        self.value = 6

    def moves(self, board):
        res = []
        maxWidth = len(board[0])
        maxHeight = len(board)
        maxDist = max(maxWidth, maxHeight)
        for x, y in self.diag:
            for dist in range(1, maxDist):
                tempX = x * dist + self.position[0]
                tempY = y * dist + self.position[1]
                if tempX >= 0 and tempX < maxHeight and tempY >= 0 and tempY < maxWidth:
                    if board[tempX][tempY] != self.color:
                        if board[tempX][tempY] == opponentColor(self.color):
                            res.append((tempX, tempY))
                            break
                        else:
                            res.append((tempX, tempY))
                    elif board[tempX][tempY] == self.color:
                        break
        for x, y in self.knight:
            tempX = x + self.position[0]
            tempY = y + self.position[1]
            if (
                tempX >= 0
                and tempX < maxHeight
                and tempY >= 0
                and tempY < maxWidth
                and board[tempX][tempY] != self.color
            ):
                res.append((tempX, tempY))
        return res

    pass


class Empress(Piece):
    def __init__(self, position, color):
        super().__init__(position, color)
        self.name = "Empress"
        self.value = 8

    def moves(self, board):
        res = []
        maxWidth = len(board[0])
        maxHeight = len(board)
        maxDist = max(maxWidth, maxHeight)
        for x, y in self.horiVert:
            for dist in range(1, maxDist):
                tempX = x * dist + self.position[0]
                tempY = y * dist + self.position[1]
                if tempX >= 0 and tempX < maxHeight and tempY >= 0 and tempY < maxWidth:
                    if board[tempX][tempY] != self.color:
                        if board[tempX][tempY] == opponentColor(self.color):
                            res.append((tempX, tempY))
                            break
                        else:
                            res.append((tempX, tempY))
                    elif board[tempX][tempY] == self.color:
                        break
        for x, y in self.knight:
            tempX = x + self.position[0]
            tempY = y + self.position[1]
            if (
                tempX >= 0
                and tempX < maxHeight
                and tempY >= 0
                and tempY < maxWidth
                and board[tempX][tempY] != self.color
            ):
                res.append((tempX, tempY))
        return res


class Pawn(Piece):
    def __init__(self, position, color):
        super().__init__(position, color)
        self.name = "Pawn"
        self.value = 1

    def moves(self, board):
        res = []
        tempX = self.position[0]
        tempY = self.position[1]
        maxWidth = len(board[0])
        maxHeight = len(board)
        if self.color == 0:
            if tempX + 1 < maxHeight and board[tempX + 1][tempY] == -1:
                res.append((tempX + 1, tempY))
            if (
                tempX + 1 < maxHeight
                and tempY - 1 >= 0
                and board[tempX + 1][tempY - 1] == opponentColor(self.color)
            ):
                res.append((tempX + 1, tempY - 1))
            if (
                tempX + 1 < maxHeight
                and tempY + 1 < maxWidth
                and board[tempX + 1][tempY + 1] == opponentColor(self.color)
            ):
                res.append((tempX + 1, tempY + 1))
        else:
            if tempX - 1 >= 0 and board[tempX - 1][tempY] == -1:
                res.append((tempX - 1, tempY))
            if (
                tempX - 1 >= 0
                and tempY - 1 >= 0
                and board[tempX - 1][tempY - 1] == opponentColor(self.color)
            ):
                res.append((tempX - 1, tempY - 1))
            if (
                tempX - 1 >= 0
                and tempY + 1 < maxWidth
                and board[tempX - 1][tempY + 1] == opponentColor(self.color)
            ):
                res.append((tempX - 1, tempY + 1))
        return res


#############################################################################
######## State
#############################################################################
# Black is 1 White is 0 empty space is -1
class State:
    def __init__(self, gameboard) -> None:
        self.whitePieces = {}
        self.blackPieces = {}
        self.board = [[-1 for _ in range(5)] for _ in range(5)]
        self.blackKing = {}
        self.whiteKing = {}
        for r, c in gameboard.keys():
            x, y = decode((r, c))
            piece, player = gameboard[(r, c)]
            if player == "Black":
                if piece == "King":
                    self.blackKing[(x, y)] = createPiece([piece, [x, y]], 1)
                self.blackPieces[(x, y)] = createPiece([piece, [x, y]], 1)
                self.board[x][y] = 1
            else:
                if piece == "King":
                    self.whiteKing[(x, y)] = createPiece([piece, [x, y]], 0)
                self.whitePieces[(x, y)] = createPiece([piece, [x, y]], 0)
                self.board[x][y] = 0

    def get_valid_moves(self, color):
        res = []
        if color == 0:  # White/ Max
            for position in self.whitePieces.keys():
                piece = self.whitePieces[position]
                moves = piece.moves(self.board)
                pieceMoves = list(map(lambda x: (position, x), moves))
                res.extend(pieceMoves)
        else:
            for position in self.blackPieces.keys():
                piece = self.blackPieces[position]
                moves = piece.moves(self.board)
                pieceMoves = list(map(lambda x: (position, x), moves))
                res.extend(pieceMoves)
        return res

    def evaluate(self):
        val = 0
        for pos in self.whitePieces.keys():
            val += self.whitePieces[pos].value
        for pos in self.blackPieces.keys():
            val -= self.blackPieces[pos].value
        return val

    def isTerminal(self):
        return len(self.blackKing) == 0 or len(self.whiteKing) == 0

    # Gives the move,  followed by the piece that is captured
    def move(self, fromMove, toMove, color):
        pieceCaptured = None
        if color == 0:  # White Player
            oldX, oldY = fromMove
            newX, newY = toMove
            # Check if captures a black piece
            if (newX, newY) in self.blackPieces:
                if (newX, newY) in self.blackKing:
                    # Check if captures a king
                    del self.blackKing[(newX, newY)]
                pieceCaptured = self.blackPieces[(newX, newY)]
                del self.blackPieces[(newX, newY)]
            pieceToMove = self.whitePieces[fromMove]
            if pieceToMove.name == "King":
                del self.whiteKing[(oldX, oldY)]
                self.whiteKing[(newX, newY)] = pieceToMove
            del self.whitePieces[fromMove]
            pieceToMove.position = [newX, newY]
            self.whitePieces[toMove] = pieceToMove
            # Change the board
            self.board[newX][newY] = 0
            self.board[oldX][oldY] = -1
            return pieceCaptured, pieceToMove, fromMove
        else:  # Black Player
            oldX, oldY = fromMove
            newX, newY = toMove
            # Capture a  white piece
            if (newX, newY) in self.whitePieces:
                if (newX, newY) in self.whiteKing:
                    del self.whiteKing[(newX, newY)]
                pieceCaptured = self.whitePieces[(newX, newY)]
                del self.whitePieces[(newX, newY)]
            pieceToMove = self.blackPieces[fromMove]
            if pieceToMove.name == "King":
                del self.blackKing[(oldX, oldY)]
                self.blackKing[(newX, newY)] = pieceToMove
            del self.blackPieces[fromMove]
            # King move
            pieceToMove.position = [newX, newY]
            self.blackPieces[toMove] = pieceToMove
            self.board[newX][newY] = 1
            self.board[oldX][oldY] = -1
            return pieceCaptured, pieceToMove, fromMove

    def unmove(self, pieceCaptured, pieceMoved, fromMove, color):
        # White player
        if color == 0:
            currX, currY = pieceMoved.position
            x, y = fromMove  # Where it came from
            # No piece taken
            if pieceCaptured is None:
                self.board[x][y] = 0
                # Empty space in new position
                self.board[currX][currY] = -1
            else:
                self.board[x][y] = 0
                # Piece placed back there
                self.board[currX][currY] = 1
                if pieceCaptured.name == "King":
                    self.blackKing[(currX, currY)] = pieceCaptured
                self.blackPieces[(currX, currY)] = pieceCaptured
            # Delete current location
            del self.whitePieces[(currX, currY)]
            pieceMoved.position = [x, y]
            self.whitePieces[(x, y)] = pieceMoved
            if pieceMoved.name == "King":
                # Unmove the king
                del self.whiteKing[(currX, currY)]
                self.whiteKing[(x, y)] = pieceMoved
        else:
            currX, currY = pieceMoved.position
            x, y = fromMove  # Where it came from
            # No piece taken
            if pieceCaptured is None:
                self.board[x][y] = 1
                # Empty space in new position
                self.board[currX][currY] = -1
            else:
                self.board[x][y] = 1
                # Piece placed back there
                self.board[currX][currY] = 0
                if pieceCaptured.name == "King":
                    self.whiteKing[(currX, currY)] = pieceCaptured
                self.whitePieces[(currX, currY)] = pieceCaptured
            # Delete current location
            del self.blackPieces[(currX, currY)]
            pieceMoved.position = [x, y]
            self.blackPieces[(x, y)] = pieceMoved
            if pieceMoved.name == "King":
                # Unmove the king
                del self.blackKing[(currX, currY)]
                self.blackKing[(x, y)] = pieceMoved


def maxValue(state, alpha, beta, depth):
    if depth == 0 or state.isTerminal():
        return None, state.evaluate()
    else:
        bestValue = -float("inf")
        bestMove = None
        moves = state.get_valid_moves(0)
        # ((fromX, fromY) , (toX, toY))
        for move in moves:
            currPos, nextPos = move
            pieceCaptured, pieceToMove, fromMove = state.move(
                currPos, nextPos, 0
            )  # White Player
            tempMove = saveMove(currPos, nextPos)
            move, newValue = minValue(state, alpha, beta, depth - 1)
            state.unmove(pieceCaptured, pieceToMove, fromMove, 0)
            if newValue > bestValue:
                bestMove = tempMove
                bestValue = newValue
                alpha = max(alpha, bestValue)
            if bestValue >= beta:
                break
        return bestMove, bestValue


def minValue(state, alpha, beta, depth):
    if depth == 0 or state.isTerminal():
        return None, state.evaluate()
    else:
        bestValue = float("inf")
        bestMove = None
        moves = state.get_valid_moves(1)
        for move in moves:
            currPos, nextPos = move
            pieceCaptured, pieceToMove, fromMove = state.move(
                currPos, nextPos, 1
            )  # Black Player
            tempMove = saveMove(currPos, nextPos)
            move, newValue = maxValue(state, alpha, beta, depth - 1)
            state.unmove(pieceCaptured, pieceToMove, fromMove, 1)
            if newValue < bestValue:
                bestMove = tempMove
                bestValue = newValue
                beta = min(beta, bestValue)
            if bestValue <= alpha:
                break
        return bestMove, bestValue


# Implement your minimax with alpha-beta pruning algorithm here.
def ab(gameboard):
    state = State(gameboard)
    alpha = -float("inf")
    beta = float("inf")
    move, next_state = maxValue(state, alpha, beta, 5)
    return move


def calculate(state, piece, position):
    x, y = piece.position
    if state.board[x][y] == -1:
        return -piece.value
    else:
        return -1


def saveMove(fromMove, toMove):
    return (encode(fromMove), encode(toMove))


def encode(position):
    x, y = position
    return (chr(y + 97), x)


def decode(position):
    y, x = position
    return (x, ord(y) - 97)


#############################################################################
######## Parser function and helper functions
#############################################################################
### DO NOT EDIT/REMOVE THE FUNCTION BELOW###
# Return number of rows, cols, grid containing obstacles and step costs of coordinates, enemy pieces, own piece, and goal positions
def parse(testcase):
    handle = open(testcase, "r")

    get_par = lambda x: x.split(":")[1]
    rows = int(get_par(handle.readline()))  # Integer
    cols = int(get_par(handle.readline()))  # Integer
    gameboard = {}

    enemy_piece_nums = get_par(handle.readline()).split()
    num_enemy_pieces = 0  # Read Enemy Pieces Positions
    for num in enemy_piece_nums:
        num_enemy_pieces += int(num)

    handle.readline()  # Ignore header
    for i in range(num_enemy_pieces):
        line = handle.readline()[1:-2]
        coords, piece = add_piece(line)
        gameboard[coords] = (piece, "Black")

    own_piece_nums = get_par(handle.readline()).split()
    num_own_pieces = 0  # Read Own Pieces Positions
    for num in own_piece_nums:
        num_own_pieces += int(num)

    handle.readline()  # Ignore header
    for i in range(num_own_pieces):
        line = handle.readline()[1:-2]
        coords, piece = add_piece(line)
        gameboard[coords] = (piece, "White")

    return rows, cols, gameboard


def opponentColor(color):
    return [1, 0][color]


def add_piece(comma_seperated) -> Piece:
    piece, ch_coord = comma_seperated.split(",")
    r, c = from_chess_coord(ch_coord)
    return [(r, c), piece]


def from_chess_coord(ch_coord):
    return (int(ch_coord[1:]), ord(ch_coord[0]) - 97)


def createPiece(piece, color):
    pieceName = piece[0]
    coord = piece[1]
    letter = pieceName[0]
    if letter == "Q":
        return Queen(coord, color)
    elif letter == "B":
        return Bishop(coord, color)
    elif letter == "R":
        return Rook(coord, color)
    elif letter == "K":
        if pieceName[1] == "n":
            return Knight(coord, color)
        else:
            return King(coord, color)
    elif letter == "F":
        return Ferz(coord, color)
    elif letter == "P":
        if pieceName[1] == "r":
            return Princess(coord, color)
        else:
            return Pawn(coord, color)
    else:
        return Empress(coord, color)


# You may call this function if you need to set up the board
def setUpBoard():
    config = sys.argv[1]
    rows, cols, gameboard = parse(config)


### DO NOT EDIT/REMOVE THE FUNCTION HEADER BELOW###
# Chess Pieces: King, Queen, Knight, Bishop, Rook, Princess, Empress, Ferz, Pawn (First letter capitalized)
# Colours: White, Black (First Letter capitalized)
# Positions: Tuple. (column (String format), row (Int)). Example: ('a', 0)

# Parameters:
# gameboard: Dictionary of positions (Key) to the tuple of piece type and its colour (Value). This represents the current pieces left on the board.
# Key: position is a tuple with the x-axis in String format and the y-axis in integer format.
# Value: tuple of piece type and piece colour with both values being in String format. Note that the first letter for both type and colour are capitalized as well.
# gameboard example: {('a', 0) : ('Queen', 'White'), ('d', 10) : ('Knight', 'Black'), ('g', 25) : ('Rook', 'White')}
#
# Return value:
# move: A tuple containing the starting position of the piece being moved to the new ending position for the piece. x-axis in String format and y-axis in integer format.
# move example: (('a', 0), ('b', 3))


def studentAgent(gameboard):
    # You can code in here but you cannot remove this function, change its parameter or change the return type
    move = ab(gameboard)
    return move  # Format to be returned (('a', 0), ('b', 3))


pieceMapping = {
    "\u2659": ("Pawn", "White"),
    "\u265F": ("Pawn", "Black"),
    "\u2656": ("Rook", "White"),
    "\u265C": ("Rook", "Black"),
    "\u2658": ("Knight", "White"),
    "\u265E": ("Knight", "Black"),
    "\u2657": ("Bishop", "White"),
    "\u265D": ("Bishop", "Black"),
    "\u2655": ("Queen", "White"),
    "\u265B": ("Queen", "Black"),
    "\u2654": ("King", "White"),
    "\u265A": ("King", "Black"),
}


def parse(testcase):
    gameboard = {}
    for i in range(5):
        for j in range(5):
            if testcase[i][j] != "":
                gameboard[encode((i, j))] = pieceMapping[testcase[i][j].split("|")[0]]

    # get_par = lambda x: x.split(":")[1]
    # rows = int(get_par(handle.readline()))  # Integer
    # cols = int(get_par(handle.readline()))  # Integer
    # gameboard = {}

    # enemy_piece_nums = get_par(handle.readline()).split()
    # num_enemy_pieces = 0  # Read Enemy Pieces Positions
    # for num in enemy_piece_nums:
    #     num_enemy_pieces += int(num)

    # handle.readline()  # Ignore header
    # for i in range(num_enemy_pieces):
    #     line = handle.readline()[1:-2]
    #     coords, piece = add_piece(line)
    #     gameboard[coords] = (piece, "Black")

    # own_piece_nums = get_par(handle.readline()).split()
    # num_own_pieces = 0  # Read Own Pieces Positions
    # for num in own_piece_nums:
    #     num_own_pieces += int(num)

    # handle.readline()  # Ignore header
    # for i in range(num_own_pieces):
    #     line = handle.readline()[1:-2]
    #     coords, piece = add_piece(line)
    #     gameboard[coords] = (piece, "White")

    return gameboard


@minichess.route("/minichess", methods=["POST"])
def getCommon():
    w = request.json["board"]
    gameboard = parse(w)
    print(gameboard)
    a, b = ab(gameboard)
    c, d = decode(a)
    e, f = decode(b)
    return jsonify({"move": [c, d, e, f]})
