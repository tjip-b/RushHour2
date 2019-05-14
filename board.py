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
        
    def make_children2(self):
        returnlist = []
        for car in self.cars:
            car.moveability(self)
            # horiontal
            if car.direction.startswith("h"):
                if car.moveability_list[0] is not 0:
                    for i in range(0, car.moveability_list[0]):
                        print(i)
                        car.move3(i + 1)
                        boardy = self.build(self.width_height + 1, self.cars)
                        print(boardy)
                        returnlist.append(boardy)
                if car.moveability_list[1] is not 0:
                    for i in range(0, car.moveability_list[0]):
                        print(i)
                        car.move3(i + 1)
                        boardy = self.build(self.width_height, self.cars)
                        print(boardy)
                        returnlist.append(boardy)
                
            # vertical
            else: 
                if car.moveability_list[0] is not 0:
                    pass
                if car.moveability_list[1] is not 0:
                    pass

    def make_children(self):
        """ Makes all possible child moves.
            Returns list of child boards
        """
        returnlist = []
        for j, car in enumerate(self.cars):
            car.moveability(self)
            boardcopy = copy.deepcopy(self)
            if car.direction == "horizontal":
                if car.moveability_list[0] is not 0:
                    # left
                    for i in range(0, car.moveability_list[0]):
                        print(car.name)
                        current = -abs(i)
                        boardcopy = car.move4(boardcopy, current - 1)
                        returnlist.append(copy.deepcopy(boardcopy))
                        

                if car.moveability_list[1] is not 0:
                    # right
                    for i in range(0, car.moveability_list[0]):
                        car.move4(boardcopy, i + 1)
                        returnlist.append(copy.deepcopy(boardcopy))
            else:
                # check for double moveables
                if car.moveability_list[0] is not 0 and car.moveability_list[1] is not 0:
                    print("hello")
                    doublecopy = copy.deepcopy(boardcopy)
                    # up
                    print(car.moveability_list[0])
                    for i in range(0, car.moveability_list[0]):
                        current = -abs(i)
                        car.move4(doublecopy, current - 1)
                        returnlist.append(copy.deepcopy(doublecopy))
                    triplecopy = copy.deepcopy(boardcopy)
                    print("damn")
                    print(triplecopy)
                    # down
                    for i in range(0, car.moveability_list[1]):
                        car.move4(boardcopy, i + 1)
                        returnlist.append(copy.deepcopy(boardcopy))
                        print("triplecopy")
                        print(boardcopy)
                    continue

                if car.moveability_list[0] is not 0:
                    # up
                    for i in range(0, car.moveability_list[0]):
                        current = -abs(i)
                        car.move4(boardcopy, current - 1)
                        returnlist.append(copy.deepcopy(boardcopy))
                if car.moveability_list[1] is not 0:
                    # down
                    for i in range(0, car.moveability_list[1]):
                        car.move4(boardcopy, i + 1)
                        returnlist.append(copy.deepcopy(boardcopy))
                        
        return returnlist

    def build(self, size, cars):
        """ 
        builds a board, based on the size of the board and the cars whcih are given as input
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

    
