import random
import itertools
from collections import Counter
import copy

#we will be using kruskal's algorithm to generate a random maze

def generatemaze(n):
    #it will be a 2d array of size n*n
    maze = [[i+n*j for i in range(n)] for j in range(n)]
    #walls will be a 2d array of size n-1*n-1
    walls_horz = [[1 for i in range(n-1)]for j in range(n)]
    walls_vert = [[1 for i in range(n)]for j in range(n-1)]
    walls_remaining = [i for i in range(2*(n-1)*(n))]
    #print(walls_remaining)
    while Counter(i for i in itertools.chain(*maze)).most_common(1)[0][1] != n*n:
        wall = random.choice(walls_remaining)
        print(wall)
        if wall < (n-1)*(n):
            #removing vertical wall at the position btw x,y and x+1,y
            walls_remaining.remove(wall)
            x = wall % (n-1)
            y = wall // (n-1)
            walls_vert[x][y] = 0
            #print(x,y)
            if maze[x][y] != maze[x+1][y]:
                k = copy.deepcopy(maze[x+1][y])
                for i in range(n):
                    for j in range(n):
                        if maze[i][j] == k:
                            maze[i][j] = maze[x][y]
        else:
            wall = wall - (n-1)*(n)
            walls_remaining.remove((n-1)*(n) + wall)
            x = wall % (n)
            y = wall // (n)
            walls_horz[x][y] = 0
            if maze[x][y] != maze[x][y+1]:
                k = copy.deepcopy(maze[x][y+1])
                for i in range(n):
                    for j in range(n):
                        if maze[i][j] == k:
                            maze[i][j] = maze[x][y]

        #print(maze)
    return walls_vert,walls_horz
#print(generatemaze(30))