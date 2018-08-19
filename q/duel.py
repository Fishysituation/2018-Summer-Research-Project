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

roundNo = 5000
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
def play(learner1, learner2):

    hist1, hist2 = [], []
    #generate players
    player1, player2 = prisoner.adaptivePlayer("other"), prisoner.adaptivePlayer("other")
    #initial states
    state1, state2 = 0, 0


    for i in range(0, roundNo):

        move1, move2 = learner1.getAction(state1), learner2.getAction(state2)

        #toss coin to see if agents explore
        move1, move2 = tryExplore(move1, i), tryExplore(move2, i)

        #update history
        hist1.append(move1)
        hist2.append(move2)

        #UPDATE LEARNERS
        #observe rewawrd and new state
        ns1 = learner1.getState([hist1, hist2])
        r1 = player1.payoff(move1, move2)
        #update table
        learner1.updateTable(state1, move1, ns1, r1)
        
        #leaner 2   
        ns2 = learner2.getState([hist2, hist1])
        r2 = player2.payoff(move2, move1)
        learner2.updateTable(state2, move2, ns2, r2)
        
        #update states
        state1, state2 = ns1, ns2


#entry point
def Main():

    #init 2 learners to use
    learner1 = qLearner()
    learner2 = qLearner()

    #play strategy and update table
    play(learner1, learner2)

    #display results
    learner1.display()
    learner2.display()            



Main()
