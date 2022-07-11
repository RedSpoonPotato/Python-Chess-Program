from piece import *
import copy

File = {
    'a': 0, 
    'b': 1,
    'c': 2,
    'd': 3,
    'e': 4,
    'f': 5,
    'g': 6,
    'h': 7,
    'UF': None
    }
Rank = {
    '1': 0,
    '2': 1,
    '3': 2,
    '4': 3,
    '5': 4,
    '6': 5,
    '7': 6,
    '8': 7,
    'UR:': None
}

class Position:
    def __init__(self, file:int = None, rank:int = None):
        self.file = file
        self.rank = rank
    def __repr__(self) -> str:
        return "({}, {})".format(self.file, self.rank)


class Move:
    def __init__(self, iPos:Position, fPos:Position):
        self.iPos = iPos
        self.fPos = fPos 

# replace PositionList struct with list
# replace MoveList struct with list

class Board:

    def __init__(self):
        self.grid = [[Piece() for rank in range(8)] for file in range(8)]
        self.whiteUpForEnPassant = [False for x in range(8)]
        self.blackUpForEnPassant = [False for x in range(8)]
        self.whiteKingMoved = False
        self.blackKingMoved = False
        self.whiteRookMoved = [False for x in range(2)]
        self.blackRookMoved = [False for x in range(2)]

    def __repr__(self) -> str:
        # grid
        s = str(self.grid[0])
        for x in range(1,8):
            s += '\n'
            s += str(self.grid[x])
        # special info
        s += ('\nWHITE Passant: ' + str(self.whiteUpForEnPassant) + ' KingMoved: ' + 
            str([self.whiteKingMoved]) + ' RookMoved ' + str(self.whiteRookMoved))
        s += ('\nBLACK Passant: ' + str(self.blackUpForEnPassant) + ' KingMoved: ' + 
            str([self.blackKingMoved]) + ' RookMoved ' + str(self.blackRookMoved))
        return s
    
def startingBoard(self: Board) -> None:
    # handling colors
    for rank in range(0,2):
        for file in range(0,8):
            self.grid[file][rank].color = 'white'
    for rank in range(2,6):
        for file in range(0,8):
            self.grid[file][rank].color = 'NoColor'
    for rank in range(6,8):
        for file in range(0,8):
            self.grid[file][rank].color = 'black'
    # handling piece types
    # (rank 1)
    self.grid[File['a']][Rank['1']].pieceType = 'rook'
    self.grid[File['b']][Rank['1']].pieceType = 'knight'
    self.grid[File['c']][Rank['1']].pieceType = 'bishop'
    self.grid[File['d']][Rank['1']].pieceType = 'queen'
    self.grid[File['e']][Rank['1']].pieceType = 'king'
    self.grid[File['f']][Rank['1']].pieceType = 'bishop'
    self.grid[File['g']][Rank['1']].pieceType = 'knight'
    self.grid[File['h']][Rank['1']].pieceType = 'rook'
    # (rank 2)
    for file in range(0,8): 
        self.grid[file][Rank['2']].pieceType = 'pawn'
    # (rank 3 - 6)
    for rank in range(2,6):
        for file in range(0,8):
            self.grid[file][rank].pieceType = 'empty'
    # (rank 7)
    for file in range(0,8): 
        self.grid[file][Rank['7']].pieceType = 'pawn'
    # (rank 8)
    self.grid[File['a']][Rank['8']].pieceType = 'rook'
    self.grid[File['b']][Rank['8']].pieceType = 'knight'
    self.grid[File['c']][Rank['8']].pieceType = 'bishop'
    self.grid[File['d']][Rank['8']].pieceType = 'queen'
    self.grid[File['e']][Rank['8']].pieceType = 'king'
    self.grid[File['f']][Rank['8']].pieceType = 'bishop'
    self.grid[File['g']][Rank['8']].pieceType = 'knight'
    self.grid[File['h']][Rank['8']].pieceType = 'rook'
    # handling extra board information
    self.blackKingMoved = False
    self.blackRookMoved[0] = False
    self.blackRookMoved[1] = False
    self.whiteKingMoved = False
    self.whiteRookMoved[0] = False
    self.whiteRookMoved[1] = False
    for x in range(0,8):
        self.blackUpForEnPassant[x] = False
        self.whiteUpForEnPassant[x] = False

