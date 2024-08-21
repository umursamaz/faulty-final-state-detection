import fsm_readers

fsm_path = "../examples/PURE2024/test_machines/16_states/test_machine_16_states_17_seed.csv"
faulty_fsm_path = "../examples/PURE2024/faulty_test_machines/16_states/faulty_test_machine_16_states_17_seed.csv"
transition_tour_path = "../examples/PURE2024/transition_tours/16_states/transition_tour_16_states_17_seed.csv"


state_num, transition_num, input_num, output_num, seed, transitions = fsm_readers.read_fsm(fsm_path)
fault_idx, state_num, transition_num, input_num, output_num, seed, transitions = fsm_readers.read_faulty_fsm(faulty_fsm_path)
transition_tour_inp, transition_tour_outp = fsm_readers.read_transitions_tour(transition_tour_path)
