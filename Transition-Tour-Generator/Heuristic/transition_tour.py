from collections import defaultdict

def read_fsm(file_path):
    with open(file_path, 'r') as f:
        f.readline()
        state_num, transition_num, input_num, output_num, seed = map(int, f.readline().strip().split(","))
        f.readline()

        def read_transitions(string):
            string = string.strip()
            try:
                return int(string)
            except:
                return string
        edges = [tuple(map(read_transitions, f.readline().strip().split(","))) for _ in range(transition_num)]
    return  state_num, transition_num, input_num, output_num, seed, edges

def append_fsm(file_path,  tour, input_seq, output_seq):
    with open(file_path, 'a') as f:
        f.write("transition_tour & input_sequence & output_sequence\n")
        f.write(", ".join(map(str, tour)) + "\n")
        f.write(", ".join(map(str, input_seq)) + "\n")
        f.wtite(", ".join(map(str, output_seq)) + "\n")

def write_fsm(file_path,  tour, input_seq, output_seq):
    with open(file_path, 'w') as f:
        f.write("transition_tour & input_sequence & output_sequence\n")
        f.write(", ".join(map(str, tour)) + "\n")
        f.write(", ".join(map(str, input_seq)) + "\n")
        f.write(", ".join(map(str, output_seq)) + "\n")


def transition_tour(n, transitions):
    # Create adjacency list
    graph = defaultdict(list)

    # Create state -> state -> output -> input map of all transitions
    graph_input_output = defaultdict(lambda: defaultdict(lambda: dict()))


    for u, v, input, output in transitions:
        # To consider possible transisitons between states input is
        graph[u].append((v, input))
        graph_input_output[u][v][input] = output

    # Create set of uncovered transitions
    # To consider possible multiple transitions between states, output is also added
    uncovered = set((u, v, input) for u, v, input, output in transitions)
    
    # Start from node 0 / can be any node
    current = 0
    path = [0]
    input_sequence = []
    output_sequence = []
    
    while uncovered:
        # Try to find an uncovered edge from the current node
        next_node = None
        next_input = None

        for neighbor, input in graph[current]:
            if (current, neighbor, input) in uncovered:
                next_node = neighbor
                next_input = input
                uncovered.remove((current, neighbor, input))
                break
        
        if next_node is not None:
            # Move to the next node
            input_sequence.append(next_input)
            output_sequence.append(graph_input_output[current][next_node][next_input])
            current = next_node
            path.append(current)
        else:
            # All transitions from current node are covered, try to reach a node with uncovered transitions
            
            temp_path, temp_inp_seq, temp_outp_seq = find_path_uncovered(graph, graph_input_output, uncovered, current)
            
            path.extend(temp_path[1:])
            input_sequence.extend(temp_inp_seq)
            output_sequence.extend(temp_outp_seq)
            current = temp_path[-1]
                

    # Complete the circuit by returning to the start
    if path[0] != path[-1]:
        temp_path, temp_inp_seq, temp_outp_seq = find_path(graph, graph_input_output, path[-1], path[0])
        if temp_path:
            path.extend(temp_path[1:])
            input_sequence.extend(temp_inp_seq)
            output_sequence.extend(temp_outp_seq)

    return path, input_sequence, output_sequence


def find_path(graph, graph_input_output, start, end):
    visited = set()
    # set of inputs and outputs are also recorded in addition to the path of states
    queue = [(start, [start], [], [])]

    while queue:
        (node, path, input_seq, output_seq) = queue.pop(0)

        if node == end:
            return path, input_seq, output_seq
        else:
            if node not in visited:
                visited.add(node)
                for neighbor, input in graph[node]:
                    if neighbor not in visited:
                        queue.append((neighbor, path + [neighbor], 
                        input_seq + [input], 
                        output_seq + [graph_input_output[node][neighbor][input]]))

    return None, None, None



def find_path_uncovered(graph, graph_input_output, uncovered, start):
    visited = set()
    # set of inputs and outputs are also recorded in addition to the path of states
    queue = [(start, [start], [], [])]
    
    while queue:
        (node, path, input_seq, output_seq) = queue.pop(0)

        if any((node, neighbor, input) in uncovered for neighbor, input in graph[node]):
            return path, input_seq, output_seq

        else:
            if node not in visited:
                visited.add(node)
                for neighbor, input in graph[node]:
                    if neighbor not in visited:
                        queue.append((neighbor, path + [neighbor], 
                        input_seq + [input], 
                        output_seq + [graph_input_output[node][neighbor][input]]))
        
    return None, None, None

if __name__ == "__main__":
    fsm_path = "../../examples/PURE2024/test_machines/128_states/test_machine_128_states_56_seed.csv"
    state_num, transition_num, input_num, output_num, seed, edges = read_fsm(fsm_path)

    tour, input_seq, output_seq = transition_tour(state_num, edges)
    print(len(tour))
    print("Transition Tour:")
    print(" -> ".join(map(str, tour)))

