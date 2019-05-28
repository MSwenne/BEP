from qiskit import Aer, IBMQ, execute
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
import matplotlib.pyplot as plt
import numpy as np

# Construct quantum circuit
q = QuantumRegister(3)
c = ClassicalRegister(3)
qc = QuantumCircuit(q,c)

ctemp = ClassicalRegister(1)
qc.add_register(ctemp)

qc.x(q[0])

qc.measure(q[0], ctemp[0])
qc.x(q[1]).c_if(ctemp, 1)

qc.measure(q[0], c[0])
qc.x(q[2]).c_if(c, 1)

qc.measure(q[0], c[0])
qc.measure(q[1], c[1])
qc.measure(q[2], c[2])


# Select the QasmSimulator from the Aer provider
simulator = Aer.get_backend('qasm_simulator')

# Execute and get counts
result = execute(qc, simulator).result()
counts = result.get_counts(qc)
print(counts)