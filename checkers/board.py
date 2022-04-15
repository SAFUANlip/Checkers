import pygame
from .constants import BLACK, RED, ROWS, WHITE, COLS, SQUARE_SIZE
from .figure import Figure


class Board:
    def __init__(self):
        self.board = []
        #self.selected_piece = None
        self.red_left = self.white_left = 12
        self.red_queen = self.white_queen = 0
        self.create_board()

    def draw_field(self, win):
        win.fill(BLACK)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(win, RED, (row*SQUARE_SIZE, col*SQUARE_SIZE,\
                                            SQUARE_SIZE, SQUARE_SIZE))

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self.board[row].append(Figure(row, col, WHITE))
                    elif row > 4:
                        self.board[row].append(Figure(row, col, RED))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def draw(self, win):
        self.draw_field(win)
        for row in range(ROWS):
            for col in range(COLS):
                figure = self.board[row][col]
                if figure != 0:
                    figure.draw(win)

    def remove(self, figures):
        for figure in figures:
            self.board[figure.row][figure.col] = 0
            if figure != 0:
                if figure.color == RED:
                    self.red_left -= 1
                else:
                    self.white_left -= 1

    def winner(self):
        if self.red_left <= 0:
            return WHITE
        elif self.white_left <= 0:
            return RED

        return None

    def move(self, figure, row, col):
        # swapp
        self.board[figure.row][figure.col], self.board[row][col] = self.board[row][col], self.board[figure.row][figure.col]
        figure.move(row, col)

        if row == ROWS - 1 and figure.color == WHITE:
            self.white_queen += 1
            figure.turn_queen()
            print(f"red: {self.red_queen}, white: {self.white_queen}")

        elif row == 0 and figure.color == RED:
            self.red_queen += 1
            figure.turn_queen()
            print(f"red: {self.red_queen}, white: {self.white_queen}")

    def get_figure(self, row, col):
        return self.board[row][col]

    def get_valid_moves(self, figure):
        moves = {}
        left = figure.col - 1
        right = figure.col + 1
        row = figure.row

        if figure.color == RED or figure.queen:
            moves.update(self._traverse_left(row - 1, max(row-3, -1), -1, figure.color, left))
            moves.update(self._traverse_right(row - 1, max(row-3, -1), -1, figure.color, right))
        if figure.color == WHITE or figure.queen:
            moves.update(self._traverse_left(row + 1, min(row + 3, ROWS), 1, figure.color, left))
            moves.update(self._traverse_right(row + 1, min(row + 3, ROWS), 1, figure.color, right))
        return moves

    def _traverse_left(self, start, stop, step, color, left):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break
            current = self.board[r][left]
            if current == 0:
                moves[(r, left)] = last  # if we saw the figure what we need pass
                if last:
                    left -= 1
                break
            elif current.color == color:
                break
            else:
                last = [current]
            left -= 1
        return moves

    def _traverse_right(self, start, stop, step, color, right):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break
            current = self.board[r][right]
            if current == 0:
                moves[(r, right)] = last
                if last:
                    right += 1
                break
            elif current.color == color:
                break
            else:
                last = [current]
            right += 1
        return moves