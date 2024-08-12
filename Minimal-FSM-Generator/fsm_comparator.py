import filecmp

file1 = "../examples/PURE2024/test_seed_machines/test_seed_machine_1.dot"
file2 = "../examples/PURE2024/test_seed_machines/test_seed_machine_4.dot"
print("These two FSM's are the same." if filecmp.cmp(file1, file2) else "These two FSM's are different.")