import fsm_readers
from fsm import *
from heuristics_faulty_final_states import *


def test(fsm_path, faulty_fsm_path, transition_tour_path):

    state_num, transition_num, input_num, output_num, seed, transitions = fsm_readers.read_fsm(fsm_path)
    fault_idx, state_num, transition_num, input_num, output_num, seed, faulty_transitions = fsm_readers.read_faulty_fsm(faulty_fsm_path)
    transition_tour_inp, transition_tour_outp = fsm_readers.read_transitions_tour(transition_tour_path)

    specification_fsm = FSM(state_num, transition_num, input_num, output_num, seed, transitions)
    iut_fsm = FSM(state_num, transition_num, input_num, output_num, seed, faulty_transitions, fault_idx)

    output_expected, fault_inp_idx_s = specification_fsm.apply(transition_tour_inp)
    output_experiment, fault_inp_idx_i = iut_fsm.apply(transition_tour_inp)

    if output_expected != output_experiment:
        suspected_states = find_suspected_states(transition_tour_inp, output_experiment, fault_inp_idx_i, specification_fsm, iut_fsm)
        return suspected_states





fsm_path = "../examples/PURE2024/test_machines/128_states/test_machine_128_states_56_seed.csv"
faulty_fsm_path = "../examples/PURE2024/faulty_test_machines/128_states/faulty_test_machine_128_states_56_seed.csv"
transition_tour_path = "../examples/PURE2024/transition_tours/128_states/transition_tour_128_states_56_seed.csv"
    
state_num, transition_num, input_num, output_num, seed, transitions = fsm_readers.read_fsm(fsm_path)
fault_idx, state_num, transition_num, input_num, output_num, seed, faulty_transitions = fsm_readers.read_faulty_fsm(faulty_fsm_path)
transition_tour_inp, transition_tour_outp = fsm_readers.read_transitions_tour(transition_tour_path)

specification_fsm = FSM(state_num, transition_num, input_num, output_num, seed, transitions)
iut_fsm = FSM(state_num, transition_num, input_num, output_num, seed, faulty_transitions, fault_idx)

output_expected, fault_inp_idx_s = specification_fsm.apply(transition_tour_inp)
output_experiment, fault_inp_idx_i = iut_fsm.apply(transition_tour_inp)

if output_expected != output_experiment:
    print(fault_inp_idx_i)
    print(find_suspected_states(transition_tour_inp, output_experiment, fault_inp_idx_i, specification_fsm, iut_fsm))


