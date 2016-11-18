import sys
import copy 

puzzle = []
defPuzzle = [ [1,2,3], [4,0,6], [7,5,8] ]
goalPuzzle = [ [1,2,3], [4,5,6], [7,8,0] ]

class node:
    
    def __init__(self, prev, nxt):
        self.heuristic = 0 
        self.depth = 0
        self.prev = prev
        self.nxt = nxt
    
    def setPuzzle(self, puzzle):
        self.puzzleState = puzzle      
        

def inputRow(rowNo):        #gets input from user, then adds row to puzzle array
    #print '-------------------------------------'
    print rowNo + ' Row '
    print '-------------------------------------'
    noOne = input('Enter the first number of the row: ')
    noTwo = input('Enter the second number of the row: ')
    noThree = input('Enter the third number of the row: ')
    
    row = [noOne, noTwo, noThree]
    print '-------------------------------------'
    puzzle.append(row)

def getRowInput(): #gets user input for three rows
    inputRow('First')   #gets first row from user
    inputRow('Two')     #gets second row from user
    inputRow('Three')   #gets third row from user
    
def displayPuzzle(puzzle):   #displays puzzle
    print puzzle[0][0], puzzle[0][1], puzzle[0][2]
    print puzzle[1][0], puzzle[1][1], puzzle[1][2]
    print puzzle[2][0], puzzle[2][1], puzzle[2][2]

def setNode(node, puzzle, heuristic, depth):
    node.setPuzzle(puzzle)
    node.puzzleState = puzzle
    node.heuristic = heuristic
    node.depth = depth

#from http://interactivepython.org/courselib/static/pythonds/SortSearch/TheMergeSort.html
def mergeSort(alist):
    if len(alist)>1:
        mid = len(alist)//2
        lefthalf = alist[:mid]
        righthalf = alist[mid:]

        mergeSort(lefthalf)
        mergeSort(righthalf)

        i=0
        j=0
        k=0
        while i < len(lefthalf) and j < len(righthalf):
            if (lefthalf[i].heuristic + lefthalf[i].depth) < (righthalf[j].heuristic + righthalf[j].depth):
                alist[k]=lefthalf[i]
                i=i+1
            else:
                alist[k]=righthalf[j]
                j=j+1
            k=k+1

        while i < len(lefthalf):
            alist[k]=lefthalf[i]
            i=i+1
            k=k+1

        while j < len(righthalf):
            alist[k]=righthalf[j]
            j=j+1
            k=k+1

#expands the moves of the current puzzle, this only moves the zero either left, right, up or down
def expand(puzzle): 

    eList = [] #list that will take in moves later created in function

    #for moving zero to the left
    puzzleLeft = copy.deepcopy(puzzle)

    for x in puzzleLeft:
        if (x.count(0) == 1 and (x.index(0) != 0)):
            
            sIndex = x.index(0)
            x[sIndex] = x[sIndex - 1]
            x[sIndex - 1] = 0

            eList.append(puzzleLeft)

    puzzleRight = copy.deepcopy(puzzle)

    #for moving zero to the right
    for x in puzzleRight:
        if (x.count(0) == 1) and (x.index(0) != 2):
           
            sIndex = x.index(0)
         
            x[sIndex] = x[sIndex + 1]
            x[sIndex + 1] = 0

            eList.append(puzzleRight)

    puzzleUp = copy.deepcopy(puzzle)
    
    #for moving zero up
    for x in puzzle:
        if (x.count(0) == 1) and (x != puzzleUp[0]):
           
            sIndex = x.index(0)
       
            if(x == puzzle[1]):
                puzzleUp[1][sIndex] = puzzleUp[0][sIndex]
                puzzleUp[0][sIndex] = 0
                eList.append(puzzleUp)
        
            else:
                puzzleUp[2][sIndex] = puzzleUp[1][sIndex]
                puzzleUp[1][sIndex] = 0
                eList.append(puzzleUp)


    puzzleDown = copy.deepcopy(puzzle)
    #for moving zero down
    for x in puzzle:
     
        if (x.count(0) == 1) and (x != puzzle[2]):
           
            sIndex = x.index(0)
          
            if(x == puzzle[0]):
                puzzleDown[0][sIndex] = puzzleDown[1][sIndex]
                puzzleDown[1][sIndex] = 0
                eList.append(puzzleDown)
            
            else:
                puzzleDown[1][sIndex] = puzzleDown[2][sIndex]
                puzzleDown[2][sIndex] = 0
                eList.append(puzzleDown)

    return eList

