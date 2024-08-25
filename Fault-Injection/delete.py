import os

state_num = "16"



fsm_dir = "../examples/PURE2024/faulty_test_machines/"
target_dir = os.path.join(fsm_dir, f"{state_num}_states/")


for filename in os.listdir(target_dir):
    file_path = os.path.join(target_dir, filename)

    if not filename.endswith('.csv'):
        os.remove(file_path)
        print(f"Deleted: {file_path}")
    else:
        print(f"Skipped: {filename}")

# state_num = "32"
# target_dir = os.path.join(fsm_dir, f"{state_num}_states/")
# for filename in os.listdir(target_dir):
#     file_path = os.path.join(target_dir, filename)

#     if '.' not in filename:
#         os.remove(file_path)
#         print(f"Deleted: {file_path}")
#     else:
#         print(f"Skipped: {filename}")

# state_num = "64"
# target_dir = os.path.join(fsm_dir, f"{state_num}_states/")
# for filename in os.listdir(target_dir):
#     file_path = os.path.join(target_dir, filename)

#     if '.' not in filename:
#         os.remove(file_path)
#         print(f"Deleted: {file_path}")
#     else:
#         print(f"Skipped: {filename}")

# state_num = "128"
# target_dir = os.path.join(fsm_dir, f"{state_num}_states/")

# for filename in os.listdir(target_dir):
#     file_path = os.path.join(target_dir, filename)

#     if '.' not in filename:
#         os.remove(file_path)
#         print(f"Deleted: {file_path}")
#     else:
#         print(f"Skipped: {filename}")