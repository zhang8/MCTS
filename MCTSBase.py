#######
# Copyright 2020 Jian Zhang, All rights reserved
##
from abc import ABC, abstractmethod
import numpy as np

cpuct = 1
EPS = 1e-8


class TreeNode(ABC):
    '''
    Base class for MCT node. The node has to support the following four methods.
    '''
    @abstractmethod
    def is_terminal(self):
        '''
        :return: True if this node is a terminal node, False otherwise.
        '''
        pass

    @abstractmethod
    def value(self):
        '''
        :return: the value of the node form the current player's point of view
        '''
        pass

    @abstractmethod
    def find_action(self):
        '''
        Find the action with the highest upper confidence bound to take from the state represented by this MC tree node.
        :return: action as a tuple (x, y), i.e., putting down a piece at location x, y
        '''
        pass

    @abstractmethod
    def update(self, v):
        '''
        Update the statistics/counts and values for this node
        :param v: value backup following the action that was selected in the last call of "find_action"
        :return: None
        '''
        pass


class MCTSBase:
    """
    Monte Carlo Tree Search
    Note the game board will be represented by a numpy array of size [2, board_size[0], board_size[1]]
    """
    @abstractmethod
    def __init__(self, game):
        '''
        Your subclass's constructor must call super().__init__(game)
        :param game: the Gomoku game
        '''
        self.game = game

    @abstractmethod
    def reset(self):
        '''
        Clean up the internal states and make the class ready for a new tree search
        :return: None
        '''
        pass

    @abstractmethod
    def get_visit_count(self, state):
        '''
        Obtain number of visits for each valid (state, a) pairs from this state during the search
        :param state: the state represented by this node
        :return: a board_size[0] X board_size[1] matrix of visit counts. It should have zero at locations corresponding to invalid moves at this state.
        '''
        pass

    @abstractmethod
    def get_treenode(self, standardState):
        '''
        Find and return the node corresponding to the standardState in the search tree
        :param standardState: board state
        :return: tree node (None if the state is new, i.e., we need to expand the tree by adding a node corresponding to the state)
        '''
        pass

    @abstractmethod
    def new_tree_node(self, standardState, game_end):
        '''
        Create a new tree node for the search
        :param standardState: board state
        :param game_end: whether game ends after last move, takes 3 values: None-> game not end; 0 -> game ends with a tie; 1-> player who made the last move win
        :return: a new tree node
        '''
        pass

    def execute_move(self, state, a):
        '''
        Commit a move
        :param state: board state before the action
        :param a: move, a tuple (x, y)
        :return: the new state from the next player's view and the gameend indicator which takes 3 values: None-> game not end; 0 -> game ends with a tie; 1-> player who made the move win
        '''
        state[0, a[0], a[1]] = 1
        gameend = self.game.getGameEnded(state, 1, a)
        return state[[1, 0]], gameend

    def getActionProb(self, state, n_search):
        """
        This function performs n_search MCTS starting from the state.
        state: the root state of the MCTSs
        n_search: number of NCTS to be performed
        Returns:
            probs: a policy matrix the size of the board. The (i, j) entry of the matrix gives the probability of putting a piece at that locationan.
        """
        for i in range(n_search):
            self.search(state.copy())

        counts = self.get_visit_count(state)
        return counts / np.sum(counts)

    def search(self, standardState, game_end=None):
        """
        This function performs one iteration of MCTS. It is recursively called
        till a leaf node is found. The action chosen at each node is one that
        has the maximum upper confidence bound as in the paper.
        Once a leaf node is found, the neural network is called to return an
        initial policy P and a value v for the state. This value is propagated
        up the search path. In case the leaf node is a terminal state, the
        outcome is propagated up the search path. The values along the path are
        updated.
        NOTE: the return values are the negative of the value of the current
        state. This is done because if v is the value of a
        state for the current player, then its value is -v for the other player.
        Returns:
            v: the negative of the value of the current standardState
        """
        print('reach state:', standardState)
        n = self.get_treenode(standardState)
        if n is None:
            n = self.new_tree_node(standardState, game_end)  # Expansion
            print('create new tree node: (terminal, value)=', n.is_terminal(), n.value())
            return -n.value()

        if n.is_terminal():
            print('terminal state, value=', n.value())
            return -n.value()

        a = n.find_action()  # Selection
        print('search through action:', a)
        next_state, end = self.execute_move(standardState, a)

        v = self.search(next_state, end)

        n.update(v)  # Backup
        return -v