def LocateKing(self: Board, color: str,) -> Position:
    kingPos = Position()
    for rank in range(0,8):
        for file in range(0,8):
            if self.grid[file][rank].color == color and self.grid[file][rank].pieceType == 'king':
                kingPos.file = file
                kingPos.rank = rank
                return kingPos

# Moving pieces

# does not check if move is legal, nor does it update board information pertaining to castling/enPassant
def DumbMovePiece(self: Board, iPos: Position, fPos: Position): 
    self.grid[fPos.file][fPos.rank].pieceType = self.grid[iPos.file][iPos.rank].pieceType
    self.grid[fPos.file][fPos.rank].color = self.grid[iPos.file][iPos.rank].color
    self.grid[iPos.file][iPos.rank].pieceType = 'empty'
    self.grid[iPos.file][iPos.rank].color = 'NoColor'

# helper function for SmartMovePiece()
def BoardUpkeep(self: Board, iPos: Position, fPos: Position):
    pieceType = self.grid[iPos.file][iPos.rank].pieceType
    pieceColor = self.grid[iPos.file][iPos.rank].color
    # pawn info upkeep
    for x in range(8):
        self.blackUpForEnPassant[x] = False
        self.whiteUpForEnPassant[x] = False
    if pieceColor == 'white' and pieceType == 'pawn' and fPos.rank - iPos.rank == 2:
        self.whiteUpForEnPassant[iPos.file] = True
    elif pieceColor == 'black' and pieceType == 'pawn' and fPos.rank - iPos.rank == -2:
        self.blackUpForEnPassant[iPos.file] = True
    # king info upkeep
    if pieceColor == 'white' and pieceType == 'king' and self.whiteKingMoved == False:
        self.whiteKingMoved = True
    elif pieceColor == 'black' and pieceType == 'king' and self.blackKingMoved == False:
        self.blackKingMoved = True
    # rook info upkeep
    if pieceType == 'rook' and iPos.file == File['a'] and iPos.rank == Rank['1'] and self.whiteRookMoved[0] == False:
        self.whiteRookMoved[0] = True
    elif pieceType == 'rook' and iPos.file == File['h'] and iPos.rank == Rank['1'] and self.whiteRookMoved[1] == False:
        self.whiteRookMoved[1] = True
    elif pieceType == 'rook' and iPos.file == File['a'] and iPos.rank == Rank['8'] and self.blackRookMoved[0] == False:
        self.blackRookMoved[0] = True
    elif pieceType == 'rook' and iPos.file == File['h'] and iPos.rank == Rank['8'] and self.blackRookMoved[1] == False:
        self.blackRookMoved[1] = True
    # accounting for if an pieceType captures certain a rook that has not moved (set that position to hasMoved to not allow castling)
    if fPos.file == File['a'] and fPos.rank == Rank['1']:
        self.whiteRookMoved[0] = True
    elif fPos.file == File['h'] and fPos.rank == Rank['1']:
        self.whiteRookMoved[1] = True
    elif fPos.file == File['a'] and fPos.rank == Rank['8']:
        self.blackRookMoved[0] = True
    elif fPos.file == File['h'] and fPos.rank == Rank['8']:
        self.blackRookMoved[1] = True

