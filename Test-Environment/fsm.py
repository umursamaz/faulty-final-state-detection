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

        if self.isfaulty:
            self.faulty_transition = transitions[fault_idx]
    
    def reset(self):
        sellf.current_state = 0

    def apply(self, test_sequence: iter):


        def apply(inp:chr, currrent_idx: int):
            # Char inputs turned into integers starting from zero according to the order in the alphabet
            input_idx = ord(inp) % ord('a')
            transition_idx = (self.input_num * self.current_state) + input_idx
            state, next_state, inp, outp = self.transitions[transition_idx]

            # To identify first input that causes the faulty transition
            faulty_inp_idx = None
            state_before_fault = None
            if self.isfaulty:
                if self.faulty_transition == (state, next_state, inp, outp):
                    faulty_inp_idx = currrent_idx
                    state_before_fault = state

            self.current_state = next_state
            return outp, faulty_inp_idx
        
        outp_seq = []
        faulty_input_idx = None
    
        for i in range(len(test_sequence)):
            output, index = apply(test_sequence[i], i)
            outp_seq.append(output)

            if faulty_input_idx == None and index != None:
                faulty_input_idx = index

        return outp_seq, faulty_input_idx
