import pygame
import numpy as np
import math

pygame.init()
pygame.font.init()

myfont = pygame.font.SysFont('Comic Sans MS', 30)

## Variables
NUM_ROWS = 6
NUM_COLS = 7
k = 4

global player
player = 1

## Make Screen
screen = pygame.display.set_mode((NUM_COLS * 100, (NUM_ROWS+ 1) * 100))

## Title and Icon
## Background Attribution
pygame.display.set_caption("Connect 4")
icon = pygame.image.load('GameIcon.png')
p1 = pygame.image.load('piece1.png')
p2 = pygame.image.load('piece2.png')
pygame.display.set_icon(icon)

## The board
class Board:
    def __init__(self):
        self.rows = NUM_ROWS
        self.cols = NUM_COLS
        self.k = k
        self.board = np.zeros((NUM_ROWS, NUM_COLS))

    def draw_board(self):
        pygame.draw.rect(screen, (0, 0, 225), (0, 100, NUM_COLS * 100, NUM_ROWS * 100))
        for i in range(NUM_ROWS):
            for j in range(NUM_COLS):
                if self.board[i, j] == 0:
                    colour = (0,0,0)
                elif self.board[i,j] == 1:
                    colour = (255,0,0) # This is red
                else:
                    colour = (255,255,0) # This is yellow
                pygame.draw.circle(screen, colour, (100 * j + 50, 100 * i + 150 ), 45)

    def not_full(self, col):
        return self.board[0, col] == 0

    def place_piece(self, col, player):
        for row in range(self.rows - 1, -1, -1):
            if self.board[row, col] == 0:
                self.board[row, col] = player
                return [row, col]

    def in_board(self, row, col):
        valid_row = (row > -1 and row < self.rows)
        valid_col = (col > -1 and col < self.cols)
        return valid_col and valid_row

    def game_over(self, player, piece_loc):
        piece_row = piece_loc[0]
        piece_col = piece_loc[1]

        ## Check vertical
        if piece_row < self.cols - k:
            connected = True
            for row in range(piece_row, piece_row + k):
                if self.in_board(row, piece_col) and self.board[row, piece_col] != player:
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
    def click(self, x, player):
        move = math.floor(x / 100)
        if board.not_full(move):
            piece_loc = board.place_piece(move, player)




GAME_OVER = False
running = True
board = Board()

while running:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if player == 1:
                x = pygame.mouse.get_pos()[0]
                move = math.floor(x / 100)
                if board.not_full(move):
                    piece_loc = board.place_piece(move, player)
                    GAME_OVER = board.game_over(player, piece_loc)
                    player = 2
            else:
                x = pygame.mouse.get_pos()[0]
                move = math.floor(x / 100)
                if board.not_full(move):
                    piece_loc = board.place_piece(move, player)
                    GAME_OVER = board.game_over(player, piece_loc)
                    player = 1
        if GAME_OVER:
            pygame.time.wait(500)
    # if GAME_OVER:
    #     text = myfont.render("GAME OVER", False, (255, 0, 0))
    #     screen.blit(text, (0, 0))
    #     running = False
    #     pygame.time.wait(500)


    board.draw_board()

    pygame.display.update()