import pygame
import sys
import numpy as np
import board_utils as bu
import math
import ut3_game
import random_agent
import human_agent
import time


X_COLOR = (255, 128, 128)
O_COLOR = (128, 128, 255)
BLOCKED_COLOR = (32, 32, 32)
BACK_COLOR = (64, 64, 64)
LINE_COLOR = (128, 128, 128)
CHOICE_COLOR = BLOCKED_COLOR
DIRECTIVE_COLOR = (255, 255, 196)
LAST_MOVE_COLOR = (0, 255, 0)
FONT_COLOR = BLOCKED_COLOR

TURN_DELAY = 1.0


LINE_WIDTH = 4
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FONT_SIZE = 48

BOARD_SIZE = SCREEN_HEIGHT / 6
TILE_SIZE = BOARD_SIZE / 3
PAD_SPACE = BOARD_SIZE / 5

META_X_START = SCREEN_WIDTH / 2 - 0.5 * BOARD_SIZE
META_Y_START = PAD_SPACE * 2

GLOBAL_X_START = SCREEN_WIDTH / 2 - 1.5 * BOARD_SIZE - PAD_SPACE
GLOBAL_Y_START = META_Y_START + BOARD_SIZE + PAD_SPACE * 2

INNER_PADDING = BOARD_SIZE / 10

META_KEYS = {1:"X", -1: "O", None:" ", 0:"~"}
GLOBAL_KEYS = {1:"X", -1: "O", 0:" "}


TEST_DIRECTIVE = (1, 0)
TEST_LAST_MOVE = (8, 7)
# TEST_PLAYER_NAME = "Player 1"
TEST_BOARD = global_board = bu.make_global_board([
            [-1, 0, 0,    1, 0, 0,   1, 0, 0],
            [0, 1, 0,     0, 0, 0,   0, 1, 0],
            [1, -1, -1,   1, 0, 0,   0, 0, 1],

            [0, 0, -1,   0, 0, -1,   -1, 0, 0],
            [0, 1, -1,   0, -1, 0,   -1, 0, 0],
            [0, 0, -1,   -1, 0, 0,   -1, 0, 0],

            [0, -1, -1, 0, -1, 1, 1, 0, 0],
            [1, 1, 1,   0, 0, 0,  1, 0, 1],
            [-1, 0, 1,  0, 1, 0,  1, -1, -1]])

