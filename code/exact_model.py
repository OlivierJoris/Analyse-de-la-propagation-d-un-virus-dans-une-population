# Main module for the exact model (section 1 of the assignment).

import sys, random
import fileManagement, virusSpreadModel, transitionMatrix, graphics_generator

# limit of the X axis on the graphic
MAX_X = 30

if len(sys.argv) != 3:
    print("Utilisation du programme : python3 main.py nombre_d'individus "
          "fichier_contenant_la_matrice_d'adjacence")
    exit(-1)

random.seed()

populationSize = int(sys.argv[1])
fileName = sys.argv[2]

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

#  *** Question 3 & 4***

NUMBER_OF_SIMULATIONS = int(input("Number of \"simulations\" for the proportions of S/T/I and the average time :"))

susceptibleProportion = [0 for i in range(MAX_X)]
infectedProportion = [0 for i in range(MAX_X)]
curedProportion = [0 for i in range(MAX_X)]
time = 0

for i in range(NUMBER_OF_SIMULATIONS):

	sys.stdout.write("\rSimulation n°%d/%d" % ((i+1), NUMBER_OF_SIMULATIONS))
	sys.stdout.flush()

	# One "simulation" of the model.
	initialConfiguration = virusSpreadModel.load_initial_configuration(populationSize)
	proportions = virusSpreadModel.virus_evolution(tMatrix, populationSize, initialConfiguration, infectionProbability, healProbability)

	time+=proportions[3]

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

# Calculate the average time
time/=NUMBER_OF_SIMULATIONS

#print("Susceptible proportion = " + str(susceptibleProportion))
#print("Infected proportion = " + str(infectedProportion))
#print("Cured proportion = " + str(curedProportion))

# Generate the graphic
graphics_generator.graphic(susceptibleProportion, infectedProportion, curedProportion, MAX_X, NUMBER_OF_SIMULATIONS)

print("\nAverage time it takes for the virus to disappear completely : " + str(time))

exit(0)
