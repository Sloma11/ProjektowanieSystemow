import numpy as np
from matplotlib import pyplot as plt
import random
import timeit
import pandas as pd
import os
from IPython.display import display
from backSubstitution import (
    back_substitution,
    back_substitution_optimized,
    get_matrix_A,
    get_vector_B
)

def generate_times_tables():
    old_algh_times = []
    new_algh_times = []

    # sizes = np.array([25,50,100,200,500,1000, 2000])
    sizes = np.array([25,50,100,200,500])
    # sizes = np.array([2000])

    for size in sizes:
        A = [[random.randint(1, 100) if j > i else 1 if j == i else 0 for j in range(size)] for i in range(size)]
        b = [random.randint(-100, 100) for _ in range(size)]

        newA = get_matrix_A(size)
        newB = get_vector_B(size)

        # display(newA)
        # display(A)

        new_algh_times.append(timeit.timeit(lambda: back_substitution_optimized(newA, newB), number=1))
        old_algh_times.append(timeit.timeit(lambda: back_substitution(A,b), number=1))

    df = pd.DataFrame(data={'size': sizes, 'old algorithm': old_algh_times, 'new algorithm': new_algh_times})

    display(df)

    if not os.path.exists("data/"):
        os.mkdir('data')
    df.to_csv("data/execution_times.csv", index=False)

if __name__ == "__main__":
    generate_times_tables()