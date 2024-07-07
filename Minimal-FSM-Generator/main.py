from randomfsmgenerator import FSM

num_of_states  = 3
num_of_inputs  = 2
num_of_outputs = 2

myfsm = FSM(num_of_states, num_of_inputs, num_of_outputs)
myfsm.generateMinimal()
myfsm.output_for_ads("../examples/ads_example.dot")
myfsm.show()
# myfsm.draw()