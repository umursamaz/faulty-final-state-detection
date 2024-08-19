import sys
import os
import fault_injection as fi

if len(sys.argv) > 1:
    state_num = sys.argv[1]
else:
    state_num = "16"

fsm_dir = "../examples/PURE2024/test_machines/" 

fault_injection_dir = "../examples/PURE2024/fault_injections/" 

for filename in os.listdir(fsm_dir + state_num + "_states/"):

    if filename.endswith('.csv'):
        fsm_path = fsm_dir + str(state_num) + "_states/"+ filename
        state_num, transition_num, input_num, output_num, seed, transitions = fi.read_fsm(fsm_path)
     
        injected_fault, injection_idx = fi.inject_fault(state_num, transition_num, seed, transitions)
        