#prints the solution with depth, nodes expanded, and maximum queue size
def printSolution(nodesExpanded, node, queuesize):
            print ''
            print "Solution found!!"
            print ''
            print "Expanded a total of", nodesExpanded, "nodes"
            print "Maximum number of nodes in the queue was", queuesize
            print "The depth of the goal node was", node.depth

#function for detecting duplicates
def detectDup(seen, puzzle):
    for x in seen:
        if x == puzzle:
            return True
            
    return False

#uniform cost search
def uCostSearch(puzzle):  

    nodesExpanded = 0
    maxQueueSize = 0
    queue = []
    seen = []
    
    #creates root node
    rootNode = node(None, None)
    setNode(rootNode, puzzle, 1, 0) #node, puzzle, heuristic, depth
    
    #adds root node to queue
    queue.append(rootNode)
    
    print 'Solving puzzling with uniform cost search...'
    
    while 1:

        if (len(queue) == 0):
            print "Puzzle search exhausted"
            sys.exit(0)

        checkNode = node(queue[0].prev, queue[0].nxt)
        setNode(checkNode, queue[0].puzzleState, queue[0].heuristic, queue[0].depth) #node, puzzle, heuristic, depth
    
        print ''
        print "The best node to expand with g(n) =", checkNode.depth, "and h(n) =", checkNode.heuristic, "is..."
        displayPuzzle(checkNode.puzzleState)
        print "Expanding this node..."
        
        queue.pop(0)
        
        if (goalPuzzle == checkNode.puzzleState):
            print '-------------------------------------'
            printSolution(nodesExpanded, checkNode, maxQueueSize)
            
            currNode = checkNode
            
            #traceback from solution
            print '-------------------------------------'
            print "Tracing back...\n"
            while currNode is not None:
                displayPuzzle(currNode.puzzleState)
                print ''
                currNode = currNode.prev
                
            print 'Route traced'
            print '-------------------------------------'
            return
        
        #detect duplicates, if dup found, continue loop from start
        if not detectDup(seen, checkNode.puzzleState):
            expandedPuzzle = expand(checkNode.puzzleState)
        else:
            continue
        
        #append to queue only if not seen before
        seen.append(checkNode.puzzleState)
        
        for x in expandedPuzzle:
            
            eNode = node(checkNode, None)
            setNode(eNode, x, 1, checkNode.depth + 1) #node, puzzle, heuristic, depth
           
            #detect duplicates, if dup found, continue loop from start
            if not detectDup(seen, x):        
                queue.append(eNode)
            else:
                continue
            
            #every node append to queue is from the expand function, so this keep tracks the amount expanded nodes
            nodesExpanded += 1
            
            #if found goal state when expanding, solution is found
            if x == goalPuzzle:
                print '-------------------------------------'
                printSolution(nodesExpanded, eNode, maxQueueSize)
                
                currNode = eNode
                
                print '-------------------------------------'
                #traceback from solution
                print "Tracing back...\n"
                while currNode is not None:
                    print 'Current Depth: ' + str(currNode.depth)
                    displayPuzzle(currNode.puzzleState)
                    print ''
                    currNode = currNode.prev
                print 'Route traced'
                print '-------------------------------------'
                
                return
                
            if(len(queue) > maxQueueSize):
                maxQueueSize = len(queue)

def misplacedTiles(puzzle):
    
    misplace = 0
    for x in range(3):
        for y in range(3):
            # make sure we don't check blank
            if puzzle[x][y] != 0:
                # if it's not at it's proper place, it's misplaced
                if puzzle[x][y] != goalPuzzle[x][y]:
                    misplace += 1

    return misplace
    
