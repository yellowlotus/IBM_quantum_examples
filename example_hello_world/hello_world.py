from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import EstimatorV2 as Estimator
from qiskit_ibm_runtime import QiskitRuntimeService

def create_new_circuit(number_qubits):
    qc = QuantumCircuit(number_qubits)
    return qc

def add_hadamart_gate(qubit):
    qc.h(qubit)
    return qc

def perform_controlled_x(control_quibit, perform_qubit):
    qc.cx(perform_qubit, control_quibit)
    return qc

def draw_circuit():
    return qc.draw(output='mpl',  filename='example_hello_world/my_circuit.png')

def set_up_observables():
    observables_labels = ["IZ", "IX", "ZI", "XI", "ZZ", "XX"]
    observables = [SparsePauliOp(label) for label in observables_labels]
    return observables

def set_up_qiskit_service():
    # QiskitRuntimeService.save_account(channel="ibm_quantum", instance="ibm-q/open/main", token='55ace7111f743da70bd93f5e478e135071169802a4127a1956206e4ca96cff1f994a725306f5e7414402e1b8b49e6d621ad0c43df93580cf39b14b70b0a51eec')
    service = QiskitRuntimeService(channel='ibm_quantum',
                                   token='55ace7111f743da70bd93f5e478e135071169802a4127a1956206e4ca96cff1f994a725306f5e7414402e1b8b49e6d621ad0c43df93580cf39b14b70b0a51eec')

    backend = service.least_busy(simulator=False, operational=True)
    return backend


def convert_to_an_ISA_circuit_and_layout_mapped_observables(backend):
    # Convert to an ISA circuit and layout-mapped observables.
    pm = generate_preset_pass_manager(backend=backend, optimization_level=1)
    isa_circuit = pm.run(qc)

    isa_circuit.draw(output="mpl", filename='example_hello_world/my_isa_circuit.png', idle_wires=False)
    return isa_circuit

def construct_the_estimator_instance(observables, isa_circuit):
    # Construct the Estimator instance.

    estimator = Estimator(mode=backend)
    estimator.options.resilience_level = 1
    estimator.options.default_shots = 5000

    mapped_observables = [
        observable.apply_layout(isa_circuit.layout) for observable in observables
    ]
    return estimator, mapped_observables




#operations on circuit
qc=create_new_circuit(2)
qc=add_hadamart_gate(0)
qc=perform_controlled_x(0,1)


draw_circuit()

observables=set_up_observables()

backend=set_up_qiskit_service()

isa_circuit=convert_to_an_ISA_circuit_and_layout_mapped_observables(backend)

estimator, mapped_observables=construct_the_estimator_instance(observables, isa_circuit)

# One pub, with one circuit to run against five different observables.
job = estimator.run([(isa_circuit, mapped_observables)])

# Use the job ID to retrieve your job data later
print(f">>> Job ID: {job.job_id()}")


