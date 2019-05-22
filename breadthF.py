from board import Board 
from car import Car 
import helpers
import copy
import time
import random

class BreadthF():
    def __init__ (self, rushhour):
        self.queue = [] 
        self.rushhour = rushhour
    # implementation of a breadthfirst search method

    def car_distance(self):
        size = self.rushhour.board.width_height
        # print (f"size is {size}")
        exit_position = self.rushhour.board.exit_position
        for car in self.rushhour.cars:
            # print(car.col)
            if car.direction == 0:
                car.distance = size - car.col
            else:
                car.distance = abs(car.row-exit_position)
            # car.distance = x_distance + y_distance
            # print(car.distance)

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


    def moves_list(self, max_depth):
        """
        makes a list with moveable cars
        """
        moveable_cars = []
        if max_depth == True:
            for car in self.rushhour.cars:
                car.moveability(self.rushhour.board)
                
                # append car if moveable
                if car.moveability_list[0] is not 0: 
                    move = car.name[0] + "-" + str(car.moveability_list[0])
                    moveable_cars.append(move)
                
                if car.moveability_list[1] is not 0:
                    move = car.name[0] + "+" + str(car.moveability_list[1])
                    moveable_cars.append(move)
        else:
            for car in self.rushhour.cars:
                car.moveability(self.rushhour.board)
                
                # append car if moveable
                if car.moveability_list[0] is not 0:
                    for i in range(0, car.moveability_list[0]):
                        move = car.name[0] + "-" + str(i + 1)
                        moveable_cars.append(move)
                
                if car.moveability_list[1] is not 0:
                    for i in range(0, car.moveability_list[1]):
                        move = car.name[0] + "+" + str(i + 1)
                        moveable_cars.append(move)
        # print(moveable_cars) 
        return moveable_cars

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
        return move

    def BreadthFirst(self, initialboard, initialcars, max_depth):        
        nodes_at_treelevel = []
        node_counter = 0
        len_s = 0
        start = time.time()
        self.initialboard = copy.deepcopy(initialboard)
        self.initialcars = copy.deepcopy(initialcars)
        queue = []
        carlist = []
        n = 0

        # find first moveable options and place them in the queue
        move_list = self.moves_list(max_depth)
        
        for move in move_list:
            queue.append([move])
         
        # set needed for pre pruning which contains all visited boards. 
        moves_set = set()
        
        # make a dictionary with all the cars, which is used later.
        cars_dictionary = {}
        for car in self.rushhour.cars:
            cars_dictionary[car.name[0]] = 0
        
        # append dictionary to set and list. it is added as a string to the set so it can be hashed. 
        moves_set.add(str(cars_dictionary))

        # go on till solution is found or queue is empty
        print (queue)
        while queue:
            
            node_counter += 1
            # set everything to the initial state
            self.rushhour.board = copy.deepcopy(self.initialboard)
            self.rushhour.cars = copy.deepcopy(self.initialcars)

            # make a copy of the "standard" car dictionary
            dictcopy = copy.deepcopy(cars_dictionary)
            
            # take the first item from the queue and pop it.
            s = queue.pop(0) 

            if len(s) == len_s + 1:
                nodes_at_treelevel.append(node_counter)
                node_counter = 0
                len_s = len(s)

            # print in which iteration we are and the current movelist
            # print(f"n = {n}")
            n += 1
            # print(s)
            
            # iterate through the move commands in s
            for i in s:
                move = self.execute_move_command(i)
                dictcopy[i[0]] += move
            
            # build the board after all the moves are executed
            self.rushhour.board = helpers.build(self.rushhour.board.width_height + 1, self.rushhour.cars)
            print(self.rushhour.board)
            # check if a solution is found
            if self.check_if_won() == True:
                print(s)
                print("Gewonnen!")
                end = time.time()
                print(f"time is {end - start}")
                print(f"n = {n}")
                print(self.rushhour.board)
                return nodes_at_treelevel
                break

            # make all possible moves
            move_list = self.moves_list(max_depth)
            
            for move in move_list:
                
                # copy the moves that led to the present board
                scopy = copy.deepcopy(s)
                    
                # append the new move  
                scopy.append(move)

                # copy and update the dictionary with the netto car positions
                dictcopy2 = copy.deepcopy(dictcopy)
                if move[1] == "-":
                    dictcopy2[move[0]] += -int(move[2])
                else:
                    dictcopy2[move[0]] += int(move[2])

                # make a string of the dictionary
                x = str(dictcopy2)

                # check if the current set of moves leads to a board that has not been visited
                if x not in moves_set:
                    # if unique, add to the queue and the set with all the visited boards
                    queue.append(scopy)
                    moves_set.add(x)

    def BreadthFirst_adjusted(self, initialboard, initialcars, breadth):        

        start = time.time()
        self.initialboard = copy.deepcopy(initialboard)
        self.initialcars = copy.deepcopy(initialcars)
        queue = []
        carlist = []
        n = 0

        # find first moveable options and place them in the queue
        move_list = self.moves_list(True)
        # move = random.choice(move_list)
        for move in move_list:
            queue.append([move])

        # set needed for pre pruning which contains all visited boards. 
        moves_set = set()
        
        # make a dictionary with all the cars, which is used later.
        cars_dictionary = {}
        for car in self.rushhour.cars:
            cars_dictionary[car.name[0]] = 0
        
        # append dictionary to set and list. it is added as a string to the set so it can be hashed. 
        moves_set.add(str(cars_dictionary))

        # go on till solution is found or queue is empty
        while queue:
       
            counter = 0
            # set everything to the initial state
            self.rushhour.board = copy.deepcopy(self.initialboard)
            self.rushhour.cars = copy.deepcopy(self.initialcars)

            # make a copy of the "standard" car dictionary
            dictcopy = copy.deepcopy(cars_dictionary)
            
            # take the first item from the queue and pop it.
            s = queue.pop(0) 

            # print in which iteration we are and the current movelist
            print(f"n = {n}")
            n += 1
            print(s)

            # iterate through the move commands in s
            for i in s:
                move = self.execute_move_command(i)
                dictcopy[i[0]] += move
        
            # build the board after all the moves are executed
            self.rushhour.board = helpers.build(self.rushhour.board.width_height + 1, self.rushhour.cars)

   
            
            # check if a solution is found
            if self.check_if_won() == True:
                print(s)
                print("Gewonnen!")
                end = time.time()
                print(f"time is {end - start}")
                print(f"n = {n}")
                print(self.rushhour.board)
                return True
                break

            # make a list with all possible moves
            move_list = self.moves_list(True)            
            # while counter <= breadth:
            for i in range (0, 1000000):

                if counter >= breadth:
                    move_list.clear()
                    break

                try:
                    move = random.choice(move_list)
                except IndexError: 
                    break
  
            
                scopy = copy.deepcopy(s)
                
                # append the new move  
                scopy.append(move)
                dictcopy2 = copy.deepcopy(dictcopy)
                # copy and update the dictionary with the netto car positions
                if move[1] == "-":
                    dictcopy2[move[0]] += -int(move[2])
                else:
                    dictcopy2[move[0]] += int(move[2])

                # make a string of the dictionary
                x = str(dictcopy2)

                # check if the current set of moves leads to a board that has not been visited
                if x not in moves_set:
                    # if unique, add to the queue and the set with all the visited boards
                    queue.append(scopy)
                    moves_set.add(x)
                    move_list.remove(move)
                    counter += 1
                else:
                    move_list.remove(move)
         