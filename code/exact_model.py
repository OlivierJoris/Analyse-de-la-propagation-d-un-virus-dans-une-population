# Main module for the exact model (section 1 of the assignment).

import sys, random
import fileManagement, virusSpreadModel, transitionMatrix, graphics_generator

NUMBER_OF_SIMULATIONS = 20 # Represents the number of simulations for question 3

if len(sys.argv) != 4:
    print("Utilisation du programme : python3 main.py nombre_d'individus "
          "fichier_contenant_la_matrice_d'adjacence" "full|lin")
    exit(-1)

random.seed()

populationSize = int(sys.argv[1])
fileName = sys.argv[2]

# limit of the X axis on the graphic
if sys.argv[3] == "full":
	MAX_X = 30
elif sys.argv[3] == "lin":
	MAX_X = 300
else:
	MAX_X = 100

# Loading of the adjacency matrix W (see statement)
adjacencyMatrix = fileManagement.load_square_matrix(fileName, populationSize)#

# Display the matrix
# for i in range(populationSize):
#     for j in range(populationSize):
#         print(adjacencyMatrix[i][j], ',', end = '')
#     print("\n")

infectionProbability = 0.5 # Probability beta (see statement)
healProbability = 0.2 # Probability mu (see statement)

# Compute the transition matrix
tMatrix = transitionMatrix.compute_transition_matrix(adjacencyMatrix, populationSize)

#  *** Question 3 ***

susceptibleProportion = [0 for i in range(MAX_X)]
infectedProportion = [0 for i in range(MAX_X)]
curedProportion = [0 for i in range(MAX_X)]

for i in range(NUMBER_OF_SIMULATIONS):

	# One "simulation" of the model.
	initialConfiguration = virusSpreadModel.load_initial_configuration(populationSize)
	proportions = virusSpreadModel.virus_evolution(tMatrix, populationSize, initialConfiguration, infectionProbability, healProbability)

	# Saving the proportions.
	if len(proportions[0]) < MAX_X:
		max = len(proportions[0])
	else:
		max = MAX_X

	for i in range(max):
		susceptibleProportion[i] += proportions[0][i]
		infectedProportion[i] += proportions[1][i]
		curedProportion[i] += proportions[2][i]

	# Filling the lists if missing values (because a stable situation occured before 50 "times").
	if len(proportions[0]) < MAX_X:
		for i in range(len(proportions[0]), MAX_X):
			susceptibleProportion[i] += proportions[0][len(proportions[0]) - 1]
			infectedProportion[i] += proportions[1][len(proportions[0]) - 1]
			curedProportion[i] += proportions[2][len(proportions[0]) - 1]

# Calculate the mean of the tree lists.
for i in range(MAX_X):
	susceptibleProportion[i]/=NUMBER_OF_SIMULATIONS
	infectedProportion[i]/=NUMBER_OF_SIMULATIONS
	curedProportion[i]/=NUMBER_OF_SIMULATIONS

#print("Susceptible proportion = " + str(susceptibleProportion))
#print("Infected proportion = " + str(infectedProportion))
#print("Cured proportion = " + str(curedProportion))

# Generate the graphic
graphics_generator.graphic(susceptibleProportion, infectedProportion, curedProportion, MAX_X, NUMBER_OF_SIMULATIONS)

exit(0)
