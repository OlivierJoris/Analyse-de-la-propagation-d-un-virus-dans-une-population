# ------------------------------------------------------------------------------#
# Module for generating a graphic based on the proportions of susceptible people,
# infected people, and cured people.
# maxTime represents the maximum time.
#
# GOFFART Maxime (180521) & JORIS Olivier (182113)
# ------------------------------------------------------------------------------#


import matplotlib.pyplot as plt

def graphic(susceptibleProportion, infectedProportion, curedProportion, maxTime, numberOfSimulations):

	xAxis = list(range(maxTime))

	plt.plot(xAxis, susceptibleProportion, label = "Susceptible proportion", color = "blue")
	plt.plot(xAxis, infectedProportion, label = "Infected proportion", color = "red")
	plt.plot(xAxis, curedProportion, label = "Cured proportion", color = "green")
	plt.ylabel("Proportion")
	plt.xlabel("Time (t)")
	if numberOfSimulations != 0:
		plt.title("Evolution based on " + str(numberOfSimulations) + " simulations")
	else:
		plt.title("Evolution of the proportions")
	plt.legend()
	plt.show()
