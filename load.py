from board import Board
from car import Car

class Load():

    # def __init__ (self, filename):
    #     pass
        
    def load_board(self, filename):
        """
        initialize a Board object from the filename
        """
        # loadboard = [[],[]]
        loadboard = []
        redCarPosition = []
        exitPosition = 0
        empty = []
        allowed = ['!', '@', '#', '$', '%', '^', '&', '*', '/', '.', 'x', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        with open(filename, "r") as f:
            # still have lines to load in
            for i, line in enumerate(f):
                row = []
                if not line == "\n":
                    line.strip('\n')
                    for j, char in enumerate(line):
                        
                        # still have chars to add to array
                        
                        # add car positions 
                        if char.isupper() or char in allowed:
                            row.append(char)

                        # red car position (example: [2.4, 2.5]) ~~ can be deleted
                        elif char == "r":
                            redCarPosition.append(str(i) + "." + str(j))
                            row.append(char)

                        # finish y position
                        elif char == "e":
                            exitPosition = j - 1
                        
                        
                        if char == "x":
                            empty.append([j, i])
                        
                loadboard.append(row)
            # initialize board
            board = Board(i, loadboard, exitPosition, empty)
            # print(loadboard)
            return board
    
    def load_cars(self):
        """
        Searches all cars on the grid, creates car objects, append to list
        """
        positions = self.board.positions
        # letters of cars which are already taken
        taken_cars = []
        # list of car objects
        cars = []
        # list of allowed car chars
        allowed = ['!', '@', '#', '$', '%', '^', '&', '*', '/', '.', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        number = 1
        # 
        for i, row in enumerate(positions):
            for j, char in enumerate(row):
                # check for red car (which is always horizontal and of size 2)
                if (char.isupper() or char in allowed) and char not in taken_cars:
                    # trying to find a horizontal car
                    try:
                        if positions[i][j + 1] == char:
                            taken_cars.append(char)
                            # check for third 'block'
                            try:
                                if positions[i][j + 2] == char:
                                    # x = i -- y = j
                                    car = Car(char * 3, i, j, 0, 3, False, number)
                                    
                                    car.moveability(self.board)
                            
                                    cars.append(car)
                                    number += 1
                                    continue
                                # add 'x' at end of list just to be sure index error wont occur 
                                car = Car(char * 2, i, j, 0, 2, False, number)
                                car.moveability(self.board)
                                cars.append(car)
                                number += 1
                            # car found, but not a 3 tile car
                            except IndexError:
                                car = Car(char * 2, i, j, 0, 2, False, number)
                                car.moveability(self.board)
                                cars.append(car)
                                number += 1
                                continue
                    # no car found
                    except IndexError:
                        pass

                    # trying to find a vertical car
                    try:
                        if positions[i + 1][j] == char:
                            taken_cars.append(char)
                            try:
                                if positions[i + 2][j] == char:
                                    car = Car(char * 3, i, j, 1, 3, False, number)
                                    car.moveability(self.board)
                                    cars.append(car)
                                    number += 1
                                    continue
                                car = Car(char * 2, i, j, 1, 2, False, number)
                                car.moveability(self.board)
                                cars.append(car)
                                number += 1
                            except IndexError:
                                car = Car(char * 2, i, j, 1, 2, False, number)
                                car.moveability(self.board)
                                cars.append(car)
                                number += 1
                                continue
                    except IndexError:
                        continue
                elif char == "r" and char not in taken_cars:
                    redcar = Car("redCar", i, j, 0, 2, True, number)
                    redcar.moveability(self.board)
                    taken_cars.append(char)
                    cars.append(redcar)
                    number += 1        
        self.board.cars = cars
        return cars