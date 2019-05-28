from qiskit import ClassicalRegister, QuantumRegister, QuantumCircuit
from qiskit import IBMQ, execute, Aer
from qiskit.providers.aer import noise
import matplotlib as mpl
import matplotlib.pyplot as plt
from plot import plot_hist
from scipy import stats
import qiskit as qk
import numpy as np
import time
import math
import sys
import os
from cnf_oracle import cnf_oracle
from mean_inversion import mean_inversion

shots = 3

IBMQ.load_accounts()
IBMQ.backends()

def main():
	n, clauses, oracle, index, iterations, runs, solutions = get_input()
	
	values = [5001 - (5000/runs)*(i+1) for i in range(runs)]
	
	a = math.floor(math.log(clauses,2)+1)
	data_noise = [[0 for y in range(runs)] for x in range(pow(2, n))] 
	printProgressBar(0, runs, prefix = 'Progress:', suffix = 'Complete', length = 50)
	for i in range(runs):
		data = Grover_Search(n, clauses, oracle, index, iterations, values[i], shots)
		for j in range(pow(2, n )):
			if bin(j)[2:].zfill(n + 1 + a) in data:
				data_noise[j][i] += data[str(bin(j)[2:].zfill(n + 1 + a))]/shots
		printProgressBar(i+1, runs, prefix = 'Progress:', suffix = 'Complete', length = 50)

	nr = 0
	while(os.path.exists('./Data/Images/noise_incrementer({}vars,{}clauses,{}runs)({}).png'.format(n,clauses,runs,nr))):
		nr = nr + 1
		print()
	f=open("Data/noise_incrementer({}vars,{}clauses,{}runs)({}).txt".format(n,clauses,runs,nr), "a+")
	f.write("Grover with incrementer:\n\t".expandtabs(2))
	f.write("nr. of variables: {}\r\n\t".format(n).expandtabs(2))
	f.write("nr. of clauses: {}\r\n\t".format(clauses).expandtabs(2))
	f.write("solutions: {}\r\n\t".format(solutions).expandtabs(2))
	f.write("amount of runs: {}\r\n".format(runs).expandtabs(2))
	f.write("({})\r\n".format(nr).expandtabs(2))
	f.write("#########\r\n")
	print()
	print('solution(s)', solutions)
	f.write("\tdata with noise\n".expandtabs(2))
	for i in range(pow(2, n)):
		if bin(i)[2:].zfill(n) in solutions:
			print(bin(i)[2:].zfill(n),":",data_noise[i])
			f.write("\t\t{}: {}\n".format(bin(i)[2:].zfill(n),data_noise[i]).expandtabs(2))
	f.write("#########\r\n\n")
	fig = plt.figure(figsize=(15,10))
	ax = plt.gca()
	ax.set_xscale("log")
	# ax.set_xticks(values)
	locmaj = mpl.ticker.LogLocator(base=10,numticks=6) 
	ax.xaxis.set_major_locator(locmaj)
	ax.set_ylim([0,100])
	for i in range(pow(2, n)):
		if bin(i)[2:].zfill(n) in solutions:
			plt.plot(values, data_noise[i], 'g-')
				# Draw boxplots, specifying desired style
			# plt.boxplot(data_noise[i])
			plt.plot(values, data_noise[i], 'go', markersize=2)
	plt.xlabel("100% noise chance after # microseconds")
	plt.ylabel("% correct results")
	plt.title("Grover incrementer with noise")
	fig.savefig('Data/Images/noise_incrementer({}vars,{}clauses,{}runs)({}).png'.format(n,clauses,runs,nr))
	plt.show()



def Grover_Search(n, clauses, oracle, index, iterations, value, shots):
	a = math.floor(math.log(clauses,2)+1)

	## Too much qubits needed for operation (max qubits for simulator is 24)
	if (n+1) + a > 24:
		print("Too much qubits needed! (", (n+1) + a,")")
		print("Max qubits 24")
		sys.exit()

	## circuit generation
	q = QuantumRegister( n +1 + a )
	c = ClassicalRegister( n + 1 + a )
	qc = QuantumCircuit(q, c)

	for i in range(math.floor(n/2)):
		qc.swap(q[i],q[n-i-1])
	qc.barrier()
	for i in range(n):
		qc.h(q[i])
	qc.x(q[n])
	qc.h(q[n])

	for i in range(iterations):
		cnf_oracle(qc, q, n, clauses, oracle, index)
		qc.barrier()
		mean_inversion(qc, q, n, 1)

		# for i in range(n,n+a):
		# 	qc.measure(q[i], c[0])
		# 	qc.x(q[i]).c_if(c,1)

	qc.barrier()
	for i in range(math.floor(n/2)):
		qc.swap(q[i],q[n-i-1])
	qc.barrier()

	for i in range(n):
		qc.measure(q[i], c[i])

	backend = Aer.get_backend('qasm_simulator')

	# Execute noisy simulation and get counts
	# device = IBMQ.get_backend('ibmq_16_melbourne')
	# device = IBMQ.get_backend('ibmq_5_yorktown')
	device = IBMQ.get_backend('ibmq_5_tenerife')
	properties = device.properties()
	coupling_map = device.configuration().coupling_map

	for _, qubit_props in enumerate(properties.qubits):
		for item in qubit_props:
			if item.name == 'T1':
				item.value = value
			if item.name == 'T2':
				item.value = value
	for gate in properties.gates:
		for item in gate.parameters:
			if item.name == 'gate_error':
				item.value = 0.00000001
	gate_times = [
		('u1', None, 0), ('u2', None, 100), ('u3', None, 200), ('cx', None, 0)
	]
	# Construct the noise model from backend properties
	# and custom gate times
	noise_model = noise.device.basic_device_noise_model(properties,readout_error=False, thermal_relaxation=True, gate_times=gate_times)

	# Get the basis gates for the noise model
	basis_gates = noise_model.basis_gates

	result = execute(qc, backend=backend, shots=100*shots, noise_model=noise_model, basis_gates=basis_gates).result()
	# coupling_map=coupling_map,
	counts = result.get_counts(qc)
	return counts


## Helper function to get variables
def get_input():
	if len(sys.argv) == 3:
		n, clauses, k, oracle, index, answer = set_cnf()
	## Incorrect input
	else:
		sys.exit()

	if not isinstance(k,int):
		k = 1
	if pow(2, n)/k < 4:
		exit()
	iterations = math.floor((math.pi*math.sqrt(pow(2, n)/k))/4)
	runs = int(sys.argv[2])
	answer = answer[22:-1]
	solutions = answer.split(",")
	return n, clauses, oracle, index, iterations, runs, solutions


## Helper function to set cnf variables
def set_cnf():
	file = sys.argv[1]
	## Get variables from cnf file
	with open(file, 'r') as f:
		answer = f.readline()
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
	return n, clauses, k, oracle, index, answer

# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
	"""
	Call in a loop to create terminal progress bar
	@params:
		iteration   - Required  : current iteration (Int)
		total	   - Required  : total iterations (Int)
		prefix	  - Optional  : prefix string (Str)
		suffix	  - Optional  : suffix string (Str)
		decimals	- Optional  : positive number of decimals in percent complete (Int)
		length	  - Optional  : character length of bar (Int)
		fill		- Optional  : bar fill character (Str)
	"""
	percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
	filledLength = int(length * iteration // total)
	bar = fill * filledLength + '-' * (length - filledLength)
	print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
	# Print New Line on Complete
	if iteration == total: 
		print()

###########
## START ##
###########
main() 