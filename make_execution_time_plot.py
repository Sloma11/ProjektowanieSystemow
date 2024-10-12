import os
import pandas as pd
from IPython import display 
from matplotlib import pyplot as plt

path = "data/execution_times.csv"

def make_execution_time_plot():
    if not os.path.exists(path):
        print(f"[ERROR] \"{path}\" file didn't exist!")
        return
    
    df = pd.read_csv(path)
    expected_columns = ['size', 'old algorithm', 'new algorithm']
    expected_columns.sort()
    df_columns = df.columns.to_list()
    df_columns.sort()

    if df_columns != expected_columns:
        print(f"[ERROR] columns:{df_columns}, from \"{path}\" are not equals columns {expected_columns}!")
        return
    
    sizes = df['size']
    old_algh_times = df['old algorithm']
    new_algh_times = df['new algorithm']

    plt.plot(sizes, old_algh_times, label="old algorithm")
    plt.plot(sizes, new_algh_times, label="new algorithm")
    plt.legend()
    plt.savefig('data/execution_time.png')
    plt.show()

if __name__ == "__main__":
    make_execution_time_plot()