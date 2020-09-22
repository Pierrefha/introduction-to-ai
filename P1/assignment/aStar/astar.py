# prioq python module
import heapq


class Node:

    def __init__(self, posX, posY):
        self.x = posX
        self.y = posY
        self.parent = 0
        self.concreteCost = 0
        self.heuristicCost = 0
        self.f = 0

    # declare __lt__ method to handle comparision between two objects
    def __lt__(self, other):
        return self.f < other.f


class Grid:

    def __init__(self, grid, startNode, goalNode):
        self.grid = grid
        # maxCost is our representation of infinity
        self.maxCost = 9999999
        self.startNode = startNode
        self.goalNode = goalNode

    # calculates heuristic cost between node and goalNode
    def heuristicCost(self, node):
        # calc concreteCost with manhatten distance where D is
        # lowest concreteCost possible which is 1
        D = 1
        dx = abs(node.x - self.goalNode.x)
        dy = abs(node.y - self.goalNode.y)
        return D * (dx + dy)

    # calculates distance between two nodes
    def concreteCost(self, fromNode, toNode):
        horizontalTravelCost = abs(fromNode.x-toNode.x)
        verticalTravelCost = abs(fromNode.y-toNode.y)
        return horizontalTravelCost+verticalTravelCost

    # checks if node is already in list
    def nodeInList(self, node, list):
        for elem in list:
            if(elem.x == node.x and elem.y == node.y):
                return True
        return False

    # GRID[FIRST][SECOND] (y,x)
    # [[1,2,3],
    # [4,5,6],
    # [7,8,9]]
    # grid[0][2] -> 3; grid[1][0] -> 4
    def expandNeighbours(self, currentNode, openList, closedList):
        # set bounds to only check the grid
        northBound, westBound = 0, 0
        eastBound, southBound = len(grid[0])-1, len(grid)-1

        # go through all for possible neighbours while taking care of bounds.
        # Order: north,east,south,west
        if(currentNode.y-1 >= northBound and
                grid[currentNode.y-1][currentNode.x] not in ["w", "n"]):
            expandedNode = Node(currentNode.x, currentNode.y-1)
            # mark node with max cost if it's
            # neither in open nor in closed list
            if(not (self.nodeInList(expandedNode, closedList)
                    or self.nodeInList(expandedNode, openList))):
                expandedNode.concreteCost = self.maxCost
                expandedNode.parent = 0
                # mark new node in grid
                grid[currentNode.y-1][currentNode.x] = "n"
            self.updatePathCost(currentNode, expandedNode, openList)

        if(currentNode.x+1 <= eastBound and
                grid[currentNode.y][currentNode.x+1] not in ["w", "n"]):
            expandedNode = Node(currentNode.x+1, currentNode.y)
            # mark node with max cost if it's
            # neither in open nor in closed list
            if(not (self.nodeInList(expandedNode, closedList)
                    or self.nodeInList(expandedNode, openList))):
                expandedNode.concreteCost = self.maxCost
                expandedNode.parent = 0
                # mark new node in grid
                grid[currentNode.y][currentNode.x+1]="n"
            self.updatePathCost(currentNode,expandedNode,openList)

        if(currentNode.y+1 <= southBound and
                grid[currentNode.y+1][currentNode.x] not in ["w","n"]):
            expandedNode = Node(currentNode.x,currentNode.y+1)
            #mark node with max cost if it's neither in open nor in closed list
            if(not (self.nodeInList(expandedNode,closedList) or self.nodeInList(expandedNode,openList))):
                expandedNode.concreteCost = self.maxCost
                expandedNode.parent = 0
                #mark new node in grid
                grid[currentNode.y+1][currentNode.x]="n"
            self.updatePathCost(currentNode,expandedNode,openList)

        if(currentNode.x-1 >= westBound and
                grid[currentNode.y][currentNode.x-1] not in ["w","n"]):
            expandedNode = Node(currentNode.x-1,currentNode.y)
            #mark node with max cost if it's neither in open nor in closed list
            if(not (self.nodeInList(expandedNode,closedList) or self.nodeInList(expandedNode,openList))):
                expandedNode.concreteCost = self.maxCost
                expandedNode.parent = 0
                #mark new node in grid
                grid[currentNode.y][currentNode.x-1]="n"
            self.updatePathCost(currentNode,expandedNode,openList)


    #calculate lowest cost to reach our expandedNode and append it to open list
    def updatePathCost(self,currentNode,expandedNode,openList):
        travelCost = self.concreteCost(currentNode,expandedNode)
        #check if we found a shorter path
        if((currentNode.concreteCost + travelCost) < expandedNode.concreteCost):
            expandedNode.concreteCost = currentNode.concreteCost + travelCost
            expandedNode.parent = currentNode
            expandedNode.f = expandedNode.concreteCost + self.heuristicCost(expandedNode)
            #replace the old node if it already exists since we have found a cheaper path and a better parent :)
            for node in openList:
                if(node.x == expandedNode.x and node.y == expandedNode.y):
                    openList.remove(expandedNode)
            openList.append(expandedNode)
            heapq.heapify(openList)
   

    #prints the nodes we searched, the shortest path we found and the cost of that path
    def printResult(self,goalNode):
        print("searched nodes:")
        for elem in self.grid:
            print(elem)
        #print chosen path
        finalPath = [['.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.'],
               ['.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.'],
               ['.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.'],
               ['.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.'],
               ['.','.','.','.','.','.','.','.','w','.','.','.','.','.','.','.','.','.','.','.'],
               ['.','.','.','.','.','.','.','.',"w",'.','.','.','.','.','.','.','.','.','.','.'],
               ['.','.','.','.','.','.','.','.',"w",'.','.','.','.','.','.','.','.','.','.','.'],
               ['.','.','.','.','.','.','.','.',"w",'.','.','.','.','.','.','.','.','.','.','.'],
               ["w","w","w","w","w","w","w","w","w",'.','.','.','.','.','.','.','.','.','.','.'],
               ['.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.'],
               ['.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.'],
               ['.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.'],
               ['.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.'],
               ['.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.'],
               ['.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.'],
               ['.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.'],
               ['.','.','.','.','.','.','.','.',"w","w","w","w","w","w","w","w","w","w","w","w"],
               ['.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.'],
               ['.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.'],
               ['.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.']]
        #mark goal node with end
        finalPath[goalNode.y][goalNode.x]="E"

        #build list with all visited nodes
        visitedNodes = []
        currentNode = goalNode
        while(currentNode.parent != currentNode):
            visitedNodes.append(currentNode)
            currentNode = currentNode.parent
        visitedNodes.append(currentNode)

        #find all subsequent nodes that have one lower cast and are neighbour of current node
        #until we reach the start node(node.parent==node)
        currentNode = goalNode
        while(currentNode.parent != currentNode):
            for node in visitedNodes:
                if(node.concreteCost == currentNode.concreteCost-1):
                    #print("cost criteria check")
                    if((abs(node.x-currentNode.x)+abs(node.y-currentNode.y))==1):
                        #print("direct neighbour criteria check")
                        currentNode = node
                        break
            finalPath[currentNode.y][currentNode.x]="n"

        #mark start node with start
        finalPath[currentNode.y][currentNode.x]="S"
        print("optimal path: ")
        for elem in finalPath:
            print(elem)
        print("total path concreteCost: "+str(goalNode.concreteCost))

        
    #optimally efficient algorithm to find shortest path
    def aStarSearch(self):
        #closed list(list) to remember visited nodes and openList(prioQ) to chose next node
        openList = []
        closedList = []
        #parent of start node is start node
        currentNode=self.startNode
        #and f consists only of heuristicCost
        currentNode.concreteCost = 0
        currentNode.heuristicCost = self.heuristicCost(startNode)
        currentNode.f = currentNode.heuristicCost
        openList.append(startNode)

        #search all reachable nodes
        while(openList):
            nextNode = heapq.heappop(openList)
            nextNode.parent = currentNode
            #check if we reached our goal
            if(nextNode.x == self.goalNode.x and nextNode.y == self.goalNode.y):
                #mark start and goal node in grid
                grid[self.startNode.y][self.startNode.x]="S"
                self.grid[nextNode.y][nextNode.x]="E"
                nextNode.parent = currentNode
                self.printResult(nextNode)
                return
            #mark node as visited
            closedList.append(nextNode)
            #expand neighbours
            self.expandNeighbours(nextNode,openList,closedList);
            currentNode = nextNode
        #print error message if we didn't reach our goal node
        print("No path was found!")


