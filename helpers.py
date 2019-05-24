from car import Car
from board import Board
import bruteforce
import copy
import random

"""
The board where the game takes place.
The game is represented by a grid with different chars in it, which represent the cars.
"""
# def __init__():


def build(size, cars):
    board_positions = []
    row = []
    # construct an empty board
    for i in range(0, size):
        row.append("x")
    for i in range(0, size):
        board_positions.append(copy.copy(row))

    # place the cars on the board
    for car in cars:
        # print(car.name)
        # print(car.row)
        # print(car.col)
        # check the orientation of the car
        if car.direction == "horizontal":
            # change the x's to the car letter.
            for i in range(0, car.size):
                board_positions[car.row][car.col + i] = car.name[0]

        # same for vertical cars
        else:
            for i in range(int(car.size)):
                board_positions[car.row + i][car.col] = car.name[0]
    # make a new board object
    board = Board(size-1, board_positions, (size)/2-1)
    # return the board object
    return(board)


def create_random_board(size, number_of_size2_cars, number_of_size3_cars):

    if number_of_size2_cars * 2 + number_of_size3_cars * 3 >= size*size:
        print("the cars do not fit on the desired board")
        return False
    carlist = []
    alphabet = []
    for letter in range(65, 91):
        alphabet.append(chr(letter))
    allowed = ['!', '@', '#', '$', '%', '^', '&', '*', '/',
               '.', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    alphabet.extend(allowed)

    # place red car

    red_car_height = int(round(size / 2 - 1))

    red_car = Car("rr", red_car_height, size-2, 0, 2, True)
    carlist.append(red_car)
    print(alphabet)
    counter = 0

    for i in range(0, number_of_size2_cars + number_of_size3_cars):

        if number_of_size2_cars <= 0:
            car_size = 3
        elif number_of_size3_cars <= 0:
            car_size = 2
        else:
            car_size = random.randint(2, 3)

        if car_size == 2:
            number_of_size2_cars + - 1
        else:
            number_of_size3_cars + - 1

        placed = False

        # print(alphabet[counter]*2)
        board = build(size, carlist)
        while placed == False:
            valid = True
            orientation = random.randint(0, 1)
            if orientation == 0:
                column = random.randint(0, size-car_size)
                row = random.randint(0, size-1)

                while row == int(round(size / 2 - 1)):
                    row = random.randint(0, size-1)
            else:
                column = random.randint(0, size-1)
                row = random.randint(0, size-car_size)
            if orientation == 0:
                for n in range(0, car_size):
                    if board.positions[row][column + n] is not "x":
                        valid = False

            else:
                for n in range(0, car_size):
                    # print (row+n)
                    if board.positions[row+n][column] is not "x":
                        valid = False
            if valid == False:
                continue

            car_object = Car(alphabet[counter]*2, row, column, orientation, car_size, False)
            carlist.append(car_object)
            counter += 1
            placed = True

    board = build(size, carlist)
    bruteforce.randommover2(board, carlist, 200000)
    return board
