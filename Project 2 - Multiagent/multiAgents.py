# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


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
        newPos = successorGameState.getPacmanPosition()
        # newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        food = currentGameState.getFood()
        distance = float("-Inf")

        foodList = food.asList()

        if action == 'Stop':
            return float("-Inf")

        for i in range(len(newGhostStates)):
            if newGhostStates[i].getPosition() == tuple(newPos) and (newScaredTimes[i] == 0):
                return float("-Inf")

        for x in foodList:
            distance = max(distance, -1 * (manhattanDistance(newPos, x)))

        return distance
        "*** YOUR CODE HERE ***"

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

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"

        def minValue(gameState, depth, agentIndex):
            minimum = ["", float("inf")]
            actions = gameState.getLegalActions(agentIndex)

            if not actions:
                return self.evaluationFunction(gameState)

            for action in actions:
                currState = gameState.generateSuccessor(agentIndex, action)
                current = value(currState, depth, agentIndex + 1)
                newVal = current[1]
                if newVal < minimum[1]:
                    minimum = [action, newVal]
            return minimum

        def maxValue(gameState, depth, agentIndex):
            maximum = ["", -float("inf")]
            actions = gameState.getLegalActions(agentIndex)

            if not actions:
                return self.evaluationFunction(gameState)

            for action in actions:
                currState = gameState.generateSuccessor(agentIndex, action)
                current = value(currState, depth, agentIndex + 1)
                newVal = current[1]
                if newVal > maximum[1]:
                    maximum = [action, newVal]
            return maximum

        def value(gameState, depth, agentIndex):
            if agentIndex >= gameState.getNumAgents():
                depth += 1
                agentIndex = 0

            if (depth == self.depth or gameState.isWin() or gameState.isLose()):
                return ["", self.evaluationFunction(gameState)]
            elif (agentIndex == 0):
                return maxValue(gameState, depth, agentIndex)
            else:
                return minValue(gameState, depth, agentIndex)

        action = value(gameState, 0, 0)[0]
        return action

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        def minValue(gameState, depth, agentIndex, a, b):
            minimum = ["", float("inf")]
            actions = gameState.getLegalActions(agentIndex)

            if not actions:
                return self.evaluationFunction(gameState)

            for action in actions:
                currState = gameState.generateSuccessor(agentIndex, action)
                current = value(currState, depth, agentIndex + 1, a, b)
                newVal = current[1]
                if newVal < minimum[1]:
                    minimum = [action, newVal]
                if newVal < a:
                    return [action, newVal]
                b = min(b, newVal)
            return minimum

        def maxValue(gameState, depth, agentIndex, a, b):
            maximum = ["", -float("inf")]
            actions = gameState.getLegalActions(agentIndex)

            if not actions:
                return self.evaluationFunction(gameState)

            for action in actions:
                currState = gameState.generateSuccessor(agentIndex, action)
                current = value(currState, depth, agentIndex + 1, a, b)
                newVal = current[1]
                if newVal > maximum[1]:
                    maximum = [action, newVal]
                if newVal > b:
                    return [action, newVal]
                a = max(a, newVal)
            return maximum

        def value(gameState, depth, agentIndex, a, b):
            if agentIndex >= gameState.getNumAgents():
                depth += 1
                agentIndex = 0

            if (depth == self.depth or gameState.isWin() or gameState.isLose()):
                return ["", self.evaluationFunction(gameState)]
            elif (agentIndex == 0):
                return maxValue(gameState, depth, agentIndex, a, b)
            else:
                return minValue(gameState, depth, agentIndex, a, b)

        action = value(gameState, 0, 0, float("-Inf"), float("Inf"))[0]
        return action

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"

        def expectFinder(gameState, depth, agentcounter):
            expectimax = ["", 0]
            actions = gameState.getLegalActions(agentcounter)

            if not actions:
                return self.evaluationFunction(gameState)

            for action in actions:
                currState = gameState.generateSuccessor(agentcounter, action)
                current = expectimant(currState, depth, agentcounter + 1)
                newVal = current[1]
                expectimax[0] = action
                expectimax[1] += newVal
            expectimax[1] = expectimax[1] / len(actions)
            return expectimax

        def maxValue(gameState, depth, agentcounter):
            maximum = ["", -float("inf")]
            actions = gameState.getLegalActions(agentcounter)

            if not actions:
                return self.evaluationFunction(gameState)

            for action in actions:
                currState = gameState.generateSuccessor(agentcounter, action)
                current = expectimant(currState, depth, agentcounter + 1)
                if type(current) is not list:
                    newVal = current
                else:
                    newVal = current[1]
                if newVal > maximum[1]:
                    maximum = [action, newVal]
            return maximum

        def expectimant(gameState, depth, agentcounter):
            if agentcounter >= gameState.getNumAgents():
                depth += 1
                agentcounter = 0

            if (depth == self.depth or gameState.isWin() or gameState.isLose()):
                return ["",self.evaluationFunction(gameState)]
            elif (agentcounter == 0):
                return maxValue(gameState, depth, agentcounter)
            else:
                return expectFinder(gameState, depth, agentcounter)

        actionsList = expectimant(gameState, 0, 0)
        return actionsList[0]

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    position = list(currentGameState.getPacmanPosition())
    foodPos = currentGameState.getFood().asList()
    foodList = []

    for food in foodPos:
        pacmanDist = manhattanDistance(position, food)
        foodList.append(-1 * pacmanDist)

    if not foodList:
        foodList.append(0)

    return currentGameState.getScore() + max(foodList)

# Abbreviation
better = betterEvaluationFunction