def draw_global_board(screen, global_board, directive, last_move):
    if directive is None:
        draw_directive(screen, (GLOBAL_X_START, GLOBAL_Y_START), None)
    for r in range(3):
        for c in range(3):
            local_board = bu.get_local_board(global_board, (r, c))
            pos = (GLOBAL_X_START + c * (BOARD_SIZE + PAD_SPACE),
                               GLOBAL_Y_START + r * (BOARD_SIZE + PAD_SPACE))
            if directive == (r, c):
                draw_directive(screen, pos, directive)
            if last_move is not None and (last_move[0] // 3, last_move[1] // 3) == (r, c):
                draw_last_move_indicator(screen, pos, (last_move[0]%3, last_move[1]%3))
            draw_hash(screen, pos, local_board)
            draw_win_streaks(screen, pos, bu.get_win_streak(local_board))
            draw_tiles(screen, pos, local_board, GLOBAL_KEYS)

def draw_win_streaks(screen, pos, streak):
    if streak is None:
        return
    start, end = streak
    start_pos = np.array((pos[0] + start[1] * TILE_SIZE + TILE_SIZE / 2,
                 pos[1] + start[0] * TILE_SIZE + TILE_SIZE / 2))
    end_pos = np.array((pos[0] + end[1] * TILE_SIZE + TILE_SIZE / 2,
               pos[1] + end[0] * TILE_SIZE + TILE_SIZE / 2))
    d = end_pos - start_pos
    n = d / 4
    pygame.draw.line(screen, BLOCKED_COLOR, start_pos - n, end_pos + n, 2*LINE_WIDTH)

def draw_last_move_indicator(screen, pos, last_move):
    pygame.draw.rect(screen, LAST_MOVE_COLOR,
                     pygame.Rect((pos[0] + INNER_PADDING /2 + last_move[1] * (TILE_SIZE),
                                  pos[1] + INNER_PADDING /2 + last_move[0] * (TILE_SIZE)),
                                 (TILE_SIZE - INNER_PADDING,
                                  TILE_SIZE - INNER_PADDING)), width=2)

def draw_directive(screen, pos, directive):
    if directive is None:
        pygame.draw.rect(screen, DIRECTIVE_COLOR,
                         pygame.Rect((pos[0] - INNER_PADDING, pos[1] - INNER_PADDING),
                                     (BOARD_SIZE*3 + PAD_SPACE*2 + INNER_PADDING * 2, BOARD_SIZE*3 + PAD_SPACE*2 + INNER_PADDING * 2)))
    else:
        pygame.draw.rect(screen, DIRECTIVE_COLOR,
                         pygame.Rect((pos[0] - INNER_PADDING, pos[1] - INNER_PADDING),
                                     (BOARD_SIZE + INNER_PADDING * 2, BOARD_SIZE + INNER_PADDING * 2)))

def draw_meta_board(screen, meta_board):
    draw_hash(screen, (META_X_START, META_Y_START), meta_board)
    draw_win_streaks(screen, (META_X_START, META_Y_START), bu.get_win_streak(meta_board))
    draw_tiles(screen, (META_X_START, META_Y_START), meta_board, META_KEYS)

def draw_hash(screen, pos, local_board):
    # Draw vertical lines
    pygame.draw.line(screen, LINE_COLOR, (pos[0] + TILE_SIZE, pos[1]),
                     (pos[0] + TILE_SIZE, pos[1] + BOARD_SIZE),

                     LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (pos[0] + 2*TILE_SIZE, pos[1]),
                     (pos[0] + 2*TILE_SIZE, pos[1] + BOARD_SIZE),
                     LINE_WIDTH)

    # Draw horizontal lines
    pygame.draw.line(screen, LINE_COLOR, (pos[0], pos[1] + TILE_SIZE),
                     (pos[0] + BOARD_SIZE, pos[1] + TILE_SIZE),
                     LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (pos[0], pos[1] + 2*TILE_SIZE),
                     (pos[0] + BOARD_SIZE, pos[1] + 2*TILE_SIZE),
                     LINE_WIDTH)
def draw_x(screen, pos):
    pygame.draw.line(screen, X_COLOR, (pos[0] + INNER_PADDING, pos[1] + INNER_PADDING),
                     (pos[0] + TILE_SIZE - INNER_PADDING, pos[1] + TILE_SIZE - INNER_PADDING),
                     LINE_WIDTH)
    pygame.draw.line(screen, X_COLOR, (pos[0] + INNER_PADDING, pos[1] + TILE_SIZE - INNER_PADDING),
                     (pos[0] + TILE_SIZE - INNER_PADDING, pos[1] + INNER_PADDING),
                     LINE_WIDTH)

def draw_o(screen, pos):
    pygame.draw.circle(screen, O_COLOR, (pos[0] + TILE_SIZE/2, pos[1] + TILE_SIZE/2), (TILE_SIZE-INNER_PADDING*2-LINE_WIDTH), LINE_WIDTH)

def draw_blocked(screen, pos):
    pygame.draw.rect(screen, BLOCKED_COLOR,
                     pygame.Rect((pos[0] + INNER_PADDING, pos[1] + INNER_PADDING),
                                 (TILE_SIZE - INNER_PADDING*2, TILE_SIZE - INNER_PADDING*2)))

def draw_tiles(screen, pos, board, keys):
    for r in range(3):
        for c in range(3):
            if keys[board[r, c]] == "X":
                draw_x(screen, (pos[0] + c*TILE_SIZE, pos[1]+r*TILE_SIZE))
            if keys[board[r, c]] == "O":
                draw_o(screen, (pos[0] + c*TILE_SIZE, pos[1]+r*TILE_SIZE))
            if keys[board[r, c]] == "~":
                draw_blocked(screen, (pos[0] + c*TILE_SIZE, pos[1]+r*TILE_SIZE))

def dist(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

def get_input(screen):
    mouse_pos = pygame.mouse.get_pos()

    closest_dist = math.inf
    closest_tile = None
    closest_pos = None
    meta_choice = None
    for meta_r in range(3):
        for meta_c in range(3):
            for r in range(3):
                for c in range(3):
                    tile_pos = (GLOBAL_X_START + meta_c * (BOARD_SIZE + PAD_SPACE) + TILE_SIZE * c + TILE_SIZE/2,
                                GLOBAL_Y_START + meta_r * (BOARD_SIZE + PAD_SPACE) + TILE_SIZE * r + TILE_SIZE/2)
                    d = dist(tile_pos, mouse_pos)
                    if d < closest_dist and d < TILE_SIZE/2:
                        closest_dist = d
                        closest_tile = (meta_r * 3 + r, meta_c * 3 + c)
                        closest_pos = tile_pos
                        meta_choice = (meta_r, meta_c)
                    # pygame.draw.circle(screen, (0,0,0), tile_pos, 5)
    return closest_tile, closest_pos, meta_choice



def start_window(game: ut3_game.UT3Game, agent1, agent2, aggro):
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    gameFont = pygame.font.SysFont(None, FONT_SIZE)
    current_player_text = gameFont.render("Current Player:", True, FONT_COLOR)
    win_text = gameFont.render("The winner is:", True, FONT_COLOR)
    tie_text = gameFont.render("The game was a tie:", True, FONT_COLOR)
    first_player_turn = True
    is_human1 = isinstance(agent1, human_agent.HumanAgent)
    is_human2 = isinstance(agent2, human_agent.HumanAgent)

    player1_text = gameFont.render(agent1.player_name, True, X_COLOR)
    player2_text = gameFont.render(agent2.player_name, True, O_COLOR)
    game.start(agent1, agent2)

    screen.fill(pygame.Color(0, 0, 0))
    game_not_over = True
    last_turn = time.time() - TURN_DELAY
    global_board = game.global_board
    directive = None

    while True:
        screen.fill(BACK_COLOR)
        mouse_up = False
        choice_inidcator_pos = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_up = True
        if game_not_over:
            seconds_since_last_move = time.time() - last_turn
            if seconds_since_last_move > TURN_DELAY:
                agent = agent1 if first_player_turn else agent2
                is_human = is_human1 if first_player_turn else is_human2
                if not is_human:
                    game_not_over = game.make_move(agent)
                    first_player_turn = not first_player_turn
                    if not (is_human1 or is_human2):
                        last_turn = time.time()
                else:
                    choice, choice_pos, meta_choice = get_input(screen)
                    if choice is not None and \
                            not bu.is_player(global_board[choice]) \
                            and (directive is None or meta_choice == directive):
                        choice_inidcator_pos = choice_pos
                        if mouse_up:
                            agent.next_move = choice
                            game_not_over = game.make_move(agent)
                            first_player_turn = not first_player_turn
                            last_turn = time.time()

            screen.blit(current_player_text, (50, 50))
            screen.blit(player1_text if first_player_turn else player2_text, (50, 100))
        else:
            if bu.is_player(game.winner):
                screen.blit(win_text, (50, 50))
                screen.blit(player1_text if game.winner == 1 else player2_text, (50, 100))
            else:
                screen.blit(tie_text, (50, 50))




        global_board = game.global_board
        directive = game.next_local_board_index
        last_move = game.last_move

        draw_global_board(screen, global_board, directive, last_move)
        draw_meta_board(screen, bu.get_meta_board(global_board))
        if choice_inidcator_pos is not None:
            pygame.draw.circle(screen, CHOICE_COLOR, choice_inidcator_pos, TILE_SIZE / 2)
            if first_player_turn:
                draw_x(screen, (choice_inidcator_pos[0] - TILE_SIZE/2, choice_inidcator_pos[1]-TILE_SIZE/2))
            else:
                draw_o(screen, (choice_inidcator_pos[0] - TILE_SIZE/2, choice_inidcator_pos[1]-TILE_SIZE/2))


        pygame.display.flip()

if __name__ == '__main__':
    game = ut3_game.UT3Game()
    # rand_agent = random_agent.RandomAgent("Random agent 1")
    # rand_agent2 = random_agent.RandomAgent("Random agent 2")
    # start_window(game, rand_agent, rand_agent2, 0.5)

    human = human_agent.HumanAgent("Human agent1")
    human2 = human_agent.HumanAgent("Human agent2")
    start_window(game, human, human2, 0.5)