# called by SmartMovePiece() to move the corresponding rook if castling is done
def CastlingRookMove(self: Board, finalKingPos: Position):
    rookInitial = copy.deepcopy(finalKingPos)
    rookFinal = copy.deepcopy(finalKingPos) 
    if (finalKingPos.file == File['c'] and finalKingPos.rank == Rank['8']) or finalKingPos.rank == Rank['1']:
        rookInitial.file = File['a']
        rookFinal.file = File['d']
    elif (finalKingPos.file == File['g'] and finalKingPos.rank == Rank['8']) or finalKingPos.rank == Rank['1']:
        rookInitial.file = File['h']
        rookFinal = File['f']
    self.BoardUpkeep(rookInitial, rookFinal)
    self.DumbMovePiece(rookInitial, rookFinal)


# assume that move has already been checked to be legal !!!
# helper function for SmartMovePiece() that tells function if move is a castling, pawn-promo, en-pessant, or something else
def CastleOrPromotionOrEnPessant(self: Board, iPos: Position, fPos: Position) -> int:
    type = self.grid[iPos.file][iPos.rank].pieceType
    color = self.grid[iPos.file][iPos.rank].color
    # if move is promotion
    if type == 'pawn' and ((color == 'white' and fPos.rank == Rank['8']) or (color == 'black' and fPos.rank == Rank['1'])):
        return 1
    # if move is castling
    elif type == 'king' and abs(fPos.file - iPos.file == 2):
        return 2
    # if move is en-pessant
    elif    (type == 'pawn' and self.grid[fPos.file][fPos.rank].pieceType == 'empty' 
                    and abs(fPos.file - iPos.file) == abs(fPos.rank - iPos.rank)):
        return 3
    else:
        return 0

# moves piece if legal, else will return an errorcode. If not intending to promote a pawn, can set promotedType to anything.
def SmartMovePiece(self: Board, iPos: Position, fPos: Position, promoType: pieceType) -> int:
    # determine if move is legal
    errorcode = Rules(self, iPos, fPos)
    if errorcode != 0:
        return errorcode # error detected
    # en pesssanting scenario
    if CastleOrPromotionOrEnPessant(self, iPos, fPos) == 3:
        enemyPos = Position(fPos.file, iPos.rank)
        BoardUpkeep(self, iPos, enemyPos)
        DumbMovePiece(self, iPos, enemyPos)
        BoardUpkeep(self, iPos, fPos)
        DumbMovePiece(self, enemyPos, fPos)
    # castling scenario
    elif CastleOrPromotionOrEnPessant(self, iPos, fPos) == 2:
        BoardUpkeep(self, iPos, fPos)
        DumbMovePiece(self, iPos, fPos)
        CastlingRookMove(self, fPos)
    # promotion scenario
    elif CastleOrPromotionOrEnPessant(self, iPos, fPos) == 1:
        BoardUpkeep(self, iPos, fPos)
        DumbMovePiece(self, iPos, fPos)
        self.grid[fPos.file][fPos.rank].pieceType = promoType
    # all other scenarios
    else:
        BoardUpkeep(self, iPos, fPos)
        DumbMovePiece(self, iPos, fPos)
    return 0

