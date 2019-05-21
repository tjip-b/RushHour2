###############################################################################
# Course:               Heuristics
# Project:              Rush Hour
# Group:                1Formule
# Autors:               Tjip Bischoff,     Kevin Dekker,     Siebren Kazemier
# Student numbers:      11013028           11076143          12516597
# Mentor:               ing E.H. Steffens
#
# This program runs an implementation of a random mover on the
# Rush Hour game.
###############################################################################

from random import randint


class Bruteforce():
    """
    This class trys to bruteforce the Rush Hour game
    """

    def __init__(self, filename):
        self.filename = filename

    def random_mover(self, amount):
        """
        This function moves all cars random on the Rush Hour board.
        """
        # find the red_car in all the cars
        for i in range(0, amount):
            for i, car in enumerate(self.cars):
                if car.red_car:
                    red_car = self.cars[i]
                    break
            moves = 0
            moveables = ["left", "right", "up", "down"]

            while red_car.col + 1 != self.board.exit_position:
                randy = randint(0, len(self.cars) - 1)
                random_car = self.cars[randy]
                car_move = random_car.moveable(self.board)
                if red_car.moveability_list[1] > 2:
                    red_car.move(self.board, "right")
                    red_car.move(self.board, "right")
                    red_car.move(self.board, "right")
                if red_car.moveable(self.board) == "left_right":
                    rand = randint(0, 100)
                    if rand > 20:
                        red_car.move(self.board, "right")
                    else:
                        red_car.move(self.board, "left")
                    moves += 1
                    continue
                if car_move in moveables:
                    random_car.move(self.board, car_move)
                elif car_move == "left_right":
                    rand = randint(0, 1)
                    if rand == 0:
                        random_car.move(self.board, "left")
                    else:
                        random_car.move(self.board, "right")
                elif car_move == "updown":
                    rand = randint(0, 1)
                    if rand == 0:
                        random_car.move(self.board, "up")
                    else:
                        random_car.move(self.board, "down")
                else:
                    continue
                moves += 1
                print(self.board)
            print(moves)
            print(self.board)

            self.Reset()
            self.all_moves.append(moves)

        return self.all_moves
