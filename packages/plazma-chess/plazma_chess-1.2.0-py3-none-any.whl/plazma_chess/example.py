import plazma_chess as engine
import pygame as pg
import utils
from bot import Bot
from pygameGui import Button
import requests
import time
from copy import deepcopy

pg.init()

class MainMenu:
    def __init__(self, screen):
        self.selectedToText = {0: 'Local', 1: 'Bot', 2: 'Multiplayer'}
        self.selected = 0

        self.screen = screen

        self.arial60 = pg.font.SysFont("Arial", 60)
        self.arial40 = pg.font.SysFont("Arial", 40)
        self.arial20 = pg.font.SysFont("Arial", 20)

        self.titleLbl = self.arial60.render("Plazma Chess", True, (255, 255, 255))
        self.selectedLbl = self.arial40.render(f"Selected: {self.selectedToText[self.selected]}", True, (255, 255, 255))

        self.playBtn = Button(1200/2-100, 500, 200, 50, (255, 0, 255), (0, 0, 150), (255, 255, 255), "Play", 25, (0, 0, 0, 0), 70, 10)

        self.buttons = [Button(150, 375, 200, 50, (0, 0, 255), (0, 0, 150), (255, 255, 255), "Local", 25, (0, 0, 0, 0), 65, 10),
                        Button(500, 375, 200, 50, (0, 0, 255), (0, 0, 150), (255, 255, 255), "Bot", 25, (0, 0, 0, 0), 80, 10),
                        Button(850, 375, 200, 50, (0, 0, 255), (0, 0, 150), (255, 255, 255), "Multiplayer", 25, (0, 0, 0, 0), 40, 10)]
        
        self.buttons[0].clicked = True

        self.gameIndex = None
        self.color = None

    def run(self):
        clock = pg.time.Clock()

        while 1:
            self.screen.fill((0, 0, 0))

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()

                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        pos = pg.mouse.get_pos()
                        for button in self.buttons:
                            if pg.Rect(button.x, button.y, button.width, button.height).collidepoint(pos):
                                for otherButton in self.buttons: otherButton.clicked = False
                                button.clicked = True
                                self.selected = self.buttons.index(button)
                                self.selectedLbl = self.arial40.render(f"Selected: {self.selectedToText[self.selected]}", True, (255, 255, 255))
                            
                        if pg.Rect(self.playBtn.x, self.playBtn.y, self.playBtn.width, self.playBtn.height).collidepoint(pos):
                            button.clicked = True
                            if self.selected == 2:
                                self.screen.fill((0, 0, 0))
                                self.screen.blit(self.arial60.render("Finding server...", True, (255, 255, 255)), (100, 100))
                                pg.display.flip()
                                response = requests.get('https://captaindeathead.pythonanywhere.com/chess/findGame')
                                if str(response.status_code)[0] == '4': # 400 error codes
                                    self.screen.fill((0, 0, 0))
                                    self.screen.blit(self.arial60.render("Network Error! Exiting in 3 seconds...", True, (255, 255, 255)), (100, 100))
                                    pg.display.flip()
                                    time.sleep(3)
                                    pg.quit()
                                    exit()
                                else:
                                    self.gameIndex, self.color, self.playerId = response.text.split(', ')
                                    
                                    self.screen.fill((0, 0, 0))
                                    self.screen.blit(self.arial60.render("Waiting for an oppenent...", True, (255, 255, 255)), (100, 100))
                                    pg.display.flip()
                                    
                                    clock = pg.time.Clock()
                                    while 1:
                                        for event in pg.event.get():
                                            if event.type == pg.QUIT:
                                                requests.get(f'https://captaindeathead.pythonanywhere.com/chess/leaveGame?gameIndex={self.gameIndex}')
                                                pg.quit()
                                                exit()

                                        start = requests.get(f'https://captaindeathead.pythonanywhere.com/chess/gameStart?gameIndex={self.gameIndex}').text
                                        if bool(int(start)): break
                                        
                                        clock.tick(0.5)
                                    return

                            elif self.selected == 0:
                                return

            self.screen.blit(self.titleLbl, (1200/2-200, 150))
            self.screen.blit(self.selectedLbl, (1200/2-150, 300))

            for button in self.buttons: button.draw(self.screen)

            self.playBtn.draw(self.screen)

            clock.tick(60)
            pg.display.flip()

class ControlPanel:
    def __init__(self):
        self.x = 800
        self.y = 0
        self.width = 400
        self.height = 800
        self.color = (75, 0, 100)
    
    def draw(self, screen):
        pg.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

