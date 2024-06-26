from randomfsmgenerator import FSM
from collections import deque
import random
import subprocess
import time

global PyCryptoSat_Import_Successful
try:
    from pycryptosat import Solver
    PyCryptoSat_Import_Successful = True
except Exception as e:
    print("Couldn't import pycryptosat")
    PyCryptoSat_Import_Successful = False


class FileHandler:

    """
    Helps with writing a sat file in more readable fashion
    The first line of a file must be decided last
    So this class takes everything to the front or back of a list
    And writes the file last
    """

    def __init__(self, filename):

        self.filename = filename

        self.fileBuffer = deque() # Put to right take from left

    def write(self, what):

        self.fileBuffer.append(what + " 0\n")

    def writeComment(self, what):

        self.fileBuffer.append("c " + what + "\n")

    def addFirstLine(self, what):

        self.fileBuffer.appendleft(what + "\n")

    def writeTheFile(self):
        # Delete and write everything in deque 

        with open(self.filename, "w") as f:
            while len(self.fileBuffer) != 0:
                f.write(self.fileBuffer.popleft())

class ClauseHandler:

    def __init__(self, filename="SatFile"):
        #for pyCryptoSolver
        self.clauseList = deque()

        self.clausedict = {}
        self.counter = 1

        self.fileBuffer = deque()

        #for the file reading way
        self.filename = filename


    def addClause(self, elements=None):
        #x_0_0, y_0_0_0
        if elements != None:
            temp = []
            for element in elements:
                makeFalse = False
                if element[0] == "-":
                    element = element[1:]
                    makeFalse = True
                if element not in self.clausedict:
                    self.clausedict[element] = self.counter
                    self.counter += 1
                if makeFalse:
                    temp.append(-self.clausedict[element])
                else:
                    temp.append(self.clausedict[element])
            self.clauseList.append(temp)

    def addFirstLine(self, line):
        self.fileBuffer.appendleft(line + "\n")

    def writeTheFile(self):
        with open(self.filename, "w") as f:
            f.write(self.fileBuffer[0])
            while len(self.clauseList) != 0:
                line = ""
                for element in self.clauseList[0]:
                    line += "{} ".format(element)
                line += "0\n"
                f.write(line)
                self.clauseList.popleft()

    def addToSolver(self, solver=None):
        if PyCryptoSat_Import_Successful and solver != None:
            numOfClauses = len(self.clauseList)
            for i in range(numOfClauses):
                clause = self.clauseList.popleft()
                solver.add_clause(clause)

    def pyCrypto(self):
        if PyCryptoSat_Import_Successful:
            s = Solver()
            numOfClauses = len(self.clauseList)
            for i in range(numOfClauses):
                s.add_clause(self.clauseList.popleft)
            sat, solution = s.solve()
            if sat:
                return (sat, solution)
        return (sat, None)

