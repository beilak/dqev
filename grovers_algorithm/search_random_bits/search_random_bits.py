"""Experiment with searching random numbers.
Using Grover's Algorithm.
"""

import random
from qiskit.quantum_info import Statevector
from qiskit import Aer, execute
from qiskit.algorithms import Grover, AmplificationProblem
from qiskit.providers.ibmq import least_busy
from qiskit.visualization import *
from qiskit.providers import Backend
from qiskit_ibm_provider import IBMProvider
import matplotlib.pyplot as plt


# TOKEN DON'T FORGET!!!!
TOKEN = os.getenv('IBMQ_TOKEN')


def make_circuit(secret_string):
    """Make circuit"""
    # Oracle has to know what we're looking for
    oracle = Statevector.from_label(secret_string)

    problem = AmplificationProblem(
        oracle=oracle,
        is_good_state=secret_string,
    )

    grover = Grover(iterations=1)
    _circuit = grover.construct_circuit(problem)
    _circuit.measure_all()
    return _circuit


def run_on_simulator(_circuit):
    """Run Circuit on Simulator"""
    backend = Aer.get_backend('qasm_simulator')
    job = execute(_circuit, backend, shots=1024)
    result = job.result()
    return result.get_counts()


def run_on_quantum_computer(_circuit):
    """Run Circuit on real Quantum Computer"""
    # IBMQ.load_account()

    def __get_quantum_backend() -> Backend:
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

    backend = __get_quantum_backend()
    job = backend.run(_circuit)
    print(f"{ job = }")


def save_circuit(_circuit, f_name):
    """Save Circuit"""
    _circuit.draw(
        'mpl',
        filename=f_name,
    )


def grover_search_random(on_simulator: bool, on_quantum: bool):
    """Experiment with searching random numbers"""

    # Secret for searching
    secret = random.randint(0, 7)
    secret_string = format(secret, "04b")  # secret in 4-bit string format
    print(f"{ secret = }")
    print(f"{ secret_string = }")

    # Make Cirvuit
    grover_circuit = make_circuit(secret_string)
    save_circuit(grover_circuit, "Grover_search_random_circuit")

    # Run on simulator
    if on_simulator:
        counts_simulator = run_on_simulator(grover_circuit)

    # Run on real q computer
    if on_quantum:
        run_on_quantum_computer(grover_circuit)

    plot_histogram(counts_simulator, filename="Grover_random_simulator_counts")
    plt.show()


if __name__ == "__main__":
    grover_search_random(
        on_simulator=True,
        on_quantum=True,
    )


