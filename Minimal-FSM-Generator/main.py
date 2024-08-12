from randomfsmgenerator import FSM
import sys

# Capture command-line argument for num_states & seed number

if len(sys.argv) > 2:
    seed = float(sys.argv[2])
else:
    seed = 10


if len(sys.argv) > 1:
    num_of_states = int(sys.argv[1])
else:
    num_of_states = 15  # Default value if not provided
    
num_of_inputs  = 2
num_of_outputs = 2


myfsm = FSM(num_of_states, num_of_inputs, num_of_outputs, seed)
myfsm.generateStronglyConnectedMinimal()
myfsm.output_for_ads("../examples/PURE2024/test_seed_machines/test_seed_machine_5.dot")
# myfsm.show()
# myfsm.draw()