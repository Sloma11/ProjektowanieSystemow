import random
from IPython.display import display
import numpy as np

def back_substitution(a, b):
    N = len(a)
    x = [0] * N 

    for i in range(N-1, -1, -1):
        x[i] = b[i] / a[i][i]
        for j in range(i-1, -1, -1):
           b[j] = b[j] - a[j][i] * x[i]
    return x

def get_matrix_A(n):
    rng = np.random.default_rng(34)
    one = np.ones(1)
    rows = None
    for i in range(n):
        zeros = np.zeros(n - (n-i)) 
        integers = rng.integers(low=1, high=40, size=(n-i-1))

        row = np.concatenate((zeros, one, integers))
        if rows is not None:
            rows = np.concatenate((rows, row[np.newaxis, : ]))
        else:
            rows = row[np.newaxis, : ]
        
    return rows

def get_vector_B(n):
    rng = np.random.default_rng()
    return rng.random(size=(n))
        

def back_substitution_optimized(a, b):
    n = len(a)
    x = np.zeros(n)
    i_range = np.arange(n-1, -1, -1, dtype=int)
    for i in i_range:
        x[i] = b[i] / a[i][i]
        j_range = np.arange(i-1, -1, -1, dtype=int) 
        for j in j_range:
            b[j] = b[j] - a[j][i] * x[i]
    return x


if __name__ == "__main__":
    A = np.array([
        [1, -2, 1],
        [0, 1, 6],
        [0, 0, 1]
        ])

    b = np.array([4, -1, 2])

    x = back_substitution_optimized(A, b)
    print("Wektor X: ")
    display(x)




