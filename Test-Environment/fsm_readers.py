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

def read_faulty_fsm(file_path: str):
    with open(file_path, 'r') as f:
        # Addition to a correct FSM to read the faulty transition's index
        f.readline()
        fault_idx = int(f.readline().strip())

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
    return  fault_idx, state_num, transition_num, input_num, output_num, seed, edges

def read_transitions_tour(file_path: str):
    with open(file_path, 'r') as f:
        f.readline()
        f.readline()
        input_seq = f.readline().strip().split(",")
        output_seq = f.readline().strip().split(",")
    return input_seq, output_seq
