from copy import deepcopy
class Gauswithsingdiagonal:
    def __init__(self, Matrix, Lst):
        self.__MatrixA = Matrix # Матриця коефіцієнтів
        self.__LstB = Lst # Стовпець вільних членів
        self.__n = len(Lst) # Розмірність системи

    # Метод для розв'язку СЛАР
    def solve(self):
        MatrixA = deepcopy(self.__MatrixA)
        LstB = deepcopy(self.__LstB)
        n = self.__n
        # Прямий хід
        for i in range(n):
            LstB[i]/=MatrixA[i][i]
            for j in range(n-1, -1, -1):
                MatrixA[i][j] /= MatrixA[i][i]  
            for j in range(n-1, i, -1):
                LstB[j]-=MatrixA[j][i] * LstB[i]
                for k in range(n-1, -1, -1):
                    MatrixA[j][k] -= MatrixA[j][i] * MatrixA[i][k]
        # Зворотній хід
        for i in range(n-1, -1, -1):
            for j in range(i-1,-1,-1):
                LstB[j] -= LstB[i]*MatrixA[j][i]
                MatrixA[j][i] -= MatrixA[j][i]
        return LstB