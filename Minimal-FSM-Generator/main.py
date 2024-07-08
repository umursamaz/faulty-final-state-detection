from randomfsmgenerator import FSM
import sys

# Capture command-line argument for num_states
if len(sys.argv) > 1:
    num_of_states = int(sys.argv[1])
else:
    num_of_states = 15  # Default value if not provided
    
num_of_inputs  = 2
num_of_outputs = 2

myfsm = FSM(num_of_states, num_of_inputs, num_of_outputs)
myfsm.generateStronglyConnectedMinimal()
myfsm.output_for_ads("../examples/ads_example.dot")
# myfsm.show()
# myfsm.draw()