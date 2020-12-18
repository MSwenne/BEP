
import cirq

def mcu1(index, tgt, theta):
    q  = [cirq.LineQubit(i) for i in index]
    if len(index) == 0:
        yield cirq.ZPowGate(exponent=theta)(cirq.LineQubit(tgt))
    else:
        yield cirq.ZPowGate(exponent=theta)(cirq.LineQubit(tgt)).controlled_by(*q)