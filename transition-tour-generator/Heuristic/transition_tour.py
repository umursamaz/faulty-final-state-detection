from collections import defaultdict

def read_fsm(file_path):
    with open(file_path, 'r') as f:
        n = int(f.readline().strip())
        m = int(f.readline().strip())
        edges = [tuple(map(int, f.readline().strip().split())) for _ in range(m)]
    return n, m, edges

def transition_tour(n, edges):
    # Create adjacency list
    graph = defaultdict(list)
    for u, v, _ in edges:
        graph[u].append(v)
    
    # Create set of uncovered edges
    uncovered = set((u, v) for u, v, _ in edges)
    
    # Start from node 0 / can be any node
    current = 0
    path = [0]
    
    while uncovered:
        # Try to find an uncovered edge from the current node
        next_node = None
        for neighbor in graph[current]:
            if (current, neighbor) in uncovered:
                next_node = neighbor
                uncovered.remove((current, neighbor))
                break
        
        if next_node is not None:
            # Move to the next node
            current = next_node
            path.append(current)
        else:
            # All edges from current node are covered, try to reach a node with uncovered edges
            for node in range(n):
                if any((node, neighbor) in uncovered for neighbor in graph[node]):
                    # Find a path to this node
                    temp_path = find_path(graph, current, node)
                    if temp_path:
                        path.extend(temp_path[1:])
                        current = node
                        break
            else:
                # If can't reach any node with uncovered edges, break the loop
                break
    
    # Complete the circuit by returning to the start
    if path[0] != path[-1]:
        temp_path = find_path(graph, path[-1], path[0])
        if temp_path:
            path.extend(temp_path[1:])
    
    return path

def find_path(graph, start, end):
    visited = set()
    stack = [(start, [start])]
    
    while stack:
        (node, path) = stack.pop()
        if node not in visited:
            if node == end:
                return path
            visited.add(node)
            for neighbor in graph[node]:
                if neighbor not in visited:
                    stack.append((neighbor, path + [neighbor]))
    
    return None

# Main execution
file_path = 'fsm.txt'
n, m, edges = read_fsm(file_path)
tour = transition_tour(n, edges)

print("Transition Tour:")
print(" -> ".join(map(str, tour)))