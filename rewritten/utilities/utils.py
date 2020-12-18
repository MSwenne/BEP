import numpy as np
import cirq

from utilities.mcx import mcx
from utilities.mcu1 import mcu1

def incrementer(index):
    for i in range(1,len(index)-1):
        yield mcx(index[:-i], index[len(index)-i])
    if len(index) > 1:
        yield cirq.CNOT(cirq.LineQubit(index[0]),cirq.LineQubit(index[1]))
    yield cirq.X(cirq.LineQubit(index[0]))

def decrementer(index):
    yield cirq.X(cirq.LineQubit(index[0]))
    if len(index) > 1:
        yield cirq.CNOT(cirq.LineQubit(index[0]),cirq.LineQubit(index[1]))
    for i in range(2,len(index)):
        yield mcx(index[:i], index[i])

def c_incrementer(index, controls):
    for i in range(len(controls)):
        coerced = np.concatenate([index, controls[:len(controls)-i-1]])
        coerced = [int(i) for i in coerced]
        yield mcx(coerced, int(controls[len(controls)-i-1]))

def c_decrementer(index, controls):
    for i in range(len(controls)):
        coerced = np.concatenate([index, controls[:-len(controls)+i]])
        coerced = [int(i) for i in coerced]
        yield mcx(coerced, int(controls[i]))

def check_conditions(n, nr_solutions):
    if pow(2, n)/nr_solutions < 4:
        print("this does not work with grover.")
        print("total/solutions need to be larger than 4.")
        print("brute force will solve it efficiently.")
        exit(-1)
    ## Too much qubits needed for operation (max qubits for simulator is 24)
    # if (n+1) + a > 24:
    #     print("Too much qubits needed! (", (n+1) + a,")")
    #     print("Max qubits 24")
    #     exit(-1)