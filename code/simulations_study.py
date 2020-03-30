# Main module for simulation-based study (section 2 of the assignement).

import sys, random
import file_management, virus_spread_model, graphics_generator

if len(sys.argv) != 3:
    print("Program usage : python3 simulations_study.py populationSize "
          "adjacencyMatrixFileName")
    exit(-1)

random.seed()

POPULATION_SIZE = int(sys.argv[1])
FILE_NAME = sys.argv[2]

# Loading of the adjacency matrix W (see statement).
ADJACENCY_MATRIX = file_management.load_square_matrix(FILE_NAME, POPULATION_SIZE)

# Asking the user for constant parameters.
INITIAL_INFECTED_PROPORTION = float(input("Initial proportion of infected (fractions not "
                                          "supported) :"))
INITIAL_IMMUNISED_PROPORTION = float(input("Initial proportion of immunised (fractions not "
                                           "supported) :"))
INFECTION_PROBABILITY = float(input("Probability to be infected (beta in statement, fractions not "
                                    "supported) :"))
HEAL_PROBABILITY = float(input("Probability to be healed (mu in statement, fractions not "
                               "supported) :"))
NUMBER_OF_SIMULATIONS = int(input("Number of \"simulations\" for the proportions of S/T/I and the "
                                  "average time :"))
MAX_TIME = int(input("Maximum time (x axis of the output graphic) :"))

# Computing the mean of the proportions and the average time for disappearance of the virus based 
# on simulations.
meanStateProportions = virus_spread_model.compute_mean_proportions_time(ADJACENCY_MATRIX, 
                       POPULATION_SIZE, INFECTION_PROBABILITY, HEAL_PROBABILITY, 
                       NUMBER_OF_SIMULATIONS, MAX_TIME, INITIAL_INFECTED_PROPORTION, 
                       INITIAL_IMMUNISED_PROPORTION)

# Display of the average time for disappearance of the virus.
meanInfectedTime = meanStateProportions[3]
print("\nAverage time it takes for the virus to disappear completely : " + str(meanInfectedTime))

# Generation of the corresponding evolution graphic.
meanSusceptibleProportions = meanStateProportions[0]
meanInfectedProportions = meanStateProportions[1]
meanImmunisedProportions = meanStateProportions[2]
graphics_generator.graphic(meanSusceptibleProportions, meanInfectedProportions,
                           meanImmunisedProportions, MAX_TIME, NUMBER_OF_SIMULATIONS)

exit(0)
