from car import Car

class Board():
    """
    The board where the game takes place.
    The game is represented by a grid with different chars in it, which represent the cars.
    """
    def __init__(self, width_height, positions, exit_position):
        # width and height are always the same (starts counting from 0!)
        self.width_height = width_height

        # represents the positions of all cars: [[],[]]
        self.positions = positions
        
        # if red car hits the exit position, the game is over: 2.5
        self.exit_position = exit_position

        # list of all the cars in the grid
        self.cars = []


    def bounds(self, pos):
        """ Checks if in bounds
        """

    def passable(self, pos):
        """ Checks if passable
        """
        return pos not in self.cars


    def load_board(self, filename):
        # loadboard = [[],[]]
        loadboard = []
        redCarPosition = []
        exitPosition = ""
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

                        # red car position (example: [2.4, 2.5])
                        elif char == "r":
                            redCarPosition.append(str(i) + "." + str(j))
                            row.append(char)

                        # finish position
                        elif char == "e":
                            exitPosition = str(i) + "." + str(j - 1)
                loadboard.append(row)
            # initialize board
            board = Board(i, loadboard, exitPosition)
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
                                    position = [str(i) + "." + str(j), str(i) + "." + str(j + 1), str(i) + "." + str(j + 2)]
                                    car = Car(char * 3, position, "horizontal", 3, False)
                                    cars.append(car)
                                    continue
                                # add 'x' at end of list just to be sure index error wont occur
                                position = [str(i) + "." + str(j), str(i) + "." + str(j + 1)] # removed x
                                car = Car(char * 2, position, "horizontal", 2, False)
                                cars.append(car)
                            # car found, but not a 3 tile car
                            except IndexError:
                                position = [str(i) + "." + str(j), str(i) + "." + str(j + 1)] # removed x
                                car = Car(char * 2, position, "horizontal", 2, False)
                                cars.append(car)
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
                                    position = [str(i) + "." + str(j), str(i + 1) + "." + str(j), str(i + 2) + "." + str(j)]
                                    car = Car(char * 3, position, "vertical", 3, False)
                                    cars.append(car)
                                    continue
                                position = [str(i) + "." + str(j), str(i + 1) + "." + str(j)] # removed x
                                car = Car(char * 2, position, "vertical", 2, False)
                                cars.append(car)
                            except IndexError:
                                position = [str(i) + "." + str(j), str(i + 1) + "." + str(j)] # removed x
                                car = Car(char * 2, position, "vertical", 2, False)
                                cars.append(car)
                                continue
                    except IndexError:
                        continue
                elif char == "r" and char not in taken_cars:
                    position = [str(i) + "." + str(j), str(i) + "." + str(j + 1)] # removed x
                    redcar = Car("redCar", position, "horizontal", 2, True)
                    taken_cars.append(char)
                    cars.append(redcar)
        self.board.cars = cars
        return cars

    def __str__(self):
        """ Print out board in readable strings
        """
        allowed = ['!', '@', '#', '$', '%', '^', '&', '*', '/', '.', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        returnstring = ""
        for row in self.positions:
            for char in row:
                if char.isupper() or char == 'r' or char in allowed:
                    returnstring += "| " + char + " "
                else:
                    returnstring += "| " + "_" + " "
            returnstring += "\n"
        return returnstring
