from mcx_gate import incrementer, decrementer
import numpy as np

def mcu1(qc, q, index, tgt, theta):
		if len(index) == 0:
			qc.u1(theta, q[tgt])
		elif len(index) == 1:
			qc.cu1(theta, q[index[0]], q[tgt])
		elif len(index) == 2:
			qc.ccu1(theta, q[index[0]], q[index[1]], q[tgt])
		elif len(index) == 3:
			qc.c3u1(theta, q[index[0]], q[index[1]], q[index[2]], q[tgt])	
		elif len(index) == 4:
			qc.c4u1(theta, q[index[0]], q[index[1]], q[index[2]], q[index[3]], q[tgt])	
		elif len(index) == 5:
			qc.c5u1(theta, q[index[0]], q[index[1]], q[index[2]], q[index[3]], q[index[4]], q[tgt])	
		else:
			qc.barrier()
			incrementer(qc, q, index)
			qc.barrier()
			j = 0
			for i in reversed(index[1:]):
				qc.u1(-theta/(pow(2, j+2)), q[i])
				j = j + 1
			qc.barrier()
			decrementer(qc, q, index)
			qc.barrier()
			j = 0
			for i in reversed(index[1:]):
				qc.u1(theta/(pow(2, j+2)), q[i])
				j = j + 1
			qc.u1(theta/(pow(2, len(index))), q[index[0]])