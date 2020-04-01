# ------------------------------------------------------------------------------#
# Module to manage files.
#
# GOFFART Maxime (180521) & JORIS Olivier (182113)
# ------------------------------------------------------------------------------#


# ------------------------------------------------------------------------------#
# Loads the square matrix (size * size) which is in the file fileName and return
# the corresponding matrix.
# ------------------------------------------------------------------------------#
def load_square_matrix(fileName, size):

    matrix = [[0 for i in range(size)] for i in range(size)]

    # Filling of the matrix
    with open(fileName, 'r', encoding = 'utf-8') as f:
        for i in range(size):
            for j in range(size):
                matrix[i][j] = f.read(1)
                f.read(1)
            # Display the matrix
            #     print(matrix[i][j], ',', end = '')
            # print("\n")
    return matrix

# ------------------------------------------------------------------------------#
# Saves the transition matrix in the file fileName.
# Used for debugging purposes.
# ------------------------------------------------------------------------------#
def save_matrix(tMatrix, fileName):

	f = open(fileName, "w")
	for i in range(len(tMatrix)):
		for j in range(len(tMatrix)):
			f.write(str(tMatrix[i][j]) + " ")
		f.write("\n")

	f.close()
