import tarjan
from randomfsmgenerator import FSM


def create_adj_list(graph):
    adj_list = {}
    
    for node in graph:
        adj_list[node.index] = []
        for transition in node.transitions:
            adj_list[node.index].append(transition[0].index)
    return adj_list

num_of_states  = 100
num_of_inputs  = 2
num_of_outputs = 2

myfsm = FSM(num_of_states, num_of_inputs, num_of_outputs)
myfsm.generateMinimal()

adj = create_adj_list(myfsm.nodes)
# print(adj)
print()
scc = tarjan.tarjan(adj)
print(scc)