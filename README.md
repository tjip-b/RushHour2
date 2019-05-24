# RushHour2

Algortihm that solves the board game rush hour. There are three implemented methods: Breadth First, Depth First and Branchh & Bound. These methods can be applied on seven different boards (three 6x6 easy boards, three 9x9 medium boards and one 12x12 hard board) which are included in the /data folder (the seven different boards can be viewed at http://heuristieken.nl/wiki/index.php?title=Rush_Hour).

## Getting Started

No need for requirement.txt. Based only on pyhton 3.7. Should run out of the box


## Running the program

To run our program, please read through the following documentation. Things to be filled in as argument will be **bold**:
```
python rushhour.py <board> <algorithm> <depth/breadth (for depth_first)> <pruning method> <movement method>
```
Boards to choose from <board>: 
  - **easy**
  - **easy2**
  - **easy3**
  - **medium**
  - **medium2**
  - **medium3**
  - **hard**

Algorithms to choose from <algorithm>:
  - **breadth** (Breadth First Search)
  - **depth** (Depth First Search)
  - **depth_random** (Searches random into the depth)
  
Movement Method <movement method>:
  Please enter one of the following:
  - **all**: all cars make all possible movements.
  - **furthest**: all cars only make the furthest possible movements.
  
Depth/Breadth limit <depth/breadth limit>:
  - Depth: When running the depth first algorithm, please enter **an integer** as maximum depth. The algorithm will not consider boards which have more moves than the specified amount. 

  - Breadth (Optional): When running the breadth first algorithm, entering **an integer** as breadth limit will run an adjusted version of breadth first where.*.*..*...*...*....**..*......*..*.*....*....*

Different pruning for depth first <pruning method>:
  When running depth first, the method of pruning should be specified by typing:
    - **max**: if child is already in the archive > do not add child to stack
    - **min**: if child is already in the archive AND the depth of this child is higher than the depth of the node found in the archive > do not add child to stack
  
Choosing to run depth first search on the easy2 board would look like this:
```
python RushHour.py easy2 depth all max
```

Choosing to run depth_random_optimalised search on the hard board would look like this:
```
python RushHour.py hard depth_random 10000 1000
```
### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Authors

* **Kevin Dekker**
  **Siebren Kazemier**
  **Tjip Bischoff

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Erik
from the programming minor at the University of Amsterdam:
* Edwin, Daan & Wouter


