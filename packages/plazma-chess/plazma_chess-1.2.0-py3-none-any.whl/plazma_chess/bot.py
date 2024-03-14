import utils
from copy import deepcopy

class Bot:
    def __init__(self, color):
        self.DEPTH = 3
        self.color = color # 0 white : 1 black

    def evalute(self, board):
        score = 0
        for y in range(8):
            for x in range(8):
                piece = board.pieceAt((x, y))[1]
                if piece != 0:
                    if piece < 7 and self.color == 0: score += utils.PIECE_VALUES[utils.PIECE_NAMES[piece]]
                    elif piece > 6 and self.color == 1: score += utils.PIECE_VALUES[utils.PIECE_NAMES[piece]]
                    else: score -= utils.PIECE_VALUES[utils.PIECE_NAMES[piece]]
        
        return score

    def move(self, engine):
        best_move = 0
        best_piece = 0
        best_score = float('inf')
        
        whitePieces = []
        blackPieces = []

        for y in range(8):
            for x in range(8):
                piece = engine.board.pieceAt((x, y))[1]
                if piece != 0:
                    if piece < 7: whitePieces.append((x, y))
                    else: blackPieces.append((x, y))

        if self.color == 0:
            for piece in whitePieces:
                for move in engine.generateMoves(piece):
                    og = deepcopy(engine.board.board)
                    engine.move(piece, move)

                    score = self.minimax(engine, 2, True)
                    engine.board.board = deepcopy(og)
                    if score < best_score:
                        best_score = score
                        best_move = move
                        best_piece = piece
        else:
            for piece in blackPieces:
                for move in engine.generateMoves(piece):
                    og = deepcopy(engine.board.board)
                    engine.move(piece, move)

                    score = self.minimax(engine, 2, True)
                    engine.board.board = deepcopy(og)
                    if score < best_score:
                        best_score = score
                        best_move = move
                        best_piece = piece

        return (best_piece, best_move)

    def minimax(self, engine, depth, maximizing):
        if depth == 0: return self.evalute(engine.board)
        
        if maximizing:
            best_score = float('-inf')
            
            whitePieces = []
            blackPieces = []

            for y in range(8):
                for x in range(8):
                    piece = engine.board.pieceAt((x, y))[1]
                    if piece != 0:
                        if piece < 7: whitePieces.append((x, y))
                        else: blackPieces.append((x, y))

            if self.color == 0:
                for piece in whitePieces:
                    for move in engine.generateMoves(piece):
                        og = deepcopy(engine.board.board)
                        engine.move(piece, move)

                        score = self.minimax(engine, depth-1, False)
                        best_score = max(best_score, score)

                        engine.board.board = deepcopy(og)

                    return best_score
            elif self.color == 1:
                for piece in blackPieces:
                    for move in engine.generateMoves(piece):
                        og = deepcopy(engine.board.board)
                        engine.move(piece, move)

                        score = self.minimax(engine, depth-1, False)
                        best_score = max(best_score, score)

                        engine.board.board = deepcopy(og)

                    return best_score
        else:
            best_score = float('inf')
            
            whitePieces = []
            blackPieces = []

            for y in range(8):
                for x in range(8):
                    piece = engine.board.pieceAt((x, y))[1]
                    if piece != 0:
                        if piece < 7: whitePieces.append((x, y))
                        else: blackPieces.append((x, y))

            if self.color == 0:
                for piece in blackPieces:
                    for move in engine.generateMoves(piece):
                        og = deepcopy(engine.board.board)
                        engine.move(piece, move)

                        score = self.minimax(engine, depth-1, False)
                        best_score = max(best_score, score)

                        engine.board.board = deepcopy(og)

                    return best_score
            elif self.color == 1:
                for piece in whitePieces:
                    for move in engine.generateMoves(piece):
                        og = deepcopy(engine.board.board)
                        engine.move(piece, move)

                        score = self.minimax(engine, depth-1, True)
                        best_score = min(best_score, score)

                        engine.board.board = deepcopy(og)
                        
                    return best_score