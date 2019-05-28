from qiskit import ClassicalRegister, QuantumRegister, QuantumCircuit
from qiskit import IBMQ, execute, Aer
import qiskit as qk
import numpy as np
import time
import math
import sys
np.set_printoptions(threshold=np.inf)

from fpaa_oracle import fpaa_oracle
from cnf_oracle import cnf_oracle
from basic_oracle import basic_oracle
from mean_inversion import mean_inversion

# IBMQ.load_accounts()
# IBMQ.backends()

def main():
	start_time = time.time()
	n, clauses, _shots, oracle, index, oracle_option, iterations = get_input()
	if oracle_option == 0:
		a = 0
	if oracle_option == 1:
		a = math.floor(math.log(clauses,2)+1)
	if oracle_option == 2:
		a = 1
		theta = math.pi/clauses
		delta = pow(2,-0.5*pow(n,2))/4
		_lambda = pow(math.sin(theta),2)/4+pow(1/2-math.cos(theta)/2,2)
		L = int(math.ceil(2*math.log(2/delta)/math.sqrt(_lambda)))
		print("fpaa iterations:", L-1)

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
	if oracle_option != 2:
		qc.x(q[n])
		qc.h(q[n])

	for i in range(iterations):
		if oracle_option == 0:
			basic_oracle(qc, q, n, oracle)
		if oracle_option == 1:
			cnf_oracle(qc, q, n, clauses, oracle, index)
		if oracle_option == 2:
			fpaa_oracle(qc, q, n, clauses, oracle, index)
		qc.barrier()
		mean_inversion(qc, q, n, oracle_option)

		# for i in range(n,n+a):
		# 	qc.measure(q[i], c[0])
		# 	qc.x(q[i]).c_if(c,1)

	qc.barrier()
	for i in range(math.floor(n/2)):
		qc.swap(q[i],q[n-i-1])
	qc.barrier()

	# backend = qk.BasicAer.get_backend('unitary_simulator')
	# job = execute(qc, backend=backend, shots=1024, max_credits=3)
	# print(np.around(job.result().get_unitary().real,2))

	for i in range(n):
		qc.measure(q[i], c[i])

	print("Time taken for setup:",np.round(time.time() - start_time), "seconds")
	backend = qk.BasicAer.get_backend('qasm_simulator')
	# backend = qk.BasicAer.get_backend('statevector_simulator')
	job = execute(qc, backend=backend, shots=_shots, max_credits=3)
	print(job.result().get_counts())
	print("Time taken for result:",np.round(time.time() - start_time,3), "seconds")
	# Draw the circuit
	# print(qc)

## Helper function to get variables
def get_input():
	if len(sys.argv) == 4:
		_shots = int(sys.argv[2])
		## Input is oracle
		if sys.argv[1].find(".") == -1:
			n, oracle = set_oracle()
			oracle_option = 0
			clauses = 1
			index = -1
			k = 1
		## Input is cnf file
		else:
			n, clauses, k, oracle, index = set_cnf()
			oracle_option = int(sys.argv[3])
			if oracle_option != 1 and oracle_option != 2:
				error_msg("argument mismatch")
				sys.exit()
	## Incorrect input
	else:
		error_msg("argument mismatch")
		sys.exit()

	if not isinstance(k,int):
		k = 1
	if pow(2, n)/k < 4:
		error_msg("inefficient")
		exit()
	iterations = math.floor((math.pi*math.sqrt(pow(2, n)/k))/4)
	print("Amount of iterations:", iterations)
	print("Running grover's search...")
	print("")
	return n, clauses, _shots, oracle, index, oracle_option, iterations


## Helper function to set cnf variables
def set_cnf():
	file = sys.argv[1]
	## Get variables from cnf file
	with open(file, 'r') as f:
		answers = f.readline()
		n, clauses, k = [int(x) for x in next(f).split()]
		oracle = [[int(x) for x in line.split()] for line in f]
	print_cnf(oracle, answers, clauses)
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
	return n, clauses, k, oracle, index

## Helper function to set oracle variables
def set_oracle():
	oracle = int(sys.argv[1])
	n = math.floor(math.log(oracle)/math.log(2))+1
	index = range(n)
	if oracle > pow(2, n):
		print("Oracle outside qubit range")
		sys.exit()
	oracle = [int(x) for x in np.binary_repr(oracle, width=n)]
	print("oracle:")
	print(oracle)
	print("")
	return n, oracle

def print_cnf(cnf, answers, clauses):
	print("cnf:")
	for i in range(clauses):
		if cnf[i][0] < 0:
			print("(",cnf[i][0], end="")
		else:
			print("( ",cnf[i][0], end="")			
		for j in range(1,len(cnf[i])):
			if cnf[i][j] < 0:
				print(" V",cnf[i][j], end="")
			else:
				print(" V ",cnf[i][j], end="")				
		if i == clauses-1:
			print(")")
		else:
			print(") ^ ")
	print("")
	print(answers)
	print("")

def error_msg(text):
	if text == "argument mismatch":
		print("Argument mismatch!")
		print("There are 2 options:")
		print("1) Give the number of qubits, the amount of shots and an oracle")
		print("2) Give a cnf-file, the amount of shots and if you want to use fpaa")
		print("( 0 = basic oraclel; 1 = cnf oracle; 2 = fpaa oracle )")
	if text == "inefficient":
		print("this does not work with grover.")
		print("total/solutions need to be larger than 4.")
		print("brute force will solve it efficiently.")

###########
## START ##
###########
main() 