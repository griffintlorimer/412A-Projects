# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first
    [2nd Edition: p 75, 3rd Edition: p 87]

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm
    [2nd Edition: Fig. 3.18, 3rd Edition: Fig 3.7].

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    currentState = problem.getStartState()
    nodeStack = util.Stack()
    directionStack = util.Stack()
    listOfVistitedNodes = []
    directionStack.push([])
    nodeStack.push(currentState)

    while nodeStack:
        currentState = nodeStack.pop()
        if not directionStack.isEmpty():
            currentDirections = directionStack.pop()

        if problem.isGoalState(currentState):
            return currentDirections

        if not listOfVistitedNodes.__contains__(currentState):
            children = problem.getSuccessors(currentState)
            listOfVistitedNodes.append(currentState)
            for child in children:
                newDirection = []
                for direction in currentDirections:
                    newDirection.append(direction)
                newDirection.append(child[1])
                directionStack.push(newDirection)
                nodeStack.push(child[0])




def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    [2nd Edition: p 73, 3rd Edition: p 82]
    """
    "*** YOUR CODE HERE ***"
    currentState = problem.getStartState()
    nodeQueue = util.Queue()
    directionQueue = util.Queue()
    listOfVistitedNodes = []
    directionQueue.push([])
    nodeQueue.push(currentState)

    while not nodeQueue.isEmpty():
        currentState = nodeQueue.pop()
        if not directionQueue.isEmpty():
            currentDirections = directionQueue.pop()

        if problem.isGoalState(currentState):
            return currentDirections

        if not listOfVistitedNodes.__contains__(currentState):
            children = problem.getSuccessors(currentState)
            listOfVistitedNodes.append(currentState)
            for child in children:
                newDirection = []
                for direction in currentDirections:
                    newDirection.append(direction)
                newDirection.append(child[1])
                directionQueue.push(newDirection)
                nodeQueue.push(child[0])




def uniformCostSearch(problem):
    "Search the node of least total cost first. "

    # have two PQs where one represents the cost and the node (coordiantes) attached to it while the other one has the cost and directions

    "*** YOUR CODE HERE ***"
    nodeQueue = util.PriorityQueue()
    listOfVistitedNodes = []
    currentState = problem.getStartState()
    nodeQueue.push((currentState, [], 0), 0)

    while nodeQueue:
        currentState = nodeQueue.pop()

        if problem.isGoalState(currentState[0]):
            directions = currentState[1]
            return directions

        if not listOfVistitedNodes.__contains__(currentState[0]):
            children = problem.getSuccessors(currentState[0])
            listOfVistitedNodes.append(currentState[0])
            for child in children:
                newDirections = []
                for direction in currentState[1]:
                    newDirections.append(direction)
                newDirections.append(child[1])
                priority = child[2] + currentState[2]
                nodeQueue.push((child[0], newDirections, priority), priority)



def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    "*** YOUR CODE HERE ***"
    nodeQueue = util.PriorityQueue()
    listOfVistitedNodes = []
    currentState = problem.getStartState()
    nodeQueue.push((currentState, [], 0), 0)

    while nodeQueue:
        currentState = nodeQueue.pop()

        if problem.isGoalState(currentState[0]):
            directions = currentState[1]
            return directions

        if not listOfVistitedNodes.__contains__(currentState[0]):
            children = problem.getSuccessors(currentState[0])
            listOfVistitedNodes.append(currentState[0])
            for child in children:
                newDirections = []
                for direction in currentState[1]:
                    newDirections.append(direction)
                newDirections.append(child[1])
                # g(n) is gVal, h(n) is heuristic(child[0], problem), and f(n) is fVal
                # gVal is the cost to expand that node from the start state, hVal is the estimated distance to the goal, and fVal = gVal + hval
                gVal = child[2] + currentState[2]
                fVal = heuristic(child[0], problem) + gVal
                nodeQueue.push((child[0], newDirections, gVal), fVal)





# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch

def stackToList(stack):
    returnList = []
    while not stack.isEmpty():
        returnList.append(stack.pop())
    return returnList