from board import Board
from car import Car
from load import Load
from bruteforce import Bruteforce
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
        self.board = Load.load_board(self, f"data/{game}.txt")
        self.cars = Load.load_cars(self)
        self.allmoves = []
        self.initialboard = self.board
        self.initialcars = self.cars
        self.game = game
                
    def find(self):
        # while redcar_position niet op self.board.exit_position:
        print("hio")
        
    def check(self):
        """
        checks if car(s) are in certain row or colomn
        """
        print("test")
           
    def playtest(self, method):
        # print out some information about the board and cars
        print(self.board.positions)
        for line in self.board.positions:
            print(line)
        for i, car in enumerate(self.cars):
            print("No.%s: CAR: %s" % (i, car))
            print(car.direction)
            print(f"X pos: {car.row} y pos: {car.col}")
            print('\n')
        print(self.board.width_height)        
        print(self.board)
        
        # brute force the game! 
        if method == "bruteforce":
                        
            n = 1
            Bruteforce.randommover(self,  1)
            average = self.Average(self.allmoves) 
            print(f"avarage of {self.game} board for {n} runs = {average}")
        
    def Average(self, lst): 
        return sum(lst) / len(lst) 
    
    def Reset(self):
        self.board = Load.load_board(self, f"data/{self.game}.txt")
        self.cars = Load.load_cars(self)

if __name__ == "__main__":
    rushhour = RushHour("easy")
    rushhour.playtest("bruteforce")

    print(f"width_height: {rushhour.board.width_height}")

    for car in rushhour.cars:
        print(car.name)
        print(car.moveability_list)
    print(rushhour.board)
    print(rushhour.initialboard)