def misplacedAStar(puzzle):   #A* with the misplaced tile heuristic
    nodesExpanded = 0
    maxQueueSize = 0
    queue = []
    seen = []
    
    print 'Solving puzzle with misplaced tiles A*...'
    
    #creates root node
    rootNode = node(None, None)
    
    setNode(rootNode, puzzle, misplacedTiles(puzzle), 0) #node, puzzle, heuristic, depth
    
    #adds root node to queue
    queue.append(rootNode)
    
    while 1:

        if (len(queue) == 0):
            print "Puzzle search exhausted"
            sys.exit(0)

        checkNode = node(queue[0].prev, queue[0].nxt)
        setNode(checkNode, queue[0].puzzleState, queue[0].heuristic, queue[0].depth) #node, puzzle, heuristic, depth
    
        print ''
        print "The best node to expand with g(n) =", checkNode.depth, "and h(n) =", checkNode.heuristic, "is..."
        displayPuzzle(checkNode.puzzleState)
        print "Expanding this node..."
        
        queue.pop(0)
        
        if (goalPuzzle == checkNode.puzzleState):
            
            print '-------------------------------------'
            printSolution(nodesExpanded, checkNode, maxQueueSize)
            
            #traceback from solution
            currNode = checkNode
            print '-------------------------------------'    
            print "Tracing back...\n"
            
            while currNode is not None:
                print 'Current Depth: ' + str(currNode.depth)
                displayPuzzle(currNode.puzzleState)
                print ''
                currNode = currNode.prev
            
            print 'Route traced'
            print '-------------------------------------'
            #e = rawinput("Press anything to exit...")
            return
        
        #detect duplicates, if dup found, continue loop from start
        if not detectDup(seen, checkNode.puzzleState):
            expandedPuzzle = expand(checkNode.puzzleState)
        else:
            continue
        
        #append to queue only if not seen before
        seen.append(checkNode.puzzleState)
        
        for x in expandedPuzzle:
            
            eNode = node(checkNode, None)
            setNode(eNode, x, misplacedTiles(x), checkNode.depth + 1) #node, puzzle, heuristic, depth
           
            #detect duplicates, if dup found, continue loop from start
            if not detectDup(seen, x):        
                queue.append(eNode)
            else:
                continue
            
            #every node append to queue is from the expand function, so this keep tracks the amount expanded nodes
            nodesExpanded += 1
            
            #if found goal state when expanding, solution is found
            if x == goalPuzzle:
                print '-------------------------------------'
                printSolution(nodesExpanded, eNode, maxQueueSize)
                print '-------------------------------------'
                currNode = eNode
                print "Tracing back...\n"
                while currNode is not None:
                    print 'Current Depth: ' + str(currNode.depth)
                    displayPuzzle(currNode.puzzleState)
                    print ''
                    currNode = currNode.prev
                print 'Route traced'
                print '-------------------------------------'   
                #e = rawinput("Press anything to exit...")
                return
                
            if(len(queue) > maxQueueSize):
                maxQueueSize = len(queue)

        mergeSort(queue)


def manhattan(puzzle):

    mDistance = 0
    puzzleContents = [1, 2, 3, 4, 5, 6, 7, 8]
    # search through the numbers in the puzzle
    for x in puzzleContents:
        for i in range(3):
            for j in range(3):
                # get where the number should be
                if (x == goalPuzzle[i][j]):
                    goalRow = i
                    goalCol = j
                # get where the number is now
                if (x == puzzle[i][j]):
                    puzzleRow = i
                    puzzleCol = j
        # calculate the Manhattan Distance based on the points (row/col)
        mDistance += ( abs(goalRow - puzzleRow) + abs(goalCol - puzzleCol) )

    return mDistance
    
