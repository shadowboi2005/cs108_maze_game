## Maze Generator
## Wilson's Loop Erased Random Walk Algorithm
## Author: CaptainFlint

"""
Wilson's Algorithm is an algorithm to generate a
uniform spanning tree using a loop erased random walk.
Algorithm:
1. Choose a random cell and add it to the visited list
2. Choose another random cell (Don’t add to visited list).
   This is the current cell.
3. Choose a random cell that is adjacent to the current cell
   (Don’t add to visited list). This is your new current cell.
4. Save the direction that you traveled on the previous cell.
5. If the current cell is not in the visited cells list:
   a. Go to 3
6. Else:
   a. Starting at the cell selected in step 2, follow the arrows
      and remove the edges that are crossed.
   b. Add all cells that are passed into the visited list
7. If all cells have not been visited
   a. Go to 2
Source: http://people.cs.ksu.edu/~ashley78/wiki.ashleycoleman.me/index.php/Wilson's_Algorithm.html
"""

import random

class WilsonMazeGenerator:
    """Maze Generator using Wilson's Loop Erased Random Walk Algorithm"""

    def __init__(self,height,width):
        """WilsonMazeGenerator(int,int) -> WilsonMazeGenerator
        Creates a maze generator with specified width and height.
        width: width of generated mazes
        height: height of generated mazes"""        
        self.width = 2*(width//2) + 1   # Make width odd
        self.height = 2*(height//2) + 1 # Make height odd

        # grid of cells
        self.grid = [[0 for j in range(self.width)] for i in range(self.height)]

        # declare instance variable
        self.visited = []    # visited cells
        self.unvisited = []  # unvisited cells
        self.path = dict()   # random walk path

        # valid directions in random walk
        self.directions = [(0,1),(1,0),(0,-1),(-1,0)]

        # indicates whether a maze is generated
        self.generated = False

        # shortest solution
        self.solution = []
        self.showSolution = False
        self.start = (self.height-1,0)
        self.end = (0,self.width-1)

    def __str__(self):
        """WilsonMazeGenerator.__str__() -> str
        outputs a string version of the grid"""
        out = "##"*(self.width+1)+"\n"
        for i in range(self.height):
            out += "#"
            for j in range(self.width):
                if self.grid[i][j] == 0:
                    out += "##"
                else:
                    if not self.showSolution:
                        out += "  "
                    elif (i,j) in self.solution:
                        out += "**"
                    else:
                        out += "  "
            out += "#\n"
        return out + "##"*(self.width+1)

    def get_grid(self):
        """WilsonMazeGenerator.get_grid() -> list
        returns the maze grid"""
        return self.grid

    def get_solution(self):
        """WilsonMazeGenerator.get_solution() -> list
        Returns the solution to the maze as a list
        of tuples"""
        return self.solution

    def show_solution(self,show):
        """WilsonMazeGenerator.show_solution(boolean) -> None
        Set whether WilsonMazeGenerator.__str__() outputs the
        solution or not"""
        self.showSolution = show
    
    def generate_maze(self):
        """WilsonMazeGenerator.generate_maze() -> None
        Generates the maze according to the Wilson Loop Erased Random
        Walk Algorithm"""
        # reset the grid before generation
        self.initialize_grid()

        # choose the first cell to put in the visited list
        # see Step 1 of the algorithm.
        current = self.unvisited.pop(random.randint(0,len(self.unvisited)-1))
        self.visited.append(current)
        self.cut(current)

        # loop until all cells have been visited
        while len(self.unvisited) > 0:
            # choose a random cell to start the walk (Step 2)
            first = self.unvisited[random.randint(0,len(self.unvisited)-1)]
            current = first
            # loop until the random walk reaches a visited cell
            while True:
                # choose direction to walk (Step 3)
                dirNum = random.randint(0,3)
                # check if direction is valid. If not, choose new direction
                while not self.is_valid_direction(current,dirNum):
                    dirNum = random.randint(0,3)
                # save the cell and direction in the path
                self.path[current] = dirNum
                # get the next cell in that direction
                current = self.get_next_cell(current,dirNum,2)
                if (current in self.visited): # visited cell is reached (Step 5)
                    break

            current = first # go to start of path
            # loop until the end of path is reached
            while True:
                # add cell to visited and cut into the maze
                self.visited.append(current)
                self.unvisited.remove(current) # (Step 6.b)
                self.cut(current)

                # follow the direction to next cell (Step 6.a)
                dirNum = self.path[current]
                crossed = self.get_next_cell(current,dirNum,1)
                self.cut(crossed) # cut crossed edge

                current = self.get_next_cell(current,dirNum,2)
                if (current in self.visited): # end of path is reached
                    self.path = dict() # clear the path
                    break
                
        self.generated = True

    def solve_maze(self):
        """WilsonMazeGenerator.solve_maze() -> None
        Solves the maze according to the Wilson Loop Erased Random
        Walk Algorithm"""
        # if there is no maze to solve, cut the method
        if not self.generated:
            return None

        # initialize with empty path at starting cell
        self.path = dict()
        current = self.start

        # loop until the ending cell is reached
        while True:
            while True:
                # choose valid direction
                # must remain in the grid
                # also must not cross a wall
                dirNum = random.randint(0,3)
                adjacent = self.get_next_cell(current,dirNum,1)
                if self.is_valid_direction(current,dirNum):
                    hasWall = (self.grid[adjacent[0]][adjacent[1]] == 0)
                    if not hasWall:
                        break
            # add cell and direction to path
            self.path[current] = dirNum

            # get next cell
            current = self.get_next_cell(current,dirNum,2)
            if current == self.end: 
                break # break if ending cell is reached

        # go to start of path
        current = self.start
        self.solution.append(current)
        # loop until end of path is reached
        while not (current == self.end):
            dirNum = self.path[current] # get direction
            # add adjacent and crossed cells to solution
            crossed = self.get_next_cell(current,dirNum,1)
            current = self.get_next_cell(current,dirNum,2)
            self.solution.append(crossed)
            self.solution.append(current)

        self.path = dict()
                
    ## Private Methods ##
    ## Do Not Use Outside This Class ##
                
    def get_next_cell(self,cell,dirNum,fact):
        """WilsonMazeGenerator.get_next_cell(tuple,int,int) -> tuple
        Outputs the next cell when moved a distance fact in the the
        direction specified by dirNum from the initial cell.
        cell: tuple (y,x) representing position of initial cell
        dirNum: int with values 0,1,2,3
        fact: int distance to next cell"""
        dirTup = self.directions[dirNum]
        return (cell[0]+fact*dirTup[0],cell[1]+fact*dirTup[1])

    def is_valid_direction(self,cell,dirNum):
        """WilsonMazeGenerator(tuple,int) -> boolean
        Checks if the adjacent cell in the direction specified by
        dirNum is within the grid
        cell: tuple (y,x) representing position of initial cell
        dirNum: int with values 0,1,2,3"""
        newCell = self.get_next_cell(cell,dirNum,2)
        tooSmall = newCell[0] < 0 or newCell[1] < 0
        tooBig = newCell[0] >= self.height or newCell[1] >= self.width
        return not (tooSmall or tooBig)

    def initialize_grid(self):
        """WilsonMazeGenerator.initialize_grid() -> None
        Resets the maze grid to blank before generating a maze."""
        for i in range(self.height):
            for j in range(self.width):
                self.grid[i][j] = 0
                
        # fill up unvisited cells
        for r in range(self.height):
            for c in range(self.width):
                if r % 2 == 0 and c % 2 == 0:
                    self.unvisited.append((r,c))

        self.visited = []
        self.path = dict()
        self.generated = False

    def cut(self,cell):
        """WilsonMazeGenerator.cut(tuple) -> None
        Sets the value of the grid at the location specified by cell
        to 1
        cell: tuple (y,x) location of where to cut"""
        self.grid[cell[0]][cell[1]] = 1

################
'''         
gen = WilsonMazeGenerator(10,10)
gen.generate_maze()
print("Maze Generated")
gen.solve_maze()
print("Solution Generated")
quest = input("Do you want the solution shown? (Y/N) ")
gen.show_solution(quest.strip().lower() == "y")
print(gen)
'''
