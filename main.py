import pygame
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, RED, WHITE
from checkers.board import Board
from checkers.game import Game
from minimax.algorithm import minimax

# big help from https://www.youtube.com/channel/UC4JX40jDee_tINbkjycV4Sg

FPS = 60

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')


def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col


def main():
    go = True
    clock = pygame.time.Clock()
    game = Game(WINDOW)

    while go:
        clock.tick(FPS)

        if game.turn == WHITE:
            value, new_board = minimax(game.get_board(), 4, WHITE, game)
            game.ai_move(new_board)

        if game.winner() != None:
            if game.winner() == WHITE:
                print('white won')
            else:
                print('red won')
            go = False

        for event in pygame.event.get():  # check that something happened
            if event.type == pygame.QUIT:
                go = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)

        game.update()

    pygame.quit()

main()