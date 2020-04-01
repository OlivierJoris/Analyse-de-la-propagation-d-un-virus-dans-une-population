# ------------------------------------------------------------------------------#
# Main module for simulation-based study (section 2 of the assignement).
#
# Usage : python3 simulations_study.py <N> <W>
#
# GOFFART Maxime (180521) & JORIS Olivier (182113)
# ------------------------------------------------------------------------------#


import sys, random
import file_management, virus_spread_model, graphics_generator

if len(sys.argv) != 3:
    print("Program usage : python3 simulations_study.py populationSize "
          "adjacencyMatrixFileName")
    exit(-1)

random.seed()

populationSize = int(sys.argv[1])
fileName = sys.argv[2]

# Loading of the adjacency matrix W (see statement)
adjacencyMatrix = file_management.load_square_matrix(fileName, populationSize)

# Asking the user for constant parameters
initialInfectedProportion = float(input("Initial proportion of infected (fractions not "
                                          "supported) : "))
initialImmunisedProportion = float(input("Initial proportion of vaccinated (fractions not "
                                           "supported) : "))
infectionProbability = float(input("Probability to be infected (beta in statement, fractions not "
                                    "supported) : "))
healProbability = float(input("Probability to be healed (mu in statement, fractions not "
                               "supported) : "))
maxInteractionsNumber = int(input("Maximum number of interactions for one person "
                                  "(containment mesures): "))
simulationsNumber = int(input("Number of \"simulations\" for the proportions of S/R/I and the "
                                  "average time : "))
maxTime = int(input("Maximum time (x axis of the output graphic) : "))

# Computing the mean of the proportions and the average time for disappearance of the virus based
# on simulations
meanStateProportions = virus_spread_model.compute_mean_proportions_time(adjacencyMatrix,
                       populationSize, infectionProbability, healProbability,
                       simulationsNumber, maxTime, initialInfectedProportion,
                       initialImmunisedProportion, maxInteractionsNumber)

# Displays of the average time for disappearance of the virus
meanInfectedTime = meanStateProportions[3]
print("\nAverage time it takes for the virus to disappear completely : " + str(meanInfectedTime))

# Generation of the corresponding evolution graphic
meanSusceptibleProportions = meanStateProportions[0]
meanInfectedProportions = meanStateProportions[1]
meanImmunisedProportions = meanStateProportions[2]
graphics_generator.graphic(meanSusceptibleProportions, meanInfectedProportions,
                           meanImmunisedProportions, maxTime, simulationsNumber)

exit(0)
