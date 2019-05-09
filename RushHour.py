from board import Board
from car import Car
from load import Load
from bruteforce import Bruteforce
from breadthF import BreadthF
from depthF import DepthF
from random import randint
import time
import sys
import copy

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
        self.initialboard = copy.deepcopy(self.board)
        self.initialcars = copy.deepcopy(self.cars)
        self.game = game
           
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

if __name__ == "__main__":

    # select the board 
    rushhour = RushHour("supereasy")
    
    # bf = BreadthF(rushhour)
    # bf.BreadthFirst()

    rushhour2 = RushHour("supereasy")

    df = DepthF(rushhour2)
    df.depth_first()

    # execute the breadthfirst method
    
    # execute the bruteforce method
    # rushhour.playtest("bruteforce")
   
     