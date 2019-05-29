# -*- coding: utf-8 -*-

# Copyright 2017, IBM.
#
# This source code is licensed under the Apache License, Version 2.0 found in
# the LICENSE.txt file in the root directory of this source tree.

"""
c4u1 gate. 4-Controlled-U1.
"""

from qiskit.circuit import Gate
from qiskit.circuit import QuantumCircuit
from qiskit.circuit import InstructionSet
from qiskit.circuit import QuantumRegister
from qiskit.dagcircuit import DAGCircuit
from qiskit.extensions.standard import header  # pylint: disable=unused-import
from qiskit.extensions.standard.u1 import U1Gate
from qiskit.extensions.standard.cx import CnotGate
from qiskit.extensions.standard.ccx import ToffoliGate
from qiskit.extensions.standard.c3x import C3NotGate
from qiskit.extensions.standard.c4x import C4NotGate

class C4U1Gate(Gate):
    """C4U1Gate instruction."""

    def __init__(self, theta, ctl1, ctl2, ctl3, ctl4, tgt, circ=None):
        """Create new c4u1 instruction."""
        super().__init__("c4u1", [theta], [ctl1, ctl2, ctl3, ctl4, tgt], circ)

    def _define_decompositions(self):
        decomposition = DAGCircuit()
        q = QuantumRegister(5, "q")
        decomposition.add_qreg(q)
        decomposition.add_basis_element("u1", 1, 0, 1)
        decomposition.add_basis_element("cx", 2, 0, 0)
        decomposition.add_basis_element("ccx", 3, 0, 0)
        decomposition.add_basis_element("c3x", 4, 0, 0)
        decomposition.add_basis_element("c4x", 5, 0, 0)
        rule = [
            C4NotGate(q[0], q[1], q[2], q[3] ,q[4]),
            C3NotGate(q[0], q[1], q[2], q[3]),
            ToffoliGate(q[0], q[1], q[2]),
            CnotGate(q[0], q[1]),
            U1Gate(-self.param[0]/16, q[1]),
            U1Gate(-self.param[0]/8, q[2]),
            U1Gate(-self.param[0]/4, q[3]),
            U1Gate(-self.param[0]/2, q[4]),
            CnotGate(q[0], q[1]),
            ToffoliGate(q[0], q[1], q[2]),
            C3NotGate(q[0], q[1], q[2], q[3]),
            C4NotGate(q[0], q[1], q[2], q[3], q[4]),
            U1Gate(self.param[0]/16, q[0]),
            U1Gate(self.param[0]/16, q[1]),
            U1Gate(self.param[0]/8, q[2]),
            U1Gate(self.param[0]/4, q[3]),
            U1Gate(self.param[0]/2, q[4])
        ]
        for inst in rule:
            decomposition.apply_operation_back(inst)
        self._decompositions = [decomposition]
    def inverse(self):
        """Special case. Return self."""
        return self

    def reapply(self, circ):
        """Reapply this instruction to corresponding qubits in circ."""
        self._modifiers(circ.c4u1(self.param[0], self.qargs[0], self.qargs[1], self.qargs[2], self.qargs[3], self.qargs[4]))


def c4u1(self, theta, ctl1, ctl2, ctl3, ctl4, tgt):
    """Apply c4u1 to circuit.
    If qargs is None, applies to all the qbits.
    Args is a list of QuantumRegister or single qubits.
    For QuantumRegister, applies c4u1 to all the qbits in that register."""
    return self._attach(C4U1Gate(theta, ctl1, ctl2, ctl3, ctl4, tgt, self))


QuantumCircuit.c4u1 = c4u1