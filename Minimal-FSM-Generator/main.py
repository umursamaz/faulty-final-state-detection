from randomfsmgenerator import FSM
import sys


# Default values for commandline arguments
MACHINE_NUM = 1
SEED_NUM = 1
STATE_NUM = 16

# Default values for other parameters
num_of_inputs  = 2
num_of_outputs = 2

# Capture command-line argument for num_states & seed number & machine number

if len(sys.argv) > 3:
   seed = int(sys.argv[3])
else:
   seed = SEED_NUM

if len(sys.argv) > 2:
    num_of_machines = int(sys.argv[2])
else:
    num_of_machines = MACHINE_NUM

if len(sys.argv) > 1:
    num_of_states = int(sys.argv[1])
else:
    num_of_states = STATE_NUM  # Default value if not provided
    
# Generate and save FSMs
for i in range(num_of_machines):
    myfsm = FSM(num_of_states, num_of_inputs, num_of_outputs, seed)
    myfsm.generateStronglyConnectedMinimal()
    myfsm.output_for_ads("../examples/test_machines/" + str(num_of_states) + "_states/test_machine_" + str(num_of_states) + "_states_" + str(seed) + "_seed")
    seed += 1

# myfsm.show()
# myfsm.draw()