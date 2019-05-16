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
        """ Makes all possible moves from a certain 
            positions on the board and returns a list 
            of all those child boards
        """
        returnlist = []
        for j, car in enumerate(self.cars):
            # movement possibilities of the car is based on the moveability_list
            car.moveability(self)
            # start over with a fresh board for every new car
            boardcopy = copy.deepcopy(self)

            # remember car starting positions for next iteration
            car_col = car.col
            car_row = car.row
            rowrow = car_row
            

            if car.name == "AA":
                print(f"ROWROW: {rowrow}")
                print(f"CAR AA 1ROW: {car.row}")
            
            if car.direction == "horizontal":
                # check for double moveables
                if car.moveability_list[0] is not 0 and car.moveability_list[1] is not 0:
                    # make copy and remember row position
                    doublecopy = copy.deepcopy(boardcopy)
                    col_save = car.col

                    # create all possible leftward positions
                    for i in range(0, car.moveability_list[0]):
                        current = -abs(i)
                        car.move4(boardcopy, current - 1)
                        boardcopy.cars[j].col = car.col
                        returnlist.append(copy.deepcopy(boardcopy))
                    
                    # create all possible rightward positions from copy
                    car.col = col_save
                    for i in range(0, car.moveability_list[1]):
                        car.move4(doublecopy, i + 1)
                        doublecopy.cars[j].col = car.col
                        returnlist.append(copy.deepcopy(doublecopy))
                    continue

                if car.moveability_list[0] is not 0:
                    # create all possible leftward positions
                    for i in range(0, car.moveability_list[0]):
                        print(car.name)
                        current = -abs(i)
                        boardcopy = car.move4(boardcopy, current - 1)
                        boardcopy.cars[j].col = car.col
                        returnlist.append(copy.deepcopy(boardcopy))
                        
                if car.moveability_list[1] is not 0:
                    # create all possible rightward positions 
                    for i in range(0, car.moveability_list[0]):
                        car.move4(boardcopy, i + 1)
                        boardcopy.cars[j].col = car.col
                        returnlist.append(copy.deepcopy(boardcopy))
            
            else:
                # check for double moveables
                if car.moveability_list[0] is not 0 and car.moveability_list[1] is not 0:
                    # make copy and remember row position
                    doublecopy = copy.deepcopy(boardcopy)
                    row_save = car.row
                    
                    # create all possible upward positions
                    for i in range(0, car.moveability_list[0]):
                        current = -abs(i)
                        car.move4(boardcopy, current - 1)
                        boardcopy.cars[j].row = car.row
                        returnlist.append(copy.deepcopy(boardcopy))
                    
                    # create all possible downward positions from copy
                    car.row = row_save
                    for i in range(0, car.moveability_list[1]):
                        car.move4(doublecopy, i + 1)
                        doublecopy.cars[j].row = car.row
                        returnlist.append(copy.deepcopy(doublecopy))
                    continue

                if car.moveability_list[0] is not 0:
                    # create all possible upward positions
                    for i in range(0, car.moveability_list[0]):
                        current = -abs(i)
                        car.move4(boardcopy, current - 1)
                        boardcopy.cars[j].row = car.row
                        returnlist.append(copy.deepcopy(boardcopy))
                if car.moveability_list[1] is not 0:
                    # create all possible downward positions
                    for i in range(0, car.moveability_list[1]):
                        car.move4(boardcopy, i + 1)
                        boardcopy.cars[j].row = car.row
                        returnlist.append(copy.deepcopy(boardcopy))
            
            # reset car positions for next board
            self.cars[j].col = car_col

            print(f"CAR AA ROW: {car.row}")
            print(car_row)
            print(f"ROWROW2: {rowrow}")
            self.cars[j].row = car_row


        # return list of all children               
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

    
