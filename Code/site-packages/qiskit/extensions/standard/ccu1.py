# -*- coding: utf-8 -*-

# Copyright 2017, IBM.
#
# This source code is licensed under the Apache License, Version 2.0 found in
# the LICENSE.txt file in the root directory of this source tree.

"""
ccu1 gate. Contolled-Controlled-U1.
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

class CCU1Gate(Gate):
    """CCU1Gate instruction."""

    def __init__(self, theta, ctl1, ctl2, tgt, circ=None):
        """Create new ccu1 instruction."""
        super().__init__("ccu1", [theta], [ctl1, ctl2, tgt], circ)

    def _define_decompositions(self):
        decomposition = DAGCircuit()
        q = QuantumRegister(3, "q")
        decomposition.add_qreg(q)
        decomposition.add_basis_element("u1", 1, 0, 1)
        decomposition.add_basis_element("cx", 2, 0, 0)
        decomposition.add_basis_element("ccx", 3, 0, 0)
        rule = [
            ToffoliGate(q[0], q[1], q[2]),
            CnotGate(q[0], q[1]),
            U1Gate(-self.param[0]/4, q[1]),
            U1Gate(-self.param[0]/2, q[2]),
            CnotGate(q[0], q[1]),
            ToffoliGate(q[0], q[1], q[2]),
            U1Gate(self.param[0]/4, q[0]),
            U1Gate(self.param[0]/4, q[1]),
            U1Gate(self.param[0]/2, q[2])
        ]
        for inst in rule:
            decomposition.apply_operation_back(inst)
        self._decompositions = [decomposition]
    def inverse(self):
        """Special case. Return self."""
        return self

    def reapply(self, circ):
        """Reapply this instruction to corresponding qubits in circ."""
        self._modifiers(circ.ccu1(self.param[0], self.qargs[0], self.qargs[1], self.qargs[2]))


def ccu1(self, theta, ctl1, ctl2, tgt):
    """Apply ccu1 to circuit.
    If qargs is None, applies to all the qbits.
    Args is a list of QuantumRegister or single qubits.
    For QuantumRegister, applies ccu1 to all the qbits in that register."""
    return self._attach(CCU1Gate(theta, ctl1, ctl2, tgt, self))


QuantumCircuit.ccu1 = ccu1