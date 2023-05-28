from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit import Aer, transpile

import matplotlib.pyplot as plt
from qiskit.visualization import plot_histogram


# Qubit
qreg_q = QuantumRegister(1, 'q')

# Classic bit
creg_c = ClassicalRegister(1, 'c')

# Quantum circuit
circuit = QuantumCircuit(qreg_q, creg_c)

# Reset to position |0>
circuit.reset(qreg_q[0])

# Add Hadamard Gate (Convert to Superposition)
# Superposition Formula is ( |0> + |1>) / sqrt(2)
circuit.h(qreg_q[0])

# Measure. Get answer from Quantum to classical bit
circuit.measure(qreg_q[0], creg_c[0])

circuit.draw(
    'mpl',
    filename="first_qapp",
)

# Run on Simulator
backend_sim = Aer.get_backend('qasm_simulator')
job_sim = backend_sim.run(
    transpile(circuit, backend_sim),
    shots=1024,
)

# Collect and show result
result_sim = job_sim.result()
counts = result_sim.get_counts(circuit)
print(counts)

plot_histogram(
    counts,
    filename="first_qapp_result"
)
plt.show()
