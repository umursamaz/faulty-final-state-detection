import filecmp

file1 = "../examples/PURE2024/test_seed_machines/test_seed_machine_1.dot"
file2 = "../examples/PURE2024/test_seed_machines/test_seed_machine_3.dot"
print(filecmp.cmp(file1, file2))