# general rules function that tells if a move is legal
def Rules(self, iPos: Position, fPos: Position) -> int:
    # error checking
    if iPos.rank == fPos.rank and iPos.file == fPos.file:
        return 5 # attemting to move a piece to the same spot
    if self.grid[iPos.file][iPos.rank].color == self.grid[fPos.file][fPos.rank].color:
        return 6 # attemping to move a piece to a spot where the same color resides
    if not(0 <= iPos.file <= 7) or not(0 <= iPos.rank <= 7):
        return 7 # attemping to move a piece that is outside the bounds of the board
    if not(0 <= fPos.file <= 7) or not(0 <= fPos.rank <= 7):
        return 8 # attemping to move a piece to a spot outside the bounds of the board
    # checking if move works ideally
    match self.grid[iPos.file][iPos.rank].pieceType:
        case 'empty':
            return 3 # attempting to move an 'empty' piece
        case 'king':
            movePossibleIdeally = KingRules(self, iPos, fPos)
        case 'queen':
            movePossibleIdeally = QueenRules(self, iPos, fPos)
        case 'bishop':
            movePossibleIdeally = BishopRules(self, iPos, fPos)
        case 'knight':
            movePossibleIdeally = KnightRules(self, iPos, fPos)
        case 'rook':
            movePossibleIdeally = RookRules(self, iPos, fPos)
        case 'pawn':
            movePossibleIdeally = PawnRules(self, iPos, fPos)
        case default:
            return 4 # piece is of unknown type
    if movePossibleIdeally == False:
        return 2 # attempting to move piece in such that way that is not even legal ideally
    # checking if move also works non-ideally
    tempBoard = copy.deepcopy(self)
    if CastleOrPromotionOrEnPessant(tempBoard, iPos, fPos) == 0:
        DumbMovePiece(tempBoard, iPos, fPos)
    # if move is en-pessant
    elif CastleOrPromotionOrEnPessant(tempBoard, iPos, fPos) == 3:
        enemyPos = Position(fPos.file, iPos.rank)
        DumbMovePiece(tempBoard, iPos, enemyPos)
        DumbMovePiece(tempBoard, enemyPos, fPos)
    # if move is castling
    elif CastleOrPromotionOrEnPessant(tempBoard, iPos, fPos) == 2:
        DumbMovePiece(tempBoard, iPos, fPos)
        CastlingRookMove(tempBoard, fPos)
    # if movie is pawn promo
    elif CastleOrPromotionOrEnPessant(tempBoard, iPos, fPos) == 1:
        DumbMovePiece(tempBoard, iPos, fPos)
        tempBoard.grid[fPos.file][fPos.rank].type = 'queen' #default value for promo, can change later
    if CheckForCheck(tempBoard,LocateKing(tempBoard, self.grid[iPos.file][iPos.rank].color)):
        return 1 # attempting to move a piece such that the player's king would be in check
    else:
        return 0 # move is legal

# modified rules() function for calling CheckForCheck(), only checks the ideal case
def ModifiedRules(self: Board, iPos: Position, fPos: Position) -> int:
    # error checking
    if iPos.rank == fPos.rank and iPos.file == fPos.file:
        return 5 # attemting to move a piece to the same spot
    if self.grid[iPos.file][iPos.rank].color == self.grid[fPos.file][fPos.rank].color:
        return 6 # attemping to move a piece to a spot where the same color resides
    if not(0 <= iPos.file <= 7) or not(0 <= iPos.rank <= 7):
        return 7 # attemping to move a piece that is outside the bounds of the board
    if not(0 <= fPos.file <= 7) or not(0 <= fPos.rank <= 7):
        return 8 # attemping to move a piece to a spot outside the bounds of the board
    # checking if move works ideally
    print("using match statement:",iPos,self.grid[iPos.file][iPos.rank],fPos, self.grid[fPos.file][fPos.rank])
    match self.grid[iPos.file][iPos.rank].pieceType:
        case 'empty':
            return 3 # attempting to move an 'empty' piece
        case 'king':
            movePossibleIdeally = KingRules(self, iPos, fPos)
        case 'queen':
            movePossibleIdeally = QueenRules(self, iPos, fPos)
        case 'bishop':
            movePossibleIdeally = BishopRules(self, iPos, fPos)
        case 'knight':
            movePossibleIdeally = KnightRules(self, iPos, fPos)
        case 'rook':
            movePossibleIdeally = RookRules(self, iPos, fPos)
        case 'pawn':
            movePossibleIdeally = PawnRules(self, iPos, fPos)
        case default:
            return 4 # piece is of unknown type
    if movePossibleIdeally == False:
        return 2 # attempting to move piece in such that way that is not even legal ideally
    else:
        return 0 # move is legal ideally
    
# helper functions for move ideally(remember to read instructions at top of Board.py source code)

