import numpy as np
import pygame

class GameGUI:
    def __init__(self, board_sz):
        self.board_sz = board_sz
        # color, white for player 1, black for player -1
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)

        # screen
        self.width = 800
        self.height = 800
        self.grid_width = self.width / (board_sz + 3)

        # init
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Gomoku")

        # timer
        self.clock = pygame.time.Clock()

        # background image
        self.background_img = pygame.image.load('background.png').convert()

        # font
        self.font_size = 16
        self.font = pygame.font.SysFont('Arial', self.font_size)
        self.font2 = pygame.font.SysFont('Arial', 50)
        

    def wait_to_exit(self):
        while True:
            self.clock.tick(1)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

    def _draw_background(self):
        # load background
        self.screen.blit(self.background_img, (0, 0))

        # draw lines
        rect_lines = [
            ((self.grid_width, self.grid_width),
             (self.grid_width, self.height - self.grid_width)),
            ((self.grid_width, self.grid_width), (self.width - self.grid_width,
                                                  self.grid_width)),
            ((self.grid_width, self.height - self.grid_width),
             (self.width - self.grid_width, self.height - self.grid_width)),
            ((self.width - self.grid_width, self.grid_width),
             (self.width - self.grid_width, self.height - self.grid_width)),
        ]
        for line in rect_lines:
            pygame.draw.line(self.screen, self.black, line[0], line[1], 2)

        # draw grid
        for i in range(self.board_sz):
            pygame.draw.line(
                    self.screen, self.black,
                    (self.grid_width * (2 + i), self.grid_width),
                    (self.grid_width * (2 + i), self.height - self.grid_width))
            pygame.draw.line(
                    self.screen, self.black,
                    (self.grid_width, self.grid_width * (2 + i)),
                    (self.height - self.grid_width, self.grid_width * (2 + i)))

    def _draw_chessman(self, board, hist):
        # draw chessmen
        for i in range(self.board_sz):
            for j in range(self.board_sz):
                if board[i][j] != 0:
                    # circle
                    position = (int(self.grid_width * (j + 2)),
                                int(self.grid_width * (i + 2)))
                    color = self.white if board[i][j] == 1 else self.black
                    pygame.draw.circle(self.screen, color, position,
                                       int(self.grid_width / 2.3))
                    # text
                    p_h_offset = self.font_size // 2 if hist[i][j] > 9 else self.font_size // 4
                    position = (position[0] - p_h_offset, position[1] - self.font_size // 2)
                    color = self.white if board[i][j] == -1 else self.black
                    text = self.font.render(str(hist[i][j]), 3, color)
                    self.screen.blit(text, position)
        pygame.display.flip()

    def draw_result(self, result):
        position = (300, 100)
        if result == 1:
            s = 'Player 1 Win !'
        elif result == -1:
            s = 'Player 2 Win !'
        else:
            s = 'Tie !'
        text = self.font2.render(s, True, (255, 0, 0))
        self.screen.blit(text, position)
        pygame.display.flip()



class GUIPlayer:
    def __init__(self, id, gui=None):
        self.id = id
        self.gui = gui

    def get_move(self, board):
        while True:
            self.gui.clock.tick(1)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return (-1, -1)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_y, mouse_x = event.pos
                    position = (int(mouse_x / self.gui.grid_width + 0.5) - 2,
                                int(mouse_y / self.gui.grid_width + 0.5) - 2)

                    if position[0] in range(0, self.gui.board_sz) and position[1] in range(0, self.gui.board_sz) \
                                and np.sum(board[:, position[0], position[1]]) == 0:
                        return position
