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
        x[i] = b[i] / a[i][i] # @
        for j in range(i-1, -1, -1):
           b[j] = b[j] - a[j][i] * x[i] # O
    return x

def get_first_table(n):
    table_dict = {
        'i': [],
        'xi': [], 
        'bi': [],
        'aii': [],
    }
    for i in range(n, 0, -1):
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
    for i in range(n, 0, -1):
        print(i)
        for j in range(i-1, 0, -1):
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
    table.loc[-1] = [0 for _ in value]
    for i, val in enumerate(value):
        table.iloc[-1][table.columns[i]] = val

def get_vertices(merged_table):
    # VERTICES
    ver1 = merged_table[['i', 'j']].dropna().drop_duplicates()
    ver1.loc[:, 'type'] = 1
    ver2 = merged_table['aii'].dropna().drop_duplicates()
    ver2i = [i[0] for i in ver2[:ver2.shape[0]]]
    ver2 = pd.DataFrame(data={'i': ver2i, 'j': ver2i, 'type': [0 for _ in ver2i]})

    vertices = pd.concat([ver1, ver2], axis=0)
    vertices = vertices.sort_values(['i','j'], ignore_index=True, ascending=False).reset_index(drop=True)
    return vertices.astype(int)

def get_connections(merged_table):
    # CONNECTIONS
    # wrong
    # x_conn = merged_table[['aii', 'aji']].dropna().rename(columns={"aii":"from", "aji":"to"})

    x_conn = {'from': [], 'to': []}
    for i in range(merged_table.shape[0] - 1):
        to = [
            int(merged_table.iloc[i].loc['i']), 
            int(merged_table.iloc[i].loc['j'])
        ]
        x_conn['to'].append(to)
        # print (to[1], " ", to[0] -1)

        fr = None
        if to[1] != to[0] -1:
            fr = [
                int(merged_table.iloc[i-1].loc['i']),
                int(merged_table.iloc[i-1].loc['j'])
            ]
        else:
            fr = int(merged_table.iloc[i].loc['i'])
            fr = [fr, fr]
            print(fr)
        x_conn['from'].append(fr)
    x_conn = pd.DataFrame(data=x_conn)
    
    conn_hepl_table = merged_table[['bi', 'bj', 'i', 'j']]
    b_conn = pd.DataFrame(data={"from": [[0,0]], "to": [[0,0]]})
    print(b_conn.shape)
    
    for i in range(conn_hepl_table.shape[0]):

        if i != conn_hepl_table.shape[0]-1:

            to = find_by_value(conn_hepl_table[i+1:], 'bj', conn_hepl_table["bj"][i], ['i','j'])
            if to is not None:
                to = to.astype(int)
                fr = [
                    int(conn_hepl_table['i'][i]),
                    int(conn_hepl_table['j'][i])
                ]
                b_conn.loc[i] = [fr,to]
                # append_value(b_conn, [fr, to])
                
            else:
                to = int(find_by_value(conn_hepl_table, 'bi', conn_hepl_table["bj"][i], 'i'))
                to = [to, to]
                fr = [
                    int(conn_hepl_table['i'][i]),
                    int(conn_hepl_table['j'][i])
                ]
                b_conn.loc[i] = [fr,to]
                # append_value(b_conn, [fr, to])

    connections = pd.concat([x_conn, b_conn], axis=0).reset_index(drop=True)
    return connections

def fix_i(i, j):
    return i + j - 1

def fix_j(i, j, N):
    return j - i + 1 if j < i +(N+1) / 2 \
        else N - j + i + 1 + (1 - N%2)
    # added +(1-N%2)

def fix_vertices(vertices, N):
    new_vertices = {'i': [], 'j': [], 'type': []}
    for idx in range(vertices.shape[0]):
        row = vertices.iloc[idx]
        i = row.loc['j']
        j = row.loc['i']

        ii = fix_i(i, j)
        jj = fix_j(i, j, N)

        new_vertices['j'].append(ii)
        new_vertices['i'].append(jj)
        new_vertices['type'].append(row.loc['type']) 
    return pd.DataFrame(data=new_vertices)

def fix_connections(connections, N):
    new_connections = {'to': [], 'from': []}
    for idx in range(connections.shape[0]):
        row = connections.iloc[idx]
        for col in ['to', 'from']:
            i = row.loc[col][1]
            j = row.loc[col][0]

            ii = fix_i(i, j)
            jj = fix_j(i, j, N)

            new_connections[col].append([jj, ii])
    return pd.DataFrame(data=new_connections)


        
    
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

size = 5

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
print("----- VERTICES ----")
vertices = get_vertices(merged_help_table)
display(vertices)

print("----- CONNECTIONS ----")
connections = get_connections(merged_help_table)
display(connections)
print("----- GRAPH -----")
# graph = Graph(connections, vertices)
# graph.print()

from graph_gen_sdl import draw_graph

draw_graph(vertices, connections)


fixed_verts = fix_vertices(vertices, size)
print("----- FIXED VERTICES ----")
display(fixed_verts)

fixed_connections = fix_connections(connections, size)
print("----- FIXED CONNECTIONS ----")
display(fixed_connections)

draw_graph(fixed_verts, fixed_connections)
