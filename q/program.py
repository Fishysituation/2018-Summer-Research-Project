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

def display(qTable):
    for y in range(0, stateNo):
        for x in range(0, actionNo):
            print(str(qTable[y][x]) + "\t", end = '')
        print()

    outs = ''
    for i in range(0, stateNo):
        if qTable[i][0] > qTable[i][1]:
            outs += "0"
        else:
            outs += "1"
    
    print(outs)

    print()


#init the table with random rewards
def generate():
    qTable = []
    for y in range(0, stateNo):
        row = []
        for x in range(0, actionNo):
            #random float between 0, 1
            row.append(r.uniform(0, 0.5))
        qTable.append(row)
    
    return qTable


#find correct state (row in table)
def getState(history):
    state = 0
    #if not first round
    if len(history[0]) > 0:
        state = 1 + (2 * history[0][-1]) + history[1][-1]
    return state


#choose action with greatest reward (column in table)
def getAction(row):
    largest = row[0]
    index = 0
    for i in range(1, actionNo):
        if row[i] > largest:
            largest = row[i]
            index = i
    return index


#use update rule
def updateTable(qTable, s, a, sp, r):
    r = r/10
    oldEstimate = (1-learningRate) * qTable[s][a]
    newEstimate = learningRate * (r + (discountFactor * qTable[sp][getAction(qTable[sp])]))
    
    qTable[s][a] = oldEstimate + newEstimate

    #use update rule shown in "Multiagent reinforcement learning in the Iterated Prisoner's Dilemma"
    #qTable[s][a] += learningRate * (r + (discountFactor * qTable[sp][getAction(qTable[sp])]) - qTable[s][a])
    return


def play(qTable, opponent):
    oppHistory = []
    playerHistory = []
    #generate player
    player = prisoner.adaptivePlayer("other")
    
    #initial state
    state = 0

    for i in range(0, roundNo):
          
        oppMove = opponent.move([oppHistory, playerHistory])
        playerMove = getAction(qTable[state])

        #switch player move as a function of roundNo - more exploration at start
        toss = r.uniform(0, 1)
        if toss < (40 - (i/100))/100:
            playerMove = abs(playerMove-1)
            #print(str(i) + " " + str(toss) + str(playerMove))

        oppHistory.append(oppMove)
        playerHistory.append(playerMove)

        #observe rewawrd and new state
        newState = getState([playerHistory, oppHistory])
        reward = player.payoff(playerMove, oppMove)


        updateTable(qTable, state, playerMove, newState, reward)


        state = newState


        #print("Player: " + str(playerMove) + " " + opponent.strategy + ": " + str(oppMove))

    #print("\nPlayer Score: " + str(player.score) + "\n\n")

    return player.score


def Main():
    strategies = [prisoner.strategies[3]]

    allModels = []

    #policy mapping
    qTable = generate()
    display(qTable)
    

    for i in range(0, iterations):        
        #change order of strategies
        r.shuffle(strategies)

        for n in range(0, len(strategies)):
            #play strategy and update table
            play(qTable, prisoner.player(strategies[n]))

    #display results
    display(qTable)
            



Main()
