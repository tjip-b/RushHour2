# Python3 Program to print BFS traversal 
# from a given source vertex. BFS(int s) 
# traverses vertices reachable from s. 
from collections import defaultdict 

# This class represents a directed graph 
# using adjacency list representation 
class Graph: 

	# Constructor 
	def __init__(self): 

		# default dictionary to store graph 
		self.graph = defaultdict(list) 

	# function to add an edge to graph 
	def addEdge(self,u,v): 
		self.graph[u].append(v) 

	def addNode(self,u):
		self.graph[u]
	# Function to print a BFS of graph 
	def BFS(self, s): 

		# Mark all the vertices as not visited 
		visited = [False] * (len(self.graph)) 

		# Create a queue for BFS 
		queue = [] 

		# Mark the source node as 
		# visited and enqueue it 
		queue.append(s) 
		visited[s] = True

		while queue: 

			# Dequeue a vertex from 
			# queue and print it 
			s = queue.pop(0) 
			print (s, end = ", ") 
            # print (s, end = ", ") 
            # print (self.graph)
			# Get all adjacent vertices of the 
			# dequeued vertex s. If a adjacent 
			# has not been visited, then mark it 
			# visited and enqueue it 
            
			for i in self.graph[s]: 
				print(self.graph)
				print(visited)
				print (i)
				if visited[i] == False: 
					queue.append(i) 
					visited[i] = True

# Driver code 

# Create a graph given in 
# the above diagram 
g = Graph() 
g.addEdge(0, 8) 
g.addEdge(0, 1) 
g.addEdge(1, 2) 
g.addEdge(2, 0) 
g.addEdge(2, 3) 
# g.addEdge(3, 3) 
# g.addEdge(3, 4) 
# g.addEdge(3, 5) 
g.addEdge(4, 0) 
g.addEdge(4, 5) 
g.addEdge(5, 6)
g.addEdge(6, 5)  
g.addNode(7)
g.addNode(3)
g.addNode(8)

print ("Following is Breadth First Traversal"
				" (starting from vertex 2)") 
g.BFS(2) 
print(g.graph)

# This code is contributed by Neelam Yadav 
