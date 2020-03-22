# Fonctions relatives à la gestion de fichiers.

# Charge la matrice carrée de taille size * size contenue dans le fichier fileName et retourne
# la matrice correspondante.
def loadSquareMatrix(fileName, size):

    matrix = [[0 for i in range(size)] for i in range(size)]

    # Remplissage de la matrice
    with open(fileName, 'r', encoding = 'utf-8') as f:
        for i in range(size):
            for j in range(size):
                matrix[i][j] = f.read(1)
                f.read(1)
            # Afficher la matrice pour test
            #     print(matrix[i][j], ',', end = '') 
            # print("\n")
    return matrix
