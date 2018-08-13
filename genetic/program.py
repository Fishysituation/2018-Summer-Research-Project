import random as r

populationSize = 20
generationNo = 50

#goal string, all lower case characters 97-122
targetString = "thisisthetargetstring"
strLen = len(targetString)


#class for an individual gene
class individual:

    string = []
    fitness = 0

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
        self.fitness = count
    
    #displays individual as string, not list
    def displayString(self):
        for i in range(0, strLen):
            print(self.string[i], end = '')
        print(' : ' + str(self.fitness), end = '')
        print()

    #randomly changes character in string
    def mutate(self):
        index = r.randint(0, strLen-1)
        self.string[index] = chr(r.randint(97, 122))

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


#display all members in population, in order fitness
def displayAll(population):
    for i in range(0, populationSize):
        population[i].displayString()


#calculate and display total and mean average
def calculateOverall(population):
    total = 0
    for i in range(0, populationSize):
        total += population[i].fitness
    print("Total fitnes: " + str(total))
    print("Average: " + str(total/populationSize) + "\n")


#find all unique fitnesses and their frequency
def getUniqueFitness(population):

    scores = [[population[0].fitness, 1]]

    for i in range(1, populationSize):
        if population[i].fitness == scores[-1][0]:
            scores[-1][1] += 1
        else:
            scores.append([population[i].fitness, 1])
    return scores
    

#pick individual randomly with fitness bias
def pickRandomBreeding(denominator, scores):
    num = r.randint(1, denominator)
    #actual index to return
    count = -1

    for i in range(0, len(scores)):
        for n in range(0, scores[i][1]):
            count += 1
            num -= (len(scores) - i)
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
    

#breed two random picked members in population and breed
def breed(population):
    #unique fitnesses
    scores = getUniqueFitness(population)

    #calculate denominator for breeding
    denominator = 0
    for i in range(0, len(scores)):
        denominator += (len(scores)-i)*scores[i][1]

    #pick two unique indicies
    index1 = pickRandomBreeding(denominator, scores)
    index2 = pickRandomBreeding(denominator, scores)

    while index1 == index2:
        index2 = pickRandomBreeding(denominator, scores)

    
    splitIndex = r.randint(1, strLen-2)

    print("\nCrossing " + str(index1) + ", " + str(index2) + " at index " + str(splitIndex) + ":")
    population[index1].displayString()
    population[index2].displayString()
    print()
    
    #create new dna by crossing and copy to each individual
    new1 = cross(population[index1].string, population[index2].string, splitIndex)
    new2 = cross(population[index2].string, population[index1].string, splitIndex)

    population[index1].string = new1
    population[index2].string = new2

    #update fitnesses and display result
    population[index1].calculateFitness()
    population[index2].calculateFitness()

    print("Result:")
    population[index1].displayString()
    population[index2].displayString()
    print()

    #update position of individuals in population
    reorder(population)



#reorder population by fitness
#you tried to implement something more efficient but failed f
def reorder(population):
    population.sort(reverse = True)




#mutate one character in member in population
def mutate(population):
    num = r.randint(0, populationSize-1)
    print("Mutating index " + str(num))
    print("Old string: ", end = '')
    population[num].displayString()
    population[num].mutate()
    population[num].calculateFitness()
    print("New string: ", end = '')
    population[num].displayString()
    reorder(population)
    print()



#main function
def Main():

    #all individuals, ordered by fitness descending
    population = [] 
    #generate initial population
    population = generate()

    for i in range(0, generationNo):
        #breed two individuals
        breed(population)
        #mutate one individual
        mutate(population)

        calculateOverall(population)
        displayAll(population)
        
        print()


Main()