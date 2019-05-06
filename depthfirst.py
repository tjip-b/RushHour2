from load import Load
from board import Board
from car import Car
import copy
import time


class Vertex:
    def __init__(self, n):
        self.name = n
        self.neighbors = list()

        self.discovery = 0
        self.finish = 0
        self.color = 'black'

    def add_neighbor(self, v):
        nset = set(self.neighbors)
        if v not in nset:
            self.neighbors.append(v)
            self.neighbors.sort()


class Graph:
    vertices = {}
    time = 0

    def add_vertex(self, vertex):
        if isinstance(vertex, Vertex) and vertex.name not in self.vertices:
            self.vertices[vertex.name] = vertex
            return True
        else:
            return False

    def add_edge(self, u, v):
        if u in self.vertices and v in self.vertices:
            for key, value in self.vertices.items():
                if key == u:
                    value.add_neighbor(v)
                if key == v:
                    value.add_neighbor(u)
            return True
        else:
            return False

    def print_graph(self):
        for key in sorted(list(self.vertices.keys())):
            print(key + str(self.vertices[key].neighbors) + " " + str(self.vertices[key].discovery))

    def _dfs(self, vertex):
        global time
        vertex.color = 'red'
        vertex.discovery = time
        time += 1
        for v in vertex.neighbors:
            if self.vertices[v].color == 'black':
                self._dfs(self.vertices[v])
        vertex.color = 'blue'
        vertex.finish = time
        time += 1

    def dfs(self, vertex):
        global time
        time = 1
        self._dfs(vertex)


g = Graph()

a = Vertex('A')

for i in range(ord('A'), ord('K')):
    g.add_vertex(Vertex(chr(i)))

edges = ['AB', 'AE', 'BF', 'CG', 'DE', 'DH', 'EH', 'FG', 'FI', 'FJ', 'GJ', 'HI']

for edge in edges:
    g.add_edge(edge[:1], edge[1:])

g.dfs(a)
g.print_graph()

#
# class Dfirst():
#     def __init__(self, queue):
#         self.queue = []
#
#     def Depthfirst(self, initialboard, initialcars):
#         start = time.time()
#         self.initialboard = copy.deepcopy(initialboard)
#         self.initalcars = copy.deepcopy(initialcars)
#         carlist = []
#         queue = []
#         number_of_moves = 0
#         # print(self.board)
#
#         print(queue)
#         # Find first moveable options and place them in the queue
#         # print(self.board)
#         for car in self.cars:
#             car.moveability(self.board)
#             # print(f"{car.col} , {car.row}")
#             # print(car.name)
#             # print(car.moveability_list)
#             if car.moveability_list[0] is not 0:
#                 queue.append([car.name[0] + "-1"])
#             if car.moveability_list[1] is not 0:
#                 queue.append([car.name[0] + "+1"])
#         print(self.initialboard)
#         print(queue)
#         BoardCopy = copy.deepcopy(self.board.positions)
#         carlist.append(BoardCopy)
#         for car in self.cars:
#             if car.name[0] == "r":
#                 redcarposition_inital = copy.deepcopy(car.col)
#
#         # For later use, now just with a n in range so there is no risk for crashing terminals
#         # while queue and len(queue) < 1000 and self.cars.redcar is not redcar_position:
#         for n in range(0, 10):
#
#             self.board = copy.deepcopy(self.initialboard)
#             self.cars = copy.deepcopy(self.initialcars)
#
#             # print(redcarposition)
#
#             s = queue.pop(0)
#             print(f"n = {n}")
#             print(s)
#
#             for i in s:
#                 CAR = None
#                 carletter = i[0]
#                 for car in self.cars:
#                     if car.name[0] == (carletter):
#                         CAR = car
#                         break
#                 dir = CAR.direction
#                 if dir == "horizontal":
#                     if i[1] == "+":
#                         move_dir = "right"
#                     else:
#                         move_dir = "left"
#
#                 else:
#                     if i[1] == "+":
#                         move_dir = "down"
#                     else:
#                         move_dir = "up"
#                 number_of_moves = i[2]
#                 # print(car.name)
#                 # print(move_dir)
#
#                 CAR.move2(self.board, move_dir)
#
#             for i, car in enumerate(self.cars):
#                 if car.red_car:
#                     redcar = self.cars[i]
#                     break
#
#             if redcar.col + 1 == self.board.exit_position:
#                 print(s)
#                 print("Gewonnen!")
#                 end = time.time()
#                 print(f"time is {start - end}")
#                 print(self.board)
#                 return True
#                 break
#
#             # if redcar.col == redcarposition_inital + 1:
#             #     print(self.board)
#             #     print("één naar rechts")
#             #     queue.clear()
#             #     carlist.clear()
#             #     # exit()
#             #     BreadthF.BreadthFirst(self, self.board, self.cars)
#             #     return True
#
#             if self.board.positions in carlist:
#                 # print("Board already been solved")
#                 continue
#
#             # if len(carlist) > 1000:
#             #     del carlist[0]
#             BoardCopy = copy.deepcopy(self.board.positions)
#             # print(BoardCopy)
#             carlist.append(BoardCopy)
#             # print(f"length of carlist = {len(carlist)}")
#
#             for car in self.cars:
#                 car.moveability(self.board)
#
#                 if car.moveability_list[0] is not 0:
#                     scopy = copy.deepcopy(s)
#                     # if scopy[-1][0] == car.name[0]:
#                     #     if scopy[-1][1] is not "-":
#                     #         continue
#                     scopy.append(car.name[0] + "-1")
#                     queue.append(scopy)
#
#                 if car.moveability_list[1] is not 0:
#                     scopy = copy.deepcopy(s)
#                     # if scopy[-1][0] == car.name[0]:
#                     #     if scopy[-1][1] is not "+":
#                     #         continue
#                     scopy.append(car.name[0] + "+1")
#                     queue.append(scopy)
#
#             # print(self.board)
