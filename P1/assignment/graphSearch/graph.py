from collections import deque
import collections
from prettytable import PrettyTable
import utils
import heapq

#the goal for this module here is to use a graph and implement bfs dfs and ufs in python
class Node:

    #attributes also don't have to be declared when they are used in construct

    #in python only one constructor exists, if you want to init "default constructor use default values like var=value in parameterlist
    def __init__(self,name):
        self.parent = 0
        self.name = name
        self.edges = []
        self.value = 0

    #declare __lt__ method to handle comparision between two objects of this class
    def __lt__(self, other):
        return self.value < other.value

class Edge:

    #start = start node; end = end node; value = path cost;
    def __init__(self, edge):
        self.start = edge[0]
        self.end = edge[1]
        self.value = edge[2]

class Graph:


    #fifo(queue using deque() from collections for better runtime)
    #lifo(stack using list since it's implemented like a stack)
    #prioQ(prioQ using heapq
    def __init__(self, node_list, edges):
        self.nodes = []
        #add names of all our nodes to node list
        for name in node_list:
            self.nodes.append(Node(name))

        #init edges with correct values
        for e in edges:
            e = (utils.getNode(e[0],self.nodes), utils.getNode(e[1], self.nodes), e[2])

            #make sure we add edge A -> B as well as B -> A
            self.nodes[next((i for i,v in enumerate(self.nodes) if v.name == e[0].name), -1)].edges.append(Edge(e))
            self.nodes[next((i for i,v in enumerate(self.nodes) if v.name == e[1].name), -1)].edges.append(Edge((e[1], e[0], e[2])))
            #isn't this one bracket to much at line 48 at the end?


    def Print(self):
        node_list = self.nodes
        node_list.sort(key=lambda x : x.name)

        t = PrettyTable(['  '] +[i.name for i in node_list])
        for node in node_list:
            edge_values = ['X'] * len(node_list)
            for edge in node.edges:
                edge_values[ next((i for i,e in enumerate(node_list) if e.name == edge.end.name))] = edge.value
            t.add_row([node.name] + edge_values)
        print(t)


    def PrintCostAndPath(self,mode,endNode):
        currentNode=endNode
        cost=0
        result = []
        while(currentNode.parent != currentNode):
            result.append(currentNode.name)
            #get cost of path to parent
            for edge in currentNode.edges:
                if((edge.start == currentNode) and (edge.end == currentNode.parent)):
                        cost += edge.value
            currentNode = currentNode.parent
        result.append(currentNode.name)
        result.reverse()
        print(f"Search mode: {mode} Path that was found: {result} cost for the path: {cost}.")


    def ExpandNodesBFS(self,queue,visited,node):
        #expand all children that have not been visited and set parent
        for edge in node.edges:
            #edge[X].start edge[X].end edge[X].value
            if(edge.end not in visited):
                edge.end.parent=node
                queue.append(edge.end)


    def BFS(self,start,end):
        #breadth-first-search the graph from start node to end node
        queue = deque() #append to right and pop from left from the frontier (= 'Grenze', komische Bennenung?)
        visited = [] #store nodes we have visited already
        currentNode = start
        #set parent to itself only for the start node
        currentNode.parent = start
        while True:
            visited.append(currentNode)
            self.ExpandNodesBFS(queue,visited,currentNode)
            #return fail if frontier queue is empty
            if(len(queue)==0):
                return print('No path was found!')
            #take next node out of frontier
            nextNode = queue.popleft()
            currentNode = nextNode
            #check if we reached our goal
            if(currentNode == end):
                break
        self.PrintCostAndPath('BFS',currentNode)


    def ExpandNodesDFS(self,queue,visited,node):
        #expand the children that has not been visited and set parent
        for edge in node.edges:
            #edge[X].start edge[X].end edge[X].value
            if(edge.end not in visited):
                edge.end.parent=node
                queue.append(edge.end)


    def DFS(self,start,end):
        #depth-first-search the graph from start node to end node
        stack = [] #append to right and pop from right of the frontier
        visited = [] #store nodes we have visited already
        currentNode = start
        #set parent to itself only for the start node
        currentNode.parent = start
        while True:
            visited.append(currentNode)
            self.ExpandNodesDFS(stack,visited,currentNode)
            #return fail if frontier queue is empty
            if(len(stack)==0):
                return print('No path was found!')
            #take next node out of frontier
            nextNode = stack.pop()
            currentNode = nextNode
            #check if we reached our goal
            if(currentNode == end):
                break
        self.PrintCostAndPath('DFS',currentNode)


    def ExpandNodesUCS(self,queue,visited,node):
        #expand the children that have not been visited
        for edge in node.edges:
            #edge[X].start edge[X].end edge[X].value
            if (edge.end not in visited) and (edge.end not in queue):
                edge.end.parent = node
                edge.end.value = edge.value+self.getPathCost(edge.end)
                heapq.heappush(queue,edge.end)
            elif edge.end in queue:
                #get current value of item in queue
                maxIndex = queue.index(edge.end)
                maxElement = queue[maxIndex]
                maxValue = self.getPathCost(maxElement)
                #calc new path value
                newValue = edge.value + self.getPathCost(node)
                #if its smaller set correct values and heapify
                if newValue < maxValue:
                    maxElement.parent=node
                    heapq.heapify(queue)


    def getPathCost(self,node):
        currentNode = node
        cost =0
        while(currentNode.parent != currentNode):
            #get cost of path to parent
            for edge in currentNode.edges:
                if((edge.start == currentNode) and (edge.end == currentNode.parent)):
                        cost += edge.value
            currentNode = currentNode.parent
        return cost


    def UCS(self,start,end):
        #uniform-cost-search the graph from start node to end node //kinda funny name since its bfs for graphs that are NOT uniform in cost
        heap = [] #append with heappush and pop smallest with heappop
        visited = [] #store nodes we have visited already
        currentNode = start
        #set parent to itself only for the start node
        currentNode.parent = start
        while True:
            visited.append(currentNode)
            self.ExpandNodesUCS(heap,visited,currentNode)
            #return fail if frontier queue is empty
            if(len(heap)==0):
                return print('No path was found!')
            #take next node out of frontier
            nextNode = heapq.heappop(heap)
            currentNode = nextNode
            #check if we reached our goal
            if(currentNode == end):
                break
        self.PrintCostAndPath('UCS',currentNode)




