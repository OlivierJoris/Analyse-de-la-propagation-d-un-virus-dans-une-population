# Module relative to the spread model of the virus.
import random

# Load an initial configuration with 1 infected and a 1 / populationSize probability to be this 
# first infected of the population.
def load_initial_configuration(populationSize):

    initialConfiguration = ['S' for i in range(populationSize)]

    random.seed()
    randNumber = random.randint(0, populationSize - 1)
    initialConfiguration[randNumber] = 'I'

    return initialConfiguration
