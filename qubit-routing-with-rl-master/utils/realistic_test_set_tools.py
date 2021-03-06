import os
import sys
from qiskit import QuantumCircuit


sys.path.insert(0, os.path.abspath('/home/darwesh/quantum-routing-optimisation/qubit-routing-with-rl-master'))
from environments.circuits import QubitCircuit

def import_test_set():
    print('Importing test set...')

    directory_path = "../realistic_test_set/"

    # files = os.listdir(directory_path)
    # qasm_files = list(filter(lambda file_name: len(file_name) > 5 and file_name[-5:] == ".qasm", files))

    file = os.listdir(directory_path)

    circuits = []

    file_name = '../realistic_test_set/test.qasm'
    for file_line in file:
        file_path = directory_path + file_line

        if os.path.getsize(file_path) > 10000:
            continue
        qiskit_circuit = QuantumCircuit.from_qasm_file(file_name)

        gates = []

        for gate_obj, qubits, _ in qiskit_circuit.data:
            if len(qubits) > 1:
                if gate_obj.__class__.__name__ not in ["CnotGate", "CXGate"]:
                    exit("Non-cnot gate (" + gate_obj.__class__.__name__ + ") found for circuit: " + str(file_name))

                gate = (qubits[0].index, qubits[1].index)
                gates.append(gate)

        circuit = QubitCircuit.from_gates(16, gates)


        circuits.append(circuit)

        # if i % int(len(qasm_files) / 3) == 0:
        #     print('Import ' + str(int(100 * i / len(qasm_files))) + '% complete')

    return list(filter(lambda c: c.depth() < 200, circuits))


circuits = list(filter(lambda c: c.depth() < 100, import_test_set()))

for circuit in circuits:
    print('Circuit depth:', circuit.depth())
    max_qubits = [max(q1, q2) for (q1, q2) in circuit.gates]
    print('Max qubit used:', max(max_qubits))
    print()