def KingRules(self: Board, iPos: Position, fPos: Position) -> bool:
    # normal scenario
    if abs(fPos.file - iPos.file) <= 1 and abs(fPos.rank - iPos.rank) <= 1:
        return True
    # castling scenario
    if not(fPos.rank - iPos.rank == 0 and abs(fPos.file - iPos.file) == 2):
        return False
    kingColor = self.grid[iPos.file][iPos.rank].color
    if      kingColor == 'white' and self.whiteKingMoved == False: None
    elif    kingColor == 'black' and self.blackKingMoved == False: None
    else: return False
    if  (fPos.file == File['c'] and fPos.rank == Rank['1'] and kingColor == 'white' and 
        self.grid[File['b']][Rank['1']].pieceType == 'empty' and self.grid[File['c']][Rank['1']].pieceType == 'empty' and
        self.grid[File['d']][Rank['1']].pieceType == 'empty' and self.whiteRookMoved[0] == False):
        return True
    elif (fPos.file == File['g'] and fPos.rank == Rank['1'] and kingColor == 'white' and 
        self.grid[File['f']][Rank['1']].pieceType == 'empty' and self.grid[File['g']][Rank['1']].pieceType == 'empty' and
        self.whiteRookMoved[1] == False):
        return True
    elif (fPos.file == File['c'] and fPos.rank == Rank['8'] and kingColor == 'black' and 
        self.grid[File['b']][Rank['8']].pieceType == 'empty' and self.grid[File['c']][Rank['8']].pieceType == 'empty' and
        self.grid[File['d']][Rank['8']].pieceType == 'empty' and self.blackRookMoved[0] == False):
        return True
    elif (fPos.file == File['g'] and fPos.rank == Rank['8'] and kingColor == 'black' and 
        self.grid[File['f']][Rank['8']].pieceType == 'empty' and self.grid[File['g']][Rank['8']].pieceType == 'empty' and
        self.blackRookMoved[1] == False):
        return True
    else:
        return False

