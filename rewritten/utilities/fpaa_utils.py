from math import pi, floor, ceil, log, cos, sin,sqrt
from mpmath import acos, acot, tan
from mpmath import sqrt as mpsqrt
from mpmath import cos as mpcos
import numpy as np
import cirq

from utilities.mcx import mcx
from utilities.utils import mcu1

def build_init(n):
    for i in range(n):
        yield cirq.H(cirq.LineQubit(i))

def build_mean_inversion(n):
    yield cirq.X(cirq.LineQubit(n+1))
    yield cirq.H(cirq.LineQubit(n+1))
    ## Hadamard gate
    for i in range(n):
        yield cirq.H(cirq.LineQubit(i))
    ## Pauli X gate
    for i in range(n):
        yield cirq.X(cirq.LineQubit(i))
    yield mcx(range(n), n+1)
    ## Pauli X gate
    for i in range(n):
        yield cirq.X(cirq.LineQubit(i))
    ## Hadamard gate
    for i in range(n):
        yield cirq.H(cirq.LineQubit(i))
    yield cirq.H(cirq.LineQubit(n+1))
    yield cirq.X(cirq.LineQubit(n+1))

def build_oracle(n, clauses, oracle, index):
    theta = pi/clauses
    delta = pow(2,-0.5*pow(n,2))/2
    _lambda = pow(sin(theta),2)/4+pow(1/2-cos(theta)/2,2)
    L = int(ceil(2*log(2/delta)/sqrt(_lambda)))
    gamma = mpcos(acos(1/delta)/L)
    # print(f'theta: {theta}\ndelta: {delta}\n_lambda: {_lambda}\nL: {L}\ngamma: {gamma}\n')
    
    yield cirq.H(cirq.LineQubit(n))
    yield A_matrix(n, clauses, oracle, theta)
    for k in range(1,L):
        alpha = abs(2*acot(tan(2*pi*(  k    )/L)*mpsqrt(1-1/pow(gamma,-2))))
        beta = -abs(2*acot(tan(2*pi*(L-(k-1))/L)*mpsqrt(1-1/pow(gamma,-2))))
        yield cirq.H(cirq.LineQubit(n))
        yield U_matrix(n, beta)
        yield cirq.H(cirq.LineQubit(n))
        yield A_matrix(n, clauses, oracle, -theta)
        yield cirq.H(cirq.LineQubit(n))
        yield U_matrix(n, alpha)
        yield cirq.H(cirq.LineQubit(n))
        yield A_matrix(n, clauses, oracle, theta)
    yield cirq.H(cirq.LineQubit(n))
    
    yield cirq.X(cirq.LineQubit(n))
    yield cirq.X(cirq.LineQubit(n+1))
    yield cirq.H(cirq.LineQubit(n+1))
    yield cirq.CNOT(cirq.LineQubit(n),cirq.LineQubit(n+1))
    yield cirq.H(cirq.LineQubit(n+1))
    yield cirq.X(cirq.LineQubit(n+1))
    yield cirq.X(cirq.LineQubit(n))

def U_matrix(n, angle):
    yield cirq.CNOT(cirq.LineQubit(n), cirq.LineQubit(n+1))
    yield cirq.ZPowGate(exponent=float(angle)/pi)(cirq.LineQubit(n+1))
    yield cirq.CNOT(cirq.LineQubit(n), cirq.LineQubit(n+1))
    
def A_matrix(n, clauses, oracle, theta):
    for j in range(clauses):
        for i in range(n):
            if not abs(oracle[j][i]):
                yield cirq.X(cirq.LineQubit(i))
        yield mcu1(range(n), n, float(theta)/pi)
        for i in range(n):
            if not abs(oracle[j][i]):
                yield cirq.X(cirq.LineQubit(i))