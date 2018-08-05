import random as r

populationSize = 30
#goal string, all lower case characters 97-122
targetString = "thisisthetargetstring"
strLen = len(targetString)

#all individuals, ordered by fitness descending
population = [] 


class individual:

    string = []
    fitness = 0

    def __init__(self, initialString):
        for i in range(0, strLen):
            self.string = initialString
        self.calculateFitness()
        self.displayString()

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



#pick two random members in population and breed
def breed():
    return


#reorder population by fitness
def reorder():
    #bubble-like implementation
    return



#mutate one character in member in population
def mutate():
    return


#main function
def Main():

    #generate initial population
    population = generate()
        
    print(len(population))

    #unique fitnesses
    scores = []

    #display all in order fitness 
    for i in range(0, populationSize):
        population[i].displayString()

    #while target string not seen

        #breed two individuals

        #mutate 


Main()