def PawnRules(self: Board, iPos: Position, fPos: Position) -> bool:
    pawnColor = self.grid[iPos.file][iPos.rank].color
    # pawn moving straight 1 space:
    # (white case)
    if fPos.file == iPos.file and fPos.rank == iPos.rank+1 and pawnColor == 'white':
        if self.grid[fPos.file][fPos.rank].pieceType == 'empty': return True
        else: return False
    # (black case)
    if fPos.file == iPos.file and fPos.rank == iPos.rank-1 and pawnColor == 'black':
        if self.grid[fPos.file][fPos.rank].pieceType == 'empty': return True
        else: return False
    # pawn moves straight 2 spaces on its first turn
    # (white case)
    if fPos.file == iPos.file and fPos.rank == iPos.rank+2 and pawnColor == 'white':
        if iPos.rank != Rank['2']: return False
        if self.grid[fPos.file][fPos.rank].pieceType == 'empty' and self.grid[fPos.file][fPos.rank-1].pieceType == 'empty': return True
        else: return False
    # (black case)
    if fPos.file == iPos.file and fPos.rank == iPos.rank-2 and pawnColor == 'black':
        if iPos.rank != Rank['7']: return False
        if self.grid[fPos.file][fPos.rank].pieceType == 'empty' and self.grid[fPos.file][fPos.rank+1].pieceType == 'empty': return True
        else: return False
    # pawns captures piece and moves diagonally
    # (white case)
    if ((fPos.file == iPos.file+1 or fPos.file==iPos.file-1) and fPos.rank==iPos.rank+1 
        and pawnColor == 'white' and self.grid[fPos.file][fPos.rank].color == 'black'
    ):
        return True
    # (black case)
    if ((fPos.file == iPos.file+1 or fPos.file==iPos.file-1) and fPos.rank==iPos.rank-1 
        and pawnColor == 'black' and self.grid[fPos.file][fPos.rank].color == 'white'
    ):
        return True
    # En-Passanting Scenario
    # (white case moving to the right)
    if (fPos.file == iPos.file+1 and fPos.rank == iPos.rank+1 and pawnColor == 'white' and iPos.rank == Rank['5'] and self.blackUpForEnPassant[iPos.file+1] == True
        and self.grid[iPos.file+1][iPos.rank].color == 'black' and self.grid[iPos.file+1][iPos.rank].pieceType == 'pawn' and self.grid[fPos.file][fPos.rank].pieceType == 'empty'):
        return True
    # (white case moving to the left)
    elif (fPos.file == iPos.file-1 and fPos.rank == iPos.rank+1 and pawnColor == 'white' and iPos.rank == Rank['5'] and self.blackUpForEnPassant[iPos.file-1] == True
        and self.grid[iPos.file-1][iPos.rank].color == 'black' and self.grid[iPos.file-1][iPos.rank].pieceType == 'pawn' and self.grid[fPos.file][fPos.rank].pieceType == 'empty'):
        return True
    # (black case moving to the right)
    elif (fPos.file == iPos.file+1 and fPos.rank == iPos.rank-1 and pawnColor == 'black' and iPos.rank == Rank['4'] and self.whiteUpForEnPassant[iPos.file+1] == True
        and self.grid[iPos.file+1][iPos.rank].color == 'white' and self.grid[iPos.file+1][iPos.rank].pieceType == 'pawn' and self.grid[fPos.file][fPos.rank].pieceType == 'empty'):
        return True
    # (black case moving to the left)
    elif (fPos.file == iPos.file-1 and fPos.rank == iPos.rank-1 and pawnColor == 'black' and iPos.rank == Rank['4'] and self.whiteUpForEnPassant[iPos.file-1] == True
        and self.grid[iPos.file-1][iPos.rank].color == 'white' and self.grid[iPos.file-1][iPos.rank].pieceType == 'pawn' and self.grid[fPos.file][fPos.rank].pieceType == 'empty'):
        return True
    else:
        return False
    
def QueenRules(self: Board, iPos: Position, fPos: Position) -> bool:
    return BishopRules(self, iPos, fPos) or RookRules(self, iPos, fPos)

def BishopRules(self: Board, iPos: Position, fPos: Position) -> bool:
    # makes sure bishop is attempting to move diagonally
    if abs(fPos.file - iPos.file) != abs(fPos.rank - iPos.rank): return False
    # moving to bottom right
    if fPos.file > iPos.file and fPos.rank < iPos.rank:
        for x in range(1,abs(fPos.file - iPos.file)):
            if self.grid[iPos.file + x][iPos.rank - x].pieceType != 'empty':
                print("1!")
                return False
        return True
    # moving to top right
    if fPos.file > iPos.file and fPos.rank > iPos.rank:
        for x in range(1,abs(fPos.file - iPos.file)):
            if self.grid[iPos.file + x][iPos.rank + x].pieceType != 'empty':
                print('2!')
                return False
        return True
    # moving to top left
    if fPos.file < iPos.file and fPos.rank > iPos.rank:
        for x in range(1,abs(fPos.file - iPos.file)):
            if self.grid[iPos.file - x][iPos.rank + x].pieceType != 'empty':
                print("3!")
                return False
        return True
    # moving to bottom left
    if fPos.file < iPos.file and fPos.rank < iPos.rank:
        for x in range(1,abs(fPos.file - iPos.file)):
            if self.grid[iPos.file - x][iPos.rank - x].pieceType != 'empty':
                print("4!")
                return False
        return True
    print("5!")
    return False

