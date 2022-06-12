from copy import deepcopy
from numpy.linalg import det
class Cramer:
    def __init__(self, Matrix, Lst):
        self.__MatrixA = Matrix # Матриця коефіцієнтів
        self.__LstB = Lst # Стовпець вільних членів
        self.__n = len(Lst) # Розмірність системи
    
    # Метод для розв'язку СЛАР
    def solve(self):
        MatrixA = self.__MatrixA
        LstB = self.__LstB
        n = self.__n
        res=[]
        d = det(MatrixA) 
        MatrixAcopy = deepcopy(MatrixA)
        for i in range(n):
            for j in range(n):
                MatrixAcopy[j][i] = LstB[j]
            dt=det(MatrixAcopy)
            MatrixAcopy = deepcopy(MatrixA)
            res.append(dt/d)
        return res