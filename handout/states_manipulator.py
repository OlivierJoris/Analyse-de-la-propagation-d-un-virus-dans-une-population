# ------------------------------------------------------------------------------#
# Module to manage the states of a Markov chain.
#
# GOFFART Maxime (180521) & JORIS Olivier (182113)
# ------------------------------------------------------------------------------#


# ------------------------------------------------------------------------------#
# Function to obtain all the possible states of the chain when adding an
# individual to the states originalSequence.
# ------------------------------------------------------------------------------#
def compute_states(originalSequence):

	basicSequence = ['S', 'I', 'R']
	newSequence = []

	for i in range(len(originalSequence)):
		for j in range(len(basicSequence)):
			newSequence.append(originalSequence[i] + basicSequence[j])

	return newSequence

# ------------------------------------------------------------------------------#
# Function to get the index of a state based on the list which contains all the
# states and the desired state.
# ------------------------------------------------------------------------------#
def states_get_index(states, consideredState):

	for i in range(len(states)):
		if states[i] == consideredState:
			return i

	return -1

# ------------------------------------------------------------------------------#
# Function to find all the possible initial states (only one infected).
# ------------------------------------------------------------------------------#
def find_initial_states(states, populationSize):

	initialStates = []

	if len(states) != pow(3, populationSize):
		print("Error with sizes")
		return []

	numberInfected = 0
	numberCured = 0

	for i in range(len(states)):
		numberInfected = 0
		numberCured = 0
		for j in range(populationSize):
			if states[i][j] == 'I':
				numberInfected+=1
			elif states[i][j] == 'R':
				numberCured+=1

		if numberInfected == 1 and numberCured == 0:
			initialStates.append(states[i])

	return initialStates

# ------------------------------------------------------------------------------#
# Function to determine if the situation of the population is stable or not
# based on the current state of the population.
# Returns False if there're humains who are still infected and so the situation
# 	can still evolve.
# Else, returns True.
# ------------------------------------------------------------------------------#
def stable_situation(currentState):

	for i in range(len(currentState)):
		if currentState[i] == 'I':
			return False;

	return True

#------------------------------------------------------------------------------#
# Returns a list containing every absorbing states based on a list of states.
# ------------------------------------------------------------------------------#
def find_absorbing_state(states):

	absorbingStates = []

	for i in range(len(states)):
		if stable_situation(states[i]):
			absorbingStates.append(states[i])

	return absorbingStates

# ------------------------------------------------------------------------------#
# Function which returns the proportions of susceptible people, infected people,
# and cured people based on the state of the chain.
# ------------------------------------------------------------------------------#
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

	return [susceptible/populationSize, infected/populationSize, cured/populationSize]
