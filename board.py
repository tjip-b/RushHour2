from car import Car
import copy
class Board():
    """
    The board where the game takes place.
    The game is represented by a grid with different chars in it, which represent the cars.
    """
    def __init__(self, width_height, positions, exit_position, empty):       
        # width and height are always the same (starts counting from 0!)
        self.width_height = width_height
        
        # represents the positions of all cars: [[],[]]
        self.positions = positions
        
        # if redcar.y hits the exit positions y position, the game is over.
        self.exit_position = exit_position   

        # list of all the cars in the grid
        self.cars = []

        self.empty = empty
        

    def bounds(self, pos):
        """ Checks if in bounds
        """

    def passable(self, pos):
        """ Checks if passable
        """
        return pos not in self.cars

    

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

    # builds a board, based on the size of the board and the cars whcih are given as input
    def build(self, size, cars):
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
        board = Board(size-1, board_positions, (size)/2-1, 0)  
        
        # return the board object
        return(board)