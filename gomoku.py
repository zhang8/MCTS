# -*- coding: utf-8 -*-
##
# Copyright 2020 Jian Zhang, All rights reserved
##
import logging as log
import numpy as np

def check_winner(L):
    N = len(L)
    if N < 5:
        return False
    else:
        s = np.sum(L[:5])
        if s == 5:
            return True
        if N > 5:
            for i in range(N-5):
                s = s - L[i] + L[i+5]
                if s == 5:
                    return True
        return False

##
# Game
# board: 3d numpy array of size [n_player, board_height, board_width].
# The game class keep a board where board[0] is the first player and
# board[1] is the second player (in the order they make moves).
# standardBoard for a player x is the board where board[0] is for x
# and board[1] is for the opponent.
# Players: 1 or -1. The first player is numbered as 1.
class Gomoku:
    def __init__(self, board_sz=11, gui=False):
        super().__init__()
        self.board_sz = board_sz
        self.board = np.zeros((2, board_sz, board_sz), dtype=np.int)
        self.number = np.zeros((board_sz, board_sz), dtype=int)
        self.k = 1  # step number
        self.result = 0
        if gui:
            self.gui = GameGUI(board_sz)
        else:
            self.gui = None

    def convertPlayer(self, p):
        '''
        convert player id 1, -1 to 0, 1
        :param p: player id i or -1
        :return: player id 0 or 1
        '''
        return int((1-p)/2)

    def stringRepresentation(self, board):
        '''
        give a string representation of a numpy array
        :param board: numpy array
        :return:
        '''
        return np.array2string(board.reshape(-1))

    def getGameEnded(self, pbs, lp, lm): # board, last_player, last_move
        '''
        Check if game ends after the last move
        :param pbs: game board
        :param lp: last player
        :param lm: last move as a tuple (x, y)
        :return: If game ends, return the winning (i.e., the last) player id. If a tie, return zero. If game continues, return None.
        '''
        if np.sum(pbs) == self.board_sz*self.board_sz:  # tie
            return 0

        p = self.convertPlayer(lp)
        sz = self.board_sz
        x, y = lm

        xd, xu = min(x, 4), min(sz-1-x, 4)
        yl, yr = min(y, 4), min(sz-1-y, 4)
        fs0, fs1 = min(xd, yl), min(xu, yr)
        bs0, bs1 = min(xu, yl), min(xd, yr)

        if check_winner(pbs[p, (x-xd):(x+xu+1), y]) or check_winner(pbs[p, x, (y-yl):(y+yr+1)]):
            return lp
        elif check_winner(pbs[p, np.arange((x-fs0), (x+fs1+1)), np.arange((y-fs0), (y+fs1+1))]):
            return lp
        elif check_winner(pbs[p, np.arange((x+bs0), (x-bs1-1), -1), np.arange((y-bs0), (y+bs1+1))]):
            return lp
        else:
            return None

    def reset(self):
        self.board.fill(0)
        self.number.fill(0)
        self.k = 1
        self.result = 0

    def draw(self):
        if self.gui:
            self.gui._draw_background()
            self.gui._draw_chessman(self.board[0, :, :]-self.board[1, :, :], self.number)

    # execute a move
    def execute_move(self, p, x, y):
        assert np.sum(self.board[:, x, y]) == 0

        self.board[self.convertPlayer(p), x, y] = 1
        win = self.getGameEnded(self.board, p, (x, y))
        self.number[x][y] = self.k
        self.k += 1
        return win

    # main loop
    def play(self, p1, p2):
        players = {1:p1, -1:p2}
        self.reset()
        pi = 1
        self.draw()
        while True:
            if pi == 1:
                standardBoard = self.board
            else:
                standardBoard = self.board[[1, 0]]
            x, y = players[pi].get_move(standardBoard)
            if x < 0:
                break
            log.debug('player: %d,  move: (%d, %d)' % (pi, x, y))
            win = self.execute_move(pi, x, y)
            self.draw()
            
            if win is not None:
                self.result = win
                break
            pi = -pi


class RandomPlayer():
    def get_move(self, board):
        b = (board[0, :, :] + board[1, :, :]) - 1
        ix, jx = np.nonzero(b)
        idx = [i for i in zip(ix, jx)]
        return idx[np.random.choice(len(idx))]


from hw2 import MCTS
class NeuralMCTSPlayer():
    def __init__(self, game, n_mcts_per_step):
        self.mcts = MCTS(game)
        self.n_mcts_per_step = n_mcts_per_step

    def get_move(self, standardBoard):
        self.mcts.reset()
        pi = self.mcts.getActionProb(standardBoard, self.n_mcts_per_step)
        move = np.unravel_index(np.argmax(pi), pi.shape)
        assert(np.sum(standardBoard[:, move[0], move[1]]) == 0)
        return move


if __name__ == "__main__":
    from gamegui import GameGUI, GUIPlayer

    g = Gomoku(11, True)
    p1 = GUIPlayer(1, g.gui)
    p2 = NeuralMCTSPlayer(g, 100)

    print('start GUI game, close window to exit.')
    g.play(p1, p2)

    g.gui.draw_result(g.result)
    g.gui.wait_to_exit()

