# Fichier principal.

import sys, fileManagement, virusSpreadModel, transitionMatrix

if len(sys.argv) != 3:
    print("Utilisation du programme : python3 main.py nombre_d'individus "
          "fichier_contenant_la_matrice_d'adjacence")
    exit(-1)

peopleNumber = int(sys.argv[1])
fileName = sys.argv[2]

adjacencyMatrix = fileManagement.loadSquareMatrix(fileName, peopleNumber) # Chargement de la
# matrice d'adjacence w (cf. énoncé)

# Afficher la matrice pour test
# for i in range(peopleNumber):
#     for j in range(peopleNumber):
#         print(adjacencyMatrix[i][j], ',', end = '')
#     print("\n")

initialConfiguration = virusSpreadModel.loadInitialConfiguration(peopleNumber)
infectionProbability = 0.5 # Probabilité beta (cf. énoncé)
healProbability = 0.2 # Probabilité mu (cf. énoncé)

# Afficher la configuration initiale
# for i in range(peopleNumber):
#     print(initialConfiguration[i], ',')

tMatrix = transitionMatrix.compute_transition_matrix(adjacencyMatrix, peopleNumber)

exit(0)
