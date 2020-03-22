# Fonctions relatives au modèle de propagation du virus.
import random

# Charge une configuration initiale avec 1 infecté et une probabilité de 1 / peopleNumber d'être 
# ce premier infecté de la population. 
def loadInitialConfiguration(peopleNumber):

    initialConfiguration = ['S' for i in range(peopleNumber)]

    random.seed()
    randNumber = random.randint(0, peopleNumber - 1)
    initialConfiguration[randNumber] = 'I'

    return initialConfiguration
