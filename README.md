# 7343 Homework 2

Your task in this homework is to implement the Monte Carlo Tree Search used in *AlphaZero* for the board game Gomoku (five in a line). For simplicity, we consider only the Gomoku game with a 11x11 board. 
1. You should implement a class named "MCTS" which must be a subclass of the class MCTSBase. The MCTSBase class already has the overall search process. In your MCTS class, you need to fill in the missing components by implementing (override) the abstract methods. (Do not change/override the non-abstract methods.) 
2. Your code also needs to implement another class (use any class name you want) that is a subclass of the TreeNode class and completes the implementation of the abstract methods in that class. 
3. The tree search process needs to utilize a deep neural network. Given a state s, the DNN  estimates the state value of s as well as computes the policy at s (the probability of actions). You should implement such a neural network and use it in the code for some of the abstract methods.     

Also pay attention:
 - Do not copy code from MCTSBase.py into your hw2.py file. Simply import the symbols from MCTSBase.
 - Do not change/override non-abstract methods in the provided .py files. 
 - Read the documentation on the abstract method carefully. When you override a method, you must use the same function signature. When coding, you should have a good understanding on what parameter will be passed to that method and what we expect that method to return. If these are not followed, the tree search process cannot run.

## Submit your work
Put all your code in a single file named "hw2.py" (*you must use this file name*) and submit the file in moodle. 
(Different from hw1, you don't need to have code for downloading the weights of your trained model.)

We'll test your code as shown at the end of the gomoku.py file. The MCTS class will be imported from hw2.py. A MCTS object will be created and used in the NeuralMCTSPlayer to choose a move at each step. Make sure that your code works with gomoku.py.  
 
 
