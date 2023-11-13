import pygame as pg
from pygame.locals import (QUIT, KEYDOWN, K_KP1, K_KP2, K_KP3, K_KP4, K_KP5, K_KP6,
                           K_KP7, K_KP8, K_KP9, K_SPACE, K_ESCAPE, K_q)

WIDTH = 600
HEIGHT = 600

X_COLOR = (84, 84, 84)
O_COLOR = (242, 235, 211)

BG_COLOR = (20, 189, 172)
LINE_COLOR = (13, 161, 146)
LINE_WIDTH = 15
BOARD_ROWS = 3
BOARD_COLUMNS = 3

pg.init()
screen = pg.display.set_mode([WIDTH, HEIGHT])
pg.display.set_caption('TIC-TAC-TOE 2021 Highlander Edition')
icon = pg.image.load('tic-tac-toe.ico')
pg.display.set_icon(icon)
clock = pg.time.Clock()
FPS = 60


def new_board():
    """ Draws an empty pygame main game board and returns a list for the new game board """
    screen.fill(BG_COLOR)
    render_grid()
    render_scores()
    pg.display.update()

    return [
        '1', '2', '3',
        '4', '5', '6',
        '7', '8', '9',
    ]


def slot_selection(slot):
    global winning_token, player_token
    check_valid_slot(slot)
    player_won = winning_token = check_for_win(player_token)
    if not player_won:
        player_token = 'O' if player_token == 'X' else 'X'
    update_screen()


def check_for_win(current_player):
    """ Check if player wins """
    global scores, player_token, game_is_draw

    # check for win on horizontal lines
    if board[0] == board[1] == board[2] or board[3] == board[4] == board[5] or board[6] == board[7] == board[8]:
        scores[current_player] += 1
        return current_player

    # Check for win on vertical lines
    elif board[0] == board[3] == board[6] or board[1] == board[4] == board[7] or board[2] == board[5] == board[8]:
        scores[current_player] += 1
        return current_player

    # Check for win on diagonal lines
    elif board[0] == board[4] == board[8] or board[2] == board[4] == board[6]:
        scores[current_player] += 1
        return current_player

    # Check if board is full and nobody won
    elif slots_filled == 9 and not winning_token:
        game_is_draw = True
        scores['D'] += 1

    return False


def check_valid_slot(slot):
    global slots_filled

    position = board[int(slot)-1]

    if slot == position:
        board[int(position)-1] = player_token
        slots_filled += 1


def render_grid():
    pg.draw.line(screen, LINE_COLOR, (10, 200), (590, 200), LINE_WIDTH)  # 1st horizontal line
    pg.draw.line(screen, LINE_COLOR, (10, 400), (590, 400), LINE_WIDTH)  # 2nd horizontal line
    pg.draw.line(screen, LINE_COLOR, (200, 10), (200, 590), LINE_WIDTH)  # 1st vertical line
    pg.draw.line(screen, LINE_COLOR, (400, 10), (400, 590), LINE_WIDTH)  # 2nd vertical line


def render_token(index, token):
    """ Draws the current game board (Interpreter) """

    pos_x = 0
    pos_y = 0

    if token == 'O':

        if index == 0 or index == 1 or index == 2:
            pos_x = index * 200 + 100
            pos_y = 100

        elif index == 3 or index == 4 or index == 5:
            pos_x = (index - 3) * 200 + 100
            pos_y = 300

        elif index == 6 or index == 7 or index == 8:
            pos_x = (index - 6) * 200 + 100
            pos_y = 500

        pg.draw.circle(screen, O_COLOR, (pos_x, pos_y), 70, 15)

    elif token == 'X':

        if index == 0 or index == 1 or index == 2:
            pos_x = index * 200 + 35
            pos_y = 35

        if index == 3 or index == 4 or index == 5:
            pos_x = (index - 3) * 200 + 35
            pos_y = 235

        if index == 6 or index == 7 or index == 8:
            pos_x = (index - 6) * 200 + 35
            pos_y = 435

        pg.draw.line(screen, X_COLOR, (pos_x, pos_y), (pos_x + 130, pos_y + 130), 15)
        pg.draw.line(screen, X_COLOR, (pos_x, pos_y + 130), (pos_x + 130, pos_y), 15)


