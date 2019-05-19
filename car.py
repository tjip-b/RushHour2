
class Car():

    def __init__ (self, name, row, col, direction, size, red_car, number):
        # capital letters
        self.name = name
        self.number = number
        # x / y starting position
        self.row = row
        self.col = col

        # horizontal(0) or vertical(1)
        self.direction = direction

        # cars are always 2 or 3 tiles big
        self.size = size

        # is this car the red car?
        self.red_car = red_car 

        # distance to exit
        self.distance = 0

        # format = horizontal: [left steps, right steps] // vertical: [up steps, down steps]
        self.moveability_list = [0, 0] 


    def __str__(self):
        return self.name


#######################
#   X Y EDIT #  #  #  #  
#######################

    def moveable(self, board):
            """ Checks if car is moveable.
                Returns string of: (leftright, updown, right, left, down, up or none) based on movability
            """
            # horizontal
            if self.direction == 0:
                # the position to which the car wants to move is either 1 more or 1 less column wise
                #right = self.get_cols()[1] + self.size - 1
                #left = self.get_cols()[0] - 1
                
                # xy
                rightxy = self.col + self.size
                leftxy = self.col - 1

                # check if right or left is out of the boards margins 
                if rightxy > board.width_height:
                    move_left = board.positions[self.row][leftxy]
                    move_right = None
                elif leftxy < 0:
                    move_right = board.positions[self.row][rightxy]
                    move_left = None
                else:            
                    move_right = board.positions[self.row][rightxy]
                    move_left = board.positions[self.row][leftxy]

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
                up = self.row - 1
                #print(up)
                down = self.row + self.size
                # check if up or down is out of the boards margins 
                if up < 0:
                    # no room on the board for upward movement
                    move_down = board.positions[down][self.col]
                    move_up = None
                elif down > board.width_height:
                    # no room on the board for downward movement
                    move_up = board.positions[up][self.col]
                    move_down = None
                else:
                    # both up and down are possible positions on the board
                    move_up = board.positions[up][self.col]
                    move_down = board.positions[down][self.col]

                # try to move up and down
                if move_down == "x" and move_up == "x":
                    return "updown"
                elif move_up == "x":
                    return "up"
                elif move_down == "x":
                    return "down"
                else: 
                    return "none"

    # changes only the position of the car object, not the board itself
    def move3(self, move):
        if self.direction == 0:
            self.col += move
        if self.direction == 1:
            self.row += move
        

    # the same as move, but without the failsaves
    def move2(self, board, move_dir):
        """ Tries to move car on the board.
            Returns board with moved car and changes X and Y coordinates of car object
            Nothing changes if car was not moveable in the first place.
        """
        if move_dir == "right":           
            board.positions[self.row][self.col + self.size] = self.name[0]
            board.positions[self.row][self.col] = "x"
            
            # change car objects positions
            self.col = self.col + 1
            return board

        elif move_dir == "left":     
           
            board.positions[self.row][self.col - 1] = self.name[0]
            board.positions[self.row][self.col + self.size - 1] = "x"
            self.col = self.col - 1
            return board

        elif move_dir == "up":
        
            board.positions[self.row - 1][self.col] = self.name[0]
            board.positions[self.row + (self.size - 1)][self.col] = "x"
            self.row = self.row - 1
            return board

        elif move_dir == "down":            
            
          
            board.positions[self.row][self.col] = "x"            
            board.positions[self.row + self.size][self.col] = self.name[0]                
            self.row = self.row + 1
            return board
        else:
            return board


    def move(self, board, move_dir):
        """ Tries to move car on the board.
            Returns board with moved car and changes X and Y coordinates of car object
            Nothing changes if car was not moveable in the first place.
        """
        if move_dir == "right":
            # failsafe: do not move through other cars on board
            if board.positions[self.row][self.col + self.size].isupper() or board.positions[self.row][self.col + self.size] == 'r':
                print("No movement!")
                return board
            
            # give board correct new positions (characters)
            else:
                board.positions[self.row][self.col + self.size] = self.name[0]
                board.positions[self.row][self.col] = "x"

                # change car objects positions
                self.col = self.col + 1
                return board

        elif move_dir == "left":     
            if board.positions[self.row][self.col - 1].isupper() or board.positions[self.row][self.col - 1] == 'r':
                print("No movement!")
                return board
            else: 
                board.positions[self.row][self.col - 1] = self.name[0]
                board.positions[self.row][self.col + self.size - 1] = "x"
                self.col = self.col - 1
                return board

        elif move_dir == "up":
            #print(board.positions[self.row - 1][self.col])
            if board.positions[self.row - 1][self.col].isupper() or board.positions[self.row - 1][self.col] == 'r' or self.row - 1 < 0:
                print("No movement!")
                return board
            else:
                board.positions[self.row - 1][self.col] = self.name[0]
                board.positions[self.row + (self.size - 1)][self.col] = "x"
                self.row = self.row - 1
                return board
        elif move_dir == "down":            
            try:    
                if board.positions[self.row + self.size][self.col].isupper() or board.positions[self.row + self.size][self.col] == 'r':
                    print("No movement!")
                    return board
            except IndexError:
                print("Movement out of bounds")
                return board
            else: 
                board.positions[self.row][self.col] = "x"            
                board.positions[self.row + self.size][self.col] = self.name[0]                
                self.row = self.row + 1
                return board
        else:
            return board

    def moveability(self, board):
        self.moveability_list = [0, 0] 
        """ Checks if car is moveable.
            Returns string of: (leftright, updown, right, left, down, up or none) based on movability
        """
        # horizontal
        if self.direction == 0:

            # the position to which the car wants to move is either 1 more or 1 less column wise
            right = self.col + self.size
            left = self.col - 1
            # print (f"left = {left}")
            # check if right or left is out of the boards margins

            # print (f"left = {left}")
            # print (self.moveability_list)
            if right > board.width_height:
                move_left = board.positions[self.row][left]
                move_right = None
            elif left < 0:
                move_right = board.positions[self.row][right]
                move_left = None
            else:
                move_right = board.positions[self.row][right]
                move_left = board.positions[self.row][left]

            # try to move left and right
            # print (left)
            while move_right == "x":
                # print(f"right: {right}")
                # print (board.width_height)
                # print(board.positions[self.row][right])
                self.moveability_list[1] += 1
                right += 1
                if right > board.width_height:
                    break
                move_right = board.positions[self.row][right]
                # print(f"print right:{right}")

            while move_left == "x":
                self.moveability_list[0] += 1
                left -= 1
                if left < 0:
                    break
                move_left = board.positions[self.row][left]
                
            return self.moveability_list

        # vertical
        else:
            up = self.row - 1
            #print(up)
            down = self.row + self.size
            # check if up or down is out of the boards margins
            if up < 0:
                # no room on the board for upward movement
                move_down = board.positions[down][self.col]
                move_up = None
            elif down > board.width_height:
                # no room on the board for downward movement
                move_up = board.positions[up][self.col]
                move_down = None
            else:
                # both up and down are possible positions on the board
                move_up = board.positions[up][self.col]
                move_down = board.positions[down][self.col]

            # calculate downward movability
            while move_down == "x":
                self.moveability_list[1] += 1
                down += 1
                # ensure out of bounds array positions won't be reached
                if down > board.width_height:
                    break
                move_down = board.positions[down][self.col]
                
            # calculate upward movability
            while move_up == "x":
                self.moveability_list[0] += 1
                up -= 1
                if up < 0:
                    break
                move_up = board.positions[up][self.col]
            return self.moveability_list

            
                