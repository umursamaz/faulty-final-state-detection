import matplotlib.pyplot as plt
from mpl_toolkits.axisartist.axislines import AxesZero

# Set Times New Roman as the default font and make it bold
plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams["font.weight"] = "bold"

# Set the global font size
plt.rcParams["font.size"] = 13

# Path to the text file
file_path = 'fsm_results.txt'

# Function to read data from the text file
def read_fsm_data(file_path):
    data = {}
    with open(file_path, 'r') as file:
        lines = file.readlines()
        current_state_num = None
        for line in lines:
            if "State number" in line:
                current_state_num = int(line.split(":")[1].strip())
                data[current_state_num] = {}
            elif current_state_num is not None:
                key, value = line.split(":")
                data[current_state_num][key.strip()] = float(value.strip())
    return data

# Read the data
fsm_data = read_fsm_data(file_path)

# Extract state numbers
state_nums = sorted(fsm_data.keys())

# Extract values for plotting
num_singletons = [fsm_data[state]['num_singletons'] for state in state_nums]
num_non_singletons = [fsm_data[state]['num_non_singletons'] for state in state_nums]
perc_non_singletons = [fsm_data[state]['percantage_of_non_singletons'] for state in state_nums]
perc_singletons = [100 - perc for perc in perc_non_singletons]
avg_suspected_states = [fsm_data[state]['average_suspected_states'] for state in state_nums]
avg_applied_inputs_len = [fsm_data[state]['average_applied_inputs_length'] for state in state_nums]
ratio_input_to_state = [fsm_data[state]['ratio_of_average_applied_inputs_length_to_state_num'] for state in state_nums]

def annotate_points(state_nums, values, offset=(0,10)):
    for i, txt in enumerate(values):
        plt.annotate(f'({state_nums[i]}, {txt:.2f})',
                     (state_nums[i], values[i]), 
                     textcoords="offset points", 
                     xytext=offset, 
                     ha='center')

def remove_spines():
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['top'].set_visible(False)


# Graph 1: Percentage of Singletons
# Create figure and AxesZero for arrowed axes
fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot(axes_class=AxesZero)

# Customize the axes with arrows
for direction in ["left", "bottom"]:
    ax.axis[direction].set_axisline_style("-|>")  

# Hide the other spines (axes lines)
for direction in ["right", "top"]:
    ax.axis[direction].set_visible(False)

# Plot your data
ax.plot(state_nums, perc_singletons, marker='o', color='r')
ax.set_xlabel('State Number', fontweight='bold', fontsize=13)
ax.set_ylabel('Percentage (%)', fontweight='heavy', fontsize=13)
ax.set_title('Percentage of Singletons', fontweight='bold', fontsize=20)
ax.set_xlim(0, 130)
ax.set_ylim(60, 81)

# Annotate points
annotate_points(state_nums, perc_singletons)

# Show the plot
plt.show()


# Graph 2: Average Suspected States
# Create figure and AxesZero for arrowed axes
fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot(axes_class=AxesZero)

# Customize the axes with arrows
for direction in ["left", "bottom"]:
    ax.axis[direction].set_axisline_style("-|>")  

# Hide the other spines (axes lines)
for direction in ["right", "top"]:
    ax.axis[direction].set_visible(False)

# Plot your data
ax.plot(state_nums, avg_suspected_states, marker='o', color='g')
ax.set_xlabel('State Number', fontweight='bold', fontsize=13)
ax.set_ylabel('Average Suspected States For Non-Singletons', fontweight='bold', fontsize=13)
ax.set_title('Average Suspected States For Non-Singletons vs. State Number', fontweight='bold', fontsize=20)
ax.set_xlim(0, 130)
ax.set_ylim(2, 3.1)

# Annotate points
annotate_points(state_nums, avg_suspected_states)

# Show the plot
plt.show()


# Graph 3: Ratio of Average Applied Inputs Length to State Number
# Create figure and AxesZero for arrowed axes
fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot(axes_class=AxesZero)

# Customize the axes with arrows
for direction in ["left", "bottom"]:
    ax.axis[direction].set_axisline_style("-|>")  

# Hide the other spines (axes lines)
for direction in ["right", "top"]:
    ax.axis[direction].set_visible(False)

# Plot your data
ax.plot(state_nums, ratio_input_to_state, marker='o', color='purple')
ax.set_xlabel('State Number', fontweight='bold', fontsize=13)
ax.set_ylabel('Ratio', fontweight='bold', fontsize=13)
ax.set_title('Ratio of Average Applied Inputs Length to State Number', fontweight='bold', fontsize=20)
ax.set_xlim(0, max(state_nums) * 1.05)
ax.set_ylim(0, 1)

# Annotate points
annotate_points(state_nums, ratio_input_to_state)

# Show the plot
plt.show()