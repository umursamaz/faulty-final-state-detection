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


def transition_tour(n, edges):
    # Create adjacency list
    graph = defaultdict(list)

    # Create state -> state -> output -> input map of all transitions
    graph_input_output = defaultdict(lambda: defaultdict(lambda: dict()))


    for u, v, inp, outp in edges:
        # To consider possible edges between states, output is also added
        graph[u].append((v, outp))
        graph_input_output[u][v][outp] = inp

    # Create set of uncovered edges
    # To consider possible edges between states, output is also added
    uncovered = set((u, v, output) for u, v, input, output in edges)
    
    # Start from node 0 / can be any node
    current = 0
    path = [0]
    input_sequence = []
    output_sequence = []
    
    while uncovered:
        
        # Try to find an uncovered edge from the current node
        next_node = None
        next_output = None

        for neighbor, output in graph[current]:
            if (current, neighbor, output) in uncovered:
                next_node = neighbor
                next_output = output
                uncovered.remove((current, neighbor, output))
                break
        
        if next_node is not None:
            # Move to the next node
            input_sequence.append(graph_input_output[current][next_node][next_output])
            output_sequence.append(next_output)
            current = next_node
            path.append(current)
        else:
            # All edges from current node are covered, try to reach a node with uncovered edges
            for node in range(n):
                if any((node, neighbor, output) in uncovered for neighbor, output in graph[node]):
                    # Find a path to this node
                    temp_path, temp_inp_seq, temp_outp_seq = find_path(graph, graph_input_output, current, node)
                    if temp_path:
                        path.extend(temp_path[1:])
                        input_sequence.extend(temp_inp_seq)
                        output_sequence.extend(temp_outp_seq)
                        current = node
                        break
            else:
                # If can't reach any node with uncovered edges, break the loop
                break
    
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
    stack = [(start, [start], [], [])]
    
    while stack:
        (node, path, input_seq, output_seq) = stack.pop()
        if node not in visited:
            if node == end:
                return path, input_seq, output_seq
            visited.add(node)
            for neighbor, output in graph[node]:
                if neighbor not in visited:
                    stack.append((neighbor, path + [neighbor], 
                    input_seq + [graph_input_output[node][neighbor][output]], 
                    output_seq + [output]))
    
    return None, None, None


