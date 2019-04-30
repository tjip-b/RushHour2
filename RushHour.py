import sys
from board import Board
from car import Car
from load import Load
from bruteforce import Bruteforce
from random import randint
import time
from collections import defaultdict
# from graph import Graph
# from colorama import init
#
# init()


class RushHour():
    """
    This is the Rush Hour game.
    """

    def __init__(self, game):
        """
        Create the board within the game and create car objects
        """
        self.board = Load.load_board(self, f"data/{game}.txt")
        self.cars = Load.load_cars(self)
        self.allmoves = []
        self.initialboard = self.board
        self.initialcars = self.cars
        self.game = game

    def find(self):
        # while redcar_position niet op self.board.exit_position:
        print("hio")

    def check(self):
        """
        checks if car(s) are in certain row or colomn
        """
        print("test")

    def playtest(self, method):
        # print out some information about the board and cars
        print(self.board.positions)
        for line in self.board.positions:
            print(line)
        for i, car in enumerate(self.cars):
            print("No.%s: CAR: %s" % (i, car))
            print(car.direction)
            print(f"X pos: {car.row} y pos: {car.col}")
            print('\n')
        print(self.board.width_height)
        print(self.board)

        # brute force the game!
        if method == "bruteforce":

            n = 1
            Bruteforce.randommover(self,  1)
            average = self.Average(self.allmoves)
            print(f"avarage of {self.game} board for {n} runs = {average}")

    def Average(self, lst):
        return sum(lst) / len(lst)

    def Reset(self):
        self.board = Load.load_board(self, f"data/{self.game}.txt")
        self.cars = Load.load_cars(self)


if __name__ == "__main__":
    rushhour = RushHour("easy2")
    # rushhour.playtest("bruteforce")

    # print(f"width_height: {rushhour.board.width_height}")

    class Graph:

        # Constructor
        def __init__(self):

            # default dictionary to store graph
            self.graph = defaultdict(list)

        # function to add an edge to graph
        def addEdge(self, u, v):
            self.graph[u].append(v)

        # Function to print a BFS of graph
        def BFS(self, s):

            # Mark all the vertices as not visited
            visited = [False] * (len(self.graph))

            # Create a queue for BFS
            queue = []

            # Mark the source node as
            # visited and enqueue it
            queue.append(s)

            for count, visit in enumerate(self.graph):
                if visit == s:
                    visited[count] = True

            while queue:
                # Dequeue a vertex from
                # queue and print it
                s = queue.pop(0)
                # print(s, end=" ")

                ##################### TRY TO MOVE THE CAR ####################

                # board_save_list.append(rushhour.board.positions)
                # print(board_save_list)

                for car in rushhour.cars:
                    # update moveability
                    car.moveability(rushhour.board)

                    if car.red_car and car.moveability_list[1] > 0:
                        car.move(rushhour.board, "right")
                        queue.clear()
                    elif not car.red_car and s == car.name[0] and car.direction == "horizontal":
                        if car.moveability_list[0] > 0:
                            car.move(rushhour.board, "left")
                            queue.clear()
                        elif car.moveability_list[1] > 0:
                            car.move(rushhour.board, "right")
                            queue.clear()
                    elif not car.red_car and s == car.name[0] and car.direction == "vertical":
                        if car.moveability_list[0] > 0:
                            car.move(rushhour.board, "up")
                            queue.clear()
                        elif car.moveability_list[1] > 0:
                            car.move(rushhour.board, "down")
                            queue.clear()
                    else:
                        # Get all adjacent vertices of the
                        # dequeued vertex s. If a adjacent
                        # has not been visited, then mark it
                        # visited and enqueue it
                        for i in self.graph[s]:
                            for count, visit in enumerate(self.graph):
                                if visit == i and visited[count] == False:
                                    queue.append(i)
                                    visited[count] = True

            print(rushhour.board)
            #
            # for board in board_save_list:
            #     for line in board_save_list:
            #         for bla in line:
            #             print(bla)

    ##########################################################################
    # CAR CONNECTIONS #
    ##########################################################################

    # for car in rushhour.cars:
    #     if car.red_car:
    #         while car.col + 1 != rushhour.board.exit_position:
    haai = 0

    # remember boards
    save_boards = []

    while haai < 50:

        save_boards.append(rushhour.board.positions)

        g = Graph()

        for car in rushhour.cars:
            if car.direction == "horizontal":
                connection_left = car.col - car.moveability_list[0] - 1
                connection_right = car.col + car.size + car.moveability_list[1]

                # connection_left = car.col - 1
                # connection_right = car.col + car.size

                # add connections
                if connection_left >= 0:
                    g.addEdge(rushhour.board.positions[car.row][car.col],
                              rushhour.board.positions[car.row][connection_left])
                if connection_right <= rushhour.board.width_height:
                    g.addEdge(rushhour.board.positions[car.row][car.col],
                              rushhour.board.positions[car.row][connection_right])
            # vertical
            else:
                connection_up = car.row - car.moveability_list[0] - 1
                connection_down = car.row + car.size + car.moveability_list[1]

                # connection_up = car.row - 1
                # connection_down = car.row + car.size

                # add connection
                if connection_up >= 0:
                    g.addEdge(rushhour.board.positions[car.row][car.col],
                              rushhour.board.positions[connection_up][car.col])
                if connection_down <= rushhour.board.width_height:
                    g.addEdge(rushhour.board.positions[car.row][car.col],
                              rushhour.board.positions[connection_down][car.col])
        g.BFS('r')
        haai = haai + 1

        print(g.graph)
    # g.BFS('r')
