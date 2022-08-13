from functools import partial
from Board import *
import tkinter as tk

board = Board()
startingBoard(board)
isWhiteTurn = True
kingInCheckMate = False
selectedPiece = None

def updateGrid(board: Board):
    global backgroundButtons
    print('upating board')
    for x in range(8):
        for y in range(8):
            backgroundButtons[x][y].configure(image=piecDi[board.grid[x][y].color][board.grid[x][y].pieceType])

def buttonClick(board: Board, x:int, y:int) -> None:
    global selectedPiece
    global isWhiteTurn
    #print("isWhiteTurn: ", isWhiteTurn, " selectedPiece: ", selectedPiece)
    if  ((isWhiteTurn and board.grid[x][y].color == 'white') or
        (not(isWhiteTurn) and board.grid[x][y].color == 'black')
    ):
        print('option 1, changing selected piece')
        selectedPiece = Position(x,y)
        print(selectedPiece)
        return
    elif(selectedPiece != None and 
        ((isWhiteTurn and board.grid[x][y].color != 'white') or
        (not(isWhiteTurn) and board.grid[x][y].color != 'black'))
    ):
        # attempt to move a piece
        print('option 2, moving piece...')
        print("isWhiteTurn: ", isWhiteTurn, " selectedPiece: ", selectedPiece)
        print("file: ", x,"rank: ", y)
        print("iPos:",board.grid[selectedPiece.file][selectedPiece.rank]," fPos: ",board.grid[x][y])
        moveAttempt = SmartMovePiece(board, selectedPiece, Position(x,y), 'queen')
        print(moveAttempt)
        if moveAttempt != 0:
            return
        # move is succesful
        selectedPiece = None
        isWhiteTurn = not(isWhiteTurn)
        updateGrid(board=board)
        return
    else:
        print("option 3")
        return    
    # might have to switch x and y

window = tk.Tk()
window.geometry('700x700') 
window.title("Python Chess")
icon = tk.PhotoImage(file='images.png')
window.iconphoto(True, icon)
window.config(background='#3EB18E') # background color

#creating labels (2)
#label = tk.Label(window,text='BEANS', font=50, fg='red', bg='black', relief=tk.RAISED, bd=3)
#label.place(x=0,y=600)

piecDi = {}
piecDi['white'] = {}
piecDi['black'] = {}
piecDi['NoColor'] = {}

piecDi['white']['pawn'] = tk.PhotoImage(file='icons\white_pawn_trans.png')
piecDi['black']['pawn'] = tk.PhotoImage(file=r'icons\black_pawn_trans.png')
piecDi['white']['rook'] = tk.PhotoImage(file='icons\white_rook_trans.png')
piecDi['black']['rook'] = tk.PhotoImage(file=r'icons\black_rook_trans.png')
piecDi['white']['knight'] = tk.PhotoImage(file='icons\white_knight_trans.png')
piecDi['black']['knight'] = tk.PhotoImage(file=r'icons\black_knight_trans.png')
piecDi['white']['bishop'] = tk.PhotoImage(file='icons\white_bishop_trans.png')
piecDi['black']['bishop'] = tk.PhotoImage(file=r'icons\black_bishop_trans.png')
piecDi['white']['queen'] = tk.PhotoImage(file='icons\white_queen_trans.png')
piecDi['black']['queen'] = tk.PhotoImage(file=r'icons\black_queen_trans.png')
piecDi['white']['king'] = tk.PhotoImage(file='icons\white_king_trans.png')
piecDi['black']['king'] = tk.PhotoImage(file=r'icons\black_king_trans.png')
piecDi['NoColor']['empty'] = tk.PhotoImage(file='icons\gansparent.png')


def coords(x:int, y:int):
    print(str(x)+' '+str(y))
    global backgroundButtons
    backgroundButtons[y][x].configure(image=piecDi['white']['pawn'])

backgroundButtons = [[
    tk.Button(
        window,
        image = piecDi['black']['king'],
        bg= '#ABA79C' if (x+y)%2==0 else '#E2D4AC',
        bd= 1,
        command= partial(buttonClick, board, y, x)
        #command= partial(coords, x, y)
        )
for x in range(8)] for y in range(8)]

# intializing 


for x in range(0,8):
    for y in range(0,8):
        backgroundButtons[x][y].place(x=x*52,y=364-y*52)

updateGrid(board)

window.mainloop()
