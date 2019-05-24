###############################################################################
# Course:               Heuristics
# Project:              Rush Hour
# Group:                1Formule
# Autors:               Tjip Bischoff,     Kevin Dekker,     Siebren Kazemier
# Student numbers:      11013028           11076143          12516597
# Mentor:               ing E.H. Steffens
#
# This program runs the game of Rush Hour.
###############################################################################

from board import Board
from car import Car
from random import randint
import helpers
import time
import sys
import copy
import load
from algorithms import Algorithm


class RushHour():
    """
    This is the Rush Hour game.
    Give the board on which you want to execute an
    algorithm as paramater.
    """

    def __init__(self, game):
        self.board = load.load_board(f"data/{game}.txt")
        self.cars = load.load_cars(self.board)
        self.initial_board = copy.deepcopy(self.board)
        self.initial_cars = copy.deepcopy(self.cars)

    def play(self):
        """
        Let different algorithms 'play' the rushhour game via command-line
        input. (see the readme.md in our repository for an explenation of the
        different inputs: https://github.com/tjip-b/RushHour2)
        """
        board_list = ["easy", "easy2", "easy3", "medium",
                      "medium2", "medium3", "hard"]
        # Execute the breadthfirst method
        if ((len(sys.argv) == 4 or len(sys.argv) == 5) and
                sys.argv[2] == "breadth" and sys.argv[1] in board_list):
            rush_hour = RushHour(sys.argv[1])
            bf = Algorithm(rush_hour)
            if len(sys.argv) == 4:
                # Makes all possible moves children to be appended to the queue
                if sys.argv[3] == "all":
                    bf.breadth_first(False, 0)
                # Only makes the maximum possible moves children
                # to be appended to the queue
                else:
                    bf.breadth_first(True, 0)
            # Alternate version of breadth first takes a 'breadth'
            # parameter of > 0
            if len(sys.argv) == 5:
                if sys.argv[3] == "all":
                    bf.breadth_first(False, int(sys.argv[4]))
                else:
                    bf.breadth_first(True, int(sys.argv[4]))

        # Execute the depthfirst method
        elif ((len(sys.argv)) == 6 and sys.argv[2] == "depth" and
              sys.argv[1] in board_list and sys.argv[4].isnumeric()):
            rush_hour = RushHour(sys.argv[1])
            df = Algorithm(rush_hour)
            # Add all moves or only add the furthest moves to stack
            if sys.argv[3] == "all":
                # Pruning method maximum or only prune off
                # identical children with higher depth
                if sys.argv[5] == "min":
                    df.depth_first(int(sys.argv[4]), True, False)
                elif sys.argv[5] == "max":
                    df.depth_first(int(sys.argv[4]), False, False)
                else:
                    print("usage: please state 'min' or 'max' as 5th argument")
            elif sys.argv[3] == "furthest":
                if sys.argv[5] == "min":
                    df.depth_first(int(sys.argv[4]), True, True)
                elif sys.argv[5] == "max":
                    df.depth_first(int(sys.argv[4]), False, True)
                else:
                    print("usage: please explicitly state 'min' or \
                        'max' as 5th argument")
            else:
                print("usage: please explicitly state 'all' or \
                        'furthest' as 3th argument")

        # Execute depthrandom method
        elif ((len(sys.argv)) == 4 and sys.argv[2] == "depth_random" and
                sys.argv[1] in board_list and sys.argv[3].isnumeric()):
            
            rush_hour = RushHour(sys.argv[1])
            df = Algorithm(rush_hour)
            df.depth_random(int(sys.argv[3]))

        elif ((len(sys.argv)) == 5 and sys.argv[2] == "depth_random_optimalised"
                and sys.argv[1] in board_list and sys.argv[3].isnumeric()):
            rush_hour = RushHour(sys.argv[1])
            df = Algorithm(rush_hour)
            df.find_optimised_solution(int(sys.argv[3]), int(sys.argv[4]))

        
        elif ((len(sys.argv)) == 5 and sys.argv[1] == "build_board"):
            board = helpers.create_random_board(int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))
            print (board)
        
        else:
            print("usage: python RushHour.py <board> <method> <movement method>\
                    <depth/breadth (for depth_first)> \
                    <pruning method (for depth_first)> ")
           

if __name__ == "__main__":
    rush_hour = RushHour("easy")
    rush_hour.play()
 