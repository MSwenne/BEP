from mcx_gate import mcx

def basic_oracle(qc, q, n, oracle):
	qc.barrier(q)
	for i in range(n):
		if not oracle[i]:
			qc.x(q[i])	
	qc.barrier(q)
	mcx(qc, q, range(n), n)
	qc.barrier(q)
	for i in range(n):
		if not oracle[i]:
			qc.x(q[i])
