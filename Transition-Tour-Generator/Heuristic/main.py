import sys
import os
import transition_tour as tt

START_STATE = 0

if len(sys.argv) > 1:
    state_num = sys.argv[1]
else:
    state_num = "16"

fsm_dir = "../../examples/test_machines/" 

transition_tour_dir = "../../examples/transition_tours/" 

for filename in os.listdir(fsm_dir + state_num + "_states/"):

    if filename.endswith('.csv'):
        fsm_path = fsm_dir + str(state_num) + "_states/"+ filename
        state_num, transition_num, input_num, output_num, seed, transitions = tt.read_fsm(fsm_path)

        tour, input_seq, output_seq = tt.transition_tour(START_STATE, transitions)

        transition_tour_path = transition_tour_dir + str(state_num) + "_states/transition_tour_" + str(state_num) + "_states_" + str(seed) + "_seed.csv"
        tt.write_fsm(transition_tour_path, tour, input_seq, output_seq)
