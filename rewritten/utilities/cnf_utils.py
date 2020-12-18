from math import floor, log
import numpy as np
import cirq

from utilities.mcx import mcx
from utilities.utils import c_incrementer, c_decrementer

def build_init(n):
    for i in range(n):
        yield cirq.H(cirq.LineQubit(i))
    yield cirq.X(cirq.LineQubit(n))
    yield cirq.H(cirq.LineQubit(n))

def build_mean_inversion(n):
    ## Hadamard gate
    for i in range(0, n):
        yield cirq.H(cirq.LineQubit(i))
    ## Pauli X gate
    for i in range(n):
        yield cirq.X(cirq.LineQubit(i))
    yield mcx(range(n), n)
    ## Pauli X gate
    for i in range(n):
        yield cirq.X(cirq.LineQubit(i))
    ## Hadamard gate
    for i in range(n):
        yield cirq.H(cirq.LineQubit(i))

def build_oracle(n, a, oracle, index):
    b = floor(log(a,2))+1
    temp = [int(x) for x in np.binary_repr(a, width=b)]
    incr = []
    for i in range(b):
        incr.append(n+i+1)
    for j in range(a):
        for i in range(n):
            if not abs(oracle[j][i]):
                yield cirq.X(cirq.LineQubit(i))
        yield c_incrementer(index[j],n+1+np.array(range(b)))
        for i in range(n):
            if not abs(oracle[j][i]):
                yield cirq.X(cirq.LineQubit(i))
    for i in range(b):
        yield cirq.X(cirq.LineQubit(n+1+i))
    yield mcx(incr, n)
    for i in range(b):
        yield cirq.X(cirq.LineQubit(n+1+i))
    for j in range(a-1, -1, -1):
        for i in range(n):
            if not abs(oracle[j][i]):
                yield cirq.X(cirq.LineQubit(i))
        yield c_decrementer(index[j],n+1+np.array(range(b)))
        for i in range(n):
            if not abs(oracle[j][i]):
                yield cirq.X(cirq.LineQubit(i))