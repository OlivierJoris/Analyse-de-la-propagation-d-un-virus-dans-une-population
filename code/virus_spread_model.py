# Module relative to the spread model of the virus.

import random, numpy, transition_matrix
import matplotlib.pyplot as plt

DISPLAY_GRAPHIC = False

# Load an initial configuration with 1 infected and a 1 / populationSize probability to be this
# first infected of the population.
def load_initial_configuration(populationSize):

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
	while not(transition_matrix.stable_situation(currentState)):

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
