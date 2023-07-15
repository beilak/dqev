from qiskit import QuantumCircuit
from qiskit.visualization import plot_histogram
from qiskit import Aer, transpile
import matplotlib.pyplot as plt
from qiskit_aer.backends.qasm_simulator import QasmSimulator
from qiskit_aer.jobs.aerjob import AerJob


# Circuit
qc: QuantumCircuit = QuantumCircuit(4, 2)

# Encode Input
# name = "0 and 0"
# qc.reset(0) # Set |0>
# qc.reset(1)

# name = " 0 and 1"
# qc.reset(0)
# qc.x(1)

# name = "1 and 0"
# qc.x(0) # Convert |0> to |1>
# qc.reset(1) # Set |0>


#
name = "1 and 1"
qc.x(0) # NOT
qc.x(1) # NOT


# Aadder

qc.cx(0,2)  # CNOT
qc.cx(1,2)  # CNOT
qc.ccx(0, 1, 3)

# Measure Result
qc.measure([2,3], [0,1])

# Save QC
qc.draw(
    'mpl',
    filename=f"half_adder_{name}",
)

# SIMULATOR
backend_sim: QasmSimulator = Aer.get_backend('qasm_simulator')
job_sim: AerJob = backend_sim.run(
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
