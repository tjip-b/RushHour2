from car import Car
from board import Board
import copy
import random
import algorithms
      

def build(size, cars):
    """
    algorithm that builds a board, given the size of the board and the location of the cars
    """
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
        if car.direction == 0:

            # change the x's to the car letter.
            for i in range(0, car.size):
                board_positions[car.row][car.col + i] = car.name[0]  
        
        # same for vertical cars
        else:
            for i in range (int(car.size)):
                board_positions[car.row + i][car.col] = car.name[0]
    # make a new board object
    board = Board(size-1, board_positions, (size)/2-1)       
    # return the board object
    return(board)


def moves_list(board, cars):
        """
        This function makes a list with the cars that are moveable.
        """
        moveable_cars = []
        # Loops through all the cars
       
        for car in cars:
            car.moveability(board)

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

def create_random_board(size, number_of_size2_cars, number_of_size3_cars):
    """
    algorithm that creates a random board, with the redcar next to the exit to guarantee there is a solution,
    and makes afterwards 50000 moves to hussle the board
    """
    # check if it is theoretically possible to fit all the cars
    if number_of_size2_cars * 2 + number_of_size3_cars * 3 >= size*size:
        print("the cars do not fit on the desired board")
        return False
    
    # make the needed variables
    carlist = []
    alphabet = []
    counter = 0
    
    # construct allowed characters
    for letter in range(65, 91):
        alphabet.append(chr(letter))
    allowed = ['!', '@', '#', '$', '%', '^', '&', '*', '/', '.', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    alphabet.extend(allowed)    
    
    # calculate where the redcar goes and make the red car
    red_car_height = int(round(size / 2 - 1))
    red_car = Car("rr", red_car_height, size-2, 0, 2, True)
    carlist.append(red_car)

    # place all cars
    for i in range (0, number_of_size2_cars + number_of_size3_cars):
        
        # if there are still cars of both types left, choose random
        if number_of_size2_cars <= 0:
            car_size = 3
        elif number_of_size3_cars <= 0:
            car_size = 2
        else:    
            car_size = random.randint(2,3)

        # update the ammount of cars left to place
        if car_size == 2:
            number_of_size2_cars +- 1
        else:
            number_of_size3_cars +- 1

        # check if car is placed
        placed = False
        
        # build the board
        board = build(size, carlist)

        # try to place the car
        while placed == False:
            valid = True

            # choose a random place, but not in the same row as the red car
            orientation = random.randint(0, 1)
            if orientation == 0:
                column = random.randint(0, size-car_size)
                row = random.randint(0, size-1)

                while row == int(round(size / 2 - 1)):
                    row = random.randint(0, size-1)

            # choose a random place
            else:
                column = random.randint(0, size-1)
                row = random.randint(0, size-car_size)

            # check if the location is valid
            if orientation == 0:
                for n in range(0, car_size):
                    if board.positions[row][column + n] is not "x":
                        valid = False
            
            else:
                for n in range(0, car_size):
                    # print (row+n)
                    if board.positions[row+n][column] is not "x":
                        valid = False

            # if the place was invalid, check again
            if valid == False:
                continue
            
            # if it was valid, make the car object
            car_object = Car(alphabet[counter]*2, row, column, orientation, car_size, False)
            carlist.append(car_object)
            counter += 1
            placed = True

    # build the completed board
    board = build(size, carlist)
    
    # random move the board 50000 times
    for i in range (0, 50000):
        
        # pick a random move
        move_list = moves_list(board, carlist)
        move = random.choice(move_list)

        # bias for the red car to go to the left
        if move[0] == "r" and move[1] == "+":
            if random.randint(0,8) > 1:
                continue
        # move the car
        for car in carlist:
            if move[0] == car.name[0]:
                if move[1] == "+":
                    car.move3(int(move[2]))
                else:
                    car.move3(-int(move[2]))

        # build the board after the move
        board = build(size, carlist)
        
    return board