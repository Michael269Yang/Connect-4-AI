import pygame
import numpy as np
import math
from random import randint

pygame.init()
pygame.font.init()

myfont = pygame.font.SysFont('Comic Sans MS', 30)

## Constants
NUM_ROWS = 6
NUM_COLS = 7
k = 4
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)
GREY = (224,224, 224)

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
    def __init__(self, board):
        self.rows = NUM_ROWS
        self.cols = NUM_COLS
        self.k = k
        self.board = board
        self.halfSquareSize = 50
        self.squareSize = 100
        self.radius = math.floor(0.9 * self.halfSquareSize)

    def draw_board(self):
        pygame.draw.rect(screen, GREY, (0, 100, NUM_COLS * self.squareSize, NUM_ROWS * self.squareSize))

        for i in range(NUM_ROWS):
            for j in range(NUM_COLS):
                if self.board[i, j] == 0:
                    colour = BLACK
                elif self.board[i,j] == 1:
                    colour = RED
                else:
                    colour = YELLOW
                pygame.draw.circle(screen, colour, (self.squareSize * j + self.halfSquareSize,
                                                    self.squareSize * i + 150),
                                   self.radius)

        pygame.display.update()

    def not_full(self, col):
        return self.board[0, col] == 0

    def first_taken_spot(self, col):
        spot = 0
        while spot < self.rows and self.board[spot, col] == 0:
            spot += 1

        return spot

    def place_piece(self, col, player):
        for row in range(self.rows - 1, -1, -1):
            if self.board[row, col] == 0:
                self.board[row, col] = player
                return [row, col]

    def open_cols(self):
        return [col for col in range(NUM_COLS) if
                self.not_full(col)]

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
            return True

        return False

    def indiv_score(self, opp):
        score = 0
        AI = 2
        player = 1

        ## 2 if for AI, 1 is for human player

        if opp.count(AI) == 4:
            score = math.inf
        elif opp.count(AI) == 3 and opp.count(0) == 1:
            score += 13
        elif opp.count(AI) == 2 and opp.count(0) == 2:
            score += 6
        ## Subtract for player scores
        elif opp.count(player) == 4:
            score = - math.inf
        elif opp.count(player) == 3 and opp.count(0) == 1:
            score = - math.inf
        elif opp.count(player) == 2 and opp.count(0) == 2:
            score -= 5
        return score

    ## Score is from AI perspective
    def score(self):
        score = 0

        ## Check horizontals
        for row in range(NUM_ROWS):
            for col in range(NUM_COLS - k + 1):
                opp = list(self.board[row, col: col + k])
                score += self.indiv_score(opp)

        ## Check verticals
        for col in range(NUM_COLS):
            for row in range(NUM_ROWS - k + 1):
                opp = list(self.board[row: row + k, col])
                score += self.indiv_score(opp)

        ## Check diags
        for col in range(NUM_COLS - k + 1):
            for row in range(NUM_ROWS - k + 1):
                opp = [self.board[row + i, col + i] for i in range(k)]
                score += self.indiv_score(opp)

        for col in range(NUM_COLS - k + 1):
            for row in range(k, NUM_ROWS):
                opp = [self.board[row - i, col + i] for i in range(k)]
                score += self.indiv_score(opp)
        return score

    def switch_players(self, player):
        if player == 1:
            return 2
        return 1

    # player = 1 means player
    # player = 2 means AI
    # player = 0 means uninitizliaed
    def minimax(self, depth, player, alpha, beta, prev_move):
        was_winning_move = self.game_over(self.switch_players(player), [self.first_taken_spot(prev_move), prev_move])
        if depth == 0 or was_winning_move:
            return [0, self.score()]

        elif player == 2:
            max_score = [0, - math.inf]
            for col in self.open_cols():
                    arr = self.board.copy()
                    simul = Board(arr)
                    simul.place_piece(col, 2)
                    score = simul.minimax(depth - 1, 1, alpha, beta, col)[1]
                    if score > max_score[1]:
                        max_score = [col, score]
                    alpha = max(alpha, score)
                    if beta <= alpha:
                        break
            return max_score

        else:
            min_score = [0, math.inf]
            for col in self.open_cols():
                    arr = self.board.copy()
                    simul = Board(arr)
                    simul.place_piece(col, 1)
                    score = simul.minimax(depth - 1, 2, alpha, beta, col)[1]
                    if score < min_score[1]:
                        min_score = [col, score]
                    beta = min(beta, score)
                    if beta <= alpha:
                        break
            return min_score



GAME_OVER = False
running = True
arr = np.zeros((NUM_ROWS, NUM_COLS))
board = Board(arr)
clock = pygame.time.Clock()
pygame.display.update()

while running:
    screen.fill((0, 0, 0))
    board.draw_board()

    x = pygame.mouse.get_pos()[0]
    if player == 1:
        pygame.draw.circle(screen, (255, 0, 0), (x, 50), 50)
        pygame.display.update()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


        if event.type == pygame.MOUSEBUTTONDOWN:
            if player == 1:
                move = math.floor(x / 100)
                if board.not_full(move):
                    piece_loc = board.place_piece(move, player)
                    GAME_OVER = board.game_over(player, piece_loc)
                    if GAME_OVER:
                        print("The game is over. You've won")
                        label = myfont.render("GAME OVER", False, (199, 40, 40))
                        screen.blit(label, (40, 0))

                    pygame.display.update()
                    player = 2

    if player == 2 and not GAME_OVER:
        # move = randint(0, 6)
        move = board.minimax(2, 2, alpha=- math.inf, beta=math.inf, prev_move=0)[0]

        if board.not_full(move):
            piece_loc = board.place_piece(move, player)
            GAME_OVER = board.game_over(player, piece_loc)
            player = 1

    if GAME_OVER:
        running = False


pygame.quit()
