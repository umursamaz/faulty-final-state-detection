class FSM():
    def __init__(self, state_num: int, transition_num: int, input_num: int, output_num: int, seed: int, transitions: list, fault_idx = None):
        self.isfaulty = False if (fault_idx == None) else True
        self.fault_idx = fault_idx
        self.state_num = state_num
        self.transition_num = transition_num
        self.input_num = input_num
        self.seed = seed
        self.transitions = transitions
        self.current_state = 0
    
    def reset(self):
        sellf.current_state = 0

    def apply(self, test_sequence: iter):
        def apply(inp:chr):
            input_idx = ord(inp) % ord('a')
            transition_idx = (self.input_num * self.current_state) + input_idx
            state, next_state, inp, outp = self.transitions[transition_idx]
            self.current_state = next_state
            return outp
            
        outp_seq = [apply(inp) for inp in test_sequence]

        return outp_seq
