# Module relative to the spread model of the virus.
import random, numpy, transitionMatrix

# Load an initial configuration with 1 infected and a 1 / populationSize probability to be this
# first infected of the population.
def load_initial_configuration(populationSize):

	random.seed()
	randNumber = random.randint(0, populationSize - 1)

	initialConfiguration = ""

	for i in range(populationSize):
		if i != randNumber:
			initialConfiguration += ("S")
		else:
			initialConfiguration += ("I")

	return initialConfiguration

# Predict the spread of the virus based on the transition matrix, the population's size,
# the initial state of the population, the probability of being infected with we meet
# someone who's infected (beta), and the probability of being cure woth we're infected (mu)
def virus_evolution(tMatrix, populationSize, initialState, beta, mu):

	print(" ** Entering virus_evolution function **")

	print("Initial state is : " + initialState)

	states = ['S', 'I', 'R']

	# Compute all the possible states
	for i in range(populationSize - 1):
		states = transitionMatrix.compute_states(states)

	# Get the line index inside the transition matrix of the original state
	initialIndex = 0
	for i in range(len(states)):
		if states[i] == initialState:
			initialIndex = i
			break

	print("The initial state is on line index : " + str(initialIndex) + " of the states list")

	# Retrieve the correspond line inside the transition matrix
	currentMatrixLine = tMatrix[initialIndex]

	#print(currentMatrixLine)

	# Defining b and u as the paramters of the method
	b = beta
	u = mu

	# Replace b and u inside the transition matrix by the arguments of the method
	# so we can determine the probabilities on the line that we're considering in the
	# transition matrix
	probabilities = []
	for i in range(len(currentMatrixLine)):
		probabilities.append(eval(str(currentMatrixLine[i])))

	#print(probabilities)

	print("\nThe sum of the probabilities is equal to " + str(sum(probabilities)))

	# Compute the accumulated probabilities using the function cumsum of NumPy
	cumProbabilities = numpy.cumsum(probabilities)

	# Draw a random float between 0 and 1 to determine the next state of the Markov chain
	newRandom = random.uniform(0, 1.0)

	print("New random number between 0 and 1 : " + str(newRandom))

	# Determine the next step of the Markov chain using the newRandom
	for i in range(len(cumProbabilities)):
		if cumProbabilities[i] > newRandom:
			print("\nThe rank of the new state is : " + str(i))
			print("And so, the new state is : " + states[i])
			break
