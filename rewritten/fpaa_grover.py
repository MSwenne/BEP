from math import pi, floor, sqrt, log
import numpy as np
import cirq
import time

from utilities.utils import check_conditions
from utilities.fpaa_utils import build_init, build_oracle, build_mean_inversion

# Run grover's search using fixed-point amplitude-amplification
def grover_search_fpaa(n, clauses, nr_solutions, oracle, index, shots=100, apply_noise=False):
    check_conditions(n, nr_solutions)
    iterations = floor((pi*sqrt(pow(2, n)/nr_solutions))/4)

    print(f'n: {n}\nclauses: {clauses}\nnr_solutions: {nr_solutions}\nIterations: {iterations}\n')

    ## circuit generation
    c = cirq.Circuit()
    c.append(build_init(n))
    for i in range(iterations):
        c.append(build_oracle(n, clauses, oracle, index))
        c.append(build_mean_inversion(n))
        # for i in range(n,n+a):
        #     c.append(cirq.measure(q[i], c[0]))
        #     c.append(cirq.X(q[i]).c_if(c,1))
    c.append(cirq.measure(*[cirq.LineQubit(i) for i in range(n)], key='m'))
    # c.append(cirq.measure(*c.all_qubits(), key='m'))

    # Apply noise if True
    if apply_noise:
        noise = cirq.ConstantQubitNoiseModel(cirq.depolarize(0.001))
        noisy_circuit = cirq.Circuit()
        for moment in c:
            noisy_circuit.append(noise.noisy_moment(moment, sorted(c.all_qubits())))

    simulator = cirq.Simulator()
    results = simulator.run(c, repetitions=shots)
    frequencies = results.histogram(key='m')
    probs = {}
    for key, value in frequencies.items():
        probs[format(key, f'0{n}b')] = value
    print(f'Frequencies: {probs}')

    # Draw the circuit
    # print(f'Circuit:\n{c.to_text_diagram(transpose=True)}')