class SatHandler:

    def __init__(self, tracesList, numOfInputs, usePyCrypto=False):

        self.numOfInputs = numOfInputs
        self.tracesList = tracesList
        self.usePyCrypto = usePyCrypto

        self.s = None
        if self.usePyCrypto and PyCryptoSat_Import_Successful:
            self.s = Solver()
            print("Initialized solver")

        self.clauses = ClauseHandler()

        ## Creates the acyclic Fsm of trace nodes.
        self.constructTraceTree() # self.traceTree is created and filled

        self.numOfTraceNodes = len(self.traceTree.nodes)

        ###
        #This variable is used as global, handle with care
        self.numOfNodes = 0
        ###

    def varToNum(self, var):
        x, s = var.split("_")

        return int(x) * self.numOfNodes + int(s) + 1

    def numToVar(self, num):
        num -= 1

        return "{}_{}".format(int(num / self.numOfNodes), num % self.numOfNodes)

    def newVarToNum(self, newVar):
        ## newVar syntax is "y_a_i_j"
        y, a, i, j = newVar.split("_")

        a = int(a)

        # a+1 so that it doesn't clash with normal vars
        offset = (self.numOfTraceNodes * self.numOfNodes) * (a+1) 
        return offset + self.varToNum(i+"_"+j)

    def numToNewVar(self, num):

        offset = self.numOfTraceNodes * self.numOfNodes
        offsetCount = int(num/offset)

        a = offsetCount - 1

        num = num - offset * offsetCount 

        x, s = self.numToVar(num).split("_")
        return "y_{}_{}_{}".format(a, x, s)

    def constructTraceTree(self, nameInBreathFirst = True):

        self.traceTree = FSM(0, self.numOfInputs, 0) # numOfNodes, numOfInputs, numOfOutputs

        rootNode = FSM.Node(self.numOfInputs, 0) # 0 is the index
        self.traceTree.nodes.append(rootNode)

        currentNode = rootNode
        temp = None

        for trace in self.tracesList:

            currentNode = rootNode #reset this
            temp = None

            for ioTuple in trace:

                # This transition exists
                if currentNode.transitions[ioTuple[0]][0] != None: 
                    currentNode = currentNode.transitions[ioTuple[0]][0] # Keep moving

                # This transition is new, create new branch
                else:
                    temp = FSM.Node(self.numOfInputs, len(self.traceTree.nodes))
                    self.traceTree.nodes.append(temp)

                    currentNode.transitions[ioTuple[0]] = (temp, ioTuple[1])

                    currentNode = temp

        ### Name the nodes in a BDF way if the argument is true

        if nameInBreathFirst:
            newNodeList = []

            nodeQ = deque()

            nodeQ.append(rootNode)

            while len(nodeQ) != 0:

                currentNode = nodeQ.popleft()

                for transition in currentNode.transitions:

                    if transition[0] != None:
                        transition[0].parent = currentNode
                        nodeQ.append(transition[0])

                ## Set the index and append to the list
                currentNode.index = len(newNodeList)
                newNodeList.append(currentNode)

            self.traceTree.nodes = newNodeList

    def constructClauses(self, writeToFile=False, filename="SatFile", numOfNodes=-1):
        #This is for debugging
        if numOfNodes != -1:
            self.numOfNodes = numOfNodes

        countClauses = 0

        #
        #Each trace node must correspond to at least one node
        #Does not the 0_0 condition
        #
        for i in range(self.numOfTraceNodes):
            tempList = []
            for k in range(self.numOfNodes):
                tempList.append("x_{}_{}".format(i, k))
            self.clauses.addClause(tempList)
            countClauses += 1

        #
        #Each trace node must correspond to at most one node
        #
        for i in range(self.numOfTraceNodes):
            for k in range(self.numOfNodes - 1):
                for j in range(k + 1, self.numOfNodes):
                    self.clauses.addClause(["-x_{}_{}".format(i,k), "-x_{}_{}".format(i,j)])
                    countClauses += 1

        #
        #Check each transition between tracenodes and act accordingly
        #
        for i in range(self.numOfTraceNodes - 1):
            for j in range(i + 1, self.numOfTraceNodes):
                for k in range(len(self.traceTree.nodes[i].transitions)):

                    # if outputs are not None
                    if (self.traceTree.nodes[i].transitions[k][1] != None and self.traceTree.nodes[j].transitions[k][1] != None):
                        #if outputs are different
                        if (self.traceTree.nodes[i].transitions[k][1] != self.traceTree.nodes[j].transitions[k][1]):

                            for h in range(self.numOfNodes):
                                self.clauses.addClause(["-x_{}_{}".format(i,h), "-x_{}_{}".format(j,h)])
                                countClauses += 1
                            break

        for x in range(self.numOfTraceNodes):
            for a in range(len(self.traceTree.nodes[x].transitions)):
                for i in range(self.numOfNodes):
                    for j in range(self.numOfNodes):
                        if self.traceTree.nodes[x].transitions[a][0] != None:
                            #file.write("y_a_i_j -x_i -x.transitions[a][0]_j")
                            self.clauses.addClause(["y_{}_{}_{}".format(a,i,j), "-x_{}_{}".format(x,i), "-x_{}_{}".format(self.traceTree.nodes[x].transitions[a][0].index, j)])
                            countClauses += 1

        for a in range(len(self.traceTree.nodes[0].transitions)):
            for i in range(self.numOfNodes):
                for h in range(self.numOfNodes - 1):
                    for j in range(h + 1, self.numOfNodes):
                        self.clauses.addClause(["-y_{}_{}_{}".format(a,i,h), "-y_{}_{}_{}".format(a,i,j)])
                        countClauses += 1

        for a in range(len(self.traceTree.nodes[0].transitions)):
            for i in range(self.numOfNodes):
                tempList = []
                for j in range(self.numOfNodes):
                    tempList.append("y_{}_{}_{}".format(a,i,j))

                self.clauses.addClause(tempList)
                countClauses += 1


        for x in range(self.numOfTraceNodes):
            for a in range(len(self.traceTree.nodes[x].transitions)):
                for i in range(self.numOfNodes):
                    for j in range(self.numOfNodes):
                        if self.traceTree.nodes[x].transitions[a][0] != None:
                            self.clauses.addClause(["-y_{}_{}_{}".format(a,i,j), "-x_{}_{}".format(x,i), "x_{}_{}".format(self.traceTree.nodes[x].transitions[a][0].index, j)])
                            countClauses += 1

        if not self.usePyCrypto:
            varCount = self.numOfNodes * self.numOfTraceNodes * (len(self.traceTree.nodes[0].transitions) + 1)
            self.clauses.addFirstLine("p cnf {} {}".format(varCount, countClauses))
            self.clauses.writeTheFile()

    def constructSatFile(self, writeFile=True, filename="SatFile", verbose=True, numOfNodes=-1):

        #This is for debugging
        if numOfNodes != -1:
            self.numOfNodes = numOfNodes

        file = FileHandler(filename)
        clauseHandler = ClauseHandler(filename)

        countClauses = 0

        #
        #Each trace node must correspond to at least one node
        #Contains the 0_0 condition
        #
        
        if verbose:
            file.writeComment("##### Each must correspond to at least one node #####")
        for i in range(self.numOfTraceNodes):
            tempStr = ""
            commentStr = ""
            for k in range(self.numOfNodes): #min(i+1, self.numOfNodes
                tempStr += "{} ".format(self.varToNum("{}_{}".format(i, k)))
                commentStr += "{}_{} ".format(i, k)
            if verbose:
                file.writeComment(commentStr)
            file.write(tempStr)
            countClauses += 1

        #
        #Each trace node must correspond to at most one node
        #
        if verbose:
            file.writeComment("##### Each must correspond to at most one node #####")
        for i in range(self.numOfTraceNodes):
            for k in range(self.numOfNodes - 1):
                for j in range(k + 1, self.numOfNodes):
                    if verbose:
                        file.writeComment("-{}_{} -{}_{}".format(i, k, i, j))
                    file.write("-{} -{}".format(self.varToNum("{}_{}".format(i, k)), self.varToNum("{}_{}".format(i, j))))
                    countClauses += 1
        
        #
        #Check each trasition between tracenodes and act accordingly
        #
        for i in range(self.numOfTraceNodes - 1):
            for j in range(i + 1, self.numOfTraceNodes):
                for k in range(len(self.traceTree.nodes[i].transitions)):

                    # if outputs are not None
                    if (self.traceTree.nodes[i].transitions[k][1] != None and self.traceTree.nodes[j].transitions[k][1] != None):
                        #if outputs are different
                        if (self.traceTree.nodes[i].transitions[k][1] != self.traceTree.nodes[j].transitions[k][1]):

                            for h in range(self.numOfNodes):
                                if verbose:
                                    file.writeComment("-{}_{} -{}_{}".format(i, h, j, h))
                                file.write("-{} -{}".format(self.varToNum("{}_{}".format(i, h)), self.varToNum("{}_{}".format(j, h))))
                                countClauses += 1
                            break
                        #if outputs are same

                        """
                        # The Auxiliary variables will replace these
                        else:
                            iP = self.traceTree.nodes[i].transitions[k][0].index
                            jP = self.traceTree.nodes[j].transitions[k][0].index
                            for h in range(self.numOfNodes):
                                for hP in range(self.numOfNodes):
                                    if verbose:
                                        file.writeComment("-{}_{} -{}_{} -{}_{} {}_{}".format(i, h, j, h, iP, hP, jP, hP))
                                    file.write("-{} -{} -{} {}".format(self.varToNum("{}_{}".format(i, h)),\
                                                                        self.varToNum("{}_{}".format(j, h)),\
                                                                        self.varToNum("{}_{}".format(iP, hP)),\
                                                                        self.varToNum("{}_{}".format(jP, hP))))
                                    countClauses += 1
                        """
                        

        
        for x in range(self.numOfTraceNodes):
            for a in range(len(self.traceTree.nodes[x].transitions)):
                for i in range(self.numOfNodes):
                    for j in range(self.numOfNodes):
                        if self.traceTree.nodes[x].transitions[a][0] != None:
                            #file.write("y_a_i_j -x_i -x.transitions[a][0]_j")
                            file.writeComment("y_{}_{}_{} -{}_{} -{}_{}".format(a, i, j, \
                                                                                x, i, \
                                                                                self.traceTree.nodes[x].transitions[a][0].index, j))
                            file.write("{} -{} -{}".format(self.newVarToNum("y_{}_{}_{}".format(a, i, j)), \
                                                            self.varToNum("{}_{}".format(x, i)), \
                                                            self.varToNum("{}_{}".format(self.traceTree.nodes[x].transitions[a][0].index, j))))
                            countClauses += 1


        for a in range(len(self.traceTree.nodes[0].transitions)):
            for i in range(self.numOfNodes):
                for h in range(self.numOfNodes - 1):
                    for j in range(h + 1, self.numOfNodes):
                        file.writeComment("-y_{}_{}_{} -y_{}_{}_{}".format(a,i,h,\
                                                                            a,i,j))
                        file.write("-{} -{}".format(self.newVarToNum("-y_{}_{}_{}".format(a,i,h)), \
                                                    self.newVarToNum("-y_{}_{}_{}".format(a,i,j))))
                        countClauses += 1

        for a in range(len(self.traceTree.nodes[0].transitions)):
            for i in range(self.numOfNodes):
                tempStr = ""
                commentStr = ""
                for j in range(self.numOfNodes):
                    commentStr += "y_{}_{}_{} ".format(a, i, j)
                    tempStr += "{} ".format(self.newVarToNum("y_{}_{}_{}".format(a, i, j)))

                file.writeComment(commentStr)
                file.write(tempStr)
                countClauses += 1

        for x in range(self.numOfTraceNodes):
            for a in range(len(self.traceTree.nodes[x].transitions)):
                for i in range(self.numOfNodes):
                    for j in range(self.numOfNodes):
                        if self.traceTree.nodes[x].transitions[a][0] != None:
                            #file.write("y_a_i_j -x_i -x.transitions[a][0]_j")
                            file.writeComment("-y_{}_{}_{} -{}_{} {}_{}".format(a, i, j, \
                                                                                x, i, \
                                                                                self.traceTree.nodes[x].transitions[a][0].index, j))
                            file.write("-{} -{} {}".format(self.newVarToNum("y_{}_{}_{}".format(a, i, j)), \
                                                            self.varToNum("{}_{}".format(x, i)), \
                                                            self.varToNum("{}_{}".format(self.traceTree.nodes[x].transitions[a][0].index, j))))
                            countClauses += 1

        varCount = self.numOfNodes * self.numOfTraceNodes * (len(self.traceTree.nodes[0].transitions) + 1)
        file.addFirstLine("p cnf {} {}".format(varCount, countClauses))

        file.writeTheFile()

    def checkOutput(self, filename="satOutput", onlyCheck=False):

        with open(filename, "r") as f:
            
            #if the output has no solution, dont continue
            if f.readline().strip() != "s SATISFIABLE":
                return (False, None)

            #if the output has a solution BUT the onlyCheck parameter is true, dont read the output
            elif onlyCheck:
                return (True, None)

            output = []
            for line in f.readlines():
                for var in line.split()[1:]:
                    if var[0] != "-" and var != "0":
                        output.append(self.numToVar(int(var)))

            return (True, output)

    def addFormulasForSingleVariable(self, traceNo=0, numOfNodes=-1):
        if numOfNodes == -1:
            self.numOfNodes = numOfNodes
        if traceNo == 0:
            print("addFormulasForSingleVariable -> You should gice the traceNo to use this function!")
            return

        #This trace must be at least one of the nodes
        tempList = []
        for k in range(self.numOfNodes):
            tempList.append("x_{}_{}".format(traceNo, k))
        self.clauses.addClause(tempList)

        for k in range(self.numOfNodes - 1):
            for j in range(k + 1, self.numOfNodes):
                self.clauses.addClause(["-x_{}_{}".format(traceNo,k), "-x_{}_{}".format(traceNo,j)])
                countClauses += 1

        for j in range(traceNo):
            for k in range(len(self.traceTree.nodes[traceNo].transitions)):

                # if outputs are not None
                if (self.traceTree.nodes[traceNo].transitions[k][1] != None and self.traceTree.nodes[j].transitions[k][1] != None):
                    #if outputs are different
                    if (self.traceTree.nodes[traceNo].transitions[k][1] != self.traceTree.nodes[j].transitions[k][1]):

                        for h in range(self.numOfNodes):
                            self.clauses.addClause(["-x_{}_{}".format(traceNo,h), "-x_{}_{}".format(j,h)])
                            countClauses += 1
                        break

        for a in range(len(self.traceTree.nodes[traceNo].transitions)):
            for i in range(self.numOfNodes):
                for j in range(self.numOfNodes):
                    if self.traceTree.nodes[traceNo].transitions[a][0] != None:
                        #file.write("y_a_i_j -x_i -x.transitions[a][0]_j")
                        self.clauses.addClause(["y_{}_{}_{}".format(a,i,j), "-x_{}_{}".format(traceNo,i), "-x_{}_{}".format(self.traceTree.nodes[traceNo].transitions[a][0].index, j)])
                        countClauses += 1

        #Auxiliary for this
            for a in range(len(self.traceTree.nodes[traceNo].transitions)):
                for i in range(self.numOfNodes):
                    for j in range(self.numOfNodes):
                        if self.traceTree.nodes[traceNo].transitions[a][0] != None:
                            self.clauses.addClause(["-y_{}_{}_{}".format(a,i,j), "-x_{}_{}".format(traceNo,i), "x_{}_{}".format(self.traceTree.nodes[traceNo].transitions[a][0].index, j)])
                            countClauses += 1

    def oldfindFsmConsecutive(self, filename="SatFile", outputFile="satOutput"):

        self.numOfNodes = 1
        FOUND = False

        startTime = time.time()
        totalSolveTime = 0
        totalFileTime = 0

        while not FOUND:
            print("Trying with", self.numOfNodes, "nodes...")

            if self.usePyCrypto:
                self.s = Solver() #Reinitialize
                sTime = time.time()

                self.constructClauses()
                self.clauses.addToSolver(self.s)
                
                endTime = time.time()-sTime
                totalFileTime += endTime
                print("Sat preperations took", endTime, "seconds")

                sTime = time.time()
                isSatisfiable, output = self.s.solve()
                solveEnd = time.time()-sTime
                totalSolveTime += solveEnd
                print("Solving took", solveEnd, "seconds")

            else:
                sFileTime = time.time()
                
                self.constructClauses()
                
                fileEnd = time.time()-sFileTime
                totalFileTime += fileEnd
                print("Sat file construction took", fileEnd, "seconds")

                solveTime = time.time()
                subprocess.run("cryptominisat5 --verb 0 {} > {}".format(filename, outputFile), shell=True)
                solveEnd = time.time()-solveTime
                totalSolveTime += solveEnd
                print("Solving took", solveEnd, "seconds")

                isSatisfiable, output = self.checkOutput()

            if isSatisfiable:

                print("Satisfiable with", self.numOfNodes, "nodes!")
                print("Total construction time:", totalFileTime, "seconds")
                print("Total solving time:", totalSolveTime, "seconds")
                print("\nConsecutive approach took", time.time()-startTime, "seconds.")
                print()
                FOUND = True



            self.numOfNodes += 1

        return output

    def getFsmFromSolution(self, output):

        switchValueKey = {}
        for key, value in self.clauses.clausedict.items():
            if key[0] == "x":
                switchValueKey[value] = key[2:]

        #init the fsm
        traceFsm = FSM(self.numOfNodes, self.numOfInputs, 0)

        traceToNode = {}
        for i in range(1, len(output)):
            if output[i]: # only check true ones
                ## continu here



    def findFsmConsecutive(self, filename="SatFile", outputFile="satOutput"):

        self.numOfNodes = 7

        FOUND = False

        startTime = time.time()
        totalSolveTime = 0
        totalFileTime = 0

        while not FOUND:


    def findFsmBinary(self, filename="SatFile", outputFile="satOutput"):

        minNumOfNodes = 0
        maxNumOfNodes = -1

        self.numOfNodes = 1

        lastOutput = None
        FOUND = False

        startTime = time.time()

        while not FOUND:

            if maxNumOfNodes == -1:
                self.numOfNodes *= 2
            else:
                self.numOfNodes = int((minNumOfNodes + maxNumOfNodes)/2)

            print("Trying with", self.numOfNodes, "nodes...")

            self.constructSatFile()

            subprocess.run("cryptominisat5 --verb 0 {} > {}".format(filename, outputFile), shell=True)

            isSatisfiable, output = self.checkOutput()

            if isSatisfiable:
                print("Satisfiable with", self.numOfNodes, "nodes!")
                lastOutput = output
                maxNumOfNodes = self.numOfNodes

            else:
                print("Not satisfiable with", self.numOfNodes, "nodes.")
                minNumOfNodes = self.numOfNodes

            if minNumOfNodes == maxNumOfNodes - 1:
                print("Merged at", self.numOfNodes, "nodes!")

                print("\nBinary approach took", time.time()-startTime, "seconds.")

                FOUND = True

        return lastOutput

    def findFsm(self, tryBinarySearch=False, filename="SatFile", outputFile="satOutput"):

        if tryBinarySearch:
            return self.findFsmBinary(filename, outputFile)
        else:
            return self.findFsmConsecutive(filename, outputFile)


