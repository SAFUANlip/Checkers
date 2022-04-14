import pygame
from .constants import RED, WHITE, GREY, SQUARE_SIZE, QUEEN


class Figure:
    INDENT = 10
    OUTLINE = 2

    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.queen = False

        if self.color == RED:
            self.direction = -1  # because it's up in board coardinates
        else:
            self.direction = 1

        self.x = 0
        self.y = 0
        self.calc_pos()

    def calc_pos(self):
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2 # being in the center
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    def turn_queen(self):
        self.queen = True

    def draw(self, win):
        radius = SQUARE_SIZE//2 - self.INDENT
        pygame.draw.circle(win, GREY, (self.x, self.y), radius + self.OUTLINE)
        pygame.draw.circle(win, self.color, (self.x, self.y), radius)
        if self.queen:
            win.blit(QUEEN, (self.x - QUEEN.get_width()//2, self.y - QUEEN.get_height()//2))  # put image

    def move(self, row, col):
        self.row = row
        self.col = col
        self.calc_pos()

    def __repr__(self):
        return str(self.color)
