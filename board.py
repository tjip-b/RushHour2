###############################################################################
# Course:               Heuristics
# Project:              Rush Hour
# Group:                1Formule
# Autors:               Tjip Bischoff,     Kevin Dekker,     Siebren Kazemier
# Student numbers:      11013028           11076143          12516597
# Mentor:               ing E.H. Steffens
#
# This program runs an implementation of the board from the Rush Hour game.
###############################################################################

from car import Car
import copy


class Board():
    """
    The board where the game takes place.
    The game is represented by a grid with different chars in it,
    which represent the cars.
    """

    def __init__(self, width_height, positions, exit_position, empty):
        # width and height are always the same (starts counting from 0!)
        self.width_height = width_height

        # represents the positions of all cars: [[],[]]
        self.positions = positions

        # if redcar.y hits the exit positions y position, the game is over.
        self.exit_position = exit_position

        # list of all the cars in the grid
        self.cars = []
        self.empty = empty

    def build(self, size, cars):
        """
        builds a board,
        based on the size of the board and the cars which are given as input
        """
        board_positions = []
        row = []

        # construct an empty board
        for i in range(0, size):
            row.append("x")
        for i in range(0, size):
            board_positions.append(copy.copy(row))

        # place the cars on the board
        for car in cars:
            # check the orientation of the car
            if car.direction == "horizontal":
                # change the x's to the car letter.
                for i in range(0, car.size):
                    board_positions[car.row][car.col + i] = car.name[0]

            # same for vertical cars
            else:
                for i in range(int(car.size)):
                    board_positions[car.row + i][car.col] = car.name[0]

        # make a new board object
        board = Board(size-1, board_positions, (size)/2-1, 0)

        # return the board object
        return(board)

    def __str__(self):
        """
        Print out board in readable strings
        """
        allowed = ['!', '@', '#', '$', '%', '^', '&', '*', '/',
                   '.', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        return_string = ""
        for row in self.positions:
            for char in row:
                if char.isupper() or char == 'r' or char in allowed:
                    return_string += "| " + char + " "
                else:
                    return_string += "| " + "_" + " "
            return_string += "\n"
        return return_string
