###############################################################################
# Course:               Heuristics
# Project:              Rush Hour
# Group:                1Formule
# Autors:               Tjip Bischoff,     Kevin Dekker,     Siebren Kazemier
# Student numbers:      11013028           11076143          12516597
# Mentor:               ing E.H. Steffens
#
# This program creates car objects for the Rush Hour game.
###############################################################################


class Car():
    """
    This class is a representation of the cars in Rush Hour.
    """

    def __init__(self, name, row, col, direction, size, red_car):
        # capital letters
        self.name = name

        # x / y starting position
        self.row = row
        self.col = col

        # horizontal(0) or vertical(1)
        self.direction = direction

        # cars are always 2 or 3 tiles big
        self.size = size

        # is this car the red car?
        self.red_car = red_car

        # format = horizontal: [left steps, right steps]
        # // vertical: [up steps, down steps]
        self.moveability_list = [0, 0]

    def move3(self, move):
        """
        changes only the position of the car object, not the board itself
        """
        if self.direction == 0:
            self.col += move
        if self.direction == 1:
            self.row += move

    def moveability(self, board):
        """
        Checks if car is moveable.
        Returns string of: (left_right, up_down, right, left, down, up or none)
        based on movability.
        """
        self.moveability_list = [0, 0]

        # horizontal
        if self.direction == 0:
            # the position to which the car wants to move is either 1 more
            # or 1 less column wise
            right = self.col + self.size
            left = self.col - 1

            # check if right or left is out of the boards margins
            if right > board.width_height:
                move_left = board.positions[self.row][left]
                move_right = None
            elif left < 0:
                move_right = board.positions[self.row][right]
                move_left = None
            else:
                move_right = board.positions[self.row][right]
                move_left = board.positions[self.row][left]

            # try to move right
            while move_right == "x":
                self.moveability_list[1] += 1
                right += 1
                if right > board.width_height:
                    break
                move_right = board.positions[self.row][right]

            # try to move left
            while move_left == "x":
                self.moveability_list[0] += 1
                left -= 1
                if left < 0:
                    break
                move_left = board.positions[self.row][left]

            return self.moveability_list

        # vertical
        else:
            up = self.row - 1
            down = self.row + self.size

            # check if up or down is out of the boards margins
            if up < 0:
                # no room on the board for upward movement
                move_down = board.positions[down][self.col]
                move_up = None
            elif down > board.width_height:
                # no room on the board for downward movement
                move_up = board.positions[up][self.col]
                move_down = None
            else:
                # both up and down are possible positions on the board
                move_up = board.positions[up][self.col]
                move_down = board.positions[down][self.col]

            # calculate downward movability
            while move_down == "x":
                self.moveability_list[1] += 1
                down += 1
                # ensure out of bounds array positions won't be reached
                if down > board.width_height:
                    break
                move_down = board.positions[down][self.col]

            # calculate upward movability
            while move_up == "x":
                self.moveability_list[0] += 1
                up -= 1
                if up < 0:
                    break
                move_up = board.positions[up][self.col]
            return self.moveability_list
