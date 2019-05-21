from load import Load
from board import Board 
from car import Car 
import copy
import time
import random

class Depth_random():
    def __init__ (self, rushhour):
        self.queue = [] 
        self.rushhour = rushhour
    # implementation of a breadthfirst search method

    def check_if_won(self):
        """
        checks if the board is solved
        """
        # create an object for the red car, named redcar
        for car in self.rushhour.cars:
            if car.name[0] == "r":
                redcar = car

        # check if a solution is found
        if redcar.col == self.rushhour.board.width_height-1:
            return True
        else:
            return False

    def moveable_list(self):
        """
        makes a list with moveable cars
        """
        moveable_cars = []
        
        for car in self.rushhour.cars:
            car.moveability(self.rushhour.board)
            
            # append car if moveable
            if car.moveability_list[0] is not 0 or car.moveability_list[1] is not 0:
                moveable_cars.append(car)
        # print(moveable_cars) 
        return moveable_cars


    def car_distance(self):
        """
        calculates the distance of a car to the exit
        """
        size = self.rushhour.board.width_height
        # print (f"size is {size}")
        exit_position = self.rushhour.board.exit_position
        for car in self.rushhour.cars:
            # print(car.col)
            if car.direction == 0:
                car.distance = size - car.col
            else:
                car.distance = abs(car.row-exit_position)
            

    def execute_move_command(self, command):
        """
        executes a movement given as input (command)
        """
        CAR = None
        carname = command[0]

        # set CAR to the car that is in the move command
        for car in self.rushhour.cars:
            if car.name[0] == carname:
                CAR = car
                break
        
        # check if the movement is right or up (+) or left or down (-)
        if command[1] == "+":
            move = int(command[2]) 
        else:
            move = -int(command[2])
        # execute the move
        CAR.move3(move) 


    def Depth_Random(self, depth):        
        """
        Random searches for a solution till a given depth. Returns the solution
        """
        # set needed variables        
        start = time.time()
        n = 0

        # make a list with moveable cars
        moveable_cars = self.moveable_list()
       
        # pick a random car
        car = random.choice(moveable_cars)
        # if car is moveable to the left or upwards

        if car.moveability_list[0] is not 0:
            move = car.name[0] + "-" + str(car.moveability_list[0])
        else:
            move = car.name[0] + "+" + str(car.moveability_list[1] )

        # clear moveable cars
        moveable_cars.clear()
       
        # make a set that contains all visited boards
        moves_set = set()

        # make a dictionary that contains all cars with their netto movement
        cars_dictionary = {}
        for car in self.rushhour.cars:
            cars_dictionary[car.name[0]] = 0
        
        # append dictionary to set. it is added as a string to the set so it can be hashed. 
        moves_set.add(str(cars_dictionary))
        
        # make a list that will contain all executed moves 
        s = []    

        while n < depth:
            n += 1

            # execute move and save it in the dictionary
            self.execute_move_command(move)
            if move[1] == "+":
                movement = int(move[2])
            else:
                movement = -int(move[2])
            cars_dictionary[car.name[0]] += movement
            # moves_set.add(str(cars_dictionary))
            s.append(move)
            
            # build the board
            self.rushhour.board = Board.build(1, self.rushhour.board.width_height + 1, self.rushhour.cars)
            
            if self.check_if_won() == True:
                print(s)
                print("Gewonnen!")
                end = time.time()
                print(f"time is {end - start}")
                print(f"n = {n}")
                print(self.rushhour.board)
                return s

            # check all possible moves for each car and add them to a list
            moveable_cars = self.moveable_list()
                    
            for i in range (0, 1000000):
                
                # try to pick a random moveable car
                try:
                    car = random.choice(moveable_cars)
                # if no moveable cars, return False
                except IndexError: 
                    return False

                # check if car goes left or down
                if car.moveability_list[0] is not 0:
                    
                    # copy and update the dictionary with the netto car positions
                    dictcopy2 = copy.deepcopy(cars_dictionary)
                    dictcopy2[car.name[0]] += -car.moveability_list[0]

                    # make a string of the dictionary
                    x = str(dictcopy2)

                    # check if the current set of moves leads to a board that has not been visited
                    if x not in moves_set:

                        move = car.name[0] + "-" + str(car.moveability_list[0])
                        moves_set.add(x)
                        break
                    # if not, remove the car from moveable cars
                    else:
                        moveable_cars.remove(car)
                
                if car.moveability_list[1] is not 0:

                    # copy and update the dictionary with the netto car positions
                    dictcopy2 = copy.deepcopy(cars_dictionary)
                    dictcopy2[car.name[0]] += car.moveability_list[1]

                    # make a string of the dictionary
                    x = str(dictcopy2)

                    # check if the current set of moves leads to a board that has not been visited
                    if x not in moves_set:

                        # if unique, make it the next move and add to the set with all the visited boards 
                        move = car.name[0] + "+" + str(car.moveability_list[1])
                        moves_set.add(x)

                        break
                    else:
                         # if not, try to remove the car from moveable cars
                        try:
                            moveable_cars.remove(car)
                        except ValueError: 
                            pass   
        # if a solution is found that's below the given depth, return the solution 
        return s    

   
    def find_solution(self, maximum_depth):
        
        """
        Runs Depth random until it finds a solution with a depth lower than maximum depth
        """

        Copy = copy.deepcopy(self.rushhour)
        depth = maximum_depth + 1
        while depth > maximum_depth:
            self.rushhour = copy.deepcopy(Copy)
            solution = Depth_random.Depth_Random(self, depth)
            if solution is not False:
                depth = len(solution)
            print(f"the current depth = {depth}")
        return solution
    
    def optimalize_solution(self, maximum_depth, move_list):

        """
        Takes a solution as input, given by move_list and tries to shorten this solution
        """

        Copy = copy.deepcopy(self.rushhour)
        List = move_list

        # iterate till asked depth is reached
        while len(List) > maximum_depth:
            
            # we search half the length of the given tree
            search_length = int(len(List)/2)
            
            # print the list in case anybody wants to  quit the algorithm before it is finished
            print(f"the length of the list = {len(List)}")
            print(List)

            self.rushhour = copy.deepcopy(Copy)
            
            # take half of the given move list
            List = List[0:len(List)-search_length]
            
            # execute half
            for move in List:
                self.execute_move_command(move)

            # build the board after all the moves are executed
            self.rushhour.board = Board.build(1, self.rushhour.board.width_height + 1, self.rushhour.cars)
          
            board_copy = copy.deepcopy(self.rushhour)   

            # set depth to search length
            depth = search_length
            
            # counter = 0
            
            while depth > search_length - 1:
                # counter += 1
                # print(f"counter = {counter}")
                bf = copy.deepcopy(Depth_random(board_copy))
                s = bf.Depth_Random(depth)
                if s is not False:
                    depth = len(s)
                # print(counter)
            List.extend(s)
        
        # if desired depth is found, return moves.
        return List

    def find_optimised_solution(self, max_1, max_2):
        """
        finds a solution and optimalises it. The max_1 is the depth limit till which find_solution searches, max_2 is the depth limit till which it is optimised
        """
        Copy = copy.deepcopy(self)
        List = self.find_solution(max_1)
        self = copy.deepcopy(Copy)
        optimised_list = self.optimalize_solution(max_2, List)
        return optimised_list