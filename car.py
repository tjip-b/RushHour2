
class Car():

    def __init__ (self, name, x, y, direction, size, red_car):
        # capital letters
        self.name = name
    
        # x / y starting position
        self.x = x
        self.y = y

        # horizontal or vertical
        self.direction = direction

        # cars are always 2 or 3 tiles big
        self.size = size

        # is this car the red car?
        self.red_car = red_car 
    
    def __str__(self):
        return self.name


#######################
#   X Y EDIT          #  
#######################

    def moveable(self, board):
            """ Checks if car is moveable.
                Returns string of: (leftright, updown, right, left, down, up or none) based on movability
            """
            # horizontal
            if self.direction == "horizontal":
                # the position to which the car wants to move is either 1 more or 1 less column wise
                #right = self.get_cols()[1] + self.size - 1
                #left = self.get_cols()[0] - 1
                
                # xy
                rightxy = self.y + self.size
                leftxy = self.y - 1

                # check if right or left is out of the boards margins 
                if rightxy > board.width_height:
                    move_left = board.positions[self.x][leftxy]
                    move_right = None
                elif leftxy < 0:
                    move_right = board.positions[self.x][rightxy]
                    move_left = None
                else:            
                    move_right = board.positions[self.x][rightxy]
                    move_left = board.positions[self.x][leftxy]

                # try to move left and right
                if move_right == "x" and move_left == "x":
                    return "leftright"
                elif move_right == "x":
                    return "right"
                elif move_left == "x":
                    return "left"
                else: 
                    return "none"
                
            # vertical
            else:
                up = self.x - 1
                #print(up)
                down = self.x + self.size
                # check if up or down is out of the boards margins 
                if up < 0:
                    # no room on the board for upward movement
                    move_down = board.positions[down][self.y]
                    move_up = None
                elif down > board.width_height:
                    # no room on the board for downward movement
                    move_up = board.positions[up][self.y]
                    move_down = None
                else:
                    # both up and down are possible positions on the board
                    move_up = board.positions[up][self.y]
                    move_down = board.positions[down][self.y]

                # try to move up and down
                if move_down == "x" and move_up == "x":
                    return "updown"
                elif move_up == "x":
                    return "up"
                elif move_down == "x":
                    return "down"
                else: 
                    return "none"
                    
    def moveability(self, board):
        """ Checks if car is moveable.
            Returns string of: (leftright, updown, right, left, down, up or none) based on movability
        """
        # horizontal
        if self.direction == "horizontal":

            # the position to which the car wants to move is either 1 more or 1 less column wise
            right = self.get_cols()[1] + self.size - 1
            left = self.get_cols()[0] - 1
            # print (f"left = {left}")
            # check if right or left is out of the boards margins
            for i in range (0,100):
                # print (f"left = {left}")
                # print (self.moveability)
                if right > board.width_height:
                    move_left = board.positions[self.get_rows()[0]][left]
                    move_right = None
                elif left < 0:
                    move_right = board.positions[self.get_rows()[0]][right]
                    move_left = None
                else:
                    move_right = board.positions[self.get_rows()[0]][right]
                    move_left = board.positions[self.get_rows()[0]][left]

                # try to move left and right
                print (left)
                if move_right == "x" :
                    self.moveability[1] += 1
                    right = right + 1
                elif move_left == "x":
                    self.moveability[0] += 1
                    left = left -1
                else:
                    break

        # vertical
        else:
            up = self.get_rows()[0] - 1
            #print(up)
            down = self.get_rows()[1] + self.size - 1
            for i in range (0,100):
            # check if up or down is out of the boards margins
                if up < 0:
                    # no room on the board for upward movement
                    move_down = board.positions[down][self.get_cols()[0]]
                    move_up = None
                elif down > board.width_height:
                    # no room on the board for downward movement
                    move_up = board.positions[up][self.get_cols()[0]]
                    move_down = None
                else:
                    # both up and down are possible positions on the board
                    move_up = board.positions[up][self.get_cols()[0]]
                    move_down = board.positions[down][self.get_cols()[0]]

                # try to move up and down
                if move_down == "x":
                    self.moveability[0] += 1
                    down = self.get_rows()[1] + self.size - (i + 2)
                elif move_up == "x":
                    self.moveability[1] += 1
                    up = self.get_rows()[0] = (i)
                else:
                    break
    def move(self, board, move_dir):
        """ Tries to move car on the board.
            Returns board with moved car and changes X and Y coordinates of car object
            Nothing changes if car was not moveable in the first place.
        """
        if move_dir == "right":
            # failsafe: do not move through other cars on board
            if board.positions[self.x][self.y + self.size].isupper() or board.positions[self.x][self.y + self.size] == 'r':
                print("No movement!")
                return board
            
            # give board correct new positions (characters)
            else:
                board.positions[self.x][self.y + self.size] = self.name[0]
                board.positions[self.x][self.y] = "x"

                # change car objects positions
                self.y = self.y + 1
                return board

        elif move_dir == "left":     
            if board.positions[self.x][self.y - 1].isupper() or board.positions[self.x][self.y - 1] == 'r':
                print("No movement!")
                return board
            else: 
                board.positions[self.x][self.y - 1] = self.name[0]
                board.positions[self.x][self.y + self.size - 1] = "x"
                self.y = self.y - 1
                return board

        elif move_dir == "up":
            #print(board.positions[self.x - 1][self.y])
            if board.positions[self.x - 1][self.y].isupper() or board.positions[self.x - 1][self.y] == 'r':
                print("No movement!")
                return board
            else:
                board.positions[self.x - 1][self.y] = self.name[0]
                board.positions[self.x + (self.size - 1)][self.y] = "x"
                self.x = self.x - 1
                return board
        elif move_dir == "down":            
            try:    
                if board.positions[self.x + self.size][self.y].isupper() or board.positions[self.x + self.size][self.y] == 'r':
                    print("No movement!")
                    return board
            except IndexError:
                print("Movement out of bounds")
                return board
            else: 
                board.positions[self.x][self.y] = "x"            
                board.positions[self.x + self.size][self.y] = self.name[0]                
                self.x = self.x + 1
                return board
        else:
            return board