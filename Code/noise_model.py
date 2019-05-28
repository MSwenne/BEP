from qiskit import Aer, IBMQ, execute
from qiskit.providers.aer import noise
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.tools.monitor import job_monitor
import matplotlib.pyplot as plt
from scipy import stats
from plot import plot_hist
import numpy as np
import math

IBMQ.load_accounts()
IBMQ.backends()

# device = IBMQ.get_backend('ibmq_16_melbourne')
# device = IBMQ.get_backend('ibmq_5_yorktown')
device = IBMQ.get_backend('ibmq_5_tenerife')
properties = device.properties()
coupling_map = device.configuration().coupling_map

# Construct quantum circuit
q = QuantumRegister(5, 'q')
c = ClassicalRegister(5, 'c')
qc = QuantumCircuit(q,c)

# qc.x(q[1])
# qc.x(q[0])
qc.h(q[0])

qc.x(q[2])
qc.x(q[3])
qc.x(q[2])
qc.x(q[3])
qc.x(q[2])
qc.x(q[3])
qc.x(q[2])
qc.x(q[3])

qc.h(q[0])

qc.measure(q[0], c[0])
qc.measure(q[1], c[1])
qc.measure(q[2], c[2])
qc.measure(q[3], c[3])
qc.measure(q[4], c[4])

# Select the QasmSimulator from the Aer provider
simulator = Aer.get_backend('qasm_simulator')

# Execute and get counts
result = execute(qc, simulator).result()
counts = result.get_counts(qc)
print(counts)
# plot_hist(counts, 'no noise simulation')

# List of gate times for ibmq_14_melbourne device
# Note that the None parameter for u1, u2, u3 is because gate
# times are the same for all qubits
for i in range(25):
	for qubit, qubit_props in enumerate(properties.qubits):
		for item in qubit_props:
			if item.name == 'T1':
				item.value = 500
			if item.name == 'T2':
				item.value = 50.0-(2*i)
	# 		if item.name == 'frequency':
	# 			item.value = 25.0/(i+1)
	for gate in properties.gates:
		for item in gate.parameters:
			if item.name == 'gate_error':
				item.value = 0.1

	gate_times = [
		('u1', None, 0), ('u2', None, 100), ('u3', None, 200), ('cx', None, 500)
	]
	# Construct the noise model from backend properties
	# and custom gate times
	noise_model = noise.device.basic_device_noise_model(properties,readout_error=False,thermal_relaxation=True, gate_times=gate_times)
	# Get the basis gates for the noise model
	basis_gates = noise_model.basis_gates
	# Select the QasmSimulator from the Aer provider
	simulator = Aer.get_backend('qasm_simulator')

	# Execute noisy simulation and get counts
	result_noise = execute(qc, simulator,noise_model=noise_model,basis_gates=basis_gates).result()
	counts_noise = result_noise.get_counts(qc)
	num = 0
	if bin(num)[2:].zfill(5) in counts_noise:
		print("{\'00000\':",counts_noise[str(bin(num)[2:].zfill(5))],"}")
	else:
		print("error")