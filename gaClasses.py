__author__ = 'troy'

import random


class ga_data(object):
    def __init__(self,m,n):
        self.numMachines, self.numJobs = m, n
        self.dueDates = [random.randint(8,20) for i in range(n)]
        self.weights = [random.random() for i in range(n)]
        self.procTime = [random.randint(2,8) for i in range(n)]
    def printData(self):
        print 'numMachines=',self.numMachines,' numJobs=',self.numJobs
        print 'j\t\tw\t\td'
        for i in range(self.numJobs):
            print '%d\t\t%.3f\t%d' % (i,self.weights[i],self.dueDates[i])

class ga_pop(object):
    def __init__(self,totalPop,nMutate, nCross,nKeep, data):
        #generate pop
        self.totalPop, self.nMutate, self.nCross, self.nKeep, self.nImmigrate = totalPop, nMutate, nCross, nKeep, totalPop-nMutate-nCross-nKeep
        self.pop = [ga_chromosome(self.immigrate(data)) for i in range(self.totalPop)]

    def getAllFitnesses(self,data):
        for i in range(self.totalPop):
            self.fitness(self.pop[i],data)

    def fitness(self,chromo,data):
        machTime, jobCompletion,fitness = [0]*data.numMachines , [0]*data.numJobs,0
        for (mach,ignore,j) in sorted(chromo.keys):
            machTime[mach]+=data.procTime[j]
            jobCompletion[j]+=machTime[mach]
            fitness+=max(0.0,jobCompletion[j]-data.dueDates[j])*data.weights[j]
        chromo.fitness = fitness

    def sortByFitnessAndPrune(self):
        self.pop = sorted(self.pop,key=lambda chromo:chromo.fitness)[:self.nKeep]

    def immigrate(self,data):
        return [(random.randint(0,data.numMachines-1),random.random(),i) for i in range(data.numJobs)]

    def regenPopulation(self,data):
        for i in range(self.nMutate):
            chromo = ga_chromosome(self.pop[random.randint(0,self.nKeep-1)].keys)
            chromo.mutate(data)
            self.pop.append(chromo)
        for i in range(self.nImmigrate):
            chromo = ga_chromosome(self.immigrate(data))
            self.pop.append(chromo)
        for i in range(self.nCross):
            chromo = ga_chromosome(self.pop[random.randint(0,self.nKeep-1)].keys)
            chromo.crossover(data,self.pop[random.randint(0,self.nKeep-1)].keys)
            self.pop.append(chromo)

    def printSolution(self,data):
        print 'j\t\tw\t\td\tp\tm'
        #for i in range(data.numJobs):
        #    print '%d\t\t%.3f\t%d\t%d\t%d\t%.3f' % (i,data.weights[i],data.dueDates[i], data.procTime[i],self.pop[0].keys[i][0],self.pop[0].keys[i][1])
        for (m,ignore,j) in sorted(self.pop[0].keys):
            print '%d\t\t%.3f\t%d\t%d\t%d' % (j,data.weights[j],data.dueDates[j], data.procTime[j],m)


class ga_chromosome(object):
    def __init__(self,keys):
        self.keys = keys[:]
        self.fitness = 0
    def mutate(self,data):
        newKeys = []
        for i in range(len(self.keys)):
            if random.random()>0.9:
                if random.random()<0.5:
                    newKeys.append((random.randint(0,data.numMachines-1),self.keys[i][1],i))
                else:
                    newKeys.append((self.keys[i][0],random.random(),i))
            else:
                newKeys.append(self.keys[i])
        self.keys = newKeys[:]
    def crossover(self,data,chromo2keys):
        crossoverPoint = random.randint(int(.25*data.numJobs),int(.75*data.numJobs))
        newKeys = []
        for i in range(crossoverPoint):
            newKeys.append(self.keys[i])
        for i in range(crossoverPoint,data.numJobs):
            newKeys.append(chromo2keys[i])
        self.keys = newKeys[:]
