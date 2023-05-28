"""Experiments with Grover's Algorithm (with 2 qubits)."""

# import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, transpile, Aer, IBMQ, execute, assemble

from qiskit.providers.ibmq import least_busy
from qiskit.visualization import *
from qiskit.providers import Backend
from qiskit_ibm_provider import IBMProvider
from qiskit_ibm_provider.ibm_backend import IBMBackend
from qiskit.tools.monitor import job_monitor

# TOKEN DON'T FORGET!!!!
TOKEN = os.getenv('IBMQ_TOKEN')


def initialize(qc):
    """Applying H"""
    qc.h(0)
    qc.h(1)
    qc.barrier()


def oracle_11(qc):
    """Apply Z gate"""
    qc.cz(0, 1)
    qc.barrier()


def u_g(qc):
    """Creating Grover's Diffusion operator"""
    qc.h(0)
    qc.h(1)
    qc.x(0)
    qc.x(1)
    qc.h(1)
    qc.cx(0, 1)
    qc.x(0)
    qc.h(1)
    qc.h(0)
    qc.x(1)
    qc.h(1)


def make_circuit():
    """Make circuit"""
    grover_circuit = QuantumCircuit(2)  # Initializing circuit

    initialize(grover_circuit)  # Init
    oracle_11(grover_circuit)  # Add Oracle
    u_g(grover_circuit)  # Add Diffusion

    grover_circuit.measure_all()  # Add measure's

    return grover_circuit


def run_on_simulator(_circuit):
    """Run Circuit on Simulator"""
    backend = Aer.get_backend('qasm_simulator')
    job = execute(_circuit, backend, shots=1024)
    result = job.result()
    return result.get_counts()


def run_on_quantum_computer(_circuit, job_tags, waith=False):
    """Run Circuit on real Quantum Computer"""

    def __get_quantum_backend() -> IBMBackend:
        """Getting the least busy backend:"""
        # provider = IBMQ.get_provider(hub='ibm-q')
        provider = IBMProvider(token=TOKEN)
        __backend = least_busy(
            provider.backends(
                filters=lambda x: x.configuration().n_qubits >= 2
                                  and not x.configuration().simulator
                                  and x.status().operational == True),
        )
        print("least busy backend: ", __backend)
        return __backend

    backend: IBMBackend = __get_quantum_backend()

    # Optimize
    transpiled_grover_circuit = transpile(_circuit, backend, optimization_level=0)
    # qobj = assemble(transpiled_grover_circuit)
    job = backend.run(
        transpiled_grover_circuit,
        job_tags=job_tags,
        shots=1024,
    )
    print(f"{ job = }")

    # Monitor the execution of the job in the queue:
    if waith:
        job_monitor(job, interval=2)
        # # Getting the results from the computation:
        results = job.result()
        answer = results.get_counts(_circuit)
        return answer


def save_circuit(_circuit, f_name):
    """Save Circuit"""
    _circuit.draw(
        'mpl',
        filename=f_name,
    )


def grover_2q():
    grover_circuit = make_circuit()
    save_circuit(grover_circuit, "Grover_2q_circuit")

    # Run on simulator
    counts_simulator = run_on_simulator(grover_circuit)

    # Run on real q computer
    run_on_quantum_computer(grover_circuit, job_tags=["grover_2q"])

    # Run on real q computer with waiting result
    # counts_qc = run_on_quantum_computer(grover_circuit, waith=True)
    # plot_histogram(counts_qc, filename="Grover_2q_quantum_counts")

    plot_histogram(counts_simulator, filename="Grover_2q_simulator_counts")
    plt.show()


if __name__ == "__main__":
    grover_2q()
