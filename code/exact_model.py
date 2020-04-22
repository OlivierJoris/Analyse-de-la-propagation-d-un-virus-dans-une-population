# ------------------------------------------------------------------------------#
# Main module for the exact model (section 1 of the assignment).
#
# Usage : python3 exact_model.py <N> <W>
#
# GOFFART Maxime (180521) & JORIS Olivier (182113)
# ------------------------------------------------------------------------------#


import sys, random
import file_management, virus_spread_model, transition_matrix, graphics_generator, states_manipulator

if len(sys.argv) != 3:
    print("Program usage : python3 exact_model.py populationSize "
          "adjacencyMatrixFileName")
    exit(-1)

random.seed()

populationSize = int(sys.argv[1])
fileName = sys.argv[2]

# Loading of the adjacency matrix W (see statement)
adjacencyMatrix = file_management.load_square_matrix(fileName, populationSize)

infectionProbability = 0.5 # Probability beta (see statement)
healProbability = 0.2 # Probability mu (see statement)

states = ['S', 'I', 'R']

# ------------------------------------------------------------------------------#
# SECTION I
# ------------------------------------------------------------------------------#

# Computes all the possible states
for i in range(populationSize - 1):
	states = states_manipulator.compute_states(states)

print("Computing transition matrix")

# Computes the transition matrix as a matrix of strings
tMatrix = transition_matrix.compute_transition_matrix(adjacencyMatrix, populationSize)

print("\nEvaluating transition matrix")

# Evaluates the transition matrix (ie replaces beta and mu by there values)
tMatrix = transition_matrix.evaluate_transition_matrix(tMatrix, populationSize, infectionProbability, healProbability)

# ------------------------------------------------------------------------------#
# SECTION I - Q.3
# ------------------------------------------------------------------------------#

print("Computing evolution of the virus")

# Evolution of the virus (Q3 of the assignment)
virus_spread_model.virus_evolution(tMatrix, populationSize, states)

# ------------------------------------------------------------------------------#
# SECTION I - Q.4
# ------------------------------------------------------------------------------#

# Computes the average time required for the complete disappearance of the virus
averageTime = transition_matrix.find_time_virus_disappearance(tMatrix, populationSize, states)

print("It took " + str(averageTime) + " steps of the chain for the virus to completely disappear")

exit(0)
