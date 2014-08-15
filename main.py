__author__ = 'troy'

import gaClasses

#Initialize population
numMachines = 3
numJobs = 12
popSize = 100
numMutate = 20
numCrossover = 40
numKeep = 20
numIter = 400

data = gaClasses.ga_data(numMachines,numJobs)
pop = gaClasses.ga_pop(popSize,numMutate, numCrossover, numKeep,data)

bestFitness = 1e9

for i in range(numIter):
    #find fitnesses
    pop.getAllFitnesses(data)
    #sort pop by fitness
    pop.sortByFitnessAndPrune()
    if bestFitness>pop.pop[0].fitness:
        print 'iteration',i,' bestFitness=',pop.pop[0].fitness
        bestFitness = pop.pop[0].fitness
    #regen pop
    pop.regenPopulation(data)



pop.printSolution(data)