if __name__ == '__main__':
    #create grid for astar problem "w" stands for wall
    grid = [['.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.'],
               ['.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.'],
               ['.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.'],
               ['.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.'],
               ['.','.','.','.','.','.','.','.','w','.','.','.','.','.','.','.','.','.','.','.'],
               ['.','.','.','.','.','.','.','.',"w",'.','.','.','.','.','.','.','.','.','.','.'],
               ['.','.','.','.','.','.','.','.',"w",'.','.','.','.','.','.','.','.','.','.','.'],
               ['.','.','.','.','.','.','.','.',"w",'.','.','.','.','.','.','.','.','.','.','.'],
               ["w","w","w","w","w","w","w","w","w",'.','.','.','.','.','.','.','.','.','.','.'],
               ['.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.'],
               ['.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.'],
               ['.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.'],
               ['.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.'],
               ['.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.'],
               ['.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.'],
               ['.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.'],
               ['.','.','.','.','.','.','.','.',"w","w","w","w","w","w","w","w","w","w","w","w"],
               ['.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.'],
               ['.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.'],
               ['.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.']]
 
    #create start and goal nodes
    startNode = Node(0,0)
    goalNode = Node(19,19)
    #init grid
    astarGrid = Grid(grid,startNode,goalNode)
    #run A* algorithm
    astarGrid.aStarSearch()

