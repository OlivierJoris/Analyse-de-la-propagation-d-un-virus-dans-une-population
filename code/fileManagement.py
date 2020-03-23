# Module to manage files.

# Load the square matrix (size * size) which is in the file fileName and return the corresponding
# matrix.
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
