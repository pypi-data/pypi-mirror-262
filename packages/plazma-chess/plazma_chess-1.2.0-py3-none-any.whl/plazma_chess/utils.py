PIECE_UNICODES = {0: ' ', 1: '♟︎', 2: '♞', 3: '♝', 4: '♜', 5: '♛', 6: '♚', 7: '♟︎', 8: '♞', 9: '♝', 10: '♜', 11: '♛', 12: '♚'}

PIECE_VALUES = {
    'pawn': 100,
    'knight': 300,
    'bishop': 350,
    'rook': 600,
    'queen': 900,
    'king': 10000
}

PIECE_NAMES = {
    1: 'pawn',
    2: 'knight',
    3: 'bishop',
    4: 'rook',
    5: 'queen',
    6: 'king',
    7: 'pawn',
    8: 'knight',
    9: 'bishop',
    10: 'rook',
    11: 'queen',
    12: 'king'
}

ESC = '\x1b'
WHITE_BG  = ESC + '[47m'
BLACK_BG  = ESC + '[40m'
RED_BG    = ESC + '[41m'
YELLOW_BG = ESC + '[43m'
GREEN_BG  = ESC + '[42m'
BLUE_BG   = ESC + '[44m'
PURPLE_BG = ESC + '[45m'

def showState(board):
    printString = ""
    white = False
    for y in range(8):
        white = not white
        for x in range(8):
            if white: printString += WHITE_BG + PIECE_UNICODES[board[y][x]] + ' '
            else: printString += BLACK_BG + PIECE_UNICODES[board[y][x]] + ' '
            white = not white
        printString += BLACK_BG
        printString += '\n'
    return printString