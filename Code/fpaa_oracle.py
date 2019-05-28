import mpmath
import math
import numpy as np
from mcu1 import mcu1

def fpaa_oracle(qc, q, n, clauses, oracle, index):
	theta = math.pi/clauses
	delta = pow(2,-0.5*pow(n,2))/2
	_lambda = pow(math.sin(theta),2)/4+pow(1/2-math.cos(theta)/2,2)
	L = int(math.ceil(2*math.log(2/delta)/math.sqrt(_lambda)))
	gamma = mpmath.cos(mpmath.acos(1/delta)/L)

	qc.barrier()
	A_matrix(qc, q, n, clauses, oracle, theta)
	qc.barrier()

	for k in range(1,L):
		alpha = abs(2*mpmath.acot(mpmath.tan(2*math.pi*(   k   )/L)*mpmath.sqrt(1-1/pow(gamma,-2))))
		beta = -abs(2*mpmath.acot(mpmath.tan(2*math.pi*(L-(k-1))/L)*mpmath.sqrt(1-1/pow(gamma,-2))))

		qc.h(q[n])
		U_matrix(qc, q, n, beta)
		qc.h(q[n])

		Adgr_matrix(qc, q, n, clauses, oracle, theta)

		U_matrix(qc, q, n, alpha)

		A_matrix(qc, q, n, clauses, oracle, theta)
		qc.barrier()
	qc.h(q[n])
	qc.barrier()

	qc.x(q[n])
	qc.x(q[n+1])
	qc.h(q[n+1])
	qc.cx(q[n],q[n+1])
	qc.h(q[n+1])
	qc.x(q[n+1])
	qc.x(q[n])


def U_matrix(qc, q, n, angle):
	qc.cx(q[n], q[n+1])
	qc.u1(float(angle), q[n+1])
	qc.cx(q[n], q[n+1])


def A_matrix(qc, q, n, clauses, oracle, theta):
	qc.h(q[n])
	for j in range(clauses):
		qc.barrier()
		for i in range(n):
			if not abs(oracle[j][i]):
				qc.x(q[i])
		mcu1(qc, q, range(n), n, theta)
		for i in range(n):
			if not abs(oracle[j][i]):
				qc.x(q[i])


def Adgr_matrix(qc, q, n, clauses, oracle, theta):
	for j in range(clauses):
		qc.barrier()
		for i in range(n):
			if not abs(oracle[j][i]):
				qc.x(q[i])
		mcu1(qc, q, range(n), n, -theta)
		for i in range(n):
			if not abs(oracle[j][i]):
				qc.x(q[i])
	qc.barrier()
	qc.h(q[n])
