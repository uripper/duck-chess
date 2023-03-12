import pygame as pg
import sys
import random

sys.path.insert(0, 'duck_chess')
from pygame.constants import MOUSEBUTTONDOWN


import duck_chess
import duck_chess.duck_pgn
import duck_chess.variant

"""

Chess pieces from 
Cburnett, CC BY-SA 3.0 <http://creativecommons.org/licenses/by-sa/3.0/>, via Wikimedia Commons

Chess board from
החבלן, CC0, via Wikimedia Commons

SVG ducks all from https://www.svgrepo.com/

"""



# duck_move = False

# LIGHT = (147, 139, 150)
# DARK = (42, 69, 61)

# FROMMOVE = False
# TOMOVE = False

# pg.init()
# WIDTH = 800
# HEIGHT = 800
# board = duck_chess.variant.DuckBoard()
# SCREEN = pg.display.set_mode((WIDTH, HEIGHT))
# SQUARE_SIZE = 70

# pg.display.set_caption("Duck Chess")
# font = pg.font.SysFont('Roboto', 25)

# WKing = pg.image.load(
#     'Pieces\king.svg').convert_alpha()
# WKing = pg.transform.scale(WKing, (SQUARE_SIZE, SQUARE_SIZE))

# BKing = pg.image.load(
#     'Pieces\BlackKing.svg').convert_alpha()
# BKing = pg.transform.scale(BKing, (SQUARE_SIZE, SQUARE_SIZE))

# WKnight = pg.image.load(
#     'Pieces\Knight.svg').convert_alpha()
# WKnight = pg.transform.scale(WKnight, (SQUARE_SIZE, SQUARE_SIZE))

# BKnight = pg.image.load(
#     'Pieces\BlackKnight.svg').convert_alpha()
# BKnight = pg.transform.scale(BKnight, (SQUARE_SIZE, SQUARE_SIZE))

# WRook = pg.image.load(
#     'Pieces\Rook.svg').convert_alpha()
# WRook = pg.transform.scale(WRook, (SQUARE_SIZE, SQUARE_SIZE))

# BRook = pg.image.load(
#     'Pieces\BlackRook.svg').convert_alpha()
# BRook = pg.transform.scale(BRook, (SQUARE_SIZE, SQUARE_SIZE))

# WQueen = pg.image.load(
#     'Pieces\Queen.svg').convert_alpha()
# WQueen = pg.transform.scale(WQueen, (SQUARE_SIZE, SQUARE_SIZE))

# BQueen = pg.image.load(
#     'Pieces\BlackQueen.svg').convert_alpha()
# BQueen = pg.transform.scale(BQueen, (SQUARE_SIZE, SQUARE_SIZE))

# WBishop = pg.image.load(
#     'Pieces\Bishop.svg').convert_alpha()
# WBishop = pg.transform.scale(WBishop, (SQUARE_SIZE, SQUARE_SIZE))

# BBishop = pg.image.load(
#     'Pieces\BlackBishop.svg').convert_alpha()
# BBishop = pg.transform.scale(BBishop, (SQUARE_SIZE, SQUARE_SIZE))

# WPawn = pg.image.load(
#     'Pieces\Pawn.svg').convert_alpha()
# WPawn = pg.transform.scale(WPawn, (SQUARE_SIZE, SQUARE_SIZE))

# BPawn = pg.image.load(
#     'Pieces\BlackPawn.svg').convert_alpha()
# BPawn = pg.transform.scale(BPawn, (SQUARE_SIZE, SQUARE_SIZE))

# Duck = pg.image.load(
#     "Pieces\duck2.svg").convert_alpha()
# Duck = pg.transform.scale(BPawn, (SQUARE_SIZE, SQUARE_SIZE))

# BDuck = pg.image.load(
#     "Pieces\duck.svg").convert_alpha()
# BDuck = pg.transform.scale(BDuck, (SQUARE_SIZE, SQUARE_SIZE))

