# Main module.

import sys, random, fileManagement, virusSpreadModel, transitionMatrix

if len(sys.argv) != 3:
    print("Utilisation du programme : python3 main.py nombre_d'individus "
          "fichier_contenant_la_matrice_d'adjacence")
    exit(-1)

random.seed()

populationSize = int(sys.argv[1])
fileName = sys.argv[2]

adjacencyMatrix = fileManagement.load_square_matrix(fileName, populationSize) # Loading of the
# adjacency matrix W (see statement)

# Display the matrix
# for i in range(populationSize):
#     for j in range(populationSize):
#         print(adjacencyMatrix[i][j], ',', end = '')
#     print("\n")

initialConfiguration = virusSpreadModel.load_initial_configuration(populationSize)
infectionProbability = 0.5 # Probability beta (see statement)
healProbability = 0.2 # Probability mu (see statement)

# Display the initial configuration
# for i in range(populationSize):
#     print(initialConfiguration[i], ',')

tMatrix = transitionMatrix.compute_transition_matrix(adjacencyMatrix, populationSize)


proportions = virusSpreadModel.virus_evolution(tMatrix, populationSize, initialConfiguration, infectionProbability, healProbability)

print("Susceptible proportion = " + str(proportions[0]))
print("Infected proportion = " + str(proportions[1]))
print("Cured proportion = " + str(proportions[2]))

exit(0)
