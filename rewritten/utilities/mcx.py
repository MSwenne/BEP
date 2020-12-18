
import cirq

def mcx(index, tgt):
    q  = [cirq.LineQubit(i) for i in index]
    if len(index) == 0:
        yield cirq.X(cirq.LineQubit(tgt))
    else:
        yield cirq.X(cirq.LineQubit(tgt)).controlled_by(*q)