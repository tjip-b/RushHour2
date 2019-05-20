from board import Board 
from car import Car 
import copy
import time

class BreadthF():
    def __init__ (self, rushhour):
        self.queue = [] 
        self.rushhour = rushhour

        self.initialboard = copy.deepcopy(self.rushhour.initialboard)
        self.initialcars = copy.deepcopy(self.rushhour.initialcars)
      
    # implementation of a breadthfirst search method
    def BreadthFirst(self):        

        # set needed variables
        start = time.time()
        queue = []
        carlist = []
        n = 0
        searched_boards = set()

        # find first moveable options and place them in the queue
        for car in self.rushhour.cars:

            # check which cars are moveable
            car.moveability(self.rushhour.board)

            # if car is moveable to the left or upwards
            if car.moveability_list[0] is not 0:
                
                # # add all number of steps as moves to the queue
                # for i in range(1, car.moveability_list[0] + 1):
                #     queue.append([car.name[0] + "-" + str(i)])
                queue.append([car.name[0] + "-" + str(car.moveability_list[0])])
            # if car is moveable to the right or downwards
            if car.moveability_list[1] is not 0:

                # # add all number of steps as moves to the queue
                # for i in range(1, car.moveability_list[1] + 1):
                #     queue.append([car.name[0] + "+" + str(i)])

                queue.append([car.name[0] + "+" + str(car.moveability_list[1] )])
        # print(queue)
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

        # go on till solution is found or queue is empty
        while queue:
            
            # set everything to the initiak state
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

                # initialise CAR
                CAR = None
                carname = i[0]

                # set CAR to the car that is in the move command
                for car in self.rushhour.cars:
                    if car.name[0] == carname:
                        CAR = car
                        break
                
                # check if the movement is right or up (+) or left or down (-)
                if i[1] == "+":
                    move = int(i[2]) 
                else:
                    move = -int(i[2])
                # change the state of the board in the dictionary  
                dictcopy[car.name[0]] += move
                
                # execute the move
                CAR.move3(move) 
        
            # build the board after all the moves are executed
            self.rushhour.board = Board.build(1, self.rushhour.board.width_height + 1, self.rushhour.cars)

            

            # create an object for the red car, named redcar
            for car in self.rushhour.cars:
                if car.red_car:
                    redcar = car
            
            # check if a solution is found
            if redcar.col == self.rushhour.board.width_height-1:
                print(s)
                print("Gewonnen!")
                end = time.time()
                print(f"time is {end - start}")
                print(self.rushhour.board)
                print(len(s))
                return True

            # check all possible moves for each car
            for car in self.rushhour.cars:
                # if str(self.rushhour.board.positions) in searched_boards:
                #     break
                car.moveability(self.rushhour.board)

                # make sure the last moved car cannnot be moved again
                if s[-1][0] == car.name[0]:
                    continue

                # if moveable to the left or downwards
                if car.moveability_list[0] is not 0:
                    # add all possible moves
                    # for i in range(1, car.moveability_list[0] + 1):
                    #     #copy the current movelist                         
                    #     scopy = copy.deepcopy(s)
                        
                    #     # append the new move  
                    #     scopy.append(car.name[0] + "-" + str(i))

                    #     # copy and update the dictionary with the netto car positions
                    #     dictcopy2 = copy.deepcopy(dictcopy)
                    #     dictcopy2[car.name[0]] += -i

                    #     # make a string of the dictionary
                    #     x = str(dictcopy2)

                    #     # check if the current set of moves leads to a board that has not been visited
                    #     if x not in moves_set:
                    #         # if unique, add to the queue and the set with all the visited boards
                    #         queue.append(scopy)
                    #         moves_set.add(x)


                    scopy = copy.deepcopy(s)
                    
                    # append the new move  
                    scopy.append(car.name[0] + "-" + str(car.moveability_list[0]))

                    # copy and update the dictionary with the netto car positions
                    dictcopy2 = copy.deepcopy(dictcopy)
                    dictcopy2[car.name[0]] += -car.moveability_list[0]

                    # make a string of the dictionary
                    x = str(dictcopy2)

                    # check if the current set of moves leads to a board that has not been visited
                    if x not in moves_set:
                        # if unique, add to the queue and the set with all the visited boards
                        queue.append(scopy)
                        moves_set.add(x)

                # if moveable to the right or upwards
                if car.moveability_list[1] is not 0:
                    # add all possible moves
                    # for i in range(1, car.moveability_list[1] + 1):
                    #     #copy the current movelist 
                    #     scopy = copy.deepcopy(s)
                        
                    #     # append the new move  
                    #     scopy.append(car.name[0] + "+" + str(i))
                    #     # copy and update the dictionary with the netto car positions
                    #     dictcopy2 = copy.deepcopy(dictcopy)
                    #     dictcopy2[car.name[0]] += i

                    #     # make a string of the dictionary
                    #     x = str(dictcopy2)

                    #     # check if the current set of moves leads to a board that has not been visited
                    #     if x not in moves_set:
                    #         # if unique, add to the queue and the set with all the visited boards
                    #         queue.append(scopy)
                    #         moves_set.add(x)


                    scopy = copy.deepcopy(s)
                    
                    # append the new move  
                    scopy.append(car.name[0] + "+" + str(car.moveability_list[1]))

                    # copy and update the dictionary with the netto car positions
                    dictcopy2 = copy.deepcopy(dictcopy)
                    dictcopy2[car.name[0]] += car.moveability_list[1]

                    # make a string of the dictionary
                    x = str(dictcopy2)
                    # check if the current set of moves leads to a board that has not been visited
                    if x not in moves_set:
                        # if unique, add to the queue and the set with all the visited boards
                        queue.append(scopy)
                        moves_set.add(x)
                searched_boards.add(str(self.rushhour.board.positions))
            # print the ammount of visited boards.
            # print(len(moves_set))
            # print(self.rushhour.board)
            
            