class Window:
    def __init__(self):
        self.screen = pg.display.set_mode((1200, 800))
        pg.display.set_caption("Plazma Chess ♟️")
        self.engine = engine.Engine()
        self.pieceFont = pg.font.SysFont("segoeuisymbol", 100)
        self.selectedSquare = None
        self.validMoves = ()
        self.bot = Bot(1)
        self.controlPanel = ControlPanel()
        self.gamemode = 0
        self.color = 0

    def drawBoard(self):
        isWhite = False
        for y in range(8):
            isWhite = not isWhite
            for x in range(8):
                if isWhite: pg.draw.rect(self.screen, (150, 150, 0), (y*100, x*100, 100, 100))
                else: pg.draw.rect(self.screen, (50, 50, 50), (y*100, x*100, 100, 100))
                isWhite = not isWhite

        for move in self.validMoves:
            if move[1] > 7:
                pg.draw.rect(self.screen, (255, 100, 100), ((move[0]-10)*100, (move[1]-10)*100, 100, 100))
                continue
            pg.draw.rect(self.screen, (255, 100, 100), (move[0]*100, move[1]*100, 100, 100))
        if self.selectedSquare != None: pg.draw.rect(self.screen, (255, 0, 0), (self.selectedSquare[0]*100, self.selectedSquare[1]*100, 100, 100))

    def drawPieces(self, reverse=False):
        reverseBoard = deepcopy(self.engine.board.board).reverse()
        for y in range(8):
            for x in range(8):
                if reverse: piece = reverseBoard[y][x]
                else: piece = self.engine.board.board[y][x]
                if piece < 7:
                    if self.selectedSquare == (x, y):
                        pos = pg.mouse.get_pos()
                        self.screen.blit(self.pieceFont.render(utils.PIECE_UNICODES[self.engine.board.board[y][x]], True, (255, 255, 255)), (min(pos[0]-50, 750), pos[1]-70))
                    else:
                        self.screen.blit(self.pieceFont.render(utils.PIECE_UNICODES[self.engine.board.board[y][x]], True, (255, 255, 255)), (x*100, y*100-20))
                else:
                    if self.selectedSquare == (x, y):
                        pos = pg.mouse.get_pos()
                        self.screen.blit(self.pieceFont.render(utils.PIECE_UNICODES[self.engine.board.board[y][x]], True, (0, 0, 0)), (min(pos[0]-50, 750), pos[1]-70))
                    else:
                        self.screen.blit(self.pieceFont.render(utils.PIECE_UNICODES[self.engine.board.board[y][x]], True, (0, 0, 0)), (x*100, y*100-20))

    def run(self):
        mainMenu = MainMenu(self.screen)
        mainMenu.run()
        self.gamemode = mainMenu.selected

        if self.gamemode == 2:
            self.color = int(mainMenu.color)
            lastAwait = time.time()

        clock = pg.time.Clock()
        while 1:
            self.drawBoard()
            self.drawPieces()
            self.controlPanel.draw(self.screen)

            if self.gamemode == 1:
                if self.engine.turn == self.bot.color:
                    botMove = self.bot.move(self.engine)
                    self.engine.move(botMove[0], botMove[1])
                    self.engine.turn = not self.engine.turn

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()

                if self.gamemode != 2 or self.color == self.engine.turn:
                    if event.type == pg.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            pos = pg.mouse.get_pos()
                            if pos[0] < 800 and pos[1] < 800:
                                self.selectedSquare = (int(round((pos[0]-50)/100, 0)), int(round((pos[1]-50)/100, 0)))
                                piece = self.engine.board.board[self.selectedSquare[1]][self.selectedSquare[0]]
                                if piece == 0: self.selectedSquare = None
                                elif piece < 7 and self.engine.turn == 1: self.selectedSquare = None
                                elif piece > 6 and self.engine.turn == 0: self.selectedSquare = None
                                elif self.gamemode == 0 or self.engine.turn == self.color: self.validMoves = self.engine.generateMoves(self.selectedSquare)

                    if event.type == pg.MOUSEBUTTONUP and self.selectedSquare != None:
                        if event.button == 1:
                            pos = pg.mouse.get_pos()
                            if pos[0] < 800 and pos[1] < 800:
                                try:
                                    move = self.engine.move(self.selectedSquare, (int(round((pos[0]-50)/100, 0)), int(round((pos[1]-50)/100, 0))))
                                    if self.gamemode == 2: requests.get(f'https://captaindeathead.pythonanywhere.com/chess/move?gameIndex={mainMenu.gameIndex}&selectedSquare={self.selectedSquare}&newSquare={(int(round((pos[0]-50)/100, 0)), int(round((pos[1]-50)/100, 0)))}')
                                    if move == 1:
                                        if self.engine.turn == 0: print("White wins!!!")
                                        else: print("Black wins!!!")
                                        pg.quit()
                                        return
                                except: self.engine.turn = not self.engine.turn
                            self.validMoves = ()
                            self.selectedSquare = None
                            self.engine.turn = not self.engine.turn
                else:
                    if time.time() - lastAwait >= 1:
                        lastAwait = time.time()
                        status = requests.get(f'https://captaindeathead.pythonanywhere.com/chess/awaitMove?gameIndex={mainMenu.gameIndex}&playerId={mainMenu.playerId}').text
                        if status == "True":
                            self.engine.board.board = eval(status)
                            if self.engine.turn == 0: print("White wins!!!")
                            else: print("Black wins!!!")
                            pg.quit()
                            return
                        elif status != "False":
                            self.engine.board.board = eval(status)
                            self.engine.turn = not self.engine.turn

            pg.display.flip()
            clock.tick(60)

if __name__ == "__main__":
    window = Window()
    window.run()
