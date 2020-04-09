# ------------------------------------------------------------------------------#
# Module relative to the spread model of the virus.
#
# GOFFART Maxime (180521) & JORIS Olivier (182113)
# ------------------------------------------------------------------------------#


# External libraries
import random, sys
import numpy as np
from numpy.linalg import matrix_power
from numpy import dot as matrix_product
from numpy import finfo as float_info

# Own files
import transition_matrix, states_manipulator, graphics_generator

# Precision in infected proportion for considering that the virus completely
# disappear for the exact model (method virus_evolution)
#PRECISION = float_info(np.float32).eps # Epsilon machine
PRECISION = 0.001

# Limit of the X axis on the graphic
MAX_X = 35

# ------------------------------------------------------------------------------#
# Function which computes the spread of the virus based on the transition matrix
# (exact model - section 1 of the assignment).
# ------------------------------------------------------------------------------#
def virus_evolution(tMatrix, populationSize, states):

	# Finds all the possible initial states (only one infected)
	currentStates = states_manipulator.find_initial_states(states, populationSize)

	susceptibleProportion = [(populationSize - 1)/populationSize]
	infectedProportion = [1/populationSize]
	curedProportion = [0]

	# Temporary transition matrix
	tmpTMatrix = matrix_power(tMatrix, 0) # Identity matrix

	# Until a certain precision is reached
	while infectedProportion[len(infectedProportion) - 1] > PRECISION:
		#sys.stdout.write("\rTime step n°%d/%d" % ((a+1), MAX_X))
		#sys.stdout.flush()

		#print(infectedProportion[len(infectedProportion) - 1])

		#P^N = P * (P^(N-1))
		tmpTMatrix = matrix_product(tMatrix, tmpTMatrix)

		# Remembers the lines of the transition matrix that we are considering
		matrixLines = []

		numberOfStates = len(currentStates)

		# Retrieves the considered lines from the transition matrix
		for i in range(numberOfStates):
			index = states_manipulator.states_get_index(states, currentStates[i])
			matrixLines.append(tmpTMatrix[index])

		tmpS = 0
		tmpI = 0
		tmpC = 0

		# Goes through every lines of the transition matrix that we are considering
		for i in range(len(matrixLines)):

			tmpSProp = 0
			tmpIProp = 0
			tmpCProp = 0

			# Goes through each column of one line
			for j in range(len(matrixLines[0])):

				# Processes the proportions for one state
				if matrixLines[i][j] != 0:

					index = states_manipulator.states_get_index(states, currentStates[i])
					tmp = states_manipulator.states_proportions(states[j])

					tmpSProp = tmpSProp + (tmp[0] * tmpTMatrix[index][j])
					tmpIProp = tmpIProp + (tmp[1] * tmpTMatrix[index][j])
					tmpCProp = tmpCProp + (tmp[2] * tmpTMatrix[index][j])

			# Proportions for one line
			probability = 1 / numberOfStates
			tmpS+=(tmpSProp * probability)
			tmpI+=(tmpIProp * probability)
			tmpC+=(tmpCProp * probability)

		# Proportions for one step of the Markov chain
		susceptibleProportion.append(tmpS)
		infectedProportion.append(tmpI)
		curedProportion.append(tmpC)

	#print("len susceptibleProportion = " + str(len(susceptibleProportion)))
	#print("len infectedProportion = " + str(len(infectedProportion)))
	#print("len curedProportion = " + str(len(curedProportion)))

	# Resizes the arrays to get the same size repeting the last element
	if len(susceptibleProportion) < MAX_X:
		last = susceptibleProportion[len(susceptibleProportion) - 1]
		for i in range(MAX_X - len(susceptibleProportion)):
			susceptibleProportion.append(last)

	if len(infectedProportion) < MAX_X:
		last = infectedProportion[len(infectedProportion) - 1]
		for i in range(MAX_X - len(infectedProportion)):
			infectedProportion.append(last)

	if len(curedProportion) < MAX_X:
		last = curedProportion[len(curedProportion) - 1]
		for i in range(MAX_X - len(curedProportion)):
			curedProportion.append(last)

	# Display the graphic of proportions
	graphics_generator.graphic(susceptibleProportion[0:MAX_X], infectedProportion[0:MAX_X], curedProportion[0:MAX_X], MAX_X, 0)

	return

