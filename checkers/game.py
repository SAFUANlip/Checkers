import pygame
from checkers.board import Board
from .constants import RED, WHITE, BLUE, SQUARE_SIZE
from .figure import Figure


class Game:
    def __init__(self, win):
        self._init()
        self.win = win

    def winner(self):
        return self.board.winner()


    def update(self):
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def reset(self):
        self._init()

    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = RED
        self.valid_moves = {}

    def select(self, row, col):
        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)

        figure = self.board.get_figure(row, col)
        if figure != 0 and figure.color == self.turn:
            self.selected = figure
            self.valid_moves = self.board.get_valid_moves(figure)
            return True

        return False

    # _move - private
    def _move(self, row, col):
        figure = self.board.get_figure(row, col)
        if self.selected and figure == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped)
            self.change_turn()
        else:
            return False

        return True

    def change_turn(self):
        self.valid_moves = {}
        if self.turn == RED:
            self.turn = WHITE
        else:
            self.turn = RED

    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, BLUE, (col * SQUARE_SIZE + SQUARE_SIZE//2,\
                                                row * SQUARE_SIZE + SQUARE_SIZE//2), 15)