"""
1. QC
"""
import os
from qiskit import QuantumCircuit
from qiskit.visualization import plot_histogram
from qiskit import Aer, transpile
import matplotlib.pyplot as plt
from qiskit_ibm_provider import IBMProvider
from qiskit_ibm_provider.ibm_backend import IBMBackend


TOKEN = os.getenv('IBMQ_TOKEN')

# 3 Qubits
qc = QuantumCircuit(3)


qc.h(0)
qc.cx(0, [1, 2])

qc.measure_all()

qc.draw(
    'mpl',
    filename="first_qapp",
)


# SIMULATOR
backend_sim = Aer.get_backend('qasm_simulator')
job_sim = backend_sim.run(
    transpile(qc, backend_sim),
    shots=1024,
)

result_sim = job_sim.result()
counts = result_sim.get_counts(qc)
print(counts)

plot_histogram(
    counts,
    filename="first_qapp_result"
)
plt.show()


# # Connect to QUANTUM COMPUTER.
provider = IBMProvider(token=TOKEN)
backend: IBMBackend = provider.backends(
    filters=lambda x: not x.configuration().simulator
                      and x.status().operational == True,
    min_num_qubits=3,
)[0]

print(f"{ backend = }")

transpiled_qc = transpile(qc, backend)
job = backend.run(
    transpiled_qc,
    job_tags=["31", "CNOT"],
    shots=1024,
)
