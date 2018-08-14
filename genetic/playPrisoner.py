import sys
#add parent directory to python path
sys.path.append('..')

import random as r
import prisoner

populationSize = 150
generationNo = 100

#how many rounds an individual should play against another
roundNo = 20

breedRate = 0.6
mutationRate = 0.01

#chars: first round, mutual coop, opp. def., player def., mutual def.
strLen = 5

#file path for data out
pathOut = "data/geneticPrisoner2.out"


#class for an individual gene
class individual:

    string = []
    #average score of individual
    fitness = 0
    #2^fitness
    fitnessScaled = 0

    def __init__(self, initialString):
        for i in range(0, strLen):
            self.string = initialString

    #update individual's fitness
    def setFitness(self, result):
        self.fitness = result
        self.fitnessScaled = 2 ** result

    #displays individual as string, not list
    def displayString(self):
        for i in range(0, strLen):
            print(self.string[i], end = '')
        print(' : ' + str(self.fitness), end = '')
        print()

    #flat probability of mutation - mutationRate
    def tryMutate(self):
        for i in range(0, strLen):
            if r.uniform(0, 1) <= mutationRate:
                self.string[i] = str(r.randint(0, 1))

    #allows sorting
    def __lt__(self, other):
        return self.fitness < other.fitness


#play roundNo rounds between two individuals
def fight(player1, string1, player2, string2):
    history1 = []
    history2 = []
    for i in range(0, roundNo):
        move1, move2 = 0, 0
        
        #if first round
        if i == 0:
            move1 = int(string1[0])
            move2 = int(string2[0])

        else:
            index1 = 1 + 2 * int(history1[-1]) + int(history2[-1])
            index2 = 1 + 2 * int(history2[-1]) + int(history1[-1])

            move1 = int(string1[index1])
            move2 = int(string2[index2])

        player1.payoff(move1, move2)
        player2.payoff(move2, move1)

        history1.append(move1)
        history2.append(move2)


#round robbin competition for all members in population
def calculateAllFitnesses(population):
    scores = []
    players = []
    strings = []
    #create populationSize scored players
    for i in range(0, populationSize):
        players.append(prisoner.adaptivePlayer("other"))
        strings.append(population[i].string)

    #round robbin
    for i in range(0, populationSize):          #player1
        for n in range(i+1, populationSize):    #player2
            fight(players[i], strings[i], players[n], strings[n])
        #once player1 has fought all, note average score
        scores.append(players[i].score/((populationSize-1)*roundNo))
    
    return scores


#update all scores in class instance
def updateAllFitnesses(scores, population):
    for i in range(0, populationSize):
        population[i].setFitness(scores[i])



#creates random binary
def generateString():
    string = []
    for i in range(0, strLen):
        string.append(str(r.randint(0, 1)))
    return string


#init population, insertion sort by fitness
def generate():
    toReturn = []

    for i in range(0, populationSize):
        toReturn.append(individual(generateString()))
        
    return toReturn




#pick individual randomly with fitness bias
def pickRandomBreeding(sumFitness, fitnesses):
    num = r.uniform(1, sumFitness)
    #actual index to return
    count = -1
    for i in range(0, populationSize):
        count += 1
        num -= fitnesses[i]

        if num <= 0:
            return count


#merge dna of two individuals
def cross(dna1, dna2, splitIndex):
    new = []
    for i in range(0, splitIndex):
        new.append(dna1[i])
    for i in range(splitIndex, strLen):
        new.append(dna2[i])
    return new
    

#breed two random picked members in population
def breed(population, newGeneration):

    #sum all scaled fitnesses
    fitnesses = []
    sumFitness = 0
    for i in range(0, populationSize):
        sumFitness += population[i].fitnessScaled
        fitnesses.append(population[i].fitnessScaled)

    #pick two unique indicies
    index1 = pickRandomBreeding(sumFitness, fitnesses)
    index2 = pickRandomBreeding(sumFitness, fitnesses)

    while index1 == index2:
        index2 = pickRandomBreeding(sumFitness, fitnesses)

    #optionally breed a breedRate proportion of times 
    if r.uniform(0, 1) <= breedRate:

        splitIndex = r.randint(1, strLen-2)

        #create new dna by crossing and copy to each individual
        new1 = individual(cross(population[index1].string, population[index2].string, splitIndex))
        new2 = individual(cross(population[index2].string, population[index1].string, splitIndex))

        #try mutating
        new1.tryMutate()
        new2.tryMutate()
        #add to new generation
        newGeneration.append(new1)
        newGeneration.append(new2)

    else:
        #add to new generation
        newGeneration.append(population[index1])
        newGeneration.append(population[index2])
        #try mutating
        newGeneration[-1].tryMutate()
        newGeneration[-2].tryMutate()



#calculate and display total and mean average
def calculateOverall(population, generationNo):
    total = 0
    highest = population[0].fitness
    highestIndex = 0
    lowest = population[0].fitness
    for i in range(0, populationSize):
        total += population[i].fitness
        if population[i].fitness > highest:
            highest = population[i].fitness
            highestIndex = i
        elif population[i].fitness < lowest:
            lowest = population[i].fitness

    if generationNo == 0 or (generationNo+1) % 5 == 0 or int(lowest) == 3 and int(highest) == 3:
        print("Generation: " + str(generationNo))
        print("Total fittness: " + str(total))
        print("Fittest member: ", end = '')
        population[highestIndex].displayString()
        print("Average: " + str(total/populationSize) + "\n") 
        print()

    return [lowest, highest, total/populationSize]


#display all members in population, in order fitness
def displayAll(population):
    for i in range(0, populationSize):
        population[i].displayString()


#write all data out to file
def writeOut(allData):
    f = open(pathOut, 'w')
    for i in range(0, len(allData)):
        f.write(
            str(allData[i][0]) + "\t" + 
            str(allData[i][1]) + "\t" + 
            str(allData[i][2]) + "\n"
        )



#main function
def Main():

    #generate initial population
    population = generate()
    #calculate and update all fitnesses
    fitnesses = calculateAllFitnesses(population)
    updateAllFitnesses(fitnesses, population)



    allData = []

    for i in range(0, generationNo):

        #initialise new generaton
        newGeneration = []

        #while newGeneration not yet full
        while len(newGeneration) < populationSize:
            breed(population, newGeneration)
        
        population = newGeneration
        
        #calculate and update all fitnesses
        fitnesses = calculateAllFitnesses(population)
        updateAllFitnesses(fitnesses, population)

        #display all information
        newData = calculateOverall(population, i)
        
        allData.append(newData)
        

    writeOut(allData)


Main()