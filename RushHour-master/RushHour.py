from board import Board
from car import Car
from random import randint
import time
from colorama import init
init()
import sys

class RushHour():
    """
    This is the Rush Hour game.
    """

    def __init__(self, game):
        """
        Create the board within the game and create car objects
        """
        # print(game)
        self.board = self.load_board(f"data\{game}.txt")
        self.cars = self.load_cars()

    def load_board(self, filename):
        """
        initialize a Board object from the filename
        """
        return Board.load_board(self, filename)
        

    def load_cars(self):
        """
        Searches all cars on the grid, creates car objects, append to list
        """
        return Board.load_cars(self)

    def find(self):
        # while redcar_position niet op self.board.exit_position:
        print("hio")

    def check(self):
        """
        checks if car(s) are in certain row or colomn
        """
        print("test")

    
    def playtest(self):
        print(self.board.positions)
        for line in self.board.positions:
            print(line)
        for i, car in enumerate(self.cars):
            print("No.%s: CAR: %s" % (i, car))
            print(car.direction)
            print(car.position)
            print('\n')
        print(self.board.width_height)
        print(self.board)
        # rushhour.move(self.cars[32], 0)
        # rushhour.move(self.cars[36], 1)
        #car = self.cars[6]
        #move = car.moveable(self.board)
        #car.move(self.board, move)
        for car in self.cars:
            if car.name == "redCar":
                rredcar = car
                break
        print(rredcar.position[1])


        # brute force the game!

        moves = 0
        moveables = ["left", "right", "up", "down"]
        AAcar = self.cars[6]
        movedir = AAcar.moveable(self.board)
        #print(AAcar.position)
        #AAcar.move(self.board, movedir)
        #print(movedir)
        #print(AAcar.position)
        ##AAcar.move(self.board, movedir)
        #print(AAcar.position)
        #print(rredcar.position[1])
        #print(self.board.exit_position)
        while rredcar.position[1] != self.board.exit_position:
            rredcarpos = self.cars[3].position
            randy = randint(0, len(self.cars) - 1)
            randomcar = self.cars[randy]
            #print(randomcar)
            carmove = randomcar.moveable(self.board)
            #print(carmove)
            if carmove in moveables:
                randomcar.move(self.board, carmove)
            elif carmove == "leftright":
                rand = randint(0, 1)
                if rand == 0:
                    randomcar.move(self.board, "left")
                else:
                    randomcar.move(self.board, "right")
            elif carmove == "updown":
                rand = randint(0, 1)
                if rand == 0:
                    randomcar.move(self.board, "up")
                else:
                    randomcar.move(self.board, "down")
            else:
                continue
            moves += 1
            if moves % 100000 == 0:
                print(self.board)
                print(moves)
            if rredcar.position != rredcarpos:
                print(self.board)
                print(moves)
        print(moves)
        print(self.board)


if __name__ == "__main__":
    rushhour = RushHour("easy")
    rushhour.playtest()
