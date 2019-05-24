from board import Board
from car import Car
import helpers
import copy
import time
import random


class Algorithm():
    """
    This class contains all the used algarithms to solve Rush Hour.
    """

    def __init__(self, rush_hour):
        self.rush_hour = rush_hour

    def check_if_won(self):
        """
        Checks if the board is solved.
        """
        # Create an object for the red car, named red_car
        for car in self.rush_hour.cars:
            if car.name[0] == "r":
                red_car = car

        # Check if a solution is found
        if red_car.col == self.rush_hour.board.width_height-1:
            print(self.rush_hour.board)
            return True
        else:
            return False

    def moves_list(self, max_movement):
        """
        This function makes a list with the cars that are moveable.
        """
        moveable_cars = []
        # Loops through all the cars
        if max_movement == True:
            for car in self.rush_hour.cars:
                car.moveability(self.rush_hour.board)

                # Append car if moveable to list
                if car.moveability_list[0] is not 0:
                    move = car.name[0] + "-" + str(car.moveability_list[0])
                    moveable_cars.append(move)

                if car.moveability_list[1] is not 0:
                    move = car.name[0] + "+" + str(car.moveability_list[1])
                    moveable_cars.append(move)
        else:
            for car in self.rush_hour.cars:
                car.moveability(self.rush_hour.board)

                # Append car if moveable to list
                if car.moveability_list[0] is not 0:
                    for i in range(0, car.moveability_list[0]):
                        move = car.name[0] + "-" + str(i + 1)
                        moveable_cars.append(move)

                if car.moveability_list[1] is not 0:
                    for i in range(0, car.moveability_list[1]):
                        move = car.name[0] + "+" + str(i + 1)
                        moveable_cars.append(move)

        return moveable_cars

    def execute_move_command(self, command):
        """
        Executes a movement given as input (command).
        """
        CAR = None
        carname = command[0]

        # Set CAR to the car that is in the move command
        for car in self.rush_hour.cars:
            if car.name[0] == carname:
                CAR = car
                break

        # Check if the movement is right or up (+) or left or down (-)
        if command[1] == "+":
            move = int(command[2])
        else:
            move = -int(command[2])

        # Execute the move
        CAR.move3(move)
        return move

    def depth_first(self, depth, depth_pruning, max_movement):
        """
        Implementation of the depth first search algorithm for
        the rush hour game. Takes a max depth limit as parameter.
        Also takes a bool for the pruning method:
        True = maximal pruning: prune every child which has a visited board
        Flase = depth pruning: prune every child which has a visited board and
        a higher depth level than the previous board with the same positions.
        """

        # Set needed variables
        start = time.time()
        stack = []
        # Current search depth
        current_depth = -1
        # Maximum depth, devines nodes at this depth as leaves
        max_depth = depth
        # Amount of nodes
        n = 0

        # Make archive set or dict depending on pruning method
        if depth_pruning:
            # Dict needed for pruning which contains all visited boards
            archive = {}
        else:
            archive = set()
        # Dictionary with all netto car movements (equivalent to board.positions)
        cars_dictionary = {}

        # Find first moveable options and place them in the queue
        move_list = self.moves_list(max_movement)

        for move in move_list:
            stack.append([move])

        # Make a dictionary with all the cars, which is used later.
        for car in self.rush_hour.cars:
            cars_dictionary[car.name[0]] = 0

        if depth_pruning:
            # Start netto movement positions (equivalent to start board)
            # added to archive
            archive[str(cars_dictionary)] = 0
        else:
            # Append dictionary to set and list
            # It is added as a string to the set so it can be hashed.
            archive.add(str(cars_dictionary))

        while stack:
            # Set everything to the initial state
            self.rush_hour.board = copy.deepcopy(self.rush_hour.initial_board)
            self.rush_hour.cars = copy.deepcopy(self.rush_hour.initial_cars)

            # Make a copy of the "standard" car dictionary
            dict_copy = copy.deepcopy(cars_dictionary)

            # Take the first item from the stack and pop it.
            moves_list = stack.pop()

            # Print in which iteration we are and the current movelist
            print(f"n = {n}")
            n += 1

            # Check current tree depth
            current_depth = len(moves_list)
            if current_depth > max_depth:
                continue

            # Iterate through the move commands in s
            for move_string in moves_list:
                movement = self.execute_move_command(move_string)
                dict_copy[move_string[0]] += movement

            # Build the board after all the moves are executed
            self.rush_hour.board = helpers.build(
                self.rush_hour.board.width_height + 1,
                copy.deepcopy(self.rush_hour.cars))

            # Check if a solution is found
            if self.check_if_won() == True:
                print(moves_list)
                print("Gewonnen!")
                end = time.time()
                print(f"time is {end - start}")
                print(f"n = {n}")
                print(self.rush_hour.board)
                print(f"amount of moves / depth: {len(moves_list)}")
                return True

            if depth_pruning:
                # Add netto movements (equivalent to positions on the board)
                # to archive
                archive[(str(dict_copy))] = len(moves_list)

            # Make all possible moves
            move_list = self.moves_list(max_movement)

            # Make children for all possible movements
            for move in move_list:

                # Copy the moves that led to the present board
                scopy = copy.deepcopy(moves_list)

                # Append the new move
                scopy.append(move)

                # Copy and update the dictionary with the netto car positions
                dict_copy2 = copy.deepcopy(dict_copy)
                if move[1] == "-":
                    dict_copy2[move[0]] += -int(move[2])
                else:
                    dict_copy2[move[0]] += int(move[2])

                # String version of the netto moves dictionary
                # (equivalent to board.positions)
                current_netto_moves = str(dict_copy2)

                # Select type of pruning method
                if depth_pruning:
                    # Check if the current set of moves leads to a board
                    # that has not been visited
                    if current_netto_moves not in archive:
                        # If unique, add to the queue and the set
                        # with all the visited boards
                        stack.append(scopy)
                    else:
                        move_length = archive[str(current_netto_moves)]
                        if len(scopy) < move_length:
                            stack.append(scopy)
                            archive[str(current_netto_moves)] = move_length
                else:
                    # Check if the current set of moves leads to
                    # a board that has not been visited
                    if current_netto_moves not in archive:
                        # If unique, add to the queue and
                        # the set with all the visited boards
                        stack.append(scopy)
                        archive.add(current_netto_moves)

    def breadth_first(self, max_movement, breadth):
        """
        Implementation of the breadth first search algorithm for
        the rush hour game. Takes max_movement and breadth as input
        if max_movement is True, only the maximum possible moves are
        added, and if breadth > 0, the number of newly added boards from
        a board is limited to the number inputted as breadth
        """
        nodes_at_treelevel = []
        node_counter = 0
        len_s = 0
        start = time.time()
        self.initialboard = copy.deepcopy(self.rush_hour.initial_board)
        self.initialcars = copy.deepcopy(self.rush_hour.initial_cars)
        queue = []
        n = 0

        # Find first moveable options and place them in the queue
        move_list = self.moves_list(max_movement)

        for move in move_list:
            queue.append([move])

        # Set needed for pre pruning which contains all visited boards
        archive = set()

        # Make a dictionary with all the cars, which is used later
        cars_dictionary = {}
        for car in self.rush_hour.cars:
            cars_dictionary[car.name[0]] = 0

        # Append dictionary to set and list
        # It is added as a string to the set so it can be hashed
        archive.add(str(cars_dictionary))

        # Go on till solution is found or queue is empty
        while queue:
            # Uses different counters deppending on the version of breadth first
            counter = 0
            node_counter += 1

            # Set everything to the initial state
            self.rush_hour.board = copy.deepcopy(self.rush_hour.initial_board)
            self.rush_hour.cars = copy.deepcopy(self.rush_hour.initial_cars)

            # Make a copy of the "standard" car dictionary
            dict_copy = copy.deepcopy(cars_dictionary)

            # Take the first item from the queue and pop it
            moves_list = queue.pop(0)

            # Gets the amount of nodes per depth level
            if len(moves_list) == len_s + 1:
                nodes_at_treelevel.append(node_counter)
                node_counter = 0
                len_s = len(moves_list)

            # Iterate through the move commands in s
            for i in moves_list:
                move = self.execute_move_command(i)
                dict_copy[i[0]] += move

            # Build the board after all the moves are executed
            self.rush_hour.board = helpers.build(
                self.rush_hour.board.width_height + 1, self.rush_hour.cars)

            # Check if a solution is found
            if self.check_if_won() == True:
                print(moves_list)
                print("Gewonnen!")
                end = time.time()
                print(f"time is {end - start}")
                print(f"n = {sum(nodes_at_treelevel)}")
                print(self.rush_hour.board)
                return nodes_at_treelevel

            # Make all possible moves
            move_list = self.moves_list(max_movement)

            # Two versions of breadth first branch off here
            if breadth > 0:
                # While counter <= breadth:
                for i in range(0, 1000000):

                    if counter >= breadth:
                        move_list.clear()
                        break
                    try:
                        move = random.choice(move_list)
                    except IndexError:
                        break

                    scopy = copy.deepcopy(moves_list)

                    # Append the new move
                    scopy.append(move)
                    dict_copy2 = copy.deepcopy(dict_copy)
                    # Copy and update the dictionary with the netto car positions
                    if move[1] == "-":
                        dict_copy2[move[0]] += -int(move[2])
                    else:
                        dict_copy2[move[0]] += int(move[2])

                    # Make a string of the dictionary
                    dict_string = str(dict_copy2)

                    # Check if the current set of moves leads to a board
                    # that has not been visited
                    if dict_string not in archive:
                        # If unique, add to the queue and the set
                        # with all the visited boards
                        queue.append(scopy)
                        archive.add(dict_string)
                        move_list.remove(move)
                        counter += 1
                    else:
                        move_list.remove(move)

            else:
                for move in move_list:

                    # Copy the moves that led to the present board
                    scopy = copy.deepcopy(moves_list)

                    # Append the new move
                    scopy.append(move)

                    # Copy and update the dictionary with the netto car positions
                    dict_copy2 = copy.deepcopy(dict_copy)
                    if move[1] == "-":
                        dict_copy2[move[0]] += -int(move[2])
                    else:
                        dict_copy2[move[0]] += int(move[2])

                    # Make a string of the dictionary
                    dict_string = str(dict_copy2)

                    # Check if the current set of moves leads to a board
                    # that has not been visited
                    if dict_string not in archive:
                        # If unique, add to the queue
                        # and the set with all the visited boards
                        queue.append(scopy)
                        archive.add(dict_string)

    def depth_random(self, depth):
        """
        Random searches for a solution till a given depth. Returns the solution.
        """

        # Set needed variables
        start = time.time()
        n = 0

        # Make a list with moveable cars
        moveable_cars = self.moves_list(depth)

        # Pick a random move
        move = random.choice(moveable_cars)

        # Make a set that contains all visited boards
        archive = set()

        # Make a dictionary that contains all cars with their netto movement
        cars_dictionary = {}
        for car in self.rush_hour.cars:
            cars_dictionary[car.name[0]] = 0

        # Append dictionary to set. it is added as a string
        # to the set so it can be hashed.
        archive.add(str(cars_dictionary))

        # Make a list that will contain all executed moves
        moves_list = []

        while n < depth:
            n += 1

            # Execute move and save it in the dictionary
            self.execute_move_command(move)
            if move[1] == "+":
                movement = int(move[2])
            else:
                movement = -int(move[2])

            cars_dictionary[move[0]] += movement

            # Save all done moves
            moves_list.append(move)

            # Build the board
            self.rush_hour.board = helpers.build(
                self.rush_hour.board.width_height + 1, self.rush_hour.cars)

            if self.check_if_won() == True:
                print(moves_list)
                print("Gewonnen!")
                end = time.time()
                print(f"time is {end - start}")
                print(f"n = {n}")
                print(self.rush_hour.board)
                return moves_list

            # Check all possible moves for each car and add them to a list
            moveable_cars = self.moves_list(True)

            # Return
            for i in range(0, 1000000):
                try:
                    move = random.choice(moveable_cars)

                # If no moves, return False
                except IndexError:
                    print("geen zetten meer!")
                    return False

                # Copy and update the dictionary with the netto car positions
                dict_copy = copy.deepcopy(cars_dictionary)
                if move[1] == "+":
                    movement = int(move[2])
                else:
                    movement = -int(move[2])
                dict_copy[move[0]] += movement

                # Make a string of the dictionary
                dict_string = str(dict_copy)

                # Check if the current set of moves leads to a board
                # that has not been visited
                if dict_string not in archive:
                    archive.add(dict_string)
                    # print(move)
                    break

                # If not, remove the car from moveable cars
                else:
                    moveable_cars.remove(move)
        print("geen oplossing")
        return moves_list

    def find_solution(self, maximum_depth):
        """
        Runs Depth random until it finds a solution
        with a depth lower than maximum depth.
        """
        rush_hour_copy = copy.deepcopy(self.rush_hour)
        depth = maximum_depth + 1
        while depth > maximum_depth:
            self.rush_hour = copy.deepcopy(rush_hour_copy)
            solution = self.depth_random(depth)
            if solution is not False:
                depth = len(solution)
            print(f"The current depth = {depth}")
        return solution

    def optimalize_solution(self, maximum_depth, move_list):
        """
        Takes a solution as input,
        given by move_list and tries to shorten this solution.
        """

        rush_hour_copy = copy.deepcopy(self.rush_hour)
        List = move_list

        # Iterate till asked depth is reached
        while len(List) > maximum_depth:

            # We search half the length of the given tree
            search_length = int(len(List)/2)

            # Print the list in case anybody wants to quit the algorithm
            # before it is finished
            print(f"the length of the list = {len(List)}")
            print(List)

            self.rush_hour = copy.deepcopy(rush_hour_copy)

            # Take half of the given move list
            List = List[0:len(List)-search_length]

            # Execute half
            for move in List:
                self.execute_move_command(move)

            # Build the board after all the moves are executed
            self.rush_hour.board = helpers.build(
                self.rush_hour.board.width_height + 1, self.rush_hour.cars)

            board_copy = copy.deepcopy(self.rush_hour)

            # Set depth to search length
            depth = search_length

            while depth > search_length - 1:
                bf = copy.deepcopy(Algorithm(board_copy))
                moves_list = bf.depth_random(depth)
                if moves_list is not False:
                    depth = len(moves_list)
            List.extend(moves_list)

        # If desired depth is found, return moves.
        return List

    def find_optimised_solution(self, max_1, max_2):
        """
        Finds a solution and optimalises it.
        The max_1 is the depth limit till which find_solution searches,
        max_2 is the depth limit till which it is optimised.
        """
        rush_hour_copy = copy.deepcopy(self)
        List = self.find_solution(max_1)
        self = copy.deepcopy(rush_hour_copy)
        optimised_list = self.optimalize_solution(max_2, List)
        return optimised_list
