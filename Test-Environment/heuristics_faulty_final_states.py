
def find_suspected_states(input_seq, output_seq, faulty_inp_idx, specificaiton_fsm, faulty_fsm):
    i = 0
    f_state, f_output, f_inp, f_output = faulty_fsm.faulty_transition

    current_states = [(i, i) for i in range(specificaiton_fsm.state_num)]

    for input_exp, output_exp in zip(input_seq[faulty_inp_idx + 1:], output_seq[faulty_inp_idx + 1:]):
        
        print(current_states)
        next_states = []
        for state, first_parent in current_states:
            input_idx = ord(input_exp) % ord('a')
            transition_idx = (specificaiton_fsm.input_num * state) + input_idx
            s1, s2, input, output = specificaiton_fsm.transitions[transition_idx]

            if output == output_exp:
                if s1 == f_state and input == f_inp:
                    next_states.append((first_parent, first_parent))
                else:
                    next_states.append((s2, first_parent))
        current_states = next_states
        i += 1
    return set(map(lambda x: x[1], current_states))