# ------------------------------------------------------------------------------#
# Simulates a random execution of the Markov chain and returns a list with the
# state proportions at each time (second section).
# ------------------------------------------------------------------------------#
def simulate_random_chain_execution(currentConfiguration, adjacencyMatrix, populationSize,
	infectionProbability, healProbability, maxInteractionsNumber):

	if (len(adjacencyMatrix) != populationSize):
		print("ERROR : The size of the adjacency matrix doesn't match the population size.")

	infectedLines = []
	newInfected = []
	susceptibleProportions = []
	infectedProportions = []
	immunisedProportions = []
	currentInteractionsNumber = 0

	timeCounter = 0

	# Localisation of the infetcted in the population.
	for i in range(populationSize):
		if currentConfiguration[i] == 'I':
			infectedLines.append(i)

	# Addition of the initial proportion in the corresponding list.
	susceptibleProportions.append(states_manipulator.states_proportions(currentConfiguration)[0])
	infectedProportions.append(states_manipulator.states_proportions(currentConfiguration)[1])
	immunisedProportions.append(states_manipulator.states_proportions(currentConfiguration)[2])

	# Simulation of one random execution of the chain.
	while not(states_manipulator.stable_situation(currentConfiguration)):
		for currentLine in infectedLines:
			for i in range(populationSize):
				if adjacencyMatrix[currentLine][i] == '1' and currentInteractionsNumber < maxInteractionsNumber:
					randomNumber = random.uniform(0, 1.0)
					currentInteractionsNumber += 1
					if randomNumber <= infectionProbability:
						if currentConfiguration[i] == 'S':
							currentConfiguration[i] = 'I'
							newInfected.append(i)
			currentInteractionsNumber = 0

			randomNumber = random.uniform(0, 1.0)
			if randomNumber <= healProbability:
				currentConfiguration[currentLine] = 'R'
				infectedLines.remove(currentLine)

			# Addition of the new infected in the corresponding list.
			for nInfected in newInfected:
				infectedLines.append(nInfected)
				newInfected.remove(nInfected)

			# Addition of the actual proportion to the corresponding list.
			susceptibleProportions.append(states_manipulator.states_proportions(currentConfiguration)[0])
			infectedProportions.append(states_manipulator.states_proportions(currentConfiguration)[1])
			immunisedProportions.append(states_manipulator.states_proportions(currentConfiguration)[2])

		timeCounter+=1

	return [susceptibleProportions, infectedProportions, immunisedProportions, timeCounter]

# ------------------------------------------------------------------------------#
# Computes the mean of state proportions and the average time for disappearance
# of the virus based on the given number of simulations.
# ------------------------------------------------------------------------------#
def compute_mean_proportions_time(adjacencyMatrix, populationSize, infectionProbability,
	healProbability, numberOfSimulations, maxTime, initialInfectedProportion,
	initialImmunisedProportion, maxInteractionsNumber):

	susceptibleSumProportions = [0 for i in range(maxTime)]
	infectedSumProportions = [0 for i in range(maxTime)]
	immunisedSumProportions = [0 for i in range(maxTime)]

	sumInfectedTime = 0

	# Computation of the proportion sum based on simulations.
	for i in range(numberOfSimulations):

		sys.stdout.write("\rSimulation n°%d/%d" % (i, numberOfSimulations))
		sys.stdout.flush()

		initialConfiguration = load_initial_configuration_simulations(populationSize,
							   initialInfectedProportion, initialImmunisedProportion)

		stateProportions = simulate_random_chain_execution(initialConfiguration, adjacencyMatrix,
						   populationSize, infectionProbability, healProbability,
						   maxInteractionsNumber)

		susceptibleProportions = stateProportions[0]
		infectedProportions = stateProportions[1]
		immunisedProportions = stateProportions[2]
		sumInfectedTime+=stateProportions[3]

		# if len(infectedProportions) > 10:
		# 	print(infectedProportions[9])

		# Computation of the sum of infected time in order to compute the mean of this time.
		#for j in range(len(infectedProportions)):
		#	if infectedProportions[j] == 0.0:
		#		sumInfectedTime += j

		# Resizes the array to get the same size repeting the last element
		# (corresponding to a stable situation)
		if(len(susceptibleProportions) < maxTime):
			for j in range(len(susceptibleProportions), maxTime):
				susceptibleProportions.append(susceptibleProportions[j - 1])
				infectedProportions.append(infectedProportions[j - 1])
				immunisedProportions.append(immunisedProportions[j - 1])

		for j in range(maxTime):
			susceptibleSumProportions[j] += susceptibleProportions[j]
			infectedSumProportions[j] += infectedProportions[j]
			immunisedSumProportions[j] += immunisedProportions[j]

	# Computation of the proportion mean based on simulations.
	susceptibleMeanProportions = [0 for i in range(maxTime)]
	infectedMeanProportions = [0 for i in range(maxTime)]
	immunisedMeanProportions = [0 for i in range(maxTime)]

	for i in range(maxTime):
		susceptibleMeanProportions[i] = susceptibleSumProportions[i] / numberOfSimulations
		infectedMeanProportions[i] = infectedSumProportions[i] / numberOfSimulations
		immunisedMeanProportions[i] = immunisedSumProportions[i] / numberOfSimulations

	meanInfectedTime = sumInfectedTime / numberOfSimulations

	return [susceptibleMeanProportions, infectedMeanProportions, immunisedMeanProportions,
		   meanInfectedTime]

# ------------------------------------------------------------------------------#
# Loads an initial configuration with the given infected and immunised proportion.
# ------------------------------------------------------------------------------#
def load_initial_configuration_simulations(populationSize, infectedProportion,
	immunisedProportion):
	randNumbers = random.sample(range(0, populationSize - 1), int(populationSize *
							   (immunisedProportion)))

	initialConfiguration = ['S' for i in range(populationSize)]

	for i in range(len(randNumbers)):
		initialConfiguration[randNumbers[i]] = 'R'

	randNumbers = random.sample(range(0, populationSize - 1), int(populationSize *
				  (infectedProportion)))

	for i in range(len(randNumbers)):
		if initialConfiguration[randNumbers[i]] == 'S':
			initialConfiguration[randNumbers[i]] = 'I'

	return initialConfiguration
