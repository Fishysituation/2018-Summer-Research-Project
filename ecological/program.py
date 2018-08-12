import sys
#add parent directory to python path
sys.path.append("..")

import random as r
import prisoner

size = 200
pathOut = "runs/run200."

strategyNo = 5



# populate grid with equal no of strategies
def generate():
    grid = []
    count = []
    target = size * size / strategyNo

    #init count 
    for i in range(0, strategyNo):
        count.append(0)

    for y in range(0, size):
        line = []
        for x in range(0, size):
            result = r.randint(0, strategyNo - 1)
            #ensure distribution is even
            while True:
                if count[result] == target:
                    result = r.randint(0, strategyNo - 1)
                else:
                    break
            count[result] += 1
            line.append(result)
        grid.append(line)

    return grid
    

# displays a grid state
def display(grid):
    print("\n")
    for y in range(0, size):
        for x in range(0, size):
            print(" " + str(grid[y][x]), end = '')
        print()
    print()



# wraps board around in horzintal direction
def modX(num):
	if num >= 0:
		return num % size
    #if negative, check other side of board
	else:
		return num + size


# wraps board around in vertical direction
def modY(num):
	if num >= 0:
		return num % size
    #if negative, check other side of board
	else:
		return num + size


# play a round between two strategies
def battle(player, oppoenent):
    #move history of the two players
    playerHistory = []
    oppHistory = []

    #play 20 rounds
    for i in range(0, 20):
        playerMove = player.move([playerHistory, oppHistory])
        oppMove = oppoenent.move([oppHistory, playerHistory])

        playerHistory.append(playerMove)
        oppHistory.append(oppMove)

        player.payoff(playerMove, oppMove)
    return


# get the strength of single grid space
def findStrength(x, y, grid):

    strategies = prisoner.strategies
    player = prisoner.adaptivePlayer(strategies[grid[y][x]])
    opponents = []

    for j in range(y-1, y+2):
        for i in range(x-1, x+2):
            if j == y and i == x:
                pass
            else:
                #add neighbour strategy as opponent 
                opponents.append(prisoner.player(strategies[grid[modY(j)][modX(i)]]))

    for i in range(0, 8):
        battle(player, opponents[i])

    return player.score


# increment the board one time step
def increment(grid):
    #init blank return and strengths grid
    toReturn = []
    strengths = []

    for y in range(0, size):
        line = []
        strengthLine = []
        for x in range(0, size):
            line.append(None)

            #calculate strength of each grid square
            strengthLine.append(findStrength(x, y, grid))

        toReturn.append(line)
        strengths.append(strengthLine)

    #replace each grid with strongest of its neighbours
    #keep same strategy if tie
    for y in range(0, size):
        for x in range(0, size):
            maxS = strengths[y][x]
            maxx, maxy = x, y 
            for j in range(y-1, y+2):
                for i in range(x-1, x+2):
                    if strengths[modY(j)][modX(i)] > maxS:
                        maxS = strengths[modY(j)][modX(i)]
                        maxx, maxy = modX(i), modY(j)
            toReturn[y][x] = grid[maxy][maxx]
    return toReturn



# get percentages of each strategy
def calculateOverall(grid):
    names = prisoner.strategies
    count = [0, 0, 0, 0, 0] 

    for y in range(0, size):
        for x in range(0, size):
            count[grid[y][x]] += 1

    for i in range(0, 5):
        print(names[i] + ": " + str(int((count[i]/(size*size))*100)) + "%")

    return int((count[3]/(size*size))*100)

# write a grid state out to file
def writeOut(grid, f):

    for y in range(0, size):
        strout = ''
        for x in range(0, size):
            strout += str(grid[y][x])
        f.write(strout + '\n')

    f.write("\n")


# program entry point
def Main():

    for i in range(0, 5):

        grid = generate()
        tftScore = calculateOverall(grid)

        f = open(pathOut + str(i) + ".out", 'w')
        writeOut(grid, f)

        count = 1

        #play n rounds
        while tftScore < 90:
            grid = increment(grid)
            tftScore = calculateOverall(grid)
            print("Round " + str(count))
            
            writeOut(grid, f)
            count += 1

        f.close()
        

Main()

