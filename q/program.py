import sys
#add parent directory to python path
sys.path.append("..")

import random as r
import prisoner

stateNo = 5
actionNo = 2

iterations = 1

learningRate = 0.2
discountFactor = 0.95

roundNo = 30000
modelNo = 0


#class for a Q learner
class qLearner():

    def __init__(self):
        self.generate()
        self.display()
    

    #init the table with random rewards
    def generate(self):
        qTable = []
        for y in range(0, stateNo):
            row = []
            for x in range(0, actionNo):
                #random float between 0, 1
                row.append(r.uniform(0, 0.5))
            qTable.append(row)
        self.qTable = qTable


    #diplay rewards and compact strategy
    def display(self):
        for y in range(0, stateNo):
            for x in range(0, actionNo):
                print(str(self.qTable[y][x]) + "\t", end = '')
            print()

        outs = ''
        for i in range(0, stateNo):
            if self.qTable[i][0] > self.qTable[i][1]:
                outs += "0"
            else:
                outs += "1"        
        print(outs)


    #use update rule
    def updateTable(self, s, a, sp, r):
        r = r/10
        oldEstimate = (1-learningRate) * self.qTable[s][a]
        newEstimate = learningRate * (r + (discountFactor * self.qTable[sp][self.getAction(sp)]))
        self.qTable[s][a] = oldEstimate + newEstimate
        return


    #find correct state (row in table)
    def getState(self, history):
        state = 0
        #if not first round
        if len(history[0]) > 0:
            state = 1 + (2 * history[0][-1]) + history[1][-1]
        return state


    #choose action with greatest reward (column in table)
    def getAction(self, index):
        largest = self.qTable[index][0]
        index = 0
        for i in range(1, actionNo):
            if self.qTable[index][i] > largest:
                largest = self.qTable[index][i]
                index = i
        return index



#switch player move as a function of roundNo - more exploration at start
def tryExplore(playerMove, n):
    toss = r.uniform(0, 1)
    if toss < (40 - (n/100))/100:
        playerMove = abs(playerMove-1)
    return playerMove



#play roundNo rounds against an opponent
def play(learner, opponent):
    oppHistory = []
    playerHistory = []
    #generate player
    player = prisoner.adaptivePlayer("other")
    
    #initial state
    state = 0


    for i in range(0, roundNo):

        oppMove = opponent.move([oppHistory, playerHistory])
        playerMove = learner.getAction(state)

        #toss coin to see if agent explores
        playerMove = tryExplore(playerMove, i)

        #update history
        oppHistory.append(oppMove)
        playerHistory.append(playerMove)

        #observe rewawrd and new state
        newState = learner.getState([playerHistory, oppHistory])
        reward = player.payoff(playerMove, oppMove)

        #update table
        learner.updateTable(state, playerMove, newState, reward)
        
        state = newState


#entry point
def Main():
    
    strategies = [prisoner.strategies[3]]

    #init a learner to use
    learner = qLearner()
    
    for i in range(0, iterations):        
        #change order of strategies
        r.shuffle(strategies)
        for n in range(0, len(strategies)):
            #play strategy and update table
            play(learner, prisoner.player(strategies[n]))

    #display results
    learner.display()            



Main()
