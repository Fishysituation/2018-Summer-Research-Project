#train the network
#Use genetic algortihm

import sys
#add parent directory to python path
sys.path.append("..")

import network
import numpy as np
import random as r
import prisoner


populationSize = 300

generationNo = 50
strLen = 12

roundNo = 20

mutationRate = 0.01
breedRate = 0.7

weightRange = -20, 20
biasRange = -70, 0

structure = [2, 2, 2]


pathOut = "geneticPrisoner300.out"


#class for an individual gene
class individual:

    #average score of individual
    fitness = 0
    #2^fitness
    fitnessScaled = 0

    def __init__(self, initialString):
        for i in range(0, strLen):
            self.string = initialString
            self.network = network.initiate(structure, self.string)

    #update individual's fitness
    def setFitness(self, result):
        self.fitness = result
        self.fitnessScaled = 2 ** result

    #displays individual as string, not list
    def displayString(self):
        for i in range(0, strLen):
            print(str(self.string[i]) + "\t" , end = '')
        print(' : ' + str(self.fitness), end = '')
        print()

    #flat probability of mutation - mutationRate
    def tryMutate(self):
        for i in range(0, 8):
            if r.uniform(0, 1) <= mutationRate:
                self.string[i] = r.randint(weightRange[0], weightRange[1])/10
        for i in range(8, 12):
            if r.uniform(0, 1) <= mutationRate:
                self.string[i] = r.randint(biasRange[0], biasRange[1])/10

    #allows sorting
    def __lt__(self, other):
        return self.fitness < other.fitness



#hardcoded random sequence ting
def getRandomSequence():
    toReturn = []
    for i in range(0, 8):
        toReturn.append(r.randint(weightRange[0], weightRange[1])/10)
    for i in range(8, 12):
        toReturn.append(r.randint(biasRange[0], biasRange[1])/10)
    return toReturn


#populate start with random
def generate():
    population = []
    for i in range(0, populationSize):
        population.append(individual(getRandomSequence()))
    return population




#play roundNo rounds between an individual and strategy
def fight(player1, net1, opponent):
    history1 = [0]
    history2 = [0]

    for i in range(0, roundNo):

        act1 = net1.feedForward([history1[-1], history2[-1]])

        move1 = 0
        
        if structure[-1] == 2:
            move1 = net1.getHighestActivation(act1)[0]
        elif structure[-1] == 1:
            move1 = net1.binaryOutput(act1) 
        
        move2 = opponent.move(history = [history2, history1])

        player1.payoff(move1, move2)

        history1.append(move1)
        history2.append(move2)


def calculateAllFitnesses(population):
    scores = []
    #for each member in population
    for i in range(0, populationSize):
        player = prisoner.adaptivePlayer("other")
        #test against a same 4 strategies
        for x in range(0, len(prisoner.netStrategies)):
            opponent = prisoner.player(prisoner.netStrategies[x])
            fight(player, population[i].network, opponent)
        scores.append(player.score/(len(prisoner.netStrategies)*roundNo))
    
    return scores


#update all scores in class instance
def updateAllFitnesses(scores, population):
    for i in range(0, populationSize):
        population[i].setFitness(scores[i])




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
    lowestIndex = 0
    for i in range(0, populationSize):
        total += population[i].fitness
        if population[i].fitness > highest:
            highest = population[i].fitness
            highestIndex = i
        elif population[i].fitness < lowest:
            lowest = population[i].fitness
            lowestIndex = i

    if generationNo == 0 or (generationNo+1) % 5 == 0 or int(lowest) == 3 and int(highest) == 3:
        print("Generation: " + str(generationNo))
        print("Total fittness: " + str(total))
        print("Fittest member: ", end = '')
        population[highestIndex].displayString()
        print("Least fit member: ", end = '')
        population[lowestIndex].displayString()
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



def Main():

    #generate initial population
    population = generate()
    
    #calculate and update all fitnesses
    fitnesses = calculateAllFitnesses(population)
    updateAllFitnesses(fitnesses, population)
    #   displayAll(population)

    calculateOverall(population, 0)


    allData = []

    for i in range(1, generationNo):

        newGeneration = []

        #while newGeneration not yet full
        while len(newGeneration) < populationSize:
            breed(population, newGeneration)

        population = newGeneration

        #calculate and update all fitnesses
        fitnesses = calculateAllFitnesses(population)
        updateAllFitnesses(fitnesses, population)
        

        #displayAll(population)
        newData = calculateOverall(population, i)

        allData.append(newData)

    writeOut(allData)

Main()


