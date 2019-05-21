from board import Board
from car import Car
import copy
import time


class BreadthF():
    def __init__(self, rush_hour):
        self.queue = []
        self.rush_hour = rush_hour

        self.initial_board = copy.deepcopy(self.rush_hour.initial_board)
        self.initial_cars = copy.deepcopy(self.rush_hour.initial_cars)

    def win_check(board_positions):
        if board_positions[len(board_positions) / 2][len(board_positions) - 1] == 'r':
            return True

    def make_children():
            # iterate through the move commands in s
        for i in s:

            # initialise CAR
            CAR = None
            car_name = i[0]

            # set CAR to the car that is in the move command
            for car in self.rush_hour.cars:
                if car.name[0] == car_name:
                    CAR = car
                    break

            # check if the movement is right or up (+) or left or down (-)
            if i[1] == "+":
                move = int(i[2])
            else:
                move = -int(i[2])
            # change the state of the board in the dictionary
            dict_copy[car.name[0]] += move

            # execute the move
            CAR.move3(move)

        # build the board after all the moves are executed
        self.rush_hour.board = Board.build(
            1, self.rush_hour.board.width_height + 1, self.rush_hour.cars)
        # check all possible moves for each car
        for car in self.rush_hour.cars:
            car.moveability(self.rush_hour.board)

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
                #     dict_copy2 = copy.deepcopy(dict_copy)
                #     dict_copy2[car.name[0]] += -i

                #     # make a string of the dictionary
                #     x = str(dict_copy2)

                #     # check if the current set of moves leads to a board that has not been visited
                #     if x not in moves_set:
                #         # if unique, add to the queue and the set with all the visited boards
                #         queue.append(scopy)
                #         moves_set.add(x)

                scopy = copy.deepcopy(s)

                # append the new move
                scopy.append(car.name[0] + "-" + str(car.moveability_list[0]))

                # copy and update the dictionary with the netto car positions
                dict_copy2 = copy.deepcopy(dict_copy)
                dict_copy2[car.name[0]] += -car.moveability_list[0]

                # make a string of the dictionary
                x = str(dict_copy2)

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
                #     dict_copy2 = copy.deepcopy(dict_copy)
                #     dict_copy2[car.name[0]] += i

                #     # make a string of the dictionary
                #     x = str(dict_copy2)

                #     # check if the current set of moves leads to a board that has not been visited
                #     if x not in moves_set:
                #         # if unique, add to the queue and the set with all the visited boards
                #         queue.append(scopy)
                #         moves_set.add(x)

                scopy = copy.deepcopy(s)

                # append the new move
                scopy.append(car.name[0] + "+" + str(car.moveability_list[1]))

                # copy and update the dictionary with the netto car positions
                dict_copy2 = copy.deepcopy(dict_copy)
                dict_copy2[car.name[0]] += car.moveability_list[1]

                # make a string of the dictionary
                x = str(dict_copy2)

                # check if the current set of moves leads to a board that has not been visited
                if x not in moves_set:
                    # if unique, add to the queue and the set with all the visited boards
                    queue.append(scopy)
                    moves_set.add(x)

    # implementation of a breadthfirst search method
    def breadth_first(self):

        # set needed variables
        start = time.time()
        queue = []
        car_list = []
        n = 0

        # find first moveable options and place them in the queue
        for car in self.rush_hour.cars:

            # check which cars are moveable
            car.moveability(self.rush_hour.board)

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

                queue.append([car.name[0] + "+" + str(car.moveability_list[1])])
        # print(queue)
        # set needed for pre pruning which contains all visited boards.
        moves_set = set()

        # make a dictionary with all the cars, which is used later.
        cars_dictionary = {}
        for car in self.rush_hour.cars:
            cars_dictionary[car.name[0]] = 0

        # append dictionary to set and list. it is added as a string to the set so it can be hashed.
        moves_set.add(str(cars_dictionary))

        # find the initial position of the red car and make an object redcar
        for car in self.rush_hour.cars:
            if car.name[0] == "r":
                red_car_position_inital = copy.deepcopy(car.col)

        # go on till solution is found or queue is empty
        while queue:

            # set everything to the initiak state
            self.rush_hour.board = copy.deepcopy(self.initial_board)
            self.rush_hour.cars = copy.deepcopy(self.initial_cars)

            # make a copy of the "standard" car dictionary
            dict_copy = copy.deepcopy(cars_dictionary)

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
                car_name = i[0]

                # set CAR to the car that is in the move command
                for car in self.rush_hour.cars:
                    if car.name[0] == car_name:
                        CAR = car
                        break

                # check if the movement is right or up (+) or left or down (-)
                if i[1] == "+":
                    move = int(i[2])
                else:
                    move = -int(i[2])
                # change the state of the board in the dictionary
                dict_copy[car.name[0]] += move

                # execute the move
                CAR.move3(move)

            # build the board after all the moves are executed
            self.rush_hour.board = Board.build(
                1, self.rush_hour.board.width_height + 1, self.rush_hour.cars)

            # create an object for the red car, named redcar
            for car in self.rush_hour.cars:
                if car.red_car:
                    redcar = car

            # check if a solution is found
            if redcar.col == self.rush_hour.board.width_height-1:
                print(s)
                print("Gewonnen!")
                end = time.time()
                print(f"time is {end - start}")
                print(self.rush_hour.board)
                print(len(s))
                return True
                break

            # check all possible moves for each car
            for car in self.rush_hour.cars:
                car.moveability(self.rush_hour.board)

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
                    #     dict_copy2 = copy.deepcopy(dict_copy)
                    #     dict_copy2[car.name[0]] += -i

                    #     # make a string of the dictionary
                    #     x = str(dict_copy2)

                    #     # check if the current set of moves leads to a board that has not been visited
                    #     if x not in moves_set:
                    #         # if unique, add to the queue and the set with all the visited boards
                    #         queue.append(scopy)
                    #         moves_set.add(x)

                    scopy = copy.deepcopy(s)

                    # append the new move
                    scopy.append(car.name[0] + "-" + str(car.moveability_list[0]))

                    # copy and update the dictionary with the netto car positions
                    dict_copy2 = copy.deepcopy(dict_copy)
                    dict_copy2[car.name[0]] += -car.moveability_list[0]

                    # make a string of the dictionary
                    x = str(dict_copy2)

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
                    #     dict_copy2 = copy.deepcopy(dict_copy)
                    #     dict_copy2[car.name[0]] += i

                    #     # make a string of the dictionary
                    #     x = str(dict_copy2)

                    #     # check if the current set of moves leads to a board that has not been visited
                    #     if x not in moves_set:
                    #         # if unique, add to the queue and the set with all the visited boards
                    #         queue.append(scopy)
                    #         moves_set.add(x)

                    scopy = copy.deepcopy(s)

                    # append the new move
                    scopy.append(car.name[0] + "+" + str(car.moveability_list[1]))

                    # copy and update the dictionary with the netto car positions
                    dict_copy2 = copy.deepcopy(dict_copy)
                    dict_copy2[car.name[0]] += car.moveability_list[1]

                    # make a string of the dictionary
                    x = str(dict_copy2)

                    # check if the current set of moves leads to a board that has not been visited
                    if x not in moves_set:
                        # if unique, add to the queue and the set with all the visited boards
                        queue.append(scopy)
                        moves_set.add(x)
            # print the ammount of visited boards.
            # print(len(moves_set))
            # print(self.rush_hour.board)
