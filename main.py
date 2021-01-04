import numpy as np
import pygame

NUM_ROWS = 6
NUM_COLS = 6
k = 4
player = 1

global GAME_OVER
GAME_OVER = False

class Board:
    def __init__(self):
        self.rows = NUM_ROWS
        self.cols = NUM_COLS
        self.k = k
        self.board = np.zeros((NUM_ROWS, NUM_COLS))

    def show(self):
        print(self.board)

    def not_full(self, col):
        return self.board[0, col] == 0

    def place_piece(self, col, player):
        for row in range(self.rows - 1, -1, -1):
            if self.board[row, col] == 0:
                self.board[row, col] = player
                return [row, col]
                break

    def in_board(self, row, col):
        valid_row = (row > -1 and row < self.rows)
        valid_col = (col > -1 and col < self.cols)
        return valid_col and valid_row

    def game_over(self, player, piece_loc):
        piece_row = piece_loc[0]
        piece_col = piece_loc[1]

        ## Check vertical
        if piece_row <= self.cols - k:
            connected = True
            for row in range(piece_loc[0], piece_loc[0] + k):
                if self.board[row, piece_col] != player:
                    connected = False
                    break
            if connected == True:
                print("{} WINS !!!!".format(player))
                return True

        ## Check horizontal
        max_left = 0
        max_right = 0

        current_left = piece_loc[1] - 1
        current_right = piece_loc[1] + 1

        for col in range(current_left, current_left - k + 1, -1):
            if self.in_board(piece_row, col) and self.board[piece_row, col] == player:
                max_left += 1
            else:
                break
        for col in range(current_right, current_right + k - 1):
            if self.in_board(piece_row, col) and self.board[piece_row, col] == player:
                max_right += 1
            else:
                break

        if max_left + max_right + 1 >= k:
            print("{} WINS!!!".format(player))
            return True

        ## Check diags
        ## One type of diag
        max_left= 0
        max_right = 0

        left_move = 1
        right_move = 1

        for move in range(left_move, left_move + k):
            if self.in_board(piece_row - move, piece_col - move) and self.board[piece_row - move, piece_col - move] == player:
                max_left += 1
            else:
                break
        for move in range(right_move, right_move + k):
            if self.in_board(piece_row + move, piece_col + move) and self.board[piece_row + move, piece_col + move] == player:
                max_right += 1
            else:
                break
        if max_left + max_right + 1 >= k:
            print("{} WINS!!!".format(player))
            return True

        # Other type of diag
        max_left = 0
        max_right = 0

        left_move = 1
        right_move = 1

        for move in range(left_move, left_move + k):
            if self.in_board(piece_row + move, piece_col - move) and self.board[
                piece_row + move, piece_col - move] == player:
                max_left += 1
            else:
                break

        for move in range(right_move, right_move + k):
            if self.in_board(piece_row - move, piece_col + move) and self.board[
                piece_row - move, piece_col + move] == player:
                max_right += 1
            else:
                break
        if max_left + max_right + 1 >= k:
            print("{} WINS!!!".format(player))
            return True

        return False

board = Board()

for i in range(NUM_COLS):
    print(i)
while not GAME_OVER:
    if player == 1:
        move = int(input("Player 1 move (0-{})".format(NUM_COLS - 1)))
        if board.not_full(move):
            piece_loc = board.place_piece(move, player)
            board.show()
            GAME_OVER = board.game_over(player, piece_loc)
            player = 2

    elif player == 2:
        move = int(input("Player 2 move (0-{})".format(NUM_COLS - 1)))
        if board.not_full(move):
            piece_loc = board.place_piece(move, player)
            board.show()
            GAME_OVER = board.game_over(player, piece_loc)
            player = 1
