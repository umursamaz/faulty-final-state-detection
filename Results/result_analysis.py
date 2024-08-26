import os
import csv
from collections import defaultdict

# Base directory where the results are stored
base_directory = '../examples/PURE2024/results/'

# Get the current directory where the script is located
current_directory = os.path.dirname(os.path.abspath(__file__))

# Define the file path in the current directory
output_file_path = os.path.join(current_directory, 'fsm_results.txt')

# Dictionary to store categorized data
categorized_data = {
    16: [],
    32: [],
    64: [],
    128: []
}

simplified_data = {
    16: [],
    32: [],
    64: [],
    128: []
}

# Function to process each CSV file
def process_csv_file(file_path, num_states):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        
        is_singleton = None
        applied_input_sequence_length = 0
        suspected_states = None
        suspected_states_numbers = 0

        for row in reader:
            if len(row) == 2 and row[0] == 'is_singleton':
                key, value = next(reader)
                is_singleton = key.strip()
                applied_input_sequence_length = int(value.strip()) + 1 if is_singleton == 'True' else 0
                
            if len(row) == 1 and row[0] == 'suspected_states':
                suspected_states = next(reader)
                suspected_states_numbers = len(suspected_states)
                
        categorized_data[num_states].append({
            'is_singleton': is_singleton,
            'applied_input_sequence_length': applied_input_sequence_length,
            'suspected_states_numbers': suspected_states_numbers
        })
    file.close()

# Iterate over the subdirectories corresponding to state numbers
for state_num in [16, 32, 64, 128]:
    state_directory = os.path.join(base_directory, f'{state_num}_states')
    if os.path.exists(state_directory):
        for filename in os.listdir(state_directory):
            if filename.endswith('.csv'):
                file_path = os.path.join(state_directory, filename)
                process_csv_file(file_path, state_num)
    
    # Simplified data keeps the simple statistics for each state number 
    # For instance it keeps the number of singletons and the number of non-singletons
    # It also keeps the average number of suspected states for non-singletons
    # It also keeps the average number of inputs for singletons
    
    num_singletons = 0
    num_non_singletons = 0
    total_suspected_state_numbers = 0
    total_applied_input_sequence_length = 0
    
    for data in categorized_data[state_num]:
        if data['is_singleton'] == 'True':
            num_singletons += 1
            total_applied_input_sequence_length += data['applied_input_sequence_length'] if data['applied_input_sequence_length'] != None else 0
        else:
            num_non_singletons += 1
            total_suspected_state_numbers += data['suspected_states_numbers']
    
    simplified_data[state_num] = {
        'num_singletons': num_singletons,
        'num_non_singletons': num_non_singletons,
        'percantage_of_non_singletons': num_non_singletons / (num_singletons + num_non_singletons) * 100 if num_singletons + num_non_singletons > 0 else 0,
        'average_suspected_states': total_suspected_state_numbers / num_non_singletons if num_non_singletons > 0 else 0,
        'average_applied_inputs_length': total_applied_input_sequence_length / num_singletons if num_singletons > 0 else 0,
        'ratio_of_average_applied_inputs_length_to_state_num': total_applied_input_sequence_length / num_singletons / state_num
    }

    # Print the simplified data
    print(f'\nState number: {state_num}')
    # for item in simplified_data[state_num]:
    #     print(f'{item}: {simplified_data[state_num][item]}')
    with open(output_file_path, 'a') as file:  # 'a' mode opens the file in append mode
        file.write(f'State number: {state_num}\n')
        for item in simplified_data[state_num]:
            file.write(f'{item}: {simplified_data[state_num][item]}\n')