from load import Load
import copy
class BreadthF():

    def __init__ (self, queue, initalboard):
        self.queue = [] 
        self.initalboard = Load.load_board(rushhour, "data/easy.txt")


    def BreadthFirst(rushhour):
        # Iboard = Load.load_board(rushhour, "data/easy.txt")
        # boardpositions = rushhour.board.positions

        carlist = []
        queue = []
        number_of_moves = 0
        # print(rushhour.board)


        # Find first moveable options and place them in the queue
        for car in rushhour.cars:
            # print(car.name)
            # print(car.moveability_list)
            if car.moveability_list[0] is not 0:
                queue.append([car.name[0] + "-1"])
            if car.moveability_list[1] is not 0:
                queue.append([car.name[0] + "+1"])
        print(queue)    

        carlist.append(rushhour.board.positions)

        # For later use, now just with a n in range so there is no risk for crashing terminals
        # while queue and len(queue) < 1000 and rushhour.cars.redcar is not redcar_position: 
        for n in range(0, 5000):
            # rushhour.board.positions = boardpositions
            # print(rushhour.board.positions)
            # print("blablalba")
            # rushhour.board = Load.load_board(rushhour, "data/easy.txt")
            
            # print(rushhour.board.positions)
            
            # print("hallo")
            # print(f"initial bord = ... and n ={n}")
            # print(rushhour.board)
            rushhour.board = copy.deepcopy(rushhour.initialboard)
            rushhour.cars = copy.deepcopy(rushhour.initialcars)
            s = queue.pop(0) 
            print(f"n = {n}")
            print(s)
            
            for i in s:
                CAR = None
                carletter = i[0]
                for car in rushhour.cars:
                    if car.name[0] == (carletter):
                        CAR = car
                        break
                dir = CAR.direction
                if dir == "horizontal":
                    if i[1] == "+":
                        move_dir = "right"
                    else:
                        move_dir = "left"

                else:
                    if i[1] == "+":
                        move_dir = "down"
                    else:
                        move_dir = "up"
                self.number_of_moves = i[2]
                # print(car.name)
                # print(move_dir)
                
                # print(rushhour.board)
                CAR.move2(rushhour.board, move_dir)                
                # print(rushhour.board)
            # print(queue)
            for i, car in enumerate(rushhour.cars):
                if car.red_car:
                    redcar = rushhour.cars[i]
                    break
            if redcar.col + 1 == rushhour.board.exit_position:
                print("Gewonnen!")
                print(rushhour.board)
                break
            if rushhour.board.positions in carlist:
                continue

            carlist.append(rushhour.board.positions)
            for car in rushhour.cars:

                car.moveability(rushhour.board)

                if car.moveability_list[0] is not 0:
                    scopy = copy.deepcopy(s)
                    if scopy[-1][0] == car.name[0]:
                        if scopy[-1][1] is not "-":
                            continue
                    scopy.append(car.name[0] + "-1")
                    queue.append(scopy)
            
                if car.moveability_list[1] is not 0:
                    scopy = copy.deepcopy(s)
                    if scopy[-1][0] == car.name[0]:
                        if scopy[-1][1] is not "+":
                            continue
                    scopy.append(car.name[0] + "+1")
                    queue.append(scopy)
            print(rushhour.board)
        print()

    