import os
import subprocess
import platform

# Directories
FSM_GENERATOR_DIR = "./Minimal-FSM-Generator"
CPP_BINARY_DIR = "build"
EXAMPLES_DIR = "examples"

# File name
FSM_FILE = "new_example.dot"
OUTPUT_FILE = "ads_sequence.txt"

# Function to run a command in WSL
def run_in_wsl(command):
    return subprocess.run(["wsl", "bash", "-c", command], capture_output=True, text=True)

# Convert Windows path to WSL path
def convert_to_wsl_path(path):
    return subprocess.run(["wsl", "wslpath", "-a", path], capture_output=True, text=True).stdout.strip()

# Step 1: Generate FSM Example
print("Generating FSM...")
os.chdir(FSM_GENERATOR_DIR)
subprocess.run(["python", "main.py"])
os.chdir("..")

# Check if the FSM file was generated
fsm_file_path = os.path.join(EXAMPLES_DIR, FSM_FILE)
if not os.path.exists(fsm_file_path):
    print(f"Error: FSM file '{fsm_file_path}' not found.")
    exit(1)

# Step 2: Change directory to build and run the C++ program
print("Running C++ program to get ADS sequences...")

# Construct the command
cpp_executable = "./main"
command = f"{cpp_executable} -m fixed -f ../{EXAMPLES_DIR}/{FSM_FILE}"

# Print debug information
print(f"Running command: {command}")

# Run the command using WSL on Windows or directly on Linux
if platform.system() == "Windows":
    # Convert paths to WSL paths
    wsl_cpp_binary_dir = convert_to_wsl_path(CPP_BINARY_DIR)
    wsl_examples_dir = convert_to_wsl_path(EXAMPLES_DIR)
    wsl_fsm_file_path = convert_to_wsl_path(fsm_file_path)
    wsl_output_file_path = convert_to_wsl_path(os.path.join(CPP_BINARY_DIR, OUTPUT_FILE))
    
    full_command = f"cd {wsl_cpp_binary_dir} && {command}"
    print(full_command)
    result = run_in_wsl(full_command)
else:
    os.chdir(CPP_BINARY_DIR)
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    os.chdir("..")

# Print the command output for debugging
print("Command output:", result.stdout)
print("Command errors:", result.stderr)


if os.path.exists(OUTPUT_FILE):
    print(f"Success: Output file '{OUTPUT_FILE}' was generated.")
else:
    print(f"Error: Output file '{OUTPUT_FILE}' was not generated.")

print("Process completed.")
