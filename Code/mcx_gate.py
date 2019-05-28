import numpy as np
import math

def mcx(qc, q, index, tgt):
	if len(index) == 0:
		qc.x(q[tgt])
	elif len(index) == 1:
		qc.cx(q[index[0]], q[tgt])
	elif len(index) == 2:
		qc.ccx(q[index[0]], q[index[1]], q[tgt])
	elif len(index) == 3:
		qc.c3x(q[index[0]], q[index[1]], q[index[2]], q[tgt])	
	elif len(index) == 4:
		qc.c4x(q[index[0]], q[index[1]], q[index[2]], q[index[3]], q[tgt])	
	elif len(index) == 5:
		qc.c5x(q[index[0]], q[index[1]], q[index[2]], q[index[3]], q[index[4]], q[tgt])	
	else:
		qc.barrier()
		qc.h(q[tgt])
		mcx(qc,q,index[:-1], tgt)
		qc.tdg(q[tgt])
		qc.cx(q[index[len(index)-1]], q[tgt])
		qc.t(q[tgt])
		mcx(qc,q,index[:-1], tgt)
		qc.tdg(q[tgt])
		qc.cx(q[index[len(index)-1]], q[tgt])
		qc.t(q[tgt])
		qc.h(q[tgt])
		qc.barrier()
		incrementer(qc, q, index)
		qc.barrier()
		j = 0
		for i in reversed(index[1:]):
			qc.u1(-math.pi/(pow(2, j+2)), q[i])
			j = j + 1
		qc.barrier()
		decrementer(qc, q, index)
		qc.barrier()
		j = 0
		for i in reversed(index[1:]):
			qc.u1(math.pi/(pow(2, j+2)), q[i])
			j = j + 1
		qc.u1(math.pi/(pow(2, len(index))), q[index[0]])
		qc.barrier()


def incrementer(qc, q, index):
	while len(index) > 2:
		mcx(qc, q, index[:-1], index[len(index)-1])
		index = index[:-1]
	if len(index) > 1:
		qc.cx(q[int(index[0])],q[int(index[1])])
	qc.x(q[int(index[0])])

def decrementer(qc, q, index):
	qc.x(q[int(index[0])])
	if len(index) > 1:
		qc.cx(q[int(index[0])],q[int(index[1])])
	i = 2
	while i < len(index):
		mcx(qc, q, index[:i], index[i])
		i = i + 1

def c_incrementer(qc, q, index, controls):
	for i in range(len(controls)):
		coerced = np.concatenate([index, controls[:len(controls)-i-1]])
		coerced = [int(i) for i in coerced]
		mcx(qc, q, coerced, int(controls[len(controls)-i-1]))

def c_decrementer(qc, q, index, controls):
	for i in range(len(controls)):
		coerced = np.concatenate([index, controls[:-len(controls)+i]])
		coerced = [int(i) for i in coerced]
		mcx(qc, q, coerced, int(controls[i]))