import timeit
import random
import pandas as pd
from IPython.display import display


def back_substitution(a, b):
    N = len(a)
    x = [0] * N 

    for i in range(N-1, -1, -1):
        x[i] = b[i] / a[i][i]
        for j in range(i-1, -1, -1):
           b[j] = b[j] - a[j][i] * x[i]
    return x

def get_first_table(n):
    table_dict = {
        'i': [],
        'xi': [], 
        'bi': [],
        'aii': [],
    }
    idx: int = 1
    for i in range(n-1, -1, -1):
        table_dict['i'].append(i)
        table_dict['xi'].append(i)
        table_dict['bi'].append(i)
        table_dict['aii'].append(i)
    return pd.DataFrame(data=table_dict)

def get_second_table(n):
    table_dict = {
        'i': [],
        'j': [],
        'bj': [],
        'aji': [],
        'xi': [], 
    }
    idx: int = 1
    for i in range(n-1, -1, -1):
        for j in range(i-1, -1, -1):
            table_dict['i'].append(i)
            table_dict['j'].append(j)
            table_dict['bj'].append(j)
            table_dict['aji'].append([j,i])
            table_dict['xi'].append(i)
    return pd.DataFrame(data=table_dict)

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
size = 4
#size = 1000   # 0.0623225000 sekund
#size = 10000    12.2518855000 sekund
# size = 40000 #  362.3816005000 sekund


A = [[random.randint(1, 100) if j > i else 1 if j == i else 0 for j in range(size)] for i in range(size)]
b = [random.randint(-100, 100) for _ in range(size)]


def solve():
    return back_substitution(A, b)

#print("Rozwiązanie:", x)
# execution_time = timeit.timeit(solve, number=1)
# print(f"Czas trwania obliczeń: {execution_time:.10f} sekund")

ft = get_first_table(size)
st = get_second_table(size)

display(ft)
print("-------------------")
display(st)

result = pd.concat([ft, st], ignore_index=True)
print("-------------------")
display(result)
