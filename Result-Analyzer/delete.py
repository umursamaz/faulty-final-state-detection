import os

current_directory = os.path.dirname(os.path.abspath(__file__))


base_directory = '../examples/PURE2024/test_machines/'

for i in [16, 32, 64, 128]:
    state_directory = os.path.join(base_directory, f'{i}_states')
    
    
    for filename in os.listdir(state_directory):
        # Construct the full file path
        file_path = os.path.join(state_directory, filename)

        # Check if it's a file and does not contain a dot (.)
        if os.path.isfile(file_path) and '.' not in filename:
            try:
                os.remove(file_path)
                print(f"Deleted: {file_path}")
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")