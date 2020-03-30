# Main module for simulation-based study (section 2 of the assignement).

import sys, random
import file_management, virus_spread_model, graphics_generator

NUMBER_OF_SIMULATIONS = 10

if len(sys.argv) != 4:
    print("Program usage : python3 simulations_study.py populationSize "
          "adjacencyMatrixFileName initialInfectedProportion")
    exit(-1)

random.seed()

populationSize = int(sys.argv[1])
fileName = sys.argv[2]
initialInfectedProportion = float(sys.argv[3])

MAX_X = populationSize * 7

# Loading of the adjacency matrix W (see statement).
adjacencyMatrix = file_management.load_square_matrix(fileName, populationSize)

infectionProbability = 0.5 # Probability beta (see statement).
healProbability = 0.2 # Probability µ (see statement).

NUMBER_OF_SIMULATIONS = int(input("Number of \"simulations\" for the proportions of S/T/I and the average time :"))

# Computing the mean of the proportions and the average time for disappearance of the virus based 
# on simulations.
meanStateProportions = virus_spread_model.compute_mean_proportions_time(adjacencyMatrix, populationSize,
                       infectionProbability, healProbability, NUMBER_OF_SIMULATIONS, MAX_X, initialInfectedProportion)

meanSusceptibleProportions = meanStateProportions[0]
meanInfectedProportions = meanStateProportions[1]
meanImmunisedProportions = meanStateProportions[2]

meanInfectedTime = meanStateProportions[3]

print("\nAverage time it takes for the virus to disappear completely : " + str(meanInfectedTime))

# Generation of the corresponding evolution graphic.
graphics_generator.graphic(meanSusceptibleProportions, meanInfectedProportions,
                           meanImmunisedProportions, MAX_X, NUMBER_OF_SIMULATIONS)

exit(0)
