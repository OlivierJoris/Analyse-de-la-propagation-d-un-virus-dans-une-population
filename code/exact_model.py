# ------------------------------------------------------------------------------#
# Main module for the exact model (section 1 of the assignment).
#
# Usage : python3 exactct_model.py <N> <W>
#
# GOFFART Maxime (180521) & JORIS Olivier (182113)
# ------------------------------------------------------------------------------#


import sys, random
import file_management, virus_spread_model, transition_matrix, graphics_generator, states_manipulator

if len(sys.argv) != 3:
    print("Utilisation du programme : python3 exact_model.py populationSize "
          "adjacencyMatrixFileName")
    exit(-1)

random.seed()

populationSize = int(sys.argv[1])
fileName = sys.argv[2]

# Loading of the adjacency matrix W (see statement)
adjacencyMatrix = file_management.load_square_matrix(fileName, populationSize)#

infectionProbability = 0.5 # Probability beta (see statement)
healProbability = 0.2 # Probability mu (see statement)

states = ['S', 'I', 'R']

# ------------------------------------------------------------------------------#
# SECTION I
# ------------------------------------------------------------------------------#

# Computes all the possible states
for i in range(populationSize - 1):
	states = states_manipulator.compute_states(states)

sys.stdout.write("Computing transition matrix\n")
sys.stdout.flush()

# Computes the transition matrix
tMatrix = transition_matrix.compute_transition_matrix(adjacencyMatrix, populationSize)

sys.stdout.write("\nEvaluating transition matrix\n")
sys.stdout.flush()

# Evaluates the transition matrix (ie replace beta and mu by there value)
tMatrix = transition_matrix.evaluate_transition_matrix(tMatrix, populationSize, infectionProbability, healProbability)

# Computes the average time require for the complete disappearance of the virus
averageTime = transition_matrix.find_time_virus_disappearance(tMatrix, populationSize, states)

# ------------------------------------------------------------------------------#
# SECTION I - Q.3
# ------------------------------------------------------------------------------#

sys.stdout.write("Computing evolution of the virus\n")
sys.stdout.flush()

# Evolution of the virus (Q3 of the assignment)
virus_spread_model.virus_evolution(tMatrix, populationSize, states)

print("It took " + str(averageTime) + " steps of the chain for the virus to completely disappear")

exit(0)
