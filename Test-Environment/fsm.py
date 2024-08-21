class FSM():
    def __init__(self, state_num: int, transition_num: int, input_num: int, output_num: int, seed: int, transitions: list, fault_idx = None):
        self.isfaulty = False if (fault_idx == None) else True
        self.fault_idx = fault_idx
        self.state_num = state_num
        self.transition_num = transition_num
        self.input_num = input_num
        self.seed = seed
        self.transitions = transitions
    
    def appy(test_sequence: iterable):
        pass
