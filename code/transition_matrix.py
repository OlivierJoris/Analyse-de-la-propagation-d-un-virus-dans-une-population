# ------------------------------------------------------------------------------#
# Module to get the transition matrix using W (adjacency matrix) and N (the size
# of the population).
#
# GOFFART Maxime (180521) & JORIS Olivier (182113)
# ------------------------------------------------------------------------------#


import sys
import numpy as np
import states_manipulator

# ------------------------------------------------------------------------------#
# Function to display the transition matrix.
# ------------------------------------------------------------------------------#
def display(tMatrix):
	for i in range(len(tMatrix)):
		for j in range(len(tMatrix)):
			print(tMatrix[i][j], end=" | ")
		print("\n")

# ------------------------------------------------------------------------------#
# Function to compute the transition matrix (as a matrix of strings) based on
# the graph W and the size of the population.
# ------------------------------------------------------------------------------#
def compute_transition_matrix(adjacencyMatrix, populationSize):

	if(len(adjacencyMatrix) != populationSize):
		print("ERROR : adjacency matrix size doesn't match the populaion's size")
		return

	states = ['S', 'I', 'R']

	# Computes all the possible states
	for i in range(populationSize - 1):
		states = states_manipulator.compute_states(states)

	# Creates an empty transition matrix
	tMatrix = [[' ' for i in range(len(states))] for i in range(len(states))]

	# The first state which is SS is a special case

	tMatrix[0][0] = 1
	for i in range(len(states) - 1):
		tMatrix[0][i+1] = 0

	# Others lines

	for i in range(1, len(states)):
		sys.stdout.write("\rComputing line n°%d/%d of the transition matrix" % ((i+1), len(states)))
		sys.stdout.flush()
		state1 = states[i]

		# If the current state (state1) doesn't contained 'I' than we can only stay in the same state
		# Absorbent state
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

	# Remove the last '*' of each string if necessary
	for i in range(len(states)):
		for j in range(len(states)):
			tmpString = tMatrix[i][j]
			if isinstance(tmpString, str) and '0' in tmpString:
				tMatrix[i][j] = 0
			elif isinstance(tmpString, str) and tmpString.endswith('*'):
				tMatrix[i][j] = tmpString[0:(len(tmpString)-1)]

	return tMatrix

# ------------------------------------------------------------------------------#
# Function to replace beta and mu in the transition matrix (matrix of strings)
# in order to obtain a matrix of floats.
# ------------------------------------------------------------------------------#
def evaluate_transition_matrix(tMatrix, populationSize, beta, mu):

	if len(tMatrix) != pow(3, populationSize):
		print("Error : matrix size is NOT equal to populationSize^3")
		return []

	b = beta
	u = mu

	temp = [[0 for i in range(len(tMatrix))] for i in range(len(tMatrix))]

	for i in range(len(tMatrix)):
		for j in range(len(tMatrix)):
			temp[i][j] = eval(str(tMatrix[i][j]))


	return temp

# ------------------------------------------------------------------------------#
# Function to compute the time required for the complete disappearance of the
# virus.
# ------------------------------------------------------------------------------#
def find_time_virus_disappearance(tMatrix, populationSize, states):

	# Retract all the absorbing states
	absorbingStates = states_manipulator.find_absorbing_state(states)

	# Matrix B of Ax=B
	B = [-1 for i in range(len(states))]

	# Matrix A of Ax=B
	A = [[0 for i in range(len(states))] for i in range(len(states))]

	# Fill A and B
	for i in range(len(tMatrix)):
		for j in range(len(tMatrix)):

			# Absorbing states
			if i == j and states_manipulator.stable_situation(states[i]) and tMatrix[i][j] == 1:
				B[i] = 0
				A[i][j] = 1
				continue

			# Others states
			if i == j:
				A[i][j] = tMatrix[i][j] - 1
				continue

			A[i][j] = tMatrix[i][j]

	# Solving the system Ax=B
	X = np.linalg.solve(A, B)

	# Find all possible initial states (only one infected)
	initialStates = states_manipulator.find_initial_states(states, populationSize)

	counter = 0
	averageTime = 0.0

	for i in range(len(X)):
		if states[i] in initialStates:
			averageTime+=X[i]
			counter+=1

	return averageTime/counter
