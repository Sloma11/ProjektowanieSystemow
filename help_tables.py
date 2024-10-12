import pandas as pd
from IPython.display import display

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

if __name__ == "__main__":
    size = 5
    ft = get_first_table(size)
    st = get_second_table(size)



    display(ft)
    print("-------------------")
    display(st)

    result = pd.concat([ft, st], ignore_index=True)
    print("-------------------")
    display(result)