def generateSpecialFsm(numOfNodes, numOfInputs, numOfOutputs):

    newFsm = FSM(numOfNodes, numOfInputs, numOfOutputs)

    #Create nodes
    for i in range(7):
        newFsm.nodes.append(FSM.Node(numOfInputs, i))

    #Connect the "a" transitions
    for i in range(7):
        newFsm.nodes[i].transitions[0] = (newFsm.nodes[(i+1)%7], random.randint(0,1))

    #Connect all "b"s randomly
    for i in range(7):
        newFsm.nodes[i].transitions[1] = (random.choice(newFsm.nodes), random.randint(0,1))

    return newFsm

if __name__ == "__main__":

    #random.seed(50)

    #TRACES
    numOfTraces = 1
    traceLength = 1000
    

    #FSM
    numOfNodes  = 13
    numOfInputs = 2
    numOfOutputs= 2

    #myFSM = FSM(numOfNodes, numOfInputs, numOfOutputs)
    #myFSM.generateMinimal()

    myFSM = generateSpecialFsm(numOfNodes, numOfInputs, numOfOutputs)

    #myFSM.draw()

    #Get the traces
    tracesList = []
    for i in range(numOfTraces):
        tracesList.append(myFSM.generateRandomTrace(traceLength, 0))

    #Using sat handler
    SAT = SatHandler(tracesList, numOfInputs, usePyCrypto=True)

    #SAT.traceTree.draw(makePng=True)

    DEBUG = False
    
    if DEBUG:
        
        SAT.constructClauses(numOfNodes=4)

    else:
        output = SAT.findFsm() #Add the param True for binary approach
