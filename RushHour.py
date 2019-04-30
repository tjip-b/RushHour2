from board import Board
from car import Car
from load import Load
from bruteforce import Bruteforce
from breadthF import BreadthF
from random import randint
import time
from colorama import init
init()
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

    # def Breadthfirst(self)

        elif method == "hi":
            print(self.board.moveables)
            self.board.get_moveables()
            print(self.board.moveables)
            

    def BFS(self):
        queue = []
        archive = []
        solutions = []
        queue.insert(0, self.board)

        print(int(self.board.width_height / 2))
        print(self.board.positions[int(self.board.width_height / 2)][self.board.exit_position])

        while queue:
            startboard = queue.pop(0)
            
            movelist = startboard.get_moveables()
            print(movelist)
            moveboard = copy.deepcopy(startboard)
            for i, moves in enumerate(movelist):
                if moves == [0, 0]:
                    continue
                # two moves are possible
                elif moves[0] > 0 and moves[1] > 0:
                    print("bothways!")
                    moveboard1 = copy.deepcopy(startboard)
                    
                    moveboard.cars[i].move(moveboard, 0)
                    if moveboard.positions not in archive:
                        archive.append(copy.deepcopy(moveboard.positions))
                        solutions.append(copy.deepcopy(moveboard.positions))
                        queue.insert(0, copy.deepcopy(moveboard))
                        print(moveboard)
                    moveboard1.cars[i].move(moveboard1, 1)
                    if moveboard1.positions not in archive:
                        archive.append(copy.deepcopy(moveboard1.positions))
                        solutions.append(copy.deepcopy(moveboard1.positions))
                        queue.insert(0, copy.deepcopy(moveboard1))
                        print(moveboard1)
                    
                # move car left or up
                elif moves[0] > 0:
                    # print(f"NAME: {moveboard.cars[i].name} ROW: {moveboard.cars[i].row} COL: {moveboard.cars[i].col}")
                    # print(moveboard)
                    moveboard.cars[i].move(moveboard, 0) # 0 = move left or up
                    if moveboard.positions in archive:
                        continue
                    # add to solution checker and archive lists
                    archive.append(copy.deepcopy(moveboard.positions))
                    solutions.append(copy.deepcopy(moveboard.positions))

                    # print(f"NAME: {moveboard.cars[i].name} ROW: {moveboard.cars[i].row} COL: {moveboard.cars[i].col}")
                    print(moveboard)
                    # print(moveboard.get_moveables())
                    
                    queue.insert(0, copy.deepcopy(moveboard))
                
                # move car right or down
                elif moves[1] > 0:
                    moveboard.cars[i].move(moveboard, 1) # 1 = move right or down
                    
                    
                    # check if board position has already been rached 
                    if moveboard.positions in archive:
                        continue
                    archive.append(copy.deepcopy(moveboard.positions))
                    solutions.append(copy.deepcopy(moveboard.positions))
                    queue.insert(0, copy.deepcopy(moveboard))
                    print(moveboard)
                # reset moveboard 
                moveboard = copy.deepcopy(startboard)
            for solution in solutions:
                if solution[int(startboard.width_height / 2 - 1)][startboard.exit_position] == 'r':
                    print("Won! won! won! won! won! won!")
                    print(solution)
                    break
            solutions.clear()

    def Average(self, lst): 
        return sum(lst) / len(lst) 
    
    def Reset(self):
        self.board = Load.load_board(self, f"data/{self.game}.txt")
        self.cars = Load.load_cars(self)

if __name__ == "__main__":
    rushhour = RushHour("supereasy")
    # print(rushhour.board)
    # print(rushhour.board.empty)
    rushhour.BFS()
    # BreadthF.BreadthFirst(rushhour)
    # print(rushhour.board)
    # for car in rushhour.cars:
    #     print(car.name)
    #     print(car.col, car.row)
    # Car.move3(rushhour.cars[0], -1)
    # print(rushhour.cars[0].col, rushhour.cars[0].row)
    # rushhour.playtest("bruteforce")
    # print(rushhour.board.positions)
     