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
import bruteforce
from random import randint
import time
import sys
import copy
from algorithms import Algorithm


class RushHour():
    """
    This is the Rush Hour game.
    """

    def __init__(self, game):
        self.board = self.load_board(f"data/{game}.txt")
        self.cars = self.load_cars()
        self.initial_board = copy.deepcopy(self.board)
        self.initial_cars = copy.deepcopy(self.cars)

    def load_board(self, filename):
        """
        Initialize a Board object from the filename.
        """
        load_board = []
        red_car_position = []
        exit_position = 0
        empty = []
        allowed = ['!', '@', '#', '$', '%', '^', '&', '*', '/',
                   '.', 'x', '1', '2', '3', '4', '5', '6', '7', '8', '9']

        with open(filename, "r") as f:
            # load in lines
            for i, line in enumerate(f):
                row = []

                if not line == "\n":
                    line.strip('\n')
                    for j, char in enumerate(line):

                        # add chars to car position
                        if char.isupper() or char in allowed:
                            row.append(char)

                        # red car position (example: [2.4, 2.5]) ~~ can be deleted
                        elif char == "r":
                            red_car_position.append(str(i) + "." + str(j))
                            row.append(char)

                        # finish y position
                        elif char == "e":
                            exit_position = j - 1

                        if char == "x":
                            empty.append([j, i])

                load_board.append(row)

            # initialize board
            board = Board(i, load_board, exit_position)
            return board

    def load_cars(self):
        """
        Searches all cars on the grid, creates car objects, append to list.
        """
        positions = self.board.positions

        # letters of cars which are already taken
        taken_cars = []

        # list of car objects
        cars = []

        # list of allowed car chars
        allowed = ['!', '@', '#', '$', '%', '^', '&', '*', '/',
                   '.', '1', '2', '3', '4', '5', '6', '7', '8', '9']

        for i, row in enumerate(positions):
            for j, char in enumerate(row):

                # check for red car (which is always horizontal and of size 2)
                if (char.isupper() or char in allowed) and char not in taken_cars:

                    # trying to find a horizontal car
                    try:
                        if positions[i][j + 1] == char:
                            taken_cars.append(char)

                            # check for third 'block'
                            try:
                                if positions[i][j + 2] == char:
                                    # x = i -- y = j
                                    car = Car(char * 3, i, j, 0, 3, False)
                                    car.moveability(self.board)
                                    cars.append(car)
                                    continue

                                # add 'x' at end of list just to be sure
                                # index error wont occur
                                car = Car(char * 2, i, j, 0, 2, False)
                                car.moveability(self.board)
                                cars.append(car)

                            # car found, but not a 3 tile car
                            except IndexError:
                                car = Car(char * 2, i, j, 0, 2, False)
                                car.moveability(self.board)
                                cars.append(car)
                                continue

                    # no car found
                    except IndexError:
                        pass

                    # trying to find a vertical car
                    try:
                        if positions[i + 1][j] == char:
                            taken_cars.append(char)
                            try:
                                if positions[i + 2][j] == char:
                                    car = Car(char * 3, i, j, 1, 3, False)
                                    car.moveability(self.board)
                                    cars.append(car)
                                    continue
                                car = Car(char * 2, i, j, 1, 2, False)
                                car.moveability(self.board)
                                cars.append(car)
                            except IndexError:
                                car = Car(char * 2, i, j, 1, 2, False)
                                car.moveability(self.board)
                                cars.append(car)
                                continue
                    except IndexError:
                        continue

                elif char == "r" and char not in taken_cars:
                    redcar = Car("redCar", i, j, 0, 2, True)
                    redcar.moveability(self.board)
                    taken_cars.append(char)
                    cars.append(redcar)

        self.board.cars = cars
        return cars

    def play(self):
        board_list = ["easy", "easy2", "easy3", "medium", "medium2", "medium3", "hard"]
        # execute the breadthfirst method
        if ((len(sys.argv) == 4 or len(sys.argv) == 5) and sys.argv[2] == "breadth" and sys.argv[1] in board_list):
            print("dit is fout") 
            rush_hour = RushHour(sys.argv[1])
            bf = Algorithm(rush_hour)
            if len(sys.argv) == 4:
                # makes all possible moves children to be appended to the queue
                if sys.argv[3] == "all":
                    bf.breadth_first(False, 0)
                # only makes the maximum possible moves children to be appended to the queue
                else:
                    bf.breadth_first(True, 0)
            # alternate version of breadth first takes a 'breadth' parameter of > 0
            if len(sys.argv) == 5:
                if sys.argv[3] == "all":
                    bf.breadth_first(False, int(sys.argv[4]))
                else:
                    bf.breadth_first(True, int(sys.argv[4]))

        # execute the depthfirst method
        elif (len(sys.argv)) == 6 and sys.argv[2] == "depth" and sys.argv[1] in board_list and sys.argv[4].isnumeric():
            rush_hour = RushHour(sys.argv[1])
            df = Algorithm(rush_hour)
            # add all moves or only add the furthest moves to stack
            if sys.argv[3] == "all":
                # pruning method maximum or only prune off identical children with higher depth
                if sys.argv[5] == "max":
                    df.depth_first(int(sys.argv[4]), True, False)
                elif sys.argv[5] == "min":
                    df.depth_first(int(sys.argv[4]), False, False)
                else: 
                    print("usage: please state 'min' or 'max' as 5th argument")
            elif sys.argv[3] == "furthest":
                if sys.argv[5] == "max":
                    df.depth_first(int(sys.argv[4]), True, True)
                elif sys.argv[5] == "min":
                    df.depth_first(int(sys.argv[4]), False, True)
                else: 
                    print("usage: please explicitly state 'min' or 'max' as 5th argument")
            else:
                print("usage: please explicitly state 'all' or 'furthest' as 3th argument")
        
        # execute depthrandom method
        elif (len(sys.argv)) == 4 and sys.argv[2] == "depth_random" and sys.argv[1] in board_list and sys.argv[3].isnumeric():
            print("usage = <board> <method> <max depth>")
            rush_hour = RushHour(sys.argv[1])
            df = Algorithm(rush_hour)
            df.depth_random(int(sys.argv[3]))

        elif (len(sys.argv)) == 5 and sys.argv[2] == "depth_random_optimalised" and sys.argv[1] in board_list and sys.argv[3].isnumeric():
            rush_hour = RushHour(sys.argv[1])
            df = Algorithm(rush_hour)
            df.find_optimised_solution(int(sys.argv[3]), int(sys.argv[4]))

        else:
            print("usage: python RushHour.py <board> <method> <movement method> <depth/breadth (for depth_first)> <pruning method (for depth_first)> ")


if __name__ == "__main__":

    rush_hour = RushHour(sys.argv[1])
    rush_hour.play()