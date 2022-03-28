# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
  """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
  """


  def getAction(self, gameState):
    """
    You do not need to change this method, but you're welcome to.

    getAction chooses among the best options according to the evaluation function.

    Just like in the previous project, getAction takes a GameState and returns
    some Directions.X for some X in the set {North, South, West, East, Stop}
    """
    # Collect legal moves and successor states
    legalMoves = gameState.getLegalActions()

    # Choose one of the best actions
    scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
    bestScore = max(scores)
    bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
    chosenIndex = random.choice(bestIndices) # Pick randomly among the best

    "Add more of your code here if you want to"

    return legalMoves[chosenIndex]

  def evaluationFunction(self, currentGameState, action):
    """
    Design a better evaluation function here.

    The evaluation function takes in the current and proposed successor
    GameStates (pacman.py) and returns a number, where higher numbers are better.

    The code below extracts some useful information from the state, like the
    remaining food (newFood) and Pacman position after moving (newPos).
    newScaredTimes holds the number of moves that each ghost will remain
    scared because of Pacman having eaten a power pellet.

    Print out these variables to see what you're getting, then combine them
    to create a masterful evaluation function.
    """
    # Useful information you can extract from a GameState (pacman.py)
    successorGameState = currentGameState.generatePacmanSuccessor(action)
    newPos = successorGameState.getPacmanPosition() # position after moving (newPos)
    newFood = successorGameState.getFood()  # remaining food (newFood)
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    "*** YOUR CODE HERE ***"
    foodList = newFood.asList()
    for ghost in newGhostStates:
      if manhattanDistance(newPos, ghost.configuration.pos) < 3:
        return -successorGameState.getScore()
    # Two cases 1. Pacman is close to the ghost and will attempt to escape the ghost
    else:
      minVal = 100
      for food in foodList:
        distanceVal = manhattanDistance(food, newPos)
        if distanceVal < minVal:
          minVal = distanceVal
      return successorGameState.getScore() + (1.0 / minVal)



def scoreEvaluationFunction(currentGameState):
  """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
  """
  return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
  """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
  """

  def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
    self.index = 0 # Pacman is always agent index 0
    self.evaluationFunction = util.lookup(evalFn, globals())
    self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
  """
    Your minimax agent (question 2)
  """
  def minValue(self, state, index, counter):
    minVal = float('inf')
    minActions = state.getLegalActions(index)
    successors = []
    nextIndex = (index+1) % (state.getNumAgents())
    for action in minActions:
      successors.append(state.generateSuccessor(index, action))
    for successor in successors:
      val = self.miniMax(successor, nextIndex, counter + 1)
      if val < minVal and val is not None:
        minVal = val

    return minVal

  def maxValue(self, state, index, counter):
    maxVal = -float('inf')
    maxActions = state.getLegalActions(index)
    successors = []
    nextIndex = (index+1) % (state.getNumAgents())
    for action in maxActions:
      successors.append(state.generateSuccessor(index, action))
    for successor in successors:
      val = self.miniMax(successor, nextIndex, counter + 1)
      if val > maxVal and val is not None:
        maxVal = val

    return maxVal

  # This will control wheter to call min or max val and determine if its a leaf node
  def miniMax(self, state, index, counter):
    # Game is complete
    if state.isWin() or state.isLose() or counter > self.depth * state.getNumAgents():
      return self.evaluationFunction(state)
    # Pacman's move
    elif index is 0:
      return self.maxValue(state, index, counter)
    # Ghost's move
    else:
      return self.minValue(state, index, counter)


  def getAction(self, gameState):
    """
      Returns the minimax action from the current gameState using self.depth
      and self.evaluationFunction.

      Here are some method calls that might be useful when implementing minimax.

      gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

      Directions.STOP:
        The stop direction, which is always legal

      gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

      gameState.getNumAgents():
        Returns the total number of agents in the game
    """
    "*** YOUR CODE HERE ***"
    actions = gameState.getLegalActions(0)
    if 'Stop' in actions:
      actions.remove('Stop')
    returnVal = -999999.9
    pacmanAction = None

    for action in actions:
      successor = gameState.generateSuccessor(0, action)
      # index = 1 will start from pacman and counter = 0 will go through all possibilities
      val = self.miniMax(successor, 1, 0)
      if returnVal < val:
        returnVal = val
        pacmanAction = action


    return pacmanAction

