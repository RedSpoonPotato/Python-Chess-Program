pieceType = (
        'king',
        'queen',
        'bishop',
        'knight',
        'rook',
        'pawn',
        'empty')

Color = (
        'black', 
        'white', 
        'NoColor')

class Piece:
    def __init__(self, pieceType:str = 'empty', color:str = 'NoColor'):
        self.pieceType = pieceType
        self.color = color
    def __repr__(self) -> str:
        return '{}{}'.format(self.color, self.pieceType)