def render_winning_line(current_player):
    color = O_COLOR if current_player == 'X' else X_COLOR
    if board[0] == board[1] == board[2]:
        pg.draw.line(screen, color, (100, 100), (500, 100), 12)
    elif board[3] == board[4] == board[5]:
        pg.draw.line(screen, color, (100, 300), (500, 300), 12)
    elif board[6] == board[7] == board[8]:
        pg.draw.line(screen, color, (100, 500), (500, 500), 12)

    elif board[0] == board[3] == board[6]:
        pg.draw.line(screen, color, (100, 100), (100, 500), 12)
    elif board[1] == board[4] == board[7]:
        pg.draw.line(screen, color, (300, 100), (300, 500), 12)
    elif board[2] == board[5] == board[8]:
        pg.draw.line(screen, color, (500, 100), (500, 500), 12)

    elif board[0] == board[4] == board[8]:
        pg.draw.line(screen, color, (100, 100), (500, 500), 15)
    elif board[6] == board[4] == board[2]:
        pg.draw.line(screen, color, (100, 500), (500, 100), 15)

    render_scores()
    pg.display.update()


def render_scores():
    # Draws score table
    font_color = (255, 255, 255)
    shadow_color = (0, 0, 0)
    font = pg.font.SysFont('Courier', 24, True, False)

    score_x_shadow = font.render(f"Player 1: {scores['X']}", True, shadow_color)
    score_x = font.render(f"Player 1: {scores['X']}", True, font_color)
    score_draw_shadow = font.render(f"Draw: {scores['D']}", True, shadow_color)
    score_draw = font.render(f"Draw: {scores['D']}", True, font_color)
    score_o_shadow = font.render(f"Player 2: {scores['O']}", True, shadow_color)
    score_o = font.render(f"Player 2: {scores['O']}", True, font_color)

    screen.blit(score_x_shadow, (26, 571))
    screen.blit(score_x, (25, 570))
    screen.blit(score_draw_shadow, (251, 571))
    screen.blit(score_draw, (250, 570))
    screen.blit(score_o_shadow, (426, 571))
    screen.blit(score_o, (425, 570))


def render_text():
    """ Renders text to the screen """
    font_color = X_COLOR if winning_token == 'X' else O_COLOR
    alt_color = O_COLOR if winning_token == 'X' else X_COLOR
    # shadow_color = (0, 0, 0)

    # Renders text for the winning player
    if winning_token:
        pg.time.delay(1500)
        font1 = pg.font.SysFont('Arial', 200, True)
        font2 = pg.font.SysFont('Courier', 64, True)
        text1 = font1.render(f'{winning_token}', True, font_color)
        text2 = font2.render('WINS!', True, alt_color)
        screen.fill(BG_COLOR)
        screen.blit(text1, (250, 140))
        screen.blit(text2, (220, 340))

    # Renders text if game ends in Draw
    elif slots_filled == 9 and not winning_token:
        pg.time.delay(1500)

        font1 = pg.font.SysFont('Arial', 200, True)
        font2 = pg.font.SysFont('Courier', 64, True)
        text1 = font1.render("X", True, X_COLOR)
        text2 = font1.render("O", True, O_COLOR)
        text3 = font2.render(f"IT'S A DRAW!", True, X_COLOR)
        screen.fill(BG_COLOR)
        screen.blit(text1, (200, 140))
        screen.blit(text2, (295, 140))
        screen.blit(text3, (85, 340))


def new_game():
    global slots_filled, board, player_token, winning_token, game_is_draw
    slots_filled = 0
    board = new_board()
    player_token = 'X'
    winning_token = False
    game_is_draw = False
    update_screen()


def update_screen():
    # Fill the background
    screen.fill(BG_COLOR)
    # draw grid
    render_grid()
    # draw tokens based on board list
    for index, token in enumerate(board):
        render_token(index, token)
    # draw win lines
    render_winning_line(player_token)
    # render text
    render_text()
    # Update the screen
    pg.display.update()


scores = {'X': 0, 'O': 0, 'D': 0}
slots_filled = 0
player_token = 'X'
winning_token = False
game_is_draw = False
board = new_board()

# MAINLOOP
running = True
while running:
    for event in pg.event.get():

        if event.type == QUIT:
            running = False

        if event.type == KEYDOWN:
            if event.key == K_KP7 and not winning_token:
                slot_selection('1')
            if event.key == K_KP8 and not winning_token:
                slot_selection('2')
            if event.key == K_KP9 and not winning_token:
                slot_selection('3')
            if event.key == K_KP4 and not winning_token:
                slot_selection('4')
            if event.key == K_KP5 and not winning_token:
                slot_selection('5')
            if event.key == K_KP6 and not winning_token:
                slot_selection('6')
            if event.key == K_KP1 and not winning_token:
                slot_selection('7')
            if event.key == K_KP2 and not winning_token:
                slot_selection('8')
            if event.key == K_KP3 and not winning_token:
                slot_selection('9')
            if event.key == K_ESCAPE or event.key == K_q:
                running = False
            if event.key == K_SPACE and (winning_token or game_is_draw):
                new_game()

    # Update the screen

    pg.display.update()
    clock.tick(FPS)

pg.quit()
