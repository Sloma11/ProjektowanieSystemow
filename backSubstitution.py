import timeit
import random

def back_substitution(a, b):
    N = len(a)
    x = [0] * N  

    for i in range(N-1, -1, -1):
        x[i] = b[i] / a[i][i]
        for j in range(i-1, -1, -1):
           b[j] = b[j] - a[j][i] * x[i]
    return x

#-------------------------------------
"""""
A= [
    [1, -2, 1],
    [0, 1, 6],
    [0, 0, 1]
    ]

b = [4, -1, 2]
# 0.0000104000 sekund
#-------------------------------------
"""
#size = 1000    0.0623225000 sekund
#size = 10000    12.2518855000 sekund
size = 1000000 


A = [[random.randint(1, 100) if j >= i else 0 for j in range(size)] for i in range(size)]
b = [random.randint(-100, 100) for _ in range(size)]

def solve():
    return back_substitution(A, b)

x=solve()

#print("Rozwiązanie:", x)
execution_time = timeit.timeit(solve, number=1)
print(f"Czas trwania obliczeń: {execution_time:.10f} sekund")