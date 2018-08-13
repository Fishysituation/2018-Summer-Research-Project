import random as r

populationSize = 500

breedRate = 0.75
mutationRate = 0.01

#goal string, all lower case characters 97-122
targetString = "thisisthetargetstring"
strLen = len(targetString)

#file path for data out
pathOut = "geneticData.out"

#class for an individual gene
class individual:

    string = []
    fitness = 0
    fitnessScaled = 0

    def __init__(self, initialString):
        for i in range(0, strLen):
            self.string = initialString
        self.calculateFitness()

    #update individual's fitness
    def calculateFitness(self):
        count = 0
        for i in range(0, strLen):
            if self.string[i] == targetString[i]:
                count += 1
        self.fitness = count/strLen
        self.fitnessScaled = 2 ** self.fitness

    #displays individual as string, not list
    def displayString(self):
        for i in range(0, strLen):
            print(self.string[i], end = '')
        print(' : ' + str(self.fitness), end = '')
        print()

    #probability is a function of its fitness
    def tryMutate(self):
        count = 0
        for i in range(0, strLen):
            if r.uniform(0, 1) <= mutationRate:
                count += 1
                self.string[i] = chr(r.randint(97, 122))
        return(count)

    #allows sorting
    def __lt__(self, other):
        return self.fitness < other.fitness


#creates random lowercase string
def generateString():
    string = []
    for i in range(0, strLen):
        string .append(chr(r.randint(97, 122)))
    return string


#init population, insertion sort by fitness
def generate():   
    temp = [individual(generateString())]

    for i in range(1, populationSize):
        current = []
        member = individual(generateString())
        
        for n in range(0, len(temp)):
            if member.fitness < temp[n].fitness:
                current.append(temp[n])
            else:
                current.append(member)
                for m in range(n, len(temp)):
                    current.append(temp[m])
                break
        #if new is fittest
        if len(current) == len(temp):
            current.append(member)
        temp = current

    return temp



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
        #calculate fitness
        new1.calculateFitness()
        new2.calculateFitness()
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
        #calculate fitness
        newGeneration[-1].calculateFitness()
        newGeneration[-2].calculateFitness()



#calculate and display total and mean average
def calculateOverall(population):
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
    print("Total fittness: " + str(total))
    print("Fittest member: ", end = '')
    population[highestIndex].displayString()
    print("Average: " + str(total/populationSize) + "\n")
    
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

    #all individuals, ordered by fitness descending
    population = [] 
    #generate initial population
    population = generate()

    allData = []
    generationNo = 0
    highest = 0

    while int(highest) != 1:
        generationNo += 1
        #initialise new generaton
        newGeneration = []
        
        #while newGeneration not yet full
        while len(newGeneration) < populationSize:
            breed(population, newGeneration)
        
        population = newGeneration

        print("Generation " + str(generationNo))
        #display all information
        newData = calculateOverall(population)
        
        highest = newData[1]
        allData.append(newData)
        
        print()


    print("String was found in " + str(generationNo) + " generations.")
    writeOut(allData)


Main()