import sys
import os
from test import *

if len(sys.argv) > 1:
    state_num = sys.argv[1]
else:
    state_num = "16"

fsm_dir = "../examples/PURE2024/test_machines/" + state_num + "_states/"

fault_fsm_dir = "../examples/PURE2024/faulty_test_machines/" + state_num + "_states/"

transition_tour_dir = "../examples/PURE2024/transition_tours/" + state_num + "_states/"

for filename in os.listdir(fsm_dir):
    if filename.endswith('.csv'):
        print(test(fsm_dir + filename, fault_fsm_dir + "faulty_" + filename, transition_tour_dir + "transition_tour_" + filename[13: ]))