def RookRules(self:Board, iPos: Position, fPos: Position) -> bool:
    # check if rook is attemting to move either horizontally or vertically only
    if not((abs(fPos.file - iPos.file) == 0 and abs(fPos.rank - iPos.rank) != 0)
        or (abs(fPos.file - iPos.file) != 0 and abs(fPos.rank - iPos.rank) == 0)):
        return False
    # moving up
    if fPos.file == iPos.file and fPos.rank > iPos.rank:
        for x in range(1,abs(fPos.rank - iPos.rank)):
            if self.grid[iPos.file][iPos.rank+x].pieceType !='empty':
                return False
        return True
    # moving down
    if fPos.file == iPos.file and fPos.rank < iPos.rank:
        for x in range(1,abs(fPos.rank - iPos.rank)):
            if self.grid[iPos.file][iPos.rank-x].pieceType !='empty':
                return False
        return True
    # moving left
    if fPos.file < iPos.file and fPos.rank == iPos.rank:
        for x in range(1,abs(fPos.file - iPos.file)):
            if self.grid[iPos.file-x][iPos.rank].pieceType !='empty':
                return False
        return True
    # moving right
    if fPos.file > iPos.file and fPos.rank == iPos.rank:
        for x in range(1,abs(fPos.file - iPos.file)):
            if self.grid[iPos.file+x][iPos.rank].pieceType !='empty':
                return False
        return True
    return False

def KnightRules(self: Position, iPos: Position, fPos: Position) -> bool:
    if fPos.file == iPos.file + 2 and fPos.rank == iPos.rank + 1: return True
    if fPos.file == iPos.file + 1 and fPos.rank == iPos.rank + 2: return True
    if fPos.file == iPos.file - 1 and fPos.rank == iPos.rank + 2: return True
    if fPos.file == iPos.file - 2 and fPos.rank == iPos.rank + 1: return True
    if fPos.file == iPos.file - 2 and fPos.rank == iPos.rank - 1: return True
    if fPos.file == iPos.file - 1 and fPos.rank == iPos.rank - 2: return True
    if fPos.file == iPos.file + 1 and fPos.rank == iPos.rank - 2: return True
    if fPos.file == iPos.file + 2 and fPos.rank == iPos.rank - 1: return True
    return False

def getMoves(self: Board, pos: Position) -> list:
    PositionList = []
    finalPos = Position()
    for rank in range(0,8):
        finalPos.rank = rank
        for file in range(0,8):
            finalPos.file = file
            if Rules(self, pos, finalPos) == 0:
                PositionList.append(copy.deepcopy(finalPos))
    return PositionList

def CheckForCheck(self: Board, kingPos: Position) -> bool:
    initialPos = Position()
    for rank in range(0,8):
        initialPos.rank = rank
        for file in range(0,8):
            initialPos.file = file
            print(initialPos)
            if ModifiedRules(self, initialPos, kingPos) == 0:
                print(initialPos,'returning true..')
                return True
    return False

def CheckForCheckmate(self: Board, kingPos: Position) -> bool:
    if CheckForCheck(self, kingPos): return False
    possibleMoves = getMoves(self, kingPos)
    if len(possibleMoves) == 0: return True
    else: return False

def GetAllMoves(self: Board, teamColor: str) -> list:
    moveList = []
    currStartPos = Position()
    currFinPos = Position()
    currMove = Move()
    for rank1 in range(0,8):
        currStartPos.rank = rank1
        for file1 in range(0,8):
            currStartPos.file = file1
            currMove.iPos = copy.deepcopy(currStartPos)
            if self.grid[currStartPos.file][currStartPos.rank].color == teamColor:
                for rank in range(0,8):
                    currFinPos.rank = rank
                    for file in range(0,8):
                        currFinPos.file = file
                        if Rules(self, currStartPos, currFinPos) == 0:
                            currMove.fPos = currFinPos
                            moveList.append(currMove)
    return moveList

        

    
# board = Board()
# print(board)
# print("using file and rank: a1")
# file1 = 'a'
# rank1 = '1'
# z = copy.deepcopy(board.grid[File[file1]][Rank[rank1]])
# c = copy.deepcopy(board.grid[File[file1]][Rank[rank1]])
# print(z == c)

