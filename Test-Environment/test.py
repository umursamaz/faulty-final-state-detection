import os
import fsm_readers
from fsm import *
from heuristics_faulty_final_states import *
from result_writer import *



def test(fsm_path, faulty_fsm_dir, transition_tour_path, result_dir):

    state_num, transition_num, input_num, output_num, seed, transitions = fsm_readers.read_fsm(fsm_path)
    transition_tour_inp, transition_tour_outp = fsm_readers.read_transitions_tour(transition_tour_path)
    
    specification_fsm = FSM(state_num, transition_num, input_num, output_num, seed, transitions)
    
    faulty_fsm_dir = faulty_fsm_dir + f"{seed}_seed/"
    
    for filename in os.listdir(faulty_fsm_dir):
      if filename.endswith('.csv'):
    
        faulty_fsm_path = faulty_fsm_dir + filename
         
        fault_idx, state_num, transition_num, input_num, output_num, fsm_seed, fault_seed, faulty_transitions = fsm_readers.read_faulty_fsm(faulty_fsm_path)
        
        iut_fsm = FSM(state_num, transition_num, input_num, output_num, seed, faulty_transitions, fault_idx)
    
        output_expected, fault_inp_idx_s = specification_fsm.apply(transition_tour_inp)
        output_experiment, fault_inp_idx_i = iut_fsm.apply(transition_tour_inp)
    
        if output_expected != output_experiment:
            is_singleton, singleton_idx, suspected_states, applied_input = find_suspected_states(transition_tour_inp, output_experiment, fault_inp_idx_i, specification_fsm, iut_fsm)
            
            result_path = result_dir + f"result_{state_num}_states_{fsm_seed}_seed_{fault_seed}_fault_seed.csv"
            write_result(result_path, state_num, fsm_seed, fault_seed, is_singleton, singleton_idx, suspected_states, applied_input) 



if __name__ == "__main__":
    fsm_path = "../examples/test_machines/128_states/test_machine_128_states_56_seed.csv"
    faulty_fsm_dir = "../examples/faulty_test_machines/128_states/"
    transition_tour_path = "../examples/transition_tours/128_states/transition_tour_128_states_56_seed.csv"
        
    state_num, transition_num, input_num, output_num, seed, transitions = fsm_readers.read_fsm(fsm_path)
    transition_tour_inp, transition_tour_outp = fsm_readers.read_transitions_tour(transition_tour_path)
    
    specification_fsm = FSM(state_num, transition_num, input_num, output_num, seed, transitions)
    
    faulty_fsm_dir = faulty_fsm_dir + f"{seed}_seed/"
    
    for filename in os.listdir(faulty_fsm_dir):
      if filename.endswith('.csv'):
    
        faulty_fsm_path = faulty_fsm_dir + filename
         
        fault_idx, state_num, transition_num, input_num, output_num, fsm_seed, fault_seed, faulty_transitions = fsm_readers.read_faulty_fsm(faulty_fsm_path)
        
        iut_fsm = FSM(state_num, transition_num, input_num, output_num, seed, faulty_transitions, fault_idx)
    
        output_expected, fault_inp_idx_s = specification_fsm.apply(transition_tour_inp)
        output_experiment, fault_inp_idx_i = iut_fsm.apply(transition_tour_inp)
    
        if output_expected != output_experiment:
            is_singleton, singleton_idx, suspected_states, applied_input = find_suspected_states(transition_tour_inp, output_experiment, fault_inp_idx_i, specification_fsm, iut_fsm)
            
            
            write_result(f"example_{fault_seed}_fault_seed.csv", state_num, fsm_seed, fault_seed, is_singleton, singleton_idx, suspected_states, applied_input) 

