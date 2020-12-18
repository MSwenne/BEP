
from math import pi, floor, ceil, log, cos, sin,sqrt
from mpmath import acos, acot, tan
from mpmath import sqrt as mpsqrt
from mpmath import cos as mpcos
import numpy as np
import cirq

from utilities.fpaa_utils import A_matrix, U_matrix
from utilities.mcx import mcx
from utilities.utils import mcu1

n = 1
clauses = 1
oracle = [[1]]
theta = pi/clauses
delta = pow(2,-0.5*pow(n,2))/2
_lambda = pow(sin(theta),2)/4+pow(1/2-cos(theta)/2,2)
L = int(ceil(2*log(2/delta)/sqrt(_lambda)))
gamma = mpcos(acos(1/delta)/L)
print(f'theta: {theta}\ndelta: {delta}\n_lambda: {_lambda}\nL: {L}\ngamma: {gamma}\n')
c = cirq.Circuit()

c.append( cirq.H(cirq.LineQubit(n)))
c.append( A_matrix(n, clauses, oracle, theta))
for k in range(1,L):
    alpha = abs(2*acot(tan(2*pi*(  k    )/L)*mpsqrt(1-1/pow(gamma,-2))))
    beta = -abs(2*acot(tan(2*pi*(L-(k-1))/L)*mpsqrt(1-1/pow(gamma,-2))))
    c.append(cirq.H(cirq.LineQubit(n)))
    c.append( U_matrix(n, beta))
    c.append( cirq.H(cirq.LineQubit(n)))
    c.append( A_matrix(n, clauses, oracle, -theta))
    c.append( cirq.H(cirq.LineQubit(n)))
    c.append( U_matrix(n, alpha))
    c.append( cirq.H(cirq.LineQubit(n)))
    c.append( A_matrix(n, clauses, oracle, theta))
c.append( cirq.H(cirq.LineQubit(n)))

c.append( cirq.X(cirq.LineQubit(n)))
c.append( cirq.X(cirq.LineQubit(n+1)))
c.append( cirq.H(cirq.LineQubit(n+1)))
c.append( cirq.CNOT(cirq.LineQubit(n),cirq.LineQubit(n+1)))
c.append( cirq.H(cirq.LineQubit(n+1)))
c.append( cirq.X(cirq.LineQubit(n+1)))
c.append( cirq.X(cirq.LineQubit(n)))

c.append(cirq.measure(*[cirq.LineQubit(i) for i in range(n+2)], key='m'))

simulator = cirq.Simulator()
results = simulator.run(c, repetitions=100)
frequencies = results.histogram(key='m')
probs = {}
for key, value in frequencies.items():
    probs[format(key, f'0{n+2}b')] = value
print(f'Frequencies: {probs}')
# print(f'Circuit:\n{c.to_text_diagram(transpose=True)}')