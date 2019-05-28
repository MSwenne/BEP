from mcx_gate import mcx

def mean_inversion(qc, q, n, oracle_option):
	if oracle_option == 2:
		qc.x(q[n+1])
		qc.h(q[n+1])
	## Hadamard gate
	for i in range(0, n):
		qc.h(q[i])
	## Pauli X gate
	for i in range(n):
		qc.x(q[i])
	if oracle_option == 2:
		mcx(qc, q, range(n), n+1)
	else:
		mcx(qc, q, range(n), n)
	## Pauli X gate
	for i in range(n):
		qc.x(q[i])
	## Hadamard gate
	for i in range(n):
		qc.h(q[i])
	if oracle_option == 2:
		qc.h(q[n+1])
		qc.x(q[n+1])