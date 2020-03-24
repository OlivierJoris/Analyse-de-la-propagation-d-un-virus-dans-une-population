# Module for generating a graphic based on the proportions of susceptible people,
# infected people, and cured people.
# maxTime represents the maximum time.

import matplotlib.pyplot as plt

def graphic(susceptibleProportion, infectedProportion, curedProportion, maxTime, numberOfSimulations):

	xAxis = list(range(maxTime))

	plt.plot(xAxis, susceptibleProportion, label = "Susceptible proportion", color = "blue")
	plt.plot(xAxis, infectedProportion, label = "Infected proportion", color = "red")
	plt.plot(xAxis, curedProportion, label = "Cured proportion", color = "green")
	plt.ylabel("Proportion")
	plt.xlabel("Time")
	plt.title("Evolution based on " + str(numberOfSimulations) + " \"simulations\"")
	plt.legend()
	plt.show()
