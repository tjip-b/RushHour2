from board import Board 
from car import Car 
import helpers
import copy
import time
import random

class Algorithm():
    def __init__ (self, rushhour):
        self.rushhour = rushhour

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
            print(self.rushhour.board)
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
            
            if car.moveability_list[0] is not 0 or car.moveability_list[1] is not 0:
                moveable_cars.append(car)
        return moveable_cars

    def moves_list(self, max_movement):
        """
        makes a list with moveable cars
        """
        moveable_cars = []
        if max_movement == True:
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
        
        return moveable_cars
    
    def car_distance(self):
        """
        calculates the distance of a car to the exit
        """
        size = self.rushhour.board.width_height
        exit_position = self.rushhour.board.exit_position
        for car in self.rushhour.cars:
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
        return move
    
    def depth_first(self, depth, depth_pruning, max_movement):
        """ Implementation of the depth first search algorithm for
            the rush hour game. Takes a max depth limit as parameter.
            Also takes a bool for the pruning method:
            True = maximal pruning: prune every child which has a visited board
            Flase = depth pruning: prune every child which has a visited board and
            a higher depth level than the previous board with the same positions.
        """

        # set needed variables
        start = time.time()
        stack = []                 
        current_depth = -1          # current search depth
        max_depth = depth           # maximum depth, devines nodes at this depth as leaves
        n = 0                       # amount of nodes
        
        # make archive set or dict depending on pruning method
        if depth_pruning:
            archive = {}            # dict needed for pruning which contains all visited boards
        else:
            archive = set() 
        cars_dictionary = {}        # dictionary with all netto car movements (equivalent to board.positions)
        
        # find first moveable options and place them in the queue
        move_list = self.moves_list(max_movement)

        for move in move_list:
            stack.append([move])       

        # make a dictionary with all the cars, which is used later.
        for car in self.rushhour.cars:
            cars_dictionary[car.name[0]] = 0
        
        if depth_pruning:
            # start netto movement positions (equivalent to start board) added to archive
            archive[str(cars_dictionary)] = 0
        else:
            # append dictionary to set and list. it is added as a string to the set so it can be hashed. 
            archive.add(str(cars_dictionary)) 

        while stack:
            # set everything to the initial state
            self.rushhour.board = copy.deepcopy(self.rushhour.initial_board)
            self.rushhour.cars = copy.deepcopy(self.rushhour.initial_cars)

            # make a copy of the "standard" car dictionary
            dictcopy = copy.deepcopy(cars_dictionary)
            
            # take the first item from the stack and pop it.
            s = stack.pop() 

            # print in which iteration we are and the current movelist
            print(f"n = {n}")
            n += 1

            # check current tree depth
            current_depth = len(s)
            if current_depth > max_depth:
                continue        

            # iterate through the move commands in s
            for move_string in s:
                movement = self.execute_move_command(move_string)
                dictcopy[move_string[0]] += movement

            # build the board after all the moves are executed
            self.rushhour.board = helpers.build(self.rushhour.board.width_height + 1, copy.deepcopy(self.rushhour.cars))

            # check if a solution is found
            if self.check_if_won() == True:
                print(s)
                print("Gewonnen!")
                end = time.time()
                print(f"time is {end - start}")
                print(f"n = {n}")
                print(self.rushhour.board)
                print(f"amount of moves / depth: {len(s)}")
                return True
            
            if depth_pruning:
                # add netto movements (equivalent to positions on the board) to archive
                archive[(str(dictcopy))] = len(s) 

            # make all possible moves
            move_list = self.moves_list(max_movement)
            
            # make children for all possible movements
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

                # string version of the netto moves dictionary (equivalent to board.positions)
                current_netto_moves = str(dictcopy2)

                # select type of pruning method
                if depth_pruning:
                    # check if the current set of moves leads to a board that has not been visited
                    if current_netto_moves not in archive:
                        # if unique, add to the queue and the set with all the visited boards
                        stack.append(scopy)
                    else: 
                        move_length = archive[str(current_netto_moves)]
                        if len(scopy) < move_length:
                            stack.append(scopy)
                            archive[str(current_netto_moves)] = move_length
                else:
                    # check if the current set of moves leads to a board that has not been visited
                    if current_netto_moves not in archive:
                        # if unique, add to the queue and the set with all the visited boards
                        stack.append(scopy)
                        archive.add(current_netto_moves)

    def breadth_first(self, max_movement, breadth):        
        nodes_at_treelevel = []
        node_counter = 0
        len_s = 0
        start = time.time()
        self.initialboard = copy.deepcopy(self.rushhour.initial_board)
        self.initialcars = copy.deepcopy(self.rushhour.initial_cars)
        queue = []
        n = 0

        # find first moveable options and place them in the queue
        move_list = self.moves_list(max_movement)
        
        for move in move_list:
            queue.append([move])
         
        # set needed for pre pruning which contains all visited boards. 
        archive = set()
        
        # make a dictionary with all the cars, which is used later.
        cars_dictionary = {}
        for car in self.rushhour.cars:
            cars_dictionary[car.name[0]] = 0
        
        # append dictionary to set and list. it is added as a string to the set so it can be hashed. 
        archive.add(str(cars_dictionary))

        # go on till solution is found or queue is empty
        while queue:
            # uses different counters deppending on the version of breadth first
            counter = 0
            node_counter += 1
            
            # set everything to the initial state
            self.rushhour.board = copy.deepcopy(self.rushhour.initial_board)
            self.rushhour.cars = copy.deepcopy(self.rushhour.initial_cars)

            # make a copy of the "standard" car dictionary
            dictcopy = copy.deepcopy(cars_dictionary)
            
            # take the first item from the queue and pop it.
            s = queue.pop(0) 

            # gets the amount of nodes per depth level
            if len(s) == len_s + 1:
                nodes_at_treelevel.append(node_counter)
                node_counter = 0
                len_s = len(s)
            
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
                return nodes_at_treelevel

            # make all possible moves
            move_list = self.moves_list(max_movement)
            
            # two versions of breadth first branch off here
            if breadth > 0:
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
                    if x not in archive:
                        # if unique, add to the queue and the set with all the visited boards
                        queue.append(scopy)
                        archive.add(x)
                        move_list.remove(move)
                        counter += 1
                    else:
                        move_list.remove(move)

            else:
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
                    if x not in archive:
                        # if unique, add to the queue and the set with all the visited boards
                        queue.append(scopy)
                        archive.add(x)
    
    def depth_random(self, depth):        
        """
        Random searches for a solution till a given depth. Returns the solution
        """
        # set needed variables        
        start = time.time()
        n = 0

        # make a list with moveable cars
        moveable_cars = self.moves_list(depth)
       
        # pick a random move
        move = random.choice(moveable_cars)
       
        # make a set that contains all visited boards
        archive = set()

        # make a dictionary that contains all cars with their netto movement
        cars_dictionary = {}
        for car in self.rushhour.cars:
            cars_dictionary[car.name[0]] = 0
        
        # append dictionary to set. it is added as a string to the set so it can be hashed. 
        archive.add(str(cars_dictionary))
        
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

            # archive.add(str(cars_dictionary))
            s.append(move)
            
            # build the board
            self.rushhour.board = helpers.build(self.rushhour.board.width_height + 1, self.rushhour.cars)
            
            if self.check_if_won() == True:
                print(s)
                print("Gewonnen!")
                end = time.time()
                print(f"time is {end - start}")
                print(f"n = {n}")
                print(self.rushhour.board)
                return s

            # check all possible moves for each car and add them to a list
            moveable_cars = self.moves_list(False)
                    
            for i in range (0, 1000000):
                
                # try to pick a random move
                try:
                    move = random.choice(moveable_cars)
                # if no moves, return False
                except IndexError: 
                    return False

                # copy and update the dictionary with the netto car positions
                dictcopy2 = copy.deepcopy(cars_dictionary)
                if move[1] == "+":
                    movement = int(move[2]) 
                else:
                    movement = -int(move[2])
                dictcopy2[move[0]] += movement

                # make a string of the dictionary
                x = str(dictcopy2)

                # check if the current set of moves leads to a board that has not been visited
                if x not in archive:
                    archive.add(x)
                    break
                # if not, remove the car from moveable cars
                else:
                    moveable_cars.remove(move)
        return s 
   
    def find_solution(self, maximum_depth):
        """
        Runs Depth random until it finds a solution with a depth lower than maximum depth
        """
        Copy = copy.deepcopy(self.rushhour)
        depth = maximum_depth + 1
        while depth > maximum_depth:
            self.rushhour = copy.deepcopy(Copy)
            solution = self.depth_random(depth)
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
            self.rushhour.board = helpers.build(self.rushhour.board.width_height + 1, self.rushhour.cars)
          
            board_copy = copy.deepcopy(self.rushhour)   

            # set depth to search length
            depth = search_length
            
            # counter = 0
            
            while depth > search_length - 1:
                bf = copy.deepcopy(Algorithm(board_copy))
                s = bf.Depth_Random(depth)
                if s is not False:
                    depth = len(s)
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