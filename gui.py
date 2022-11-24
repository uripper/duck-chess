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






MUSICVOLUME = .3

LIGHT = (147, 139, 150)
DARK = (42, 69, 61)

FROMMOVE = False
TOMOVE = False

pg.init()
WIDTH = 800
HEIGHT = 800
board = duck_chess.variant.DuckBoard()
SCREEN = pg.display.set_mode((WIDTH, HEIGHT))
SQUARE_SIZE = 70

pg.display.set_caption("Duck Chess")


WKing = pg.image.load(
    'Pieces\king.svg').convert_alpha()
WKing = pg.transform.scale(WKing, (SQUARE_SIZE, SQUARE_SIZE))

BKing = pg.image.load(
    'Pieces\BlackKing.svg').convert_alpha()
BKing = pg.transform.scale(BKing, (SQUARE_SIZE, SQUARE_SIZE))

WKnight = pg.image.load(
    'Pieces\Knight.svg').convert_alpha()
WKnight = pg.transform.scale(WKnight, (SQUARE_SIZE, SQUARE_SIZE))

BKnight = pg.image.load(
    'Pieces\BlackKnight.svg').convert_alpha()
BKnight = pg.transform.scale(BKnight, (SQUARE_SIZE, SQUARE_SIZE))

WRook = pg.image.load(
    'Pieces\Rook.svg').convert_alpha()
WRook = pg.transform.scale(WRook, (SQUARE_SIZE, SQUARE_SIZE))

BRook = pg.image.load(
    'Pieces\BlackRook.svg').convert_alpha()
BRook = pg.transform.scale(BRook, (SQUARE_SIZE, SQUARE_SIZE))

WQueen = pg.image.load(
    'Pieces\Queen.svg').convert_alpha()
WQueen = pg.transform.scale(WQueen, (SQUARE_SIZE, SQUARE_SIZE))

BQueen = pg.image.load(
    'Pieces\BlackQueen.svg').convert_alpha()
BQueen = pg.transform.scale(BQueen, (SQUARE_SIZE, SQUARE_SIZE))

WBishop = pg.image.load(
    'Pieces\Bishop.svg').convert_alpha()
WBishop = pg.transform.scale(WBishop, (SQUARE_SIZE, SQUARE_SIZE))

BBishop = pg.image.load(
    'Pieces\BlackBishop.svg').convert_alpha()
BBishop = pg.transform.scale(BBishop, (SQUARE_SIZE, SQUARE_SIZE))

WPawn = pg.image.load(
    'Pieces\Pawn.svg').convert_alpha()
WPawn = pg.transform.scale(WPawn, (SQUARE_SIZE, SQUARE_SIZE))

BPawn = pg.image.load(
    'Pieces\BlackPawn.svg').convert_alpha()
BPawn = pg.transform.scale(BPawn, (SQUARE_SIZE, SQUARE_SIZE))

Duck = pg.image.load(
    "Pieces\duck.svg").convert_alpha()
Duck = pg.transform.scale(BPawn, (SQUARE_SIZE, SQUARE_SIZE))

BDuck = pg.image.load(
    "Pieces\duck2.svg").convert_alpha()
BDuck = pg.transform.scale(BDuck, (SQUARE_SIZE, SQUARE_SIZE))

pieces = [WKing, BKing, WKnight, BKnight, WRook, BRook,
          WQueen, BQueen, WBishop, BBishop, WPawn, BPawn, Duck, BDuck]


font = pg.font.SysFont('Roboto', 25)

tries = 0
GAMEOVER = False


def check_game_over():
    global GAMEOVER
    if board.is_checkmate() or board.is_stalemate() or board.is_insufficient_material() or board.is_fifty_moves() or board.is_repetition():
        GAMEOVER = True
    SCREEN_update()


def SCREEN_update():
    fen = board.fen()
    draw_squares(SCREEN)
    draw_pieces(fen)
    pg.display.update()


def rect_update(rect_moves):
    fen = board.fen()
    draw_squares(SCREEN)
    for i in rect_moves:
        pg.draw.rect(SCREEN, (255, 209, 220), i)
        pg.draw.rect(SCREEN, (169, 64, 100), i, 4)
    draw_pieces(fen)

    pg.display.update()

def get_duck_moves():
    from_move = "Z@"
    possible_moves = []
    rect_moves = []

    for i in list(board.generate_duck_moves()):
        uci = i.uci()[:2]
        if uci == from_move:
            possible_moves.append(i)
    for i in possible_moves:

        coord_index = coord_list.index(
            i.uci()[2:4])
        working_rect = rect_list[coord_index]
        rect_moves.append(working_rect)
    return rect_moves
    

