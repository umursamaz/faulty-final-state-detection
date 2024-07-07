#RANDOM FSM GENERATOR

global GraphvizImportSuccessful

import random
import tarjan

from collections import deque

try:
    from graphviz import Digraph
    from graphviz import render
except Exception as e:
    GraphvizImportSuccessful = False
else:
    GraphvizImportSuccessful = True

class FSM:
    class Node:
        def __init__(self, numOfInputs, index):
            self.transitions = []
            self.index = index 
            self.newGroup=[]

            self.parent = None ## will be used to analyse the traces later
            
            ## initialize the node to have #inputs many transitions
            for i in range(numOfInputs):
                self.transitions.append((None, None)) # Destination and output is empty for now, and index is input

    class GraphNode:
        def __init__(self, nodeTuple):
            self.nodeTuple = nodeTuple

            # connections are NOT two-ways anymore
            self.backwardsConnections = []

        def addBackwardConnection(self, smthing):
            # Here to protect from duplicates
            if smthing not in self.backwardsConnections:
                self.backwardsConnections.append(smthing)


    def __init__(self, numOfStates, numOfInputs, numOfOutputs): #x is range of randomness.
        self.numOfStates = numOfStates
        self.numOfInputs = numOfInputs
        self.numOfOutputs = numOfOutputs

        self.nodes = []
        
        #[[2,5][1,3][4]]
        self.groupsList = None

    def generate(self):
        #Create all the states:
        for i in range(self.numOfStates):
            self.nodes.append(FSM.Node(self.numOfInputs, i))
            
        #Connect them randomly
        for node in self.nodes:
            for i in range(self.numOfInputs):
                destination = random.choice(self.nodes)
                output = random.randint(0, self.numOfOutputs-1)
                node.transitions[i] = (destination, output)

    def get_reverse_transitions(self):
        reverse_transitions = []
        for node in self.nodes:
            reverse_transitions.append([])
        for node in self.nodes:
            for i in range(self.numOfInputs):
                destination = node.transitions[i][0]
                reverse_transitions[destination.index].append(node.index)
        return reverse_transitions
    
    def clear(self):
        while len(self.nodes) > 0:
            del self.nodes[0]

    def isSurelyMinimal(self):
        return self.isMinimal() and self.isMinimalGraph()

    def generateMinimal(self):

        self.generate()

        while not self.isSurelyMinimal(): #if minimality check gives false
            self.clear()
            self.generate()
            
    def generateStronglyConnectedMinimal(self):
        
        self.generate()
        
        adj = self.create_adj_list()
        # self.show(True)
        scc = tarjan.tarjan(adj)
        scc = sorted(scc, key=len, reverse=True)
        print("scc ->", scc)
        
        loops = 0
        operations = 0

        while len(scc) != 1:
            print("Multiple groups, trying connections")
            loops += 1
            for i in range(1, len(scc)):
                rt = self.get_reverse_transitions()
                group_node = scc[i][0]
                
                # Check reverse transitions of this node to see if there are any incoming transitions
                incoming = False
                for i in rt[group_node]:
                    if i != group_node:
                        incoming = True
                
                if not incoming:
                    operations += 1
                    # Choose a random node to connect to this one
                    node_index = random.choice(scc[0])
                    # Choose a random transition
                    transition_index = random.randint(0, self.numOfInputs-1)
                    
                    # Connect it back here
                    self.nodes[node_index].transitions[transition_index] = (self.nodes[group_node], self.nodes[node_index].transitions[transition_index][1])
                    print("i Connected the", transition_index, "transition of", node_index, "to", group_node)
                    
                outgoing = False
                for transition in self.nodes[group_node].transitions:
                    if transition[0].index != group_node:
                        outgoing = True
                
                if not outgoing:
                    operations += 1
                    # Choose a random node to connect to this one
                    node_index = random.choice(scc[0])
                    # Choose a random transition
                    transition_index = random.randint(0, self.numOfInputs-1)
                    
                    self.nodes[group_node].transitions[transition_index] = (self.nodes[node_index], self.nodes[group_node].transitions[transition_index][1])
                    print("o Connected the", transition_index, "transition of", group_node, "to", node_index)
                
                if incoming and outgoing:
                    operations += 1
                    if random.randint(1, 2) == 1:
                        node_index = random.choice(scc[0])
                        # Choose a random transition
                        transition_index = random.randint(0, self.numOfInputs-1)
                        
                        # Connect it back here
                        self.nodes[node_index].transitions[transition_index] = (self.nodes[group_node], self.nodes[node_index].transitions[transition_index][1])
                        print("ii Connected the", transition_index, "transition of", node_index, "to", group_node)
                    else:
                        # Choose a random node to connect to this one
                        node_index = random.choice(scc[0])
                        # Choose a random transition
                        transition_index = random.randint(0, self.numOfInputs-1)
                        
                        self.nodes[group_node].transitions[transition_index] = (self.nodes[node_index], self.nodes[group_node].transitions[transition_index][1])
                        print("oo Connected the", transition_index, "transition of", group_node, "to", node_index)
                    
            adj = self.create_adj_list()
            # self.show()
            scc = tarjan.tarjan(adj)
            scc = sorted(scc, key=len, reverse=True)
            print("scc ->", scc)

        print("Done!")
        print("Loops ->", loops, " Operations ->", operations)
        print("Is minimal =>", self.isSurelyMinimal())
        
        while not self.isSurelyMinimal():
            self.clear()
            self.generateStronglyConnectedMinimal()
    
    def create_adj_list(self):
        adj_list = {}
        
        for node in self.nodes:
            adj_list[node.index] = []
            for transition in node.transitions:
                adj_list[node.index].append(transition[0].index)
        return adj_list

    def generateRandomTrace(self, length=10, startNode=-1):
        # Generates an input trace
        # Returns a list of tuples with the format [(input, output)]

        if 0 <= startNode and startNode < len(self.nodes): 
            currentNode = self.nodes[startNode]
        else:
            currentNode = random.choice(self.nodes)

        traceList = []

        for i in range(length):
            randomInput = random.randint(0, self.numOfInputs-1)
            traceList.append((randomInput, currentNode.transitions[randomInput][1]))
            currentNode = currentNode.transitions[randomInput][0]

        return traceList

    def show(self, reverse=False):
        for node in self.nodes:
            print("Node:", node.index, ":")
            print("[", end="")
            for i in range(len(node.transitions)):
                print("(input:{}, to:{}, output:{})".format(i, node.transitions[i][0].index, node.transitions[i][1]), end="")
            print("]")
        if reverse:
            rt = self.get_reverse_transitions()
            for node_index in range(self.numOfStates):
                print("Node:", node_index, "goes to: ", end="")
                for dest in rt[node_index]:
                    print(" Node", dest, end="")
                print()
            
    def output_for_ads(self, filename='ads_example.dot'):
        """
        Very similar to FSM.show()
        
        outputs the fsm into a file with the format given in the example of hybrid_ads (../examples/lee_yannakakis_distinguishable.dot)

        Args:
            filename (str, optional): Name of the output file. Defaults to 'ads_example.dot'.
        """

        # node number -> node.index
        # transitions:
        #       goes to -> node.transitions[input][0] (another node object)
        #       output  -> node.transitions[input][1] 
        
        input_mapper = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        with open(filename, 'w') as file:
            file.write('digraph distinguishable {\n')
            for inp in range(self.numOfInputs):
                for node in self.nodes:
                    # target format = { s1 -> s2 [label="a / 0"]; }
                    file.write(f'\ts{node.index} -> s{node.transitions[inp][0].index} [label="{input_mapper[inp]} / {node.transitions[inp][1]}"];\n')
                if not inp == self.numOfInputs-1:
                    file.write('\n')
            file.write('}')
        print(f'successfully wrote the example into {filename}')

    def draw(self, _filename = "fsm", makePng = False):

        if not GraphvizImportSuccessful:
            print("You need to successfully install graphviz to use draw method")
            return 

        f = Digraph("Finite_State_Machine", filename= _filename+".gv")

        f.attr("node", shape="circle")

        for node in self.nodes:
            for i in range(self.numOfInputs):
                if (node.transitions[i][0] != None):
                    f.edge(str(node.index), str(node.transitions[i][0].index), label="i:{}/o:{}".format(i, node.transitions[i][1]))

        try:
            f.view() #Tries to view the graph
        except Exception as e:
            print(e)
            print("Unable to draw the graph")
            return


        if makePng:
            render("dot", "png", _filename+".gv") # Makes a png file
        
    def isMinimalGraph(self):

        self.createGraphNodes()
        self.connectGraphNodes()

        return self.searchInGraphNodes()

    def createGraphNodes(self):
        """ Create the graph """

        self.graphNodes = {} #keys are the actual node tuples and values are the indexes of them


        # The ultimate node
        self.graphNodes["SeparableNode"] = FSM.GraphNode("(Separable, Node)")

        # loop over all pairs and create graph nodes
        for i in range(len(self.nodes)):
            for j in range(i+1, len(self.nodes)):
                self.graphNodes[(self.nodes[i], self.nodes[j])] = FSM.GraphNode((self.nodes[i].index, self.nodes[j].index))

        #for node in self.graphNodes:
        #    print(self.graphNodes[node].nodeTuple)


    def connectGraphNodes(self):
        """ Connect the Graph """

        for graphNodeKey in self.graphNodes:

            if graphNodeKey == "SeparableNode":
                continue

            node1 = graphNodeKey[0]
            node2 = graphNodeKey[1]

            for i in range(self.numOfInputs): #Check each transition

                # Check the outputs
                if (node1.transitions[i][1] != node2.transitions[i][1]): # if different outputs
                    self.graphNodes["SeparableNode"].backwardsConnections.append(graphNodeKey)

                else: # Outputs are same

                    #Check if they go to the same state
                    if (node1.transitions[i][0].index == node2.transitions[i][0].index):
                        # No transitions added in this case
                        continue

                    else: # They go to different places

                        #This is needed because the smaller indexed node is always the first in the graphNodes dictionary
                        if (node1.transitions[i][0].index < node2.transitions[i][0].index):
                            placeTheyGoTo = (node1.transitions[i][0], node2.transitions[i][0])
                        else:
                            placeTheyGoTo = (node2.transitions[i][0], node1.transitions[i][0])

                        self.graphNodes[placeTheyGoTo].backwardsConnections.append(graphNodeKey)

        #for node in self.graphNodes:
        #    print(self.graphNodes[node], self.graphNodes[node].connections)


    def searchInGraphNodes(self):
        """ Search The Graph """

        startnode = "SeparableNode"

        visited = []

        queue = deque()
        #queue = [] # Append to the end, delete from the front

        finished = False
        
        queue.append(self.graphNodes[startnode])

        while not finished:

            if len(queue) == 0:
                finished = True
                continue

            currNode = queue[0]

            for connection in currNode.backwardsConnections:
                
                connection = self.graphNodes[connection]

                if ((connection not in visited) and (connection not in queue)):

                    queue.append(connection)
            
            visited.append(currNode)

            queue.popleft()

        if len(self.graphNodes) == len(visited):
            return True

        return False

    def printGroup(self):

        for lis in self.groupsList:
            print("(", end="")
            for node in lis:
                print(node.index, end="")
            print(")", end="")
        print("")


    def divideWithOutputs(self):

        self.groupsList = []

        self.groupsList = [[self.nodes[0]]] #initialize with one node

        for i in range(1, len(self.nodes)): #for each node

            for j in range(len(self.groupsList)): #check each group
                match = True
                for k in range(len(self.nodes[i].transitions)): #compare each output
            
                    if (self.nodes[i].transitions[k][1] != self.groupsList[j][0].transitions[k][1]): #if some outputs dont match
                        match = False
                        break

                if match: #All outputs matched, add to group, exit this loop
                    self.groupsList[j].append(self.nodes[i])
                    break

            if not match: #No group matched, create new group

                self.groupsList.append([self.nodes[i]])

        """
        for i in range(len(self.groupsList)):
            print("[", end="")
            for k in range(len(self.groupsList[i])):
                print(self.groupsList[i][k].index, end="")
            print("]")
        """

    def isMinimal(self):

        self.divideWithOutputs()
        
        
        
        temp = []
        temp2 = []
        
        Divide = True
        while(Divide):
            for i in range(len(self.groupsList)): #for every group
                for j in range(len (self.groupsList[i])): #for every elements in the group 
                    self.groupsList[i][j].newGroup = i 
                    #print(self.groupsList[i][j].index, self.groupsList[i][j].newGroup)

                    
            for i in range(len(self.groupsList)):
                samegroup = True
                temp2.append(self.groupsList[i][0]) #add first element of the ith list.
                temp.append(temp2)
                temp2 = []
                
                blockStart = len(temp)-1
                
                for j in range(1, len(self.groupsList[i])):
                    group2bePlaced = -1
                    for x in range(blockStart, len(temp)):
                        #print("***")
                        samegroup = True
                        for c in range(len(self.groupsList[i][j].transitions)):
                            if self.groupsList[i][j].transitions[c][0].newGroup != temp[x][0].transitions[c][0].newGroup:
                                #print(group2bePlaced)
                                samegroup = False

                        if samegroup:
                            group2bePlaced = x
                            break
                        
                    if group2bePlaced == -1: #append to new list
                        temp.append([self.groupsList[i][j]])   
                    else:
                        temp[x].append(self.groupsList[i][j]) # append to the corresponding list x.
                        #print("same group, do not divide")
              

            if(len(self.groupsList) == len(temp)):
                Divide =False  #if two lists are the same, no further division, break loop.

            self.groupsList = temp
            temp = []
            #self.printGroup()
        
        """
        for x in range(len(self.groupsList)):#print self.groupsList's elements
            print("[", end="")
            for k in range(len(self.groupsList[x])):
                print(self.groupsList[x][k].index, end="")
            print("]")
        """

        if len(self.groupsList) == self.numOfStates:
            return True

        return False
    
    # def generateStronglyConnected(self):
    #         # Create all the states
    #         for i in range(self.numOfStates):
    #             self.nodes.append(FSM.Node(self.numOfInputs, i))
    #         # Initially connect them to form a simple cycle
    #         for i in range(self.numOfStates):
    #             next_index = (i + 1) % self.numOfStates
    #             self.nodes[i].transitions[0] = (self.nodes[next_index], random.randint(0, self.numOfOutputs - 1))
    #         # Randomize additional transitions to ensure strong connectivity and randomness
    #         for node in self.nodes:
    #             node.transitions[1] = (random.choice(self.nodes), random.randint(0, self.numOfOutputs - 1))
    
    def generateStronglyConnected(self):
            # Create all the states
            for i in range(self.numOfStates):
                self.nodes.append(FSM.Node(self.numOfInputs, i))
            # Initially connect them to form a simple cycle
            for i in range(self.numOfStates):
                next_index = (i + 1) % self.numOfStates
                self.nodes[i].transitions[random.randint(0, self.numOfInputs - 1)] = (self.nodes[next_index], random.randint(0, self.numOfOutputs - 1))
            # Randomize additional transitions to ensure strong connectivity and randomness
            for node in self.nodes:
                for i in range(self.numOfInputs):
                    if node.transitions[i][0] is None:
                        node.transitions[i] = (random.choice(self.nodes), random.randint(0, self.numOfOutputs - 1))
                
                
    
            
if __name__ == "__main__":
    
    fsm = FSM(10,3,5)
    
    fsm.generate()
    fsm.show()

    fsm.clear()
    print("\n\n")

    fsm.generateMinimal() #We can use this now
    fsm.draw()
    fsm.show()
