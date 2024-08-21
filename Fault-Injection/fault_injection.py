import random

def read_fsm(file_path: str):
    with open(file_path, 'r') as f:
        f.readline()
        state_num, transition_num, input_num, output_num, seed = map(int, f.readline().strip().split(","))
        f.readline()

        def read_transitions(string):
            string = string.strip()
            try:
                return int(string)
            except:
                return string

        edges = [tuple(map(read_transitions, f.readline().strip().split(","))) for _ in range(transition_num)]
    return  state_num, transition_num, input_num, output_num, seed, edges

def write_faulty_fsm(file_path: str, fault_index, state_num, transition_num, input_num, output_num, seed, faulty_transitions):
    with open(file_path, 'w') as f:
        f.write("faulty_transition_index\n")
        f.write(str(fault_index) + "\n")
        f.write("state_num, transition_num, input_num, output_num, seed\n")
        f.write(f"{state_num}, {transition_num}, {input_num}, {output_num}, {seed}\n")
        f.write("source_state, destination_state, input_symbol, output_symbol\n")
        for s1, s2, inp, outp in faulty_transitions:
            f.write(f"{s1}, {s2}, {inp}, {outp}\n")


def inject_fault(state_num: int, transition_num: int, seed: int, transitions: list):

    # There is no state to invert the correct transition & program exits with an error code
    if state_num == 1:
        exit(1)
    
    random.seed(seed)

    fault_index = random.randint(1, transition_num) - 1

    s1, s2, input, output = transitions[fault_index]

    si = s2

    while si == s2:
        si = random.randint(1, state_num) - 1
    
    faulty_transitions = transitions.copy()
    faulty_transitions[fault_index] = (s1, si, input, output)

    return faulty_transitions, fault_index
    

