from board import Board 
from car import Car 
import copy
import time

class DepthF():
    def __init__ (self, rushhour, depth):
        self.rushhour = rushhour
        self.depth = depth

    def depth_first_try(self):
        stack = []                  
        cur_depth = -1              # current search depth
        max_depth = self.depth      # maximum depth, devines nodes at this depth as leaves
        last_node = None            # string of dicts of last node traversed
        carlist = []                # list of car objects 
        n = 0                       # amount of nodes
        archive = set()
        childs_list = []

        stack.append(self.rushhour.board) # push de beginstate op de stack

        while stack:
            current = copy.deepcopy(stack.pop())
            archive.add(str(copy.deepcopy(current.positions)))
            print(archive)

            # make all childs of the item
            


            for car in current.cars:
                # check which cars are moveable
                car.moveability(current.board)

                # if car is moveable to the left or upwards
                if car.moveability_list[0] is not 0:
                    
                    # add all number of steps as moves to the stack
                    for i in range(0, car.moveability_list[0]):
                        car.move()

                # if car is moveable to the right or downwards
                if car.moveability_list[1] is not 0:

                    # add all number of steps as moves to the stack
                    for i in range(1, car.moveability_list[1] + 1):
                        stack.append([car.name[0] + "+" + str(i)])
            

            # add all children to the stack
            for child in childs_list:
                stack.add(child)








    def build(self):
        """"
        builds a board, based on the size of the board and the cars whcih are given as input
        """
        size = self.rushhour.board.width_height + 1
        cars = self.rushhour.cars

        board_positions = []
        row = []

        # construct an empty board
        for i in range (0, size):
            row.append("x")
        for i in range (0, size):
            board_positions.append(copy.copy(row))
        
        # place the cars on the board
        for car in cars:
            # check the orientation of the car
            if car.direction == "horizontal":
                # change the x's to the car letter.
                for i in range(0, car.size):
                    board_positions[car.row][car.col + i] = car.name[0]
                    
            # same for vertical cars
            else:
                for i in range (int(car.size)):
                    board_positions[car.row + i][car.col] = car.name[0]

        # make a new board object
        board = Board(size-1, board_positions, (size)/2-1, 0)  
        
        # return the board object
        return(board)    


    # implementation of a breadthfirst search method
    def depth_first(self):        

        # set needed variables
        start = time.time()
        stack = []                  
        cur_depth = -1              # current search depth
        max_depth = self.depth      # maximum depth, devines nodes at this depth as leaves
        last_node = None            # string of dicts of last node traversed
        carlist = []                # list of car objects 
        n = 0                       # amount of nodes

        # find first moveable options and place them in the stack
        for car in self.rushhour.cars:

            # check which cars are moveable
            car.moveability(self.rushhour.board)

            # if car is moveable to the left or upwards
            if car.moveability_list[0] is not 0:
                
                # add all number of steps as moves to the stack
                for i in range(1, car.moveability_list[0] + 1):
                    stack.append([car.name[0] + "-" + str(i)])

            # if car is moveable to the right or downwards
            if car.moveability_list[1] is not 0:

                # add all number of steps as moves to the stack
                for i in range(1, car.moveability_list[1] + 1):
                    stack.append([car.name[0] + "+" + str(i)])

        # set needed for pre pruning which contains all visited boards. 
        moves_set = set()

        # make a dictionary with all the cars, which is used later.
        cars_dictionary = {}
        for car in self.rushhour.cars:
            cars_dictionary[car.name[0]] = 0
        
        # append dictionary to set and list. it is added as a string to the set so it can be hashed. 
        moves_set.add(str(cars_dictionary))

        # find the initial position of the red car and make an object redcar 
        for car in self.rushhour.cars:
            if car.name[0] == "r":
                redcarposition_inital = copy.deepcopy(car.col)

        print(f"pre stack: {stack}")

        # go on till solution is found or stack is empty
        while stack:
            

            # set everything to the initial state
            self.rushhour.board = copy.deepcopy(self.rushhour.initialboard)
            self.rushhour.cars = copy.deepcopy(self.rushhour.initialcars)

            # make a copy of the "standard" car dictionary
            dictcopy = copy.deepcopy(cars_dictionary)
            
            # take the first item from the stack and pop it.
            s = stack.pop() 
            
            # check depth of current item
            cur_depth = len(s)
            if cur_depth > max_depth:
                continue

            print(moves_set)

            # print in which iteration we are and the current movelist
            print(f"n = {n}")
            n += 1
            print(s)

            # iterate through the move commands in s
            for i in s:

                # initialise CAR
                CAR = None
                carletter = i[0]

                # set CAR to the car that is in the move command
                for car in self.rushhour.cars:
                    if car.name[0] == (carletter):
                        CAR = car
                        break
                
                # check if the movement is right or up (+) or left or down (-)
                if i[1] == "+":
                    move = int(i[2])
                else:
                    move = -int(i[2])
                
                # change the state of the board in the dictionary  
                dictcopy[carletter] += move
                
                # execute the move
                CAR.move3(move) 
        
            # build the board after all the moves are executed
            self.rushhour.board = self.build()

            # create an object for the red car, named redcar
            for car in self.rushhour.cars:
                if car.red_car[0]:
                    redcar = car
            
            # check if a solution is found
            if redcar.col == self.rushhour.board.width_height-1:
                print(s)
                print("Gewonnen!")
                end = time.time()
               
                # set new depth limit
                max_depth = len(s)

                print(f"time is {end - start}")
                print(self.rushhour.board)
                break

            # check all possible moves for each car
            for car in self.rushhour.cars:
                car.moveability(self.rushhour.board)

                # make sure the last moved car cannnot be moved again
                if s[-1][0] == car.name[0]:
                    continue

                # if moveable to the left or downwards
                if car.moveability_list[0] is not 0:
                    # add all possible moves
                    for i in range(1, car.moveability_list[0] + 1):
                        #copy the current movelist                         
                        scopy = copy.deepcopy(s)
                        
                        # append the new move  
                        scopy.append(car.name[0] + "-" + str(i))

                        # copy and update the dictionary with the netto car positions
                        dictcopy2 = copy.deepcopy(dictcopy)
                        dictcopy2[car.name[0]] += -i

                        stack.append(scopy)

                        # make a string of the dictionary
                        #x = str(dictcopy2)

                        # check if the current set of moves leads to a board that has not been visited
                        # if x not in moves_set:
                            # if unique, add to the stack and the set with all the visited boards
                        #    stack.append(scopy)
                        #    moves_set.add(x)

                # if moveable to the right or upwards
                if car.moveability_list[1] is not 0:
                    # add all possible moves
                    for i in range(1, car.moveability_list[1] + 1):
                        #copy the current movelist 
                        scopy = copy.deepcopy(s)
                        
                        # append the new move  
                        scopy.append(car.name[0] + "+" + str(i))
                        # copy and update the dictionary with the netto car positions
                        dictcopy2 = copy.deepcopy(dictcopy)
                        dictcopy2[car.name[0]] += i

                        stack.append(scopy)

                        # make a string of the dictionary
                        # x = str(dictcopy2)

                        # check if the current set of moves leads to a board that has not been visited
                        # if x not in moves_set:
                            # if unique, add to the stack and the set with all the visited boards
                        #    stack.append(scopy)
                        #    moves_set.add(x)
            print(stack)
            
            # print the ammount of visited boards.
            print(len(moves_set))

            