class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning (question 3)
  """
  def minValue(self, state, index, counter, alpha, beta):
    minVal = float('inf')
    minActions = state.getLegalActions(index)
    successors = []
    nextIndex = (index+1) % (state.getNumAgents())
    for action in minActions:
      successors.append(state.generateSuccessor(index, action))
    for successor in successors:
      val = self.alphaBeta(successor, nextIndex, counter + 1, alpha, beta)
      beta = min(beta, val)
      if val < minVal and val is not None:
        minVal = val
      if alpha > beta:
        return minVal

    return minVal


  def maxValue(self, state, index, counter, alpha, beta):
    maxVal = -float('inf')
    maxActions = state.getLegalActions(index)
    successors = []
    nextIndex = (index+1) % (state.getNumAgents())
    for action in maxActions:
      successors.append(state.generateSuccessor(index, action))
    for successor in successors:
      val = self.alphaBeta(successor, nextIndex, counter + 1, alpha, beta)
      alpha = max(alpha, val)
      if val > maxVal and val is not None:
        maxVal = val
      if alpha > beta:
        return maxVal

    return maxVal

  # This will control wheter to call min or max val and determine if its a leaf node
  def alphaBeta(self, state, index, counter, alpha, beta):
    # Game is complete
    if state.isWin() or state.isLose() or counter > self.depth * state.getNumAgents():
      return self.evaluationFunction(state)
    # Pacman's move
    elif index is 0:
      return self.maxValue(state, index, counter, alpha, beta)
    # Ghost's move
    else:
      return self.minValue(state, index, counter,  alpha, beta)

  def getAction(self, gameState):
    """
      Returns the minimax action using self.depth and self.evaluationFunction
    """
    "*** YOUR CODE HERE ***"
    actions = gameState.getLegalActions(0)
    if 'Stop' in actions:
      actions.remove('Stop')
    returnVal = -float('inf')
    alpha = -float('inf')
    beta = float('inf')
    pacmanAction = None
    depth = self.depth


    for action in actions:
      successor = gameState.generateSuccessor(0, action)
      # index = 1 will start from pacman and counter = 0 will go through all possibilities
      val = self.alphaBeta(successor, 1, 0, alpha, beta)
      if returnVal < val:
        returnVal = val
        pacmanAction = action

    return pacmanAction

class ExpectimaxAgent(MultiAgentSearchAgent):
  """
    Your expectimax agent (question 4)
  """
  def expValue(self, state, index, counter):
    minVal = float('inf')
    minActions = state.getLegalActions(index)
    successors = []
    nextIndex = (index+1) % (state.getNumAgents())
    for action in minActions:
      successors.append(state.generateSuccessor(index, action))
    listSize = len(successors)
    probability = float(1.0 / listSize)
    expectiVal = 0.0

    for successor in successors:
      val = self.expectiMax(successor, nextIndex, counter + 1)
      expectiVal += (probability * val)
      if expectiVal < minVal and expectiVal is not None:
        minVal = expectiVal

    return minVal

  def maxValue(self, state, index, counter):
    maxVal = -float('inf')
    maxActions = state.getLegalActions(index)
    successors = []
    nextIndex = (index+1) % (state.getNumAgents())
    for action in maxActions:
      successors.append(state.generateSuccessor(index, action))
    for successor in successors:
      val = self.expectiMax(successor, nextIndex, counter + 1)
      if val > maxVal and val is not None:
        maxVal = val

    return maxVal

  # This will control wheter to call min or max val and determine if its a leaf node
  def expectiMax(self, state, index, counter):
    # Game is complete
    if state.isWin() or state.isLose() or counter > self.depth * state.getNumAgents():
      return self.evaluationFunction(state)
    # Pacman's move
    elif index is 0:
      return self.maxValue(state, index, counter)
    # Ghost's move
    else:
      return self.expValue(state, index, counter)

  def getAction(self, gameState):
    """
      Returns the expectimax action using self.depth and self.evaluationFunction

      All ghosts should be modeled as choosing uniformly at random from their
      legal moves.
    """
    "*** YOUR CODE HERE ***"
    actions = gameState.getLegalActions(0)
    if 'Stop' in actions:
      actions.remove('Stop')
    returnVal = -float('inf')
    pacmanAction = None

    for action in actions:
      successor = gameState.generateSuccessor(0, action)
      # index = 1 will start from pacman and counter = 0 will go through all possibilities
      val = self.expectiMax(successor, 1, 0)
      if returnVal < val:
        returnVal = val
        pacmanAction = action

    return pacmanAction






def betterEvaluationFunction(currentGameState):
  """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: I started off by using my eval function from q1 and fine tuning the distance that it would have to be
    to a ghost in order to run away from it
  """

  "*** YOUR CODE HERE ***"
  pos = currentGameState.getPacmanPosition()  # position after moving (newPos)
  food = currentGameState.getFood()  # remaining food (newFood)
  ghostStates = currentGameState.getGhostStates()
  newScaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]
  capsules = len(currentGameState.data.capsules)
  foodList = food.asList()
  remaingFood = len(foodList)
  currentScore = currentGameState.data.score

  stateValue = 0
  for ghost in ghostStates:
    if manhattanDistance(pos, ghost.configuration.pos) < 2:
      return -99999.9
  # Two cases 1.
  # Pacman is close to the ghost and will attempt to escape the ghost
  else:
    closestFood = float('inf')
    for food in foodList:
      distanceVal = manhattanDistance(food, pos)
      if distanceVal < closestFood:
        closestFood = distanceVal
    pelletVal = float('inf')



  powerVal = 0
  if newScaredTimes[0] > 0:
    powerVal = newScaredTimes[0] * 2

  foodInfluence = 0
  if remaingFood is not 0:
    foodInfluence = (1.0 / remaingFood)

  returnValue = currentScore + (1.0 / closestFood) + powerVal + capsules + foodInfluence
  return returnValue



# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
  """
    Your agent for the mini-contest
  """

  def getAction(self, gameState):
    """
      Returns an action.  You can use any method you want and search to any depth you want.
      Just remember that the mini-contest is timed, so you have to trade off speed and computation.

      Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
      just make a beeline straight towards Pacman (or away from him if they're scared!)
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()