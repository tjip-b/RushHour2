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

import arcade
from board import Board
from car import Car
from bruteforce import Bruteforce
from breadthF import BreadthF
from depthF import DepthF
from depthrandom import DepthRandom
from random import randint
import time
import sys
import copy


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
            board = Board(i, load_board, exit_position, empty)
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
                                    car = Car(char * 3, i, j, "horizontal", 3, False)
                                    car.moveability(self.board)
                                    cars.append(car)
                                    continue

                                # add 'x' at end of list just to be sure
                                # index error wont occur
                                car = Car(char * 2, i, j, "horizontal", 2, False)
                                car.moveability(self.board)
                                cars.append(car)

                            # car found, but not a 3 tile car
                            except IndexError:
                                car = Car(char * 2, i, j, "horizontal", 2, False)
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
                                    car = Car(char * 3, i, j, "vertical", 3, False)
                                    car.moveability(self.board)
                                    cars.append(car)
                                    continue
                                car = Car(char * 2, i, j, "vertical", 2, False)
                                car.moveability(self.board)
                                cars.append(car)
                            except IndexError:
                                car = Car(char * 2, i, j, "vertical", 2, False)
                                car.moveability(self.board)
                                cars.append(car)
                                continue
                    except IndexError:
                        continue

                elif char == "r" and char not in taken_cars:
                    redcar = Car("redCar", i, j, "horizontal", 2, True)
                    redcar.moveability(self.board)
                    taken_cars.append(char)
                    cars.append(redcar)

        self.board.cars = cars
        return cars


if __name__ == "__main__":

    # select the board
    rush_hour2 = RushHour("easy")

    # execute the depthfirst method
    # bf = BreadthF(rush_hour2)
    # bf.breadth_first()

    # execute the depthfirst method
    # df = DepthF(rush_hour2, 450)
    # df.depth_first()
