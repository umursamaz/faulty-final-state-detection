import sys
import os
import fault_injection as fi

if len(sys.argv) > 1:
    state_num = sys.argv[1]
else:
    state_num = "64"

seed = int(state_num) * 2
fsm_dir = "../examples/PURE2024/test_machines/"

fault_injection_dir = "../examples/PURE2024/faulty_test_machines/" 

resource_dir = os.path.join(fsm_dir, f"{state_num}_states/")
target_dir = os.path.join(fault_injection_dir, f"{state_num}_states_test/")

for filename in os.listdir(resource_dir):

    if filename.endswith('.csv'):
        #fsm_path = fsm_dir + str(state_num) + "_states/" + filename
        fsm_path = resource_dir + filename
        state_num, transition_num, input_num, output_num, dummy_seed, transitions = fi.read_fsm(fsm_path)

        injection_idexes = {}
        faulty_transitions, injection_idx, input = fi.inject_fault(state_num, transition_num, transition_num, transitions)
        injection_idexes[seed] = injection_idx, input
        
        for i in range(seed-1, 0, -1):
            faulty_transitions, injection_idx, input = fi.inject_fault(state_num, transition_num, i, faulty_transitions)
            injection_idexes[i] = injection_idx, input
                
        faulty_fsm_path = target_dir + "faulty_" +  filename
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        fi.write_faulty_fsm(faulty_fsm_path, injection_idx, state_num, transition_num, input_num, output_num, i, faulty_transitions)
        
        print(f"The fault for seed of {i + 1} injected at {injection_idexes[i + 1]} in the faulty FSM {dummy_seed}.")
        