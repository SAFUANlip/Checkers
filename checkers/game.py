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
        self.flag_step_before = False

    def select(self, row, col):
        if self.selected:
            if self.flag_step_before and (row, col) in self.valid_moves or not self.flag_step_before:
                result = self._move(row, col)
                if result == 2:
                    self.selected = None
                    self.select(row, col)
                if result == 0:
                    figure = self.board.get_figure(row, col)
                    old_valid_moves = self.valid_moves
                    self.valid_moves = self.board.get_valid_moves(figure)
                    print(self.valid_moves)
                    check = False
                    for i in self.valid_moves.values():
                        if len(i):
                            check = True
                    if check and old_valid_moves[(row, col)]:
                        self.selected = self.board.get_figure(row, col)
                        self.flag_step_before = True
                        return True
                    else:
                        self.change_turn()
                        self.selected = None
                        return False
            else:
                return False

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
                return 0  # skip figure, so ve need look again, for another move
            else:
                self.change_turn()
        else:
            return 2  # False

        return 1  # True

    def change_turn(self):
        self.flag_step_before = False
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

    def get_board(self):
        return self.board

    def ai_move(self, board):
        self.board = board
        self.change_turn()