# Module to get the transition matrix using W and N and all the possible states

def compute_transition_matrix(adjacencyMatrix, populationSize):

	if(len(adjacencyMatrix) != populationSize):
		print("ERROR : adjacency matrix size doesn't match the populaion's size")
		return

	states = ['S', 'I', 'R']

	# Compute all the possible states
	for i in range(populationSize - 1):
		states = compute_states(states)

	#print("Number of differents states = " + str(len(states)) + "\n")

	# Display all the states
	#for i in range(len(states)):
	#	print(states[i])

	# Create an empty transition matrix
	tMatrix = [[' ' for i in range(len(states))] for i in range(len(states))]

	# The first state which is SS is a special case

	tMatrix[0][0] = 1
	for i in range(len(states) - 1):
		tMatrix[0][i+1] = 0

	# Others lines

	for i in range(1, len(states)):
		state1 = states[i]

		# If the current state (state1) doesn't contained 'I' than we can only stay in the same state
		if 'I' not in state1:
			for q in range(len(states)):
				if states[i] == states[q]:
					tMatrix[i][q] = '1'
				else:
					tMatrix[i][q] = '0'
			continue

		for j in range(len(states)):

			state2 = states[j]

			for k in range(len(state1)):

				# All cases
				if state1[k] == 'I' and state2[k] == 'S':
					tMatrix[i][j] = '0'
					break
				elif state1[k] == 'R' and state2[k] == 'I':
					tMatrix[i][j] = '0'
					break
				elif state1[k] == 'S' and state2[k] == 'R':
					tMatrix[i][j] = '0'
					break
				elif state1[k] == 'R' and state2[k] == 'S':
					tMatrix[i][j] = '0'
					break
				elif state1[k] == 'S' and state2[k] == 'I':
					# Under conditions that :
					#  - Anoter person is infected
					#  - They know each other
					tmp = ''
					for l in range(len(state1)):
						if state1[l] == 'I' and l != k:
							if adjacencyMatrix[l][k] == '1':
								tmp += '(1-b)*'
							#elif adjacencyMatrix[l][k] == '0':
							#	tMatrix[i][j] += '(1)*'
					if (not(len(tmp) == 0)):
						if tmp.endswith('*'):
							tmp = tmp[0:(len(tmp)-1)]
						tMatrix[i][j] += ('(1-(' + tmp +'))*')
					else:
						tMatrix[i][j] += '(0)*'

				elif state1[k] == 'S' and state2[k] == 'S':
					for l in range(len(state1)):
						if state1[l] == 'I' and l != k:
							if adjacencyMatrix[l][k] == '1':
								tMatrix[i][j] += '(1-b)*'
							elif adjacencyMatrix[l][k] == '0':
								tMatrix[i][j] += '(1)*'

				elif state1[k] == 'I' and state2[k] == 'I':
					tMatrix[i][j] += '(1-u)*'
				elif state1[k] == 'I' and state2[k] == 'R':
					tMatrix[i][j] += '(u)*'
				elif state1[k] == 'R' and state2[k] == 'R':
					tMatrix[i][j] += '(1)*'

	# Verify
	for i in range(len(states)):
		for j in range(len(states)):
			tmpString = tMatrix[i][j]
			if isinstance(tmpString, str) and '0' in tmpString:
				tMatrix[i][j] = 0
			elif isinstance(tmpString, str) and tmpString.endswith('*'):
				tMatrix[i][j] = tmpString[0:(len(tmpString)-1)]

	# Display the transition matrix
	print("   ", end=" ")
	b = 0.5
	u = 0.2
	value = 0
	for i in range(len(states)):
		print(states[i], end=" | ")
	print("\n")
	#print(states[4])
	#for i in range(len(states)):
	#	print(states[i], end=" | ")
	#	print(tMatrix[4][i], end=" | ")
	#	print(eval(str(tMatrix[4][i])))
	#	value+=(eval(str(tMatrix[4][i])))

	#print("SUM = " + str(value))
	for i in range(len(states)):
		print(states[i], end=" | ")
		value = 0
		for j in range(len(states)):
			#print(eval(str(tMatrix[i][j])), end=" | ")
			value+=(eval(str(tMatrix[i][j])))
		print(" | SUM = " + str(value) + "\n")

	return tMatrix

# Function to obtain all the possible states of the chain when adding an individual to the chain
# originalSequence
def compute_states(originalSequence):

	basicSequence = ['S', 'I', 'R']
	newSequence = []

	for i in range(len(originalSequence)):
		for j in range(len(basicSequence)):
			newSequence.append(originalSequence[i] + basicSequence[j])

	return newSequence

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
