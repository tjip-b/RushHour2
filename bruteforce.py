from random import randint
class Bruteforce():

    def __init__ (self, filename):
        pass

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