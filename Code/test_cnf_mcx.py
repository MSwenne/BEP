import math

def mcx(qc, q, a, b, c):
	mcx_r(qc, q, a, b, c)

def mcx_r(qc, q, a, b, c):
	qc.barrier()
	qc.h(q[c])
	if a+1 == b:
		qc.cx(q[a], q[c])
	else:
		mcx_r(qc,q,a,b-1,c)
	qc.tdg(q[c])
	qc.cx(q[b], q[c])
	qc.t(q[c])
	if a+1 == b:
		qc.cx(q[a], q[c])
	else:
		mcx_r(qc,q,a,b-1,c)
	qc.tdg(q[c])
	qc.cx(q[b], q[c])
	qc.t(q[c])
	qc.h(q[c])
	qc.barrier()
	incrementer(qc,q,a,b)
	qc.barrier()
	for i in range(b, a, -1):
		qc.u1(-math.pi/(pow(2, b-i+2)), q[i])
	qc.barrier()
	decrementer(qc,q,a,b)
	qc.barrier()
	for i in range(b, a, -1):
		qc.u1(math.pi/(pow(2, b-i+2)), q[i])
	qc.u1(math.pi/(pow(2, b+1)), q[a])
	qc.barrier()

def incrementer(qc, q, a, b):
	for i in range(b, a, -1):
		if a+1 == i:
			qc.cx(q[a],q[i])
		else:
			mcx(qc, q, a, i-1, i)
	qc.x(q[a])

def decrementer(qc, q, a, b):
	qc.x(q[a])
	for i in range(a+1, b+1):
		if a+1 == i:
			qc.cx(q[a],q[i])
		else:
			mcx(qc, q, a, i-1, i)