def manhattanAStar(puzzle):   #A* with the manhattan distance heuristic
    nodesExpanded = 0
    maxQueueSize = 0
    queue = []
    seen = []
    
    #creates root node
    rootNode = node(None, None)
    
    setNode(rootNode, puzzle, manhattan(puzzle), 0) #node, puzzle, heuristic, depth
    
    #adds root node to queue
    queue.append(rootNode)
    print 'Solving puzzle with manhattan A* ...'
    
    while 1:

        if (len(queue) == 0):
            print "Puzzle search exhausted"
            sys.exit(0)

        checkNode = node(queue[0].prev, queue[0].nxt)
        setNode(checkNode, queue[0].puzzleState, queue[0].heuristic, queue[0].depth) #node, puzzle, heuristic, depth
    
        print ''
        print "The best node to expand with g(n) =", checkNode.depth, "and h(n) =", checkNode.heuristic, "is..."
        displayPuzzle(checkNode.puzzleState)
        print "Expanding this node..."
        
        queue.pop(0)
        
        if (goalPuzzle == checkNode.puzzleState):
            print '-------------------------------------'   
            printSolution(nodesExpanded, checkNode, maxQueueSize)
            
            currNode = checkNode
            #traceback from solution
            print '-------------------------------------'       
            print "Tracing back...\n"
            while currNode is not None:
                print 'Current Depth: ' + str(currNode.depth)
                displayPuzzle(currNode.puzzleState)
                print ''
                currNode = currNode.prev
            print 'Route traced'
            print '-------------------------------------'       
            return
        
        #detect duplicates, if dup found, continue loop from start
        if not detectDup(seen, checkNode.puzzleState):
            expandedPuzzle = expand(checkNode.puzzleState)
        else:
            continue
        
        #append to queue only if not seen before
        seen.append(checkNode.puzzleState)
        
        for x in expandedPuzzle:
            
            eNode = node(checkNode, None)
            setNode(eNode, x, manhattan(x), checkNode.depth + 1) #node, puzzle, heuristic, depth
           
            #detect duplicates, if dup found, continue loop from start
            if not detectDup(seen, x):        
                queue.append(eNode)
            else:
                continue
            
            #every node append to queue is from the expand function, so this keep tracks the amount expanded nodes
            nodesExpanded += 1
            
            #if found goal state when expanding, solution is found
            if x == goalPuzzle:
                print '-------------------------------------'           
                printSolution(nodesExpanded, eNode, maxQueueSize)
                print '-------------------------------------'           
                
                currNode = eNode
                print "Tracing back...\n"
                #traceback from solution
                while currNode is not None:
                    print 'Current Depth: ' + str(currNode.depth)
                    displayPuzzle(currNode.puzzleState)
                    print ''
                    currNode = currNode.prev
                print 'Route traced'
                print '-------------------------------------'           

                return
                
            if(len(queue) > maxQueueSize):
                maxQueueSize = len(queue)
        
        mergeSort(queue)

def testAlgorithm(algChoice, p): #function used to decide which algorithm to use based on user input
    if algChoice == 1:
        uCostSearch(p)
    elif algChoice == 2:
        misplacedAStar(p)
    elif algChoice == 3:
        manhattanAStar(p)
    
def main(): #main function
    custom = False
    print '\nWelcome to Brian Nguyen\'s 8-puzzle solver.'
    puzzleChoice = input('Type "1" to use a default puzzle, or "2" to enter your own puzzle: ')
    
    if puzzleChoice == 1: #default puzzle
        print 'Default'
        displayPuzzle(defPuzzle)    #prints puzzle
        mainPuzzle = defPuzzle

    else:   #custom puzzle
        print 'Enter your puzzle, use a zero to represent a blank. There are three rows, and three columns'
        getRowInput()           #get puzzle input
        displayPuzzle(puzzle)   #prints puzzle
        mainPuzzle = puzzle    
        custom = True 

    #ask user to decide what algorithm to use to solve puzzle
    algChoice = input('Enter your choice of algorithm\n Type "1" for Uniform Cost\n Type "2" for A* with the Misplace Tile heristic\n Type "3" for A* with the Manhattan distance heuristic: ')
    
    if custom:
        testAlgorithm(algChoice, puzzle)
    else:
        testAlgorithm(algChoice, defPuzzle)
    
#main function
main()
