# Module to get the transition matrix using W and N

def compute_transition_matrix(adjacencyMatrix, populationSize):

	if(len(adjacencyMatrix) != populationSize):
		print("ERROR : adjacency matrix size doesn't match the populaion's size")
		return

	states = ['S', 'I', 'R']

	# Compute all the possible states
	for i in range(populationSize - 1):
		states = compute_states(states)

	print("Number of differents states = " + str(len(states)))

	# Display all the states
	for i in range(len(states)):
		print(states[i])

	# Create an empty transition matrix
	tMatrix = [[' ' for i in range(len(states))] for i in range(len(states))]

	# The first state which is SS is a special case

	tMatrix[0][0] = 1
	for i in range(len(states) - 1):
		tMatrix[0][i+1] = 0

	# Others lines

	for i in range(1, len(states)):
		state1 = states[i]
		for j in range(len(states)):

			state2 = states[j]

			for k in range(len(state1)):

				# All cases
				if state1[k] == 'I' and state2[k] == 'S':
					tMatrix[i][j] = 0
					break
				elif state1[k] == 'R' and state2[k] == 'I':
					tMatrix[i][j] = 0
					break
				elif state1[k] == 'S' and state2[k] == 'R':
					tMatrix[i][j] = 0
					break
				elif state1[k] == 'R' and state2[k] == 'S':
					tMatrix[i][j] = 0
					break
				elif state1[k] == 'S' and state2[k] == 'I':
					# Under conditions that :
					#  - Anoter person is infected
					#  - They know each other
					for l in range(len(state1)):
						if state1[l] == 'I' and l != k:
							if adjacencyMatrix[l][k] == 1:
								tMatrix[i][k] += '(b)'
				elif state1[k] == 'S' and state2[k] == 'S':
					tMatrix[i][j] += '(1-b)'
				elif state1[k] == 'I' and state2[k] == 'I':
					tMatrix[i][j] += '(1-u)'
				elif state1[k] == 'I' and state2[k] == 'R':
					tMatrix[i][j] += '(u)'
				elif state1[k] == 'R' and state2[k] == 'R':
					tMatrix[i][j] += '(1)'

	for i in range(len(states)):
		for j in range(len(states)):
			print(tMatrix[i][j], end=" | ")
		print("\n")

	return tMatrix

# Fonction qui permet d'obtenir les états possibles de la chaine lorsqu'on rajoute un
#individu à la chaine originalSequence
def compute_states(originalSequence):

	basicSequence = ['S', 'I', 'R']
	newSequence = []

	for i in range(len(originalSequence)):
		for j in range(len(basicSequence)):
			newSequence.append(originalSequence[i] + basicSequence[j])

	return newSequence
