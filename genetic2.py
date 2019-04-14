import random
import numpy as np
import sys
import matplotlib.pyplot as plt
from deap import creator, base, tools, algorithms
import time

start_time = time.clock()
''''
fixedValues = np.array([
						#(val, row, col)
						(7, 0, 3),
						(1, 1, 0),
						(4, 2, 3),
						(3, 2, 4),
						(2, 2, 6),
						(6, 3, 8),
						(5, 4, 3),
						(9, 4, 5),
						(4, 5, 6),
						(1, 5, 7),
						(8, 5, 8),
						(8, 6, 4),
						(1, 6, 5),
						(2, 7, 2),
						(5, 7, 7),
						(4, 8, 1),
						(3, 8, 6)
						])

'''
fixedValues = np.array([
						#(val, row, col)
						(9, 0, 5),
						(5, 0, 8),
						(9, 1, 2),
						(1, 1, 3),
						(7, 1, 8),
						(8, 2, 0),
						(3, 2, 5),
						(4, 2, 8),
						(9, 3, 0),
						(6, 3, 1),
						(1, 3, 5),
						(8, 3, 6),
						(2, 5, 2),
						(6, 5, 3),
						(5, 5, 7),
						(1, 5, 8),
						(3, 6, 0),
						(9, 6, 3),
                   (2, 6, 8),
                   (1, 7, 0),
                   (2, 7, 5),
                   (3, 7, 6),
                   (7, 8, 0),
                   (4, 8, 3)
                        ])
'''
fixedValues = np.array([
						#(val, row, col)
						(4, 0, 0),
						(5, 0, 5),
						(9, 1, 1),
						(6, 1, 4),
						(6, 2, 0),
						(2, 2, 4),
						(4, 2, 6),
                   (8, 2, 7),
						(8, 3, 1),
						(7, 3, 5),
						(6, 3, 7),
						(4, 3, 8),
                   (5, 4, 1),
                   (9, 4, 2),
                   (8, 4, 6),
                   (3, 4, 7),
						(7, 5, 0),
						(6, 5, 1),
						(9, 5, 3),
						(5, 5, 7),
						(7, 6, 1),
						(5, 6, 2),
                   (4, 6, 4),
                   (8, 6, 8),
                   (7, 7, 4),
                   (4, 7, 7),
                   (1, 8, 3),
                   (2, 8, 8),
                        ])
'''
def printBoard(board):
	for i in range(len(board)):
		if(i % 3 == 0 and i != 0):
			print("------+------+------")
		for j in range(len(board[i])):
			if(j % 3 == 0 and j != 0):
				sys.stdout.write("|")
			sys.stdout.write(str(board[i][j]) + " ")
		print("")

def printBoardFromDNA64(individual):
	board = buildBoardFromDNA64(individual)
	printBoard(board)

def setup():
	board = (np.indices((9,9)) + 1)[1]
	for i in range(len(board)):
		board[i] = np.random.permutation(board[i])

	for (val, row, col) in fixedValues:
			swapToPlace(board, val, row, col)

	mask = np.ones((9,9), dtype=bool)
	for (val, row, col) in fixedValues:
			mask[row][col] = False

	DNA = board[mask]
	return DNA.tolist()

def swapToPlace(board, val, line, col):
		valIndex = np.where(board[line]==val)[0][0]
		swap(board[line], valIndex, col)

def swap(arr, pos1, pos2):
	arr[pos1], arr[pos2] = arr[pos2], arr[pos1]

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

toolbox.register("pos_val", setup)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.pos_val)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def fitnessFromDNA64(individual):
	board = buildBoardFromDNA64(individual)
	return fitnessFromBoard(board),

def buildBoardFromDNA64(individual):
	flattenedIdx = list(map(lambda t: t[1]*9 + t[2], fixedValues))
	values = fixedValues.T[0]
	flatBoard = []
	fixedValuesCounter = 0
	for i in range(81):
		if(i in flattenedIdx):
			flatBoard.append(values[fixedValuesCounter])
			fixedValuesCounter += 1
			continue
		flatBoard.append(individual[i - fixedValuesCounter])
	return np.array(flatBoard).reshape(9,9)


def fitnessFromBoard(board):
	score = 0
	rows, cols = board.shape
	for row in board:
		score += len(np.unique(row))
	for col in board.T:
		score += len(np.unique(col))
	for i in range(0, 3):
	    for j in range(0, 3):
	        sub = board[3*i:3*i+3, 3*j:3*j+3]
	        score += len(np.unique(sub))
	return score

toolbox.register("evaluate", fitnessFromDNA64)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutUniformInt, low=1, up=9, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3) 

population = toolbox.population(n=1000)

gensMin = []
gensMax = []
gensAvg = []
gensStd = []

NGEN=500
MUPCT = 0.15
stagnated = 0
stagnation_limit = 300
prevMax = -1
for gen in range(NGEN):
	print("---GEN %i ---" % gen)
	offspring = algorithms.varAnd(population, toolbox, cxpb=0.8, mutpb=MUPCT)
	fits = toolbox.map(toolbox.evaluate, offspring)
	for fit, ind in zip(fits, offspring):
		ind.fitness.values = fit
	
	# Gather all the fitnesses in one list and print the stats
	fits = [ind.fitness.values[0] for ind in offspring]

	length = len(population)
	mean = sum(fits) / length
	sum2 = sum(x*x for x in fits)
	std = abs(sum2 / length - mean**2)**0.5

	currMax = max(fits)

	if(currMax == prevMax):
		stagnated+=1
	else:
		stagnated = 0
		prevMax = currMax

	gensMin.append(min(fits))
	gensMax.append(max(fits))
	gensAvg.append(mean)
	gensStd.append(std)

	print("  Max %s" % int(max(fits)))
	population = toolbox.select(offspring, k=len(population))
topk = tools.selBest(population, k=1)
for solution in topk:
	print("Pontos: %i/243" % int(fitnessFromDNA64(solution)[0]))
	printBoardFromDNA64(solution)
	print("")

plt.subplot(111)
plt.plot(gensMax, label="Max")
plt.plot(gensAvg, label="Avg")
plt.plot(gensMin, label="Min")
plt.legend(bbox_to_anchor=(0.8, 0.0, 0.2, .102), loc=3, ncol=1, mode="expand", borderaxespad=0.)
plt.title('Genetic Algorithm (Population = 1000, Crossover = 80%, Mutation = 15%)')
plt.ylabel('Fitness Value (Max 243)')
plt.xlabel('Iterations')
plt.show()
plt.savefig('GA_hard.png')

print(time.clock() - start_time, "seconds")