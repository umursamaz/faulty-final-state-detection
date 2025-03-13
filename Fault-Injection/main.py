import sys
import os
import fault_injection as fi

if len(sys.argv) > 1:
    state_num = sys.argv[1]
else:
    state_num = "64"

fsm_dir = f"../examples/test_machines/{state_num}_states/"
fault_injection_dir = f"../examples/faulty_test_machines/{state_num}_states/" 

for filename in os.listdir(fsm_dir):

    if filename.endswith('.csv'):
        #fsm_path = fsm_dir + str(state_num) + "_states/" + filename
        fsm_path = fsm_dir + filename
        state_num, transition_num, input_num, output_num, fsm_seed, transitions = fi.read_fsm(fsm_path)

        for fault_seed in range(1, transition_num + 1):
            faulty_transitions, injection_idx = fi.inject_fault(state_num, transition_num, fault_seed, transitions)

            fault_injection_path  = fault_injection_dir + f"{fsm_seed}_seed/"

            if not os.path.exists(fault_injection_path):
                os.makedirs(fault_injection_path)
            
            faulty_fsm_path = fault_injection_path + "faulty_" +  filename.strip(".csv") + f"_{fault_seed}_fault_seed.csv"
            fi.write_faulty_fsm(faulty_fsm_path, injection_idx, state_num, transition_num, input_num, output_num, fsm_seed, fault_seed, faulty_transitions)
        
        