# pieces = [WKing, BKing, WKnight, BKnight, WRook, BRook,
#           WQueen, BQueen, WBishop, BBishop, WPawn, BPawn, Duck, BDuck]



# tries = 0

class Gameplay:

    
    def __init__(self) -> None:
        super().__init__()

        pg.init()
        pg.display.set_caption("Duck Chess")


        self.GAMEOVER = False
        self.font = pg.font.SysFont('Roboto', 25)
        self.duck_move = False
        self.board = duck_chess.variant.DuckBoard()
        self.CHOOSINGMOVE = False

        self.LIGHT = (147, 139, 150)
        self.DARK = (42, 69, 61)

        self.FROMMOVE = False
        self.TOMOVE = False
        self.SQUARE_SIZE = 70
        self.WIDTH = 800
        self.HEIGHT = 800
        self.n = 20

        self.y_var = int(self.HEIGHT-(self.HEIGHT/6))
        self.SCREEN = pg.display.set_mode((self.WIDTH, self.HEIGHT))
        

                                          
    
    def start_pieces(self):
        self.WKing = pg.image.load(
        'Pieces\king.svg').convert_alpha()
        self.WKing = pg.transform.scale(self.WKing, (self.SQUARE_SIZE, self.SQUARE_SIZE))

        self.BKing = pg.image.load(
            'Pieces\BlackKing.svg').convert_alpha()
        self.BKing = pg.transform.scale(self.BKing, (self.SQUARE_SIZE, self.SQUARE_SIZE))

        self.WKnight = pg.image.load(
            'Pieces\Knight.svg').convert_alpha()
        self.WKnight = pg.transform.scale(self.WKnight, (self.SQUARE_SIZE, self.SQUARE_SIZE))

        self.BKnight = pg.image.load(
            'Pieces\BlackKnight.svg').convert_alpha()
        self.BKnight = pg.transform.scale(self.BKnight, (self.SQUARE_SIZE, self.SQUARE_SIZE))

        self.WRook = pg.image.load(
            'Pieces\Rook.svg').convert_alpha()
        self.WRook = pg.transform.scale(self.WRook, (self.SQUARE_SIZE, self.SQUARE_SIZE))

        self.BRook = pg.image.load(
            'Pieces\BlackRook.svg').convert_alpha()
        self.BRook = pg.transform.scale(self.BRook, (self.SQUARE_SIZE, self.SQUARE_SIZE))

        self.WQueen = pg.image.load(
            'Pieces\Queen.svg').convert_alpha()
        self.WQueen = pg.transform.scale(self.WQueen, (self.SQUARE_SIZE, self.SQUARE_SIZE))

        self.BQueen = pg.image.load(
            'Pieces\BlackQueen.svg').convert_alpha()
        self.BQueen = pg.transform.scale(self.BQueen, (self.SQUARE_SIZE, self.SQUARE_SIZE))

        self.WBishop = pg.image.load(
            'Pieces\Bishop.svg').convert_alpha()
        self.WBishop = pg.transform.scale(self.WBishop, (self.SQUARE_SIZE, self.SQUARE_SIZE))

        self.BBishop = pg.image.load(
            'Pieces\BlackBishop.svg').convert_alpha()
        self.BBishop = pg.transform.scale(self.BBishop, (self.SQUARE_SIZE, self.SQUARE_SIZE))

        self.WPawn = pg.image.load(
            'Pieces\Pawn.svg').convert_alpha()
        self.WPawn = pg.transform.scale(self.WPawn, (self.SQUARE_SIZE, self.SQUARE_SIZE))

        self.BPawn = pg.image.load(
            'Pieces\BlackPawn.svg').convert_alpha()
        self.BPawn = pg.transform.scale(self.BPawn, (self.SQUARE_SIZE, self.SQUARE_SIZE))

        self.Duck = pg.image.load(
            "Pieces\duck2.svg").convert_alpha()
        self.Duck = pg.transform.scale(self.Duck, (self.SQUARE_SIZE, self.SQUARE_SIZE))

        self.BDuck = pg.image.load(
            "Pieces\duck.svg").convert_alpha()
        self.BDuck = pg.transform.scale(self.BDuck, (self.SQUARE_SIZE, self.SQUARE_SIZE))

        self.pieces = [self.WKing, self.BKing, self.WKnight, self.BKnight, self.WRook, self.BRook,
                self.WQueen, self.BQueen, self.WBishop, self.BBishop, self.WPawn, self.BPawn, self.Duck, self.BDuck]
    
    def no_king(self):

        try:
            the_king = duck_chess.square_name(self.board.king(not self.board.turn))
        except TypeError:
            self.GAMEOVER = True

    def check_game_over(self):
        king_stat = self.no_king()
        if self.board.is_stalemate() or self.board.is_insufficient_material() or self.board.is_fifty_moves() or self.board.is_repetition() or king_stat:
            self.GAMEOVER = True
        self.gameover_screen()
        self.SCREEN_update()
        
    def gameover_screen(self):
        rendered_text = self.font.render("GAME OVER", True, (0, 0, 0))
        if self.no_king:
            OUTCOME = "WHITE WINS" if self.board.turn else "BLACK WINS"
        OUTCOME = self.board.outcome()
        OUTCOME = str(OUTCOME)
        OUTCOME = OUTCOME.split(" ")
        OUTCOME = OUTCOME[-1]
        OUTCOME = OUTCOME.replace("winner=", "").replace(")", "")
        if OUTCOME == "None":
            OUTCOME = "True" if self.board.turn else "False"
        if OUTCOME == "True":
            rendered_text = self.font.render("YOU WIN", True, (0, 0, 0))
            # self.SCREEN.blit(rendered_text, rendered_text,
            #                 (self.WIDTH/90)+self.n, self.y_var+50)

        elif OUTCOME == "False":
            rendered_text = self.font.render("YOU LOSE", True, (0, 0, 0))
            # self.SCREEN.blit(rendered_text, rendered_text,
            #                 (self.WIDTH/90)+self.n, self.y_var+50)

        else:
            rendered_text = self.font.render("YOU DREW", True, (0, 0, 0))
            # self.SCREEN.blit(rendered_text, rendered_text,
            #                 (self.WIDTH/90)+self.n, self.y_var+50)
            self.SCREEN_update()

            pg.time.delay(5000)
            pg.quit()
            sys.exit()
    def SCREEN_update(self):
        fen = self.board.fen()
        self.draw_squares()
        self.draw_pieces(fen)
        pg.display.update()


    def rect_update(self):
        fen = self.board.fen()
        self.draw_squares()
        for i in self.rect_moves:
            pg.draw.rect(self.SCREEN, (255, 209, 220), i)
            pg.draw.rect(self.SCREEN, (169, 64, 100), i, 4)
        self.draw_pieces(fen)

        pg.display.update()

    def get_duck_moves(self):
        self.from_move = "Z@"
        possible_moves = []
        rect_moves = []

        for i in list(self.board.generate_duck_moves()):
            uci = i.uci()[:2]
            if uci == self.from_move:
                possible_moves.append(i)
        for i in possible_moves:

            coord_index = self.coord_list.index(
                i.uci()[2:4])
            working_rect = self.rect_list[coord_index]
            rect_moves.append(working_rect)
        return rect_moves
        

    def draw_squares(self):
        self.rect_list = []
        self.coord_list = []
        colour_dict = {True: self.LIGHT, False: self.DARK}
        files = ["a", "b", "c", "d", "e", "f", "g", "h"]
        ranks = ["8", "7", "6", "5", "4", "3", "2", "1"]
        current_colour = True
        for row in range(8):
            for square in range(8):

                i = pg.draw.rect(self.SCREEN, colour_dict[current_colour], ((
                    self.SQUARE_SIZE + (square * self.SQUARE_SIZE)), self.SQUARE_SIZE + (row * self.SQUARE_SIZE), self.SQUARE_SIZE, self.SQUARE_SIZE))
                self.rect_list.append(i)
                self.coord_list.append((files[square] + ranks[row]))

                current_colour = not current_colour
            current_colour = not current_colour


    def check_for_promotion(self):
        while self.CHOOSINGMOVE:
            promotion_width = self.WIDTH - (self.WIDTH/1.125)
            promotion_height = self.HEIGHT - (self.HEIGHT/8)
            # pg.draw.rect(SCREEN, (20, 20, 20), (promotion_width,
            #                                     promotion_height, SQUARE_SIZE*6, SQUARE_SIZE*1.25))
            Queen_square = pg.draw.rect(self.SCREEN, (80, 40, 40), (promotion_width+self.SQUARE_SIZE,
                                                            promotion_height, self.SQUARE_SIZE*1.1, self.SQUARE_SIZE*1.1))
            self.SCREEN.blit(self.WQueen, (promotion_width+self.SQUARE_SIZE,
                                promotion_height))
            Rook_square = pg.draw.rect(self.SCREEN, (80, 40, 40), (promotion_width+self.SQUARE_SIZE*2,
                                                            promotion_height, self.SQUARE_SIZE*1.1, self.SQUARE_SIZE*1.1))
            self.SCREEN.blit(self.WRook, (promotion_width+self.SQUARE_SIZE*2, promotion_height))
            Bishop_square = pg.draw.rect(self.SCREEN, (80, 40, 40), (promotion_width+self.SQUARE_SIZE*3,
                                                                promotion_height, self.SQUARE_SIZE*1.1, self.SQUARE_SIZE*1.1))
            self.SCREEN.blit(self.WBishop, (promotion_width+self.SQUARE_SIZE*3,
                                promotion_height))

            Knight_square = pg.draw.rect(self.SCREEN, (80, 40, 40), (promotion_width+self.SQUARE_SIZE*4,
                                                                promotion_height, self.SQUARE_SIZE*1.1, self.SQUARE_SIZE*1.1))
            self.SCREEN.blit(self.WKnight, (promotion_width +
                                self.SQUARE_SIZE*4, promotion_height))

            self.SCREEN_update()
            for event in pg.event.get():
                if event.type == pg.MOUSEBUTTONDOWN:
                    if Queen_square.collidepoint(pg.mouse.get_pos()):
                        self.to_move = f"{self.to_move}q"
                        self.CHOOSINGMOVE = False
                        break

                    elif Rook_square.collidepoint(pg.mouse.get_pos()):
                        self.to_move = f"{self.to_move}r"
                        self.CHOOSINGMOVE = False
                        break

                    elif Bishop_square.collidepoint(pg.mouse.get_pos()):
                        self.to_move = f"{self.to_move}b"
                        self.CHOOSINGMOVE = False
                        break

                    elif Knight_square.collidepoint(pg.mouse.get_pos()):
                        self.to_move = f"{self.to_move}n"
                        self.CHOOSINGMOVE = False
                        break
                elif event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
        self.total_move = self.from_move + self.to_move
        self.board.push_san(self.total_move)


    def get_legal_moves(self):

        index = self.rect_list.index(self.rect_clicked[0])
        self.clicked_coord = self.coord_list[index]
        self.from_move = self.clicked_coord
        self.possible_moves = []

        for i in list(self.board.pseudo_legal_moves):
            uci = i.uci()[:2]
            if uci == self.from_move:
                self.possible_moves.append(i)
        for i in self.possible_moves:
            try:
                coord_index = self.coord_list.index(
                    i.uci()[2:4])
                working_rect = self.rect_list[coord_index]
                self.rect_moves.append(working_rect)
            except ValueError:
                self.check_for_promotion()


    def draw_pieces(self, fen):
        col = self.SQUARE_SIZE
        row = self.SQUARE_SIZE
        for i in fen:
            if i == " ":
                break
            elif i == "/":
                col += self.SQUARE_SIZE
                row = self.SQUARE_SIZE
            elif i in ["1", "2", "3", "4", "5", "6", "7", "8"]:
                row += self.SQUARE_SIZE*int(i)
            elif i == "K":
                self.SCREEN.blit(self.WKing, (row, col))
                row += self.SQUARE_SIZE
            elif i == "k":
                self.SCREEN.blit(self.BKing, (row, col))
                row += self.SQUARE_SIZE
            elif i == "N":
                self.SCREEN.blit(self.WKnight, (row, col))
                row += self.SQUARE_SIZE
            elif i == "n":
                self.SCREEN.blit(self.BKnight, (row, col))
                row += self.SQUARE_SIZE
            elif i == "R":
                self.SCREEN.blit(self.WRook, (row, col))
                row += self.SQUARE_SIZE
            elif i == "r":
                self.SCREEN.blit(self.BRook, (row, col))
                row += self.SQUARE_SIZE
            elif i == "Q":
                self.SCREEN.blit(self.WQueen, (row, col))
                row += self.SQUARE_SIZE
            elif i == "q":
                self.SCREEN.blit(self.BQueen, (row, col))
                row += self.SQUARE_SIZE
            elif i == "B":
                self.SCREEN.blit(self.WBishop, (row, col))
                row += self.SQUARE_SIZE
            elif i == "b":
                self.SCREEN.blit(self.BBishop, (row, col))
                row += self.SQUARE_SIZE
            elif i == "P":
                self.SCREEN.blit(self.WPawn, (row, col))
                row += self.SQUARE_SIZE
            elif i == "p":
                self.SCREEN.blit(self.BPawn, (row, col))
                row += self.SQUARE_SIZE
            elif i == "z":
                self.SCREEN.blit(self.BDuck, (row, col))
                row += self.SQUARE_SIZE
            elif i == "Z":
                self.SCREEN.blit(self.BDuck, (row, col))
                row += self.SQUARE_SIZE
            else:
                row += self.SQUARE_SIZE


    def computer_duck_move(self):
        
        move_list = list(self.board.generate_duck_moves())
        self.board.duck_push(random.choice(move_list))
        
    def make_duck_move(self):
        while self.duck_move:
            self.from_move = "Z@"
            self.rect_moves = self.get_duck_moves()
            self.rect_update()
            for event in pg.event.get():
                
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

                elif event.type == pg.MOUSEBUTTONDOWN:
                    
                    pos = pg.mouse.get_pos()
                    self.rect_clicked = [
                        rect for rect in self.rect_list if rect.collidepoint(pos)]
                    try:
                        self.rect_clicked[0]
                    except IndexError:
                        self.rect_clicked.append("None")
                    if self.rect_clicked[0] in self.rect_moves:
                        index = self.rect_list.index(
                            self.rect_clicked[0])
                        to_move = self.coord_list[index]
                        total_move = self.from_move + to_move
                        
                        self.board.duck_push(duck_chess.M
                                             ove.from_uci(total_move))
                        self.SCREEN_update()
                        self.FROMMOVE = False
                        self.TOMOVE = False
                        self.duck_move = False
                        self.computer_move()

                        break
                    
                    elif self.rect_clicked[0] not in self.rect_moves:
                        self.from_move = "Z@"

    def computer_move(self):
        legal_moves = list(self.board.pseudo_legal_moves)
        thinking = pg.time.get_ticks()

        try:
            move = random.choice(legal_moves)
            self.board.f_push(move)
            self.check_game_over()
            if self.GAMEOVER == False:
                self.computer_duck_move()
        except IndexError:
            self.check_game_over()
            if self.GAMEOVER == False:
                move = legal_moves[0]
                self.board.f_push(move)
                self.check_game_over()
                self.computer_duck_move()
        finally:
            time_thinking = random.randint(500, 1000)
            while True:
                now = pg.time.get_ticks()
                if now - thinking >= time_thinking:
                    break
            self.SCREEN_update()

    def game_loop(self):
        self.start_pieces()
        self.font = pg.font.SysFont("Arial", 20)
        self.SCREEN = pg.display.set_mode((self.WIDTH, self.HEIGHT))
        pg.init()
        while True:
            self.check_game_over()
            self.SCREEN.fill("WHITE")

            if self.GAMEOVER:
                rendered_text = self.font.render("GAME OVER", True, (0, 0, 0))
                self.SCREEN.blit(rendered_text, rendered_text,
                                (self.WIDTH/90)+self.n, self.y_var+50)
                if self.no_king():
                    OUTCOME = "WHITE WINS" if self.board.turn else "BLACK WINS"
                OUTCOME = self.board.outcome()
                OUTCOME = str(OUTCOME)
                OUTCOME = OUTCOME.split(" ")
                OUTCOME = OUTCOME[-1]
                OUTCOME = OUTCOME.replace("winner=", "").replace(")", "")
                if OUTCOME == "None":
                    OUTCOME = "True" if self.board.turn else "False"
                if OUTCOME == "True":
                    rendered_text = self.font.render("YOU WIN", True, (0, 0, 0))
                elif OUTCOME == "False":
                    rendered_text = self.font.render("YOU LOSE", True, (0, 0, 0))
                else:
                    rendered_text = self.font.render("YOU DREW", True, (0, 0, 0))
                self.SCREEN.blit(rendered_text, rendered_text,
                            (self.WIDTH/90)+self.n, self.y_var+50)

                self.SCREEN_update()

                pg.time.delay(5000)
                pg.quit()
                sys.exit()

            if self.board.turn == False:


                self.computer_move()


            else:
                for event in pg.event.get():
                    self.check_game_over()
                    if event.type == pg.QUIT:
                        pg.quit()
                        sys.exit()
                    elif event.type == pg.MOUSEBUTTONDOWN:
                        pos = pg.mouse.get_pos()
                        self.rect_clicked = [
                            rect for rect in self.rect_list if rect.collidepoint(pos)]
                        try:
                            self.rect_moves = []
                            FROMMOVE = True
                            TOMOVE = True

                            while FROMMOVE:
                                self.get_legal_moves()
                                while TOMOVE:
                                    self.rect_update()
                                    for event in pg.event.get():
                                        if event.type == pg.QUIT:
                                            pg.quit()
                                            sys.exit()

                                        elif event.type == pg.MOUSEBUTTONDOWN:
                                            pos = pg.mouse.get_pos()
                                            self.rect_clicked = [
                                                rect for rect in self.rect_list if rect.collidepoint(pos)]

                                            if self.rect_clicked[0] in self.rect_moves and self.duck_move == False:
                                                index = self.rect_list.index(
                                                    self.rect_clicked[0])
                                                to_move = self.coord_list[index]
                                                total_move = self.from_move + to_move
                                                try:
                                                    self.board.f_push(duck_chess.Move.from_uci(total_move))
                                                    print("Move Made, Duck Move Next")
                                                except ValueError:
                                                    print(f"Invalid move: {total_move}")
                                                    self.CHOOSINGMOVE=True
                                                    self.check_for_promotion()
                                                self.SCREEN_update()

                                                self.check_game_over()
                                                if self.GAMEOVER == False:
                                                    self.duck_move = True
                                                    self.make_duck_move()




                                            elif self.rect_clicked[0] not in self.rect_moves and self.duck_move == False:

                                                self.rect_moves.clear()
                                                self.get_legal_moves()

                                                self.rect_update()

                        except IndexError:
                            continue

game = Gameplay()
game.game_loop()