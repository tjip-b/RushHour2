from random import randint


def randommover(self, amount):
        for i in range(0, amount): 
            for i, car in enumerate(self.cars):
                if car.red_car:
                    redcar = self.cars[i]
                    break
            moves = 0
            moveables = ["left", "right", "up", "down"]
    

            while redcar.col + 1 != self.board.exit_position:
                randy = randint(0, len(self.cars) - 1)
                randomcar = self.cars[randy]
                carmove = randomcar.moveable(self.board)                        
                if redcar.moveability_list[1] > 2:
                    redcar.move(self.board, "right")
                    redcar.move(self.board, "right")
                    redcar.move(self.board, "right")
                if redcar.moveable(self.board) == "leftright":
                    rand = randint(0, 100)
                    if rand > 20:
                        redcar.move(self.board, "right")
                    else:
                        redcar.move(self.board, "left")
                    moves += 1
                    continue
                if carmove in moveables:
                    randomcar.move(self.board, carmove)
                elif carmove == "leftright": 
                    rand = randint(0, 1)
                    if rand == 0:
                        randomcar.move(self.board, "left")
                    else:
                        randomcar.move(self.board, "right")
                elif carmove == "updown":
                    rand = randint(0, 1)
                    if rand == 0:
                        randomcar.move(self.board, "up")
                    else:
                        randomcar.move(self.board, "down")
                else:
                    continue    
                moves += 1
                print(self.board)
            print(moves)
            print(self.board)
            
            self.Reset()
            self.allmoves.append(moves)
            
        return self.allmoves

def randommover2(board, cars, amount):
        
        for i, car in enumerate(cars):
            if car.red_car:
                redcar = cars[i]
                break
        moves = 0
        moveables = ["left", "right", "up", "down"]


        for i in range (0, amount):
            randy = randint(0, len(cars) - 1)
            randomcar = cars[randy]
            carmove = randomcar.moveable(board)                        
            # if redcar.moveability_list[1] > 2:
            #     redcar.move(board, "right")
            #     redcar.move(board, "right")
            #     redcar.move(board, "right")
            if redcar.moveable(board) == "leftright":
                rand = randint(0, 100)
                if rand > 80:
                    redcar.move(board, "right")
                else:
                    redcar.move(board, "left")
                moves += 1
                continue
            if carmove in moveables:
                randomcar.move(board, carmove)
            elif carmove == "leftright": 
                rand = randint(0, 1)
                if rand == 0:
                    randomcar.move(board, "left")
                else:
                    randomcar.move(board, "right")
            elif carmove == "updown":
                rand = randint(0, 1)
                if rand == 0:
                    randomcar.move(board, "up")
                else:
                    randomcar.move(board, "down")
            else:
                continue    
            moves += 1
            # print(board)
        # print(moves)
        return(board)
                
                
                
         