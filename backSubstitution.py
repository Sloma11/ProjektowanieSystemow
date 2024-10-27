import timeit
import random
import pandas as pd
from IPython.display import display
import numpy as np
from graph_gen import Graph

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
        table_dict['aii'].append([i,i])
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

def find_by_value(table, column_to_search, value, column_of_result):
    result = table.where(
        table[column_to_search] == value
    )[column_of_result].dropna()
    if result.size == 0:
        return None
    return result.values[0]

def append_value(table, value):
    table.loc[table.shape[0]] = value

def get_vertices_and_connections(merged_table):
    # VERTICES
    ver1 = merged_table["aii"].dropna().drop_duplicates()
    ver2 = merged_table["aji"].dropna().drop_duplicates()
    ver1 = pd.DataFrame(data= {"ver": ver1, "type": 0})
    ver2 = pd.DataFrame(data= {"ver": ver2, "type": 1})

    vertices = pd.concat([ver1, ver2], axis=0).reset_index(drop=True)

    # CONNECTIONS
    x_conn = merged_table[['aii', 'aji']].dropna().rename(columns={"aii":"from", "aji":"to"})
    
    conn_hepl_table = merged_table[['bi', 'bj', 'aii', 'aji']]
    b_conn = pd.DataFrame(data={"from": [], "to": []})
    
    for i in range(conn_hepl_table.shape[0]):

        if i != conn_hepl_table.shape[0]-1:

            to = find_by_value(conn_hepl_table[i+1:], 'bj', conn_hepl_table["bj"][i], 'aji')
            if to != None:
                append_value(b_conn, [conn_hepl_table['aji'][i], to])
                
            else:
                to = find_by_value(conn_hepl_table, 'bi', conn_hepl_table["bj"][i], 'aii')
                append_value(b_conn, [conn_hepl_table['aji'][i], to])

        connections = pd.concat([x_conn, b_conn], axis=0).reset_index(drop=True)

    return {
        "connections": connections,
        "vertices": vertices,
    }
    
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
# size = 
#size = 1000   # 0.0623225000 sekund
#size = 10000    12.2518855000 sekund
# size = 40000 #  362.3816005000 sekund


# A = [[random.randint(1, 100) if j > i else 1 if j == i else 0 for j in range(size)] for i in range(size)]
# b = [random.randint(-100, 100) for _ in range(size)]

A= [
    [1, 3, 5],
    [0, 1, 2],
    [0, 0, 1]
    ]

b = [2,4,3]

size = 100

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
print("-------------------")

merged_help_table = pd.merge(ft, st, how='left')
display(merged_help_table)
print("-------------------")

ver_and_con = get_vertices_and_connections(merged_help_table)
print("----- VERTICES ----")
display(ver_and_con['vertices'])
print("----- CONNECTIONS ----")
display(ver_and_con['connections'])

print("----- GRAPH -----")
graph = Graph(ver_and_con["connections"], ver_and_con["vertices"])
graph.print()