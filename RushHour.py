from board import Board
from car import Car
from bruteforce import Bruteforce
from breadthF import BreadthF
from depthF import DepthF
from depthrandom import depth_random
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
        self.board = self.load_board(f"data/{game}.txt")
        self.cars = self.load_cars()
        self.allmoves = []
        self.initialboard = copy.deepcopy(self.board)
        self.initialcars = copy.deepcopy(self.cars)
        self.game = game
    
    def load_board(self, filename):
        """
        initialize a Board object from the filename
        """
        # loadboard = [[],[]]
        loadboard = []
        redCarPosition = []
        exitPosition = 0
        empty = []
        allowed = ['!', '@', '#', '$', '%', '^', '&', '*', '/', '.', 'x', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        with open(filename, "r") as f:
            # still have lines to load in
            for i, line in enumerate(f):
                row = []
                if not line == "\n":
                    line.strip('\n')
                    for j, char in enumerate(line):
                        
                        # still have chars to add to array
                        
                        # add car positions 
                        if char.isupper() or char in allowed:
                            row.append(char)

                        # red car position (example: [2.4, 2.5]) ~~ can be deleted
                        elif char == "r":
                            redCarPosition.append(str(i) + "." + str(j))
                            row.append(char)

                        # finish y position
                        elif char == "e":
                            exitPosition = j - 1
                        
                        
                        if char == "x":
                            empty.append([j, i])
                        
                loadboard.append(row)
            # initialize board
            board = Board(i, loadboard, exitPosition, empty)
            # print(loadboard)
            return board
    
    def load_cars(self):
        """
        Searches all cars on the grid, creates car objects, append to list
        """
        positions = self.board.positions
        # letters of cars which are already taken
        taken_cars = []
        # list of car objects
        cars = []
        # list of allowed car chars
        allowed = ['!', '@', '#', '$', '%', '^', '&', '*', '/', '.', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        
        # 
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
                                # add 'x' at end of list just to be sure index error wont occur 
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

    listy = []
    # select the board 
    # rushhour = RushHour("easy2")



    # bf = BreadthF(rushhour)
    # bf.BreadthFirst()

    rushhour2 = RushHour("easy2")
    df = DepthF(rushhour2, 16)
    df.depth_first()


    # for i in range(70):
    #     rushhour2 = RushHour("easy2")
    #     rate = i + 1
    #     df = DepthF(rushhour2, rate)
    #     if df.depth_first() == True:
    #         print("sol found")

    # rushhour3 = RushHour("medium3")
    # dr = depth_random(rushhour3)
    # dr.DepthRandom()

    # execute the breadthfirst method
    
    # execute the bruteforce method
    # rushhour.playtest("bruteforce")
   
     