#initialise Graph and try printing it
if __name__ == '__main__':
    romania = Graph( ['Or', 'Ne', 'Ze', 'Ia', 'Ar', 'Si', 'Fa',
        'Va', 'Ri', 'Ti', 'Lu', 'Pi', 'Ur', 'Hi',
        'Me', 'Bu', 'Dr', 'Ef', 'Cr', 'Gi'],
        [
            ('Or', 'Ze', 71), ('Or', 'Si', 151),
            ('Ne', 'Ia', 87), ('Ze', 'Ar', 75),
            ('Ia', 'Va', 92), ('Ar', 'Si', 140),
            ('Ar', 'Ti', 118), ('Si', 'Fa', 99),
            ('Si', 'Ri', 80), ('Fa', 'Bu', 211),
            ('Va', 'Ur', 142), ('Ri', 'Pi', 97),
            ('Ri', 'Cr', 146), ('Ti', 'Lu', 111),
            ('Lu', 'Me', 70), ('Me', 'Dr', 75),
            ('Dr', 'Cr', 120), ('Cr', 'Pi', 138),
            ('Pi', 'Bu', 101), ('Bu', 'Gi', 90),
            ('Bu', 'Ur', 85), ('Ur', 'Hi', 98),
            ('Hi', 'Ef', 86)
        ])
    romania.Print()
    startNode = utils.getNode('Bu',romania.nodes)
    endNode = utils.getNode('Ti',romania.nodes)
    romania.BFS(startNode,endNode)
    romania.DFS(startNode,endNode)
    romania.UCS(startNode,endNode)

