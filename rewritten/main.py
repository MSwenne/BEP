import numpy as np
import time
import sys

from cnf_grover import grover_search_cnf
from fpaa_grover import grover_search_fpaa

def make_cnf(file):
    with open(file, 'r') as f:
        answers = f.readline()
        n, clauses, k = [int(x) for x in next(f).split()]
        oracle = [[int(x) for x in line.split()] for line in f]
    oracle_bin = np.negative([np.ones(n) for x in range(clauses)])
    for i in range(clauses):
        for j in oracle[i]:
            oracle_bin[i][abs(j)-1] = int(j < 0)
    oracle = oracle_bin
    index = []
    for j in range(clauses):
        index.extend([[]])
        for i in range(n):
            if oracle[j][i] != -1:
                index[j].extend([i])
    print(answers)
    print(oracle)
    return n, clauses, k, oracle, index

def experiment():
    start_val = 1
    end_val  = 100
    runs = 10
    shots = 100
    n, clauses, oracle, index, nr_solutions = make_cnf()

    dist = end_val-start_val+(end_val - start_val) / (runs-1)
    values = np.arange(start_val,end_val+(end_val - start_val) / (runs-1), dist/runs)
    data = []

    for i in range(len(values)):
        data.append(grover_search_cnf_noisy(n, clauses, shots, oracle, index, nr_solutions, values[i]))

    print(data)

def main():
    if len(sys.argv) != 2:
        print('0 for cnf, 1 for fpaa')
        exit(-1)
    n, clauses, nr_solutions, oracle, index  = make_cnf("Data/2sat_3var_1sol.cnf")
    start = time.time()
    if sys.argv[1] == '0':
        grover_search_cnf(n, clauses, nr_solutions, oracle, index)
    if sys.argv[1] == '1':
        grover_search_fpaa(n, clauses, nr_solutions, oracle, index)
    print("time: ", round(time.time()-start,3))

if __name__ == "__main__":
    main()