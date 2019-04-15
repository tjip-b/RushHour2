from collections import defaultdict
from pprint import pprint 
class FlightNetwork:
    def __init__(self):
        self.neighbors = defaultdict(list)
        self.cost = defaultdict(list)
        
    def add_flight(self, source, destination, price):
        self.neighbors[source].append(destination)
        self.cost[source].append(price)
    
    def show_flights(self):
        print("Destinations:");pprint(dict(self.neighbors))
        print("Cost:");pprint(dict(self.cost))

    """
        This function is used to backtrack the nodes in the parent dictionary to find out all 
        routes from S to D of varying lengths. The starting point (D, k) determines the length of 
        paths that would be found by this function. Length would be k. So we
        have to have a for loop from min stops to max stops to get all the routes.
    """
    def get_route(self, destination, source, parent):
        if destination[0] == source:
            return [source]    
        routes = []
        for p in parent[destination]:
            routes.extend([r + "-->" + destination[0] for r in self.get_route(p, source,  parent)])
        return routes

    """ 
        Classic level order traversal 
        * source represents S i.e. the starting point of our flight.
        * destination is D i.e. the ending point of our route.
        * stops_range is a tuple representing minimum and maximum number of stops required in the required flight routes.
    """
    def level_order_traversal(self, source, destination, stops_range):
        least_stops, max_stops = stops_range

        # The BFS queue
        queue = [(source, 0, -1)]

        # Parent dictionary used for finding the actual routes once level order traversal is done
        parent = defaultdict(list)

        # Continue until the queue is empty
        while queue:

            # Pop the front element of the queue. 
            location, cost_till_now, stops_since_source = queue.pop(0)

            # If the current location has eny neighbors i.e. any direct flights, iterate over those neighbors
            if location in self.neighbors:
                for neighbor, cost in zip(self.neighbors[location], self.cost[location]):
                    """
                        THIS STEP IS VERY IMPORTANT. We record all the parents of this `location` via which a path
                        starting from S reached `location` in `stops_since_source + 1` steps.
                    """
                    parent[(neighbor, stops_since_source + 1)].append((location, stops_since_source))

                    # If the number of stops till now is < max_stops, then we can add this `location` node for processing.
                    if stops_since_source < max_stops:
                        queue.append((neighbor, cost + cost_till_now, stops_since_source + 1))     

        # Return parent node for route backtracking.                
        return parent

f = FlightNetwork()
f.add_flight('A', 'C', 10)
f.add_flight('A', 'B', 20)
f.add_flight('A', 'F', 14)
f.add_flight('B', 'D', 20)
f.add_flight('C', 'B', 120)
f.add_flight('C', 'M', 200)
f.add_flight('D', 'C', 75)
f.add_flight('C', 'E', 145)
f.add_flight('C', 'F', 50)
f.add_flight('D', 'E', 45)
f.add_flight('D', 'F', 60)
f.add_flight('M', 'F', 45)
f.add_flight('E', 'F', 60)
f.show_flights()

parent = f.level_order_traversal('A', 'F', (2,5))

for r in range(2, 6):
    print("\nFlights with {} stops in between are as follows:".format(r))
    routes = f.get_route(('F', r), 'A', parent)
    for r in routes:
        print(r)
