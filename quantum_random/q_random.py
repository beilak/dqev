from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit import Aer, transpile, execute
import matplotlib.pyplot as plt
from qiskit.visualization import plot_histogram


def make_circuit(qubit_count: int = 1):
    """Make circuit"""
    bit = qubit_count
    qreg_q = QuantumRegister(qubit_count, 'q')
    creg_c = ClassicalRegister(bit, 'c')
    _circuit = QuantumCircuit(qreg_q, creg_c)
    for i in range(0, qubit_count):
        _circuit.reset(qreg_q[i])    # Set |0>
        _circuit.h(qreg_q[i])    # Add H
    _circuit.measure_all()
    return _circuit


def run_on_simulator(_circuit):
    """Run Circuit on Simulator"""
    backend = Aer.get_backend('qasm_simulator')
    job = execute(_circuit, backend, shots=20_000)
    result = job.result()
    return result.get_counts()


def save_circuit(_circuit, f_name):
    """Save Circuit"""
    _circuit.draw(
        'mpl',
        filename=f_name,
    )


def q_random():
    """Experiment with random """
    q = 7
    _circuit = make_circuit(q)
    save_circuit(_circuit, f"random_{q}q",)
    # Run on simulator
    counts_simulator = run_on_simulator(_circuit)
    # print(counts_simulator)

    plot_histogram(counts_simulator, filename=f"random_{q}q_simulator_counts")
    plt.xticks(fontsize=8)
    plt.show()


if __name__ == "__main__":
    q_random()
