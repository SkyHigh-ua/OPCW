from copy import deepcopy
class Gauswithmainelement:
    def __init__(self, Matrix, Lst):
        self.__MatrixA = Matrix # Матриця коефіцієнтів
        for i in range(len(Lst)):
            self.__MatrixA[i].append(Lst[i]) # Зклеювання матриці коефіцієнтів і стовпця вільних членів
        self.__n = len(Lst) # Розмірність системи

    # Метод для пошуку максимального за модулем елементу в стовпці
    def __maxinrow(self, col):
        MatrixA = self.__MatrixA
        max_element = MatrixA[col][col]
        max_row = col
        for i in range(col + 1, len(MatrixA)):
            if abs(MatrixA[i][col]) > abs(max_element):
                max_element = MatrixA[i][col]
                max_row = i
        if max_row != col:
            MatrixA[col], MatrixA[max_row] = MatrixA[max_row], MatrixA[col]

    # Метод для розв'язку СЛАР
    def solve(self):
        MatrixA = deepcopy(self.__MatrixA)
        n = self.__n
        for k in range(n - 1):
            self.__maxinrow(k)
            for i in range(k + 1, n):
                div = MatrixA[i][k] / MatrixA[k][k]
                MatrixA[i][n] -= div * MatrixA[k][n]
                for j in range(k, n):
                    MatrixA[i][j] -= div * MatrixA[k][j]
        res = [0 for i in range(n)]
        for k in range(n - 1, -1, -1):
            res[k] = (MatrixA[k][n] - sum([MatrixA[k][j] * res[j] for j in range(k + 1, n)])) / MatrixA[k][k] # Почергове знаходження коренів рівняння
        return res