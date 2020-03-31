# Module relative to the spread model of the virus.

import random, numpy, transition_matrix
import matplotlib.pyplot as plt

DISPLAY_GRAPHIC = False

# Load an initial configuration with 1 infected and a 1 / populationSize probability to be this
# first infected of the population.
def load_initial_configuration_exact_model(populationSize):

	randNumber = random.randint(0, populationSize - 1)

	initialConfiguration = ""

	for i in range(populationSize):
		if i != randNumber:
			initialConfiguration += ("S")
		else:
			initialConfiguration += ("I")

	return initialConfiguration

# Predict the spread of the virus based on the transition matrix, the population's size,
# the initial state of the population, the probability of being infected if we meet
# someone who's infected (beta), and the probability of being cure if we're infected (mu)
def virus_evolution(tMatrix, populationSize, initialState, beta, mu):

	#print("** Entering virus_evolution function **")

	#print("Initial state is : " + initialState)

	states = ['S', 'I', 'R']

	# Compute all the possible states
	for i in range(populationSize - 1):
		states = transition_matrix.compute_states(states)

	currentState = initialState

	susceptibleProportion = []
	infectedProportion = []
	curedProportion = []

	proportions = states_proportions(currentState)

	susceptibleProportion.append(proportions[0])
	infectedProportion.append(proportions[1])
	curedProportion.append(proportions[2])

	counter = 0

	# Until the situation of the population is stable we apply the model.
	while not(stable_situation(currentState)):

		# Get the line index inside the transition matrix of the current state.
		currentIndex = 0
		for i in range(len(states)):
			if states[i] == currentState:
				currentIndex = i
				break

		#print("The current state is on line index : " + str(currentIndex) + " of the states list")

		# Retrieve the correspond line inside the transition matrix.
		currentMatrixLine = tMatrix[currentIndex]

		#print(currentMatrixLine)

		# Defining b and u as the parameters of the method.
		b = beta
		u = mu

		# Replace b and u inside the transition matrix by the arguments of the method
		# so we can determine the probabilities on the line that we're considering in the
		# transition matrix.
		probabilities = []
		for i in range(len(currentMatrixLine)):
			probabilities.append(eval(str(currentMatrixLine[i])))

		#print(probabilities)

		#print("The sum of the probabilities is equal to " + str(sum(probabilities)))

		# Compute the accumulated probabilities using the function cumsum of NumPy.
		cumProbabilities = numpy.cumsum(probabilities)

		# Draw a random float between 0 and 1 to determine the next state of the Markov chain
		newRandom = random.uniform(0, 1.0)

		#print("New random number between 0 and 1 : " + str(newRandom))

		# Determine the next state of the Markov chain using the newRandom.
		for i in range(len(cumProbabilities)):
			if cumProbabilities[i] > newRandom:
				#print("\nThe rank of the new state is : " + str(i))
				#print(states[i])
				currentState = states[i]
				break

		proportions = states_proportions(currentState)

		susceptibleProportion.append(proportions[0])
		infectedProportion.append(proportions[1])
		curedProportion.append(proportions[2])
		counter+=1

	#print("Counter value = " + str(counter))

	if DISPLAY_GRAPHIC:

		xAxis = list(range(0, counter+1))

		plt.plot(xAxis, susceptibleProportion, label = "Susceptible proportion", color = "blue")
		plt.plot(xAxis, infectedProportion, label = "Infected proportion", color = "red")
		plt.plot(xAxis, curedProportion, label = "Cured proportion", color = "green")
		plt.ylabel("Proportion")
		plt.xlabel("Time")
		plt.title("Evolution")
		plt.legend()
		plt.show()

	return (susceptibleProportion, infectedProportion, curedProportion, counter)


# Function which return the proportions of susceptible people, infected people,
# and cured people
def states_proportions(currentState):

	susceptible = 0
	infected = 0
	cured = 0

	populationSize = len(currentState)

	for i in range(len(currentState)):

		if currentState[i] == 'S':
			susceptible+=1
		elif currentState[i] == 'I':
			infected+=1
		elif currentState[i] == 'R':
			cured+=1

	return (susceptible/populationSize, infected/populationSize, cured/populationSize)

# Function to determine if the situation of the population is stable or not based
# on the current state of the population.
# Return False if there're humains who are still infected and so the situation can still evolve.
# Else return True.
def stable_situation(currentState):

	stableSituation = True

	for i in range(len(currentState)):
		if currentState[i] == 'I':
			stableSituation = False
			break

	return stableSituation

# Simulate a random execution of the Markov chain and return a list with the state proportions at 
# each time (second section).
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

	# Localisation of the infetcted in the population.
	for i in range(populationSize):
		if currentConfiguration[i] == 'I':
			infectedLines.append(i)

	# Addition of the initial proportion in the corresponding list.
	susceptibleProportions.append(states_proportions(currentConfiguration)[0]) 
	infectedProportions.append(states_proportions(currentConfiguration)[1])
	immunisedProportions.append(states_proportions(currentConfiguration)[2])

	# Simulation of one random execution of the chain.
	while not(stable_situation(currentConfiguration)):
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
			susceptibleProportions.append(states_proportions(currentConfiguration)[0]) 
			infectedProportions.append(states_proportions(currentConfiguration)[1])
			immunisedProportions.append(states_proportions(currentConfiguration)[2]) 

	return [susceptibleProportions, infectedProportions, immunisedProportions]

# Compute the mean of state proportions and the average time for disappearance of the virus based 
# on the given number of simulations.
def compute_mean_proportions_time(adjacencyMatrix, populationSize, infectionProbability, 
	healProbability, numberOfSimulations, maxTime, initialInfectedProportion, 
	initialImmunisedProportion, maxInteractionsNumber):

	susceptibleSumProportions = [0 for i in range(maxTime)]
	infectedSumProportions = [0 for i in range(maxTime)]
	immunisedSumProportions = [0 for i in range(maxTime)]

	sumInfectedTime = 0

	# Computation of the proportion sum based on simulations.
	for i in range(numberOfSimulations):
		initialConfiguration = load_initial_configuration_simulations(populationSize, 
							   initialInfectedProportion, initialImmunisedProportion)

		stateProportions = simulate_random_chain_execution(initialConfiguration, adjacencyMatrix, 
						   populationSize, infectionProbability, healProbability, 
						   maxInteractionsNumber)

		susceptibleProportions = stateProportions[0]
		infectedProportions = stateProportions[1]
		immunisedProportions = stateProportions[2]

		# Computation of the sum of infected time in order to compute the mean of this time.
		for j in range(len(infectedProportions)):
			if infectedProportions[j] == 0.0:
				sumInfectedTime += j

		# Resize the array to get the same size repeting the last element 
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

# Load an initial configuration with the given infected and immunised proportion.
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
