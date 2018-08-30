import network
import random as r


#test with some random values

structure = [2,2,2]


#gen 49 
string = [1.7,     1.7,     0.3,     1.5,     -0.5,    -0.6,    1.6,     2.0,     -6.4,    -1.3,    -0.2,    -1.3]

"""
for i in range(0, 12):
    string.append(r.randint(-3, 3))
"""

instance = network.initiate(structure, string)

print(instance.weights)
print(instance.biases)

print(instance.feedForward([0, 0]))
print(instance.feedForward([0, 1]))
print(instance.feedForward([1, 0]))
print(instance.feedForward([1, 1]))


print(instance.getHighestActivation(instance.feedForward([0, 0])))