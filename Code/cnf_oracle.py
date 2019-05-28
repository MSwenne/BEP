from mcx_gate import mcx, c_incrementer, c_decrementer
import numpy as np
import math

def cnf_oracle(qc, q, n, a, oracle, index):
	b = math.floor(math.log(a,2))+1
	temp = [int(x) for x in np.binary_repr(a, width=b)]
	incr = []
	for i in range(b):
		if temp[i]:
			incr.append(n+i+1)
	for j in range(a):
		qc.barrier()
		for i in range(n):
			if not abs(oracle[j][i]):
				qc.x(q[i])
		c_incrementer(qc, q, index[j],n+1+np.array(range(b)))
		for i in range(n):
			if not abs(oracle[j][i]):
				qc.x(q[i])
	qc.barrier()
	for i in range(b):
		qc.x(q[n+1+i])
	mcx(qc, q, incr, n)
	for i in range(b):
		qc.x(q[n+1+i])
	for j in range(a-1, -1, -1):
		qc.barrier()
		for i in range(n):
			if not abs(oracle[j][i]):
				qc.x(q[i])
		c_decrementer(qc, q, index[j],n+1+np.array(range(b)))
		for i in range(n):
			if not abs(oracle[j][i]):
				qc.x(q[i])