def draw_squares(SCREEN):
    global rect_list, coord_list
    rect_list = []
    coord_list = []
    colour_dict = {True: LIGHT, False: DARK}
    files = ["a", "b", "c", "d", "e", "f", "g", "h"]
    ranks = ["8", "7", "6", "5", "4", "3", "2", "1"]
    current_colour = True
    for row in range(8):
        for square in range(8):

            i = pg.draw.rect(SCREEN, colour_dict[current_colour], ((
                SQUARE_SIZE + (square * SQUARE_SIZE)), SQUARE_SIZE + (row * SQUARE_SIZE), SQUARE_SIZE, SQUARE_SIZE))
            rect_list.append(i)
            coord_list.append((files[square] + ranks[row]))

            current_colour = not current_colour
        current_colour = not current_colour


def check_for_promotion(to_move, CHOOSINGMOVE):
    global from_move
    while CHOOSINGMOVE:
        promotion_width = WIDTH - (WIDTH/1.125)
        promotion_height = HEIGHT - (HEIGHT/8)
        # pg.draw.rect(SCREEN, (20, 20, 20), (promotion_width,
        #                                     promotion_height, SQUARE_SIZE*6, SQUARE_SIZE*1.25))
        Queen_square = pg.draw.rect(SCREEN, (80, 40, 40), (promotion_width+SQUARE_SIZE,
                                                           promotion_height, SQUARE_SIZE*1.1, SQUARE_SIZE*1.1))
        SCREEN.blit(WQueen, (promotion_width+SQUARE_SIZE,
                             promotion_height))
        Rook_square = pg.draw.rect(SCREEN, (80, 40, 40), (promotion_width+SQUARE_SIZE*2,
                                                          promotion_height, SQUARE_SIZE*1.1, SQUARE_SIZE*1.1))
        SCREEN.blit(WRook, (promotion_width+SQUARE_SIZE*2, promotion_height))
        Bishop_square = pg.draw.rect(SCREEN, (80, 40, 40), (promotion_width+SQUARE_SIZE*3,
                                                            promotion_height, SQUARE_SIZE*1.1, SQUARE_SIZE*1.1))
        SCREEN.blit(WBishop, (promotion_width+SQUARE_SIZE*3,
                              promotion_height))

        Knight_square = pg.draw.rect(SCREEN, (80, 40, 40), (promotion_width+SQUARE_SIZE*4,
                                                            promotion_height, SQUARE_SIZE*1.1, SQUARE_SIZE*1.1))
        SCREEN.blit(WKnight, (promotion_width +
                              SQUARE_SIZE*4, promotion_height))

        SCREEN_update()
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN:
                if Queen_square.collidepoint(pg.mouse.get_pos()):
                    to_move = to_move + "q"
                    CHOOSINGMOVE = False
                    break

                elif Rook_square.collidepoint(pg.mouse.get_pos()):
                    to_move = to_move + "r"
                    CHOOSINGMOVE = False
                    break

                elif Bishop_square.collidepoint(pg.mouse.get_pos()):
                    to_move = to_move + "b"
                    CHOOSINGMOVE = False
                    break

                elif Knight_square.collidepoint(pg.mouse.get_pos()):
                    to_move = to_move + "n"
                    CHOOSINGMOVE = False
                    break
            elif event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            else:
                pass

    total_move = from_move + to_move
    board.push_san(total_move)


def get_legal_moves(rect_clicked):
    global from_move
    index = rect_list.index(rect_clicked[0])
    clicked_coord = coord_list[index]
    from_move = clicked_coord
    possible_moves = []

    for i in list(board.pseudo_legal_moves):
        uci = i.uci()[:2]
        if uci == from_move:
            possible_moves.append(i)
    for i in possible_moves:
        try:
            coord_index = coord_list.index(
                i.uci()[2:4])
            working_rect = rect_list[coord_index]
            rect_moves.append(working_rect)
        except ValueError:
            check_for_promotion(i.uci()[2:])


def draw_pieces(fen):
    col = SQUARE_SIZE
    row = SQUARE_SIZE
    for i in fen:
        if i == " ":
            break
        elif i == "/":
            col += SQUARE_SIZE
            row = SQUARE_SIZE
        elif i in ["1", "2", "3", "4", "5", "6", "7", "8"]:
            row += SQUARE_SIZE*int(i)
        elif i == "K":
            SCREEN.blit(WKing, (row, col))
            row += SQUARE_SIZE
        elif i == "k":
            SCREEN.blit(BKing, (row, col))
            row += SQUARE_SIZE
        elif i == "N":
            SCREEN.blit(WKnight, (row, col))
            row += SQUARE_SIZE
        elif i == "n":
            SCREEN.blit(BKnight, (row, col))
            row += SQUARE_SIZE
        elif i == "R":
            SCREEN.blit(WRook, (row, col))
            row += SQUARE_SIZE
        elif i == "r":
            SCREEN.blit(BRook, (row, col))
            row += SQUARE_SIZE
        elif i == "Q":
            SCREEN.blit(WQueen, (row, col))
            row += SQUARE_SIZE
        elif i == "q":
            SCREEN.blit(BQueen, (row, col))
            row += SQUARE_SIZE
        elif i == "B":
            SCREEN.blit(WBishop, (row, col))
            row += SQUARE_SIZE
        elif i == "b":
            SCREEN.blit(BBishop, (row, col))
            row += SQUARE_SIZE
        elif i == "P":
            SCREEN.blit(WPawn, (row, col))
            row += SQUARE_SIZE
        elif i == "p":
            SCREEN.blit(BPawn, (row, col))
            row += SQUARE_SIZE
        elif i == "z":
            SCREEN.blit(BDuck, (row, col))
            row += SQUARE_SIZE
        elif i == "Z":
            SCREEN.blit(Duck, (row, col))
            row += SQUARE_SIZE
        else:
            row += SQUARE_SIZE


