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
        self.board = self.load_board(f"data/{game}.txt")
        self.cars = self.load_cars()
        self.allmoves = []
        self.initialboard = self.board
        self.initialcars = self.cars
        self.game = game

    def load_board(self, filename):
        """
        initialize a Board object from the filename
        """
        # loadboard = [[],[]]
        loadboard = []
        redCarPosition = []
        exitPosition = 0
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
                loadboard.append(row)
            # initialize board
            board = Board(i, loadboard, exitPosition)
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
                                    cars.append(car)
                                    continue
                                # add 'x' at end of list just to be sure index error wont occur 
                                car = Car(char * 2, i, j, "horizontal", 2, False)
                                cars.append(car)
                            # car found, but not a 3 tile car
                            except IndexError:
                                car = Car(char * 2, i, j, "horizontal", 2, False)
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
                                    cars.append(car)
                                    continue
                                car = Car(char * 2, i, j, "vertical", 2, False)
                                cars.append(car)
                            except IndexError:
                                car = Car(char * 2, i, j, "vertical", 2, False)
                                cars.append(car)
                                continue
                    except IndexError:
                        continue
                elif char == "r" and char not in taken_cars:
                    redcar = Car("redCar", i, j, "horizontal", 2, True)
                    taken_cars.append(char)
                    cars.append(redcar)        
        self.board.cars = cars
        return cars
                
    def find(self):
        # while redcar_position niet op self.board.exit_position:
        print("hio")
        
    def check(self):
        """
        checks if car(s) are in certain row or colomn
        """
        print("test")
           
    def playtest(self):
        # print out some information about the board and cars
        print(self.board.positions)
        for line in self.board.positions:
            print(line)
        for i, car in enumerate(self.cars):
            print("No.%s: CAR: %s" % (i, car))
            print(car.direction)
            print(f"X pos: {car.x} y pos: {car.y}")
            print('\n')
        print(self.board.width_height)        
        print(self.board)
        
        # brute force the game!       
        n = 500
        self.randommover(n)
        average = self.Average(self.allmoves) 
        print(f"avarage of {self.game} board for {n} runs = {average}")
        
    def Average(self, lst): 
        return sum(lst) / len(lst) 
    
    def Reset(self):
        self.board = self.load_board(f"data/{self.game}.txt")
        self.cars = self.load_cars()

    def randommover(self, amount):
        for i in range(0, amount): 
            for i, car in enumerate(self.cars):
                if car.red_car:
                    redcar = self.cars[i]
                    break
            moves = 0
            moveables = ["left", "right", "up", "down"]
      

            while redcar.y + 1 != self.board.exit_position:
                randy = randint(0, len(self.cars) - 1)
                randomcar = self.cars[randy]
                carmove = randomcar.moveable(self.board)
                if redcar.moveable(self.board) == "leftright":
                    rand = randint(0, 100)
                    if rand > 20:
                        redcar.move(self.board, "right")
                    else:
                        redcar.move(self.board, "left")
                    moves += 1
                    continue
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
            print(moves)
            print(self.board)
            
            self.Reset()
            self.allmoves.append(moves)
            
        return self.allmoves

if __name__ == "__main__":
    rushhour = RushHour("medium3")
    rushhour.playtest()
    
"""
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
                                    position = [str(i) + "." + str(j), str(i) + "." + str(j + 1), str(i) + "." + str(j + 2)]
                                    car = Car(char * 3, i, j, position, "horizontal", 3, False)
                                    cars.append(car)
                                    continue
                                # add 'x' at end of list just to be sure index error wont occur 
                                position = [str(i) + "." + str(j), str(i) + "." + str(j + 1)] # removed x
                                car = Car(char * 2, i, j, position, "horizontal", 2, False)
                                cars.append(car)
                            # car found, but not a 3 tile car
                            except IndexError:
                                position = [str(i) + "." + str(j), str(i) + "." + str(j + 1)] # removed x
                                car = Car(char * 2, i, j, position, "horizontal", 2, False)
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
                                    position = [str(i) + "." + str(j), str(i + 1) + "." + str(j), str(i + 2) + "." + str(j)]
                                    car = Car(char * 3, i, j, position, "vertical", 3, False)
                                    cars.append(car)
                                    continue
                                position = [str(i) + "." + str(j), str(i + 1) + "." + str(j)] # removed x 
                                car = Car(char * 2, i, j, position, "vertical", 2, False)
                                cars.append(car)
                            except IndexError:
                                position = [str(i) + "." + str(j), str(i + 1) + "." + str(j)] # removed x
                                car = Car(char * 2, i, j, position, "vertical", 2, False)
                                cars.append(car)
                                continue
                    except IndexError:
                        continue
                elif char == "r" and char not in taken_cars:
                    position = [str(i) + "." + str(j), str(i) + "." + str(j + 1)] # removed x
                    redcar = Car("redCar", i, j, position, "horizontal", 2, True)
                    taken_cars.append(char)
                    cars.append(redcar)        
        self.board.cars = cars
        return cars
"""