def computer_move():
    legal_moves = list(board.pseudo_legal_moves)
    thinking = pg.time.get_ticks()

    try:
        move = random.choice(legal_moves)
        board.f_push(move)
    except IndexError:
        check_game_over()
        if GAMEOVER == False:
            move = legal_moves[0]
            board.f_push(move)
    finally:
        time_thinking = random.randint(500, 1000)
        while True:
            now = pg.time.get_ticks()
            if now - thinking >= time_thinking:
                break
        SCREEN_update()


while True:
    check_game_over()

    y_var = HEIGHT-(HEIGHT/6)
    SCREEN.fill("WHITE")
    n = 20

    if GAMEOVER:
        rendered_text = font.render("GAME OVER", True, (0, 0, 0))

        OUTCOME = board.outcome()
        OUTCOME = str(OUTCOME)
        OUTCOME = OUTCOME.split(" ")
        OUTCOME = OUTCOME[-1]
        OUTCOME = OUTCOME.replace("winner=", "").replace(")", "")
        print(OUTCOME)
        if OUTCOME == "True":
            rendered_text = font.render("YOU WIN", True, (0, 0, 0))

        elif OUTCOME == "False":
            rendered_text = font.render("YOU LOSE", True, (0, 0, 0))

        else:
            rendered_text = font.render("YOU DREW", True, (0, 0, 0))
        SCREEN_update()

        pg.time.delay(5000)
        pg.quit()
        sys.exit()

    if board.turn == False:

            
        computer_move()


    else:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                pos = pg.mouse.get_pos()
                rect_clicked = [
                    rect for rect in rect_list if rect.collidepoint(pos)]
                try:
                    rect_moves = []
                    FROMMOVE = True
                    while FROMMOVE:
                        get_legal_moves(rect_clicked)
                        TOMOVE = True

                        while TOMOVE:
                            rect_update(rect_moves)
                            for event in pg.event.get():
                                if event.type == pg.QUIT:
                                    pg.quit()
                                    sys.exit()

                                elif event.type == pg.MOUSEBUTTONDOWN:
                                    pos = pg.mouse.get_pos()
                                    rect_clicked = [
                                        rect for rect in rect_list if rect.collidepoint(pos)]

                                    if rect_clicked[0] in rect_moves:
                                        index = rect_list.index(
                                            rect_clicked[0])
                                        to_move = coord_list[index]
                                        total_move = from_move + to_move
                                        try:
                                            board.f_push(duck_chess.Move.from_uci(total_move))
                                        except ValueError:
                                            check_for_promotion(
                                                to_move, CHOOSINGMOVE=True)
                                        SCREEN_update()
                                        duck_move = True
                                        while duck_move:
                                            from_move = "Z@"
                                            rect_moves = get_duck_moves()
                                            rect_update(rect_moves)
                                            for event in pg.event.get():
                                                if event.type == pg.QUIT:
                                                    pg.quit()
                                                    sys.exit()

                                                elif event.type == pg.MOUSEBUTTONDOWN:
                                                    pos = pg.mouse.get_pos()
                                                    rect_clicked = [
                                                        rect for rect in rect_list if rect.collidepoint(pos)]

                                                    if rect_clicked[0] in rect_moves:
                                                        index = rect_list.index(
                                                            rect_clicked[0])
                                                        to_move = coord_list[index]
                                                        total_move = from_move + to_move
                                                        print(total_move)
                                                        print(board.turn)
                                                        board.duck_push(duck_chess.Move.from_uci(total_move))
                                                        print(board.turn)
                                                        SCREEN_update()
                                                        FROMMOVE = False
                                                        duck_move = False

                                                
                                        FROMMOVE = False
                                        TOMOVE = False
                                        break
                                    elif rect_clicked[0] not in rect_moves:

                                        rect_moves.clear()
                                        get_legal_moves(rect_clicked)

                                        rect_update(rect_moves)

                except IndexError:
                    continue

