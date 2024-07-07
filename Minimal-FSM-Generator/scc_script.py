import tarjan
import random
from randomfsmgenerator import FSM
print("\n\n\n\n")

def create_adj_list(graph):
    adj_list = {}
    
    for node in graph:
        adj_list[node.index] = []
        for transition in node.transitions:
            adj_list[node.index].append(transition[0].index)
    return adj_list

num_of_states  = 50
num_of_inputs  = 2
num_of_outputs = 2

myfsm = FSM(num_of_states, num_of_inputs, num_of_outputs)
myfsm.generateMinimal()

adj = create_adj_list(myfsm.nodes)
myfsm.show(True)
scc = tarjan.tarjan(adj)
scc = sorted(scc, key=len, reverse=True)
print("scc ->", scc)

# Start strongly connecting

# Check if there are multiple groups
# Find biggest group
# Try to connect all smaller groups to this one

loops = 0
operations = 0

while len(scc) != 1:
    print("Multiple groups, trying connections")
    loops += 1
    for i in range(1, len(scc)):
        rt = myfsm.get_reverse_transitions()
        group_node = scc[i][0]
        
        # Check reverse transitions of this node to see if there are any incoming transitions
        incoming = False
        for i in rt[group_node]:
            if i != group_node:
                incoming = True
        
        if not incoming:
            operations += 1
            # Choose a random node to connect to this one
            node_index = random.choice(scc[0])
            # Choose a random transition
            transition_index = random.randint(0, num_of_inputs-1)
            
            # Connect it back here
            myfsm.nodes[node_index].transitions[transition_index] = (myfsm.nodes[group_node], myfsm.nodes[node_index].transitions[transition_index][1])
            print("i Connected the", transition_index, "transition of", node_index, "to", group_node)
            
        outgoing = False
        for transition in myfsm.nodes[group_node].transitions:
            if transition[0].index != group_node:
                outgoing = True
        
        if not outgoing:
            operations += 1
            # Choose a random node to connect to this one
            node_index = random.choice(scc[0])
            # Choose a random transition
            transition_index = random.randint(0, num_of_inputs-1)
            
            myfsm.nodes[group_node].transitions[transition_index] = (myfsm.nodes[node_index], myfsm.nodes[group_node].transitions[transition_index][1])
            print("o Connected the", transition_index, "transition of", group_node, "to", node_index)
        
        if incoming and outgoing:
            operations += 1
            if random.randint(1, 2) == 1:
                node_index = random.choice(scc[0])
                # Choose a random transition
                transition_index = random.randint(0, num_of_inputs-1)
                
                # Connect it back here
                myfsm.nodes[node_index].transitions[transition_index] = (myfsm.nodes[group_node], myfsm.nodes[node_index].transitions[transition_index][1])
                print("ii Connected the", transition_index, "transition of", node_index, "to", group_node)
            else:
                # Choose a random node to connect to this one
                node_index = random.choice(scc[0])
                # Choose a random transition
                transition_index = random.randint(0, num_of_inputs-1)
                
                myfsm.nodes[group_node].transitions[transition_index] = (myfsm.nodes[node_index], myfsm.nodes[group_node].transitions[transition_index][1])
                print("oo Connected the", transition_index, "transition of", group_node, "to", node_index)
            
    adj = create_adj_list(myfsm.nodes)
    # myfsm.show()
    scc = tarjan.tarjan(adj)
    scc = sorted(scc, key=len, reverse=True)
    print("scc ->", scc)

print("Done!")
print("Loops ->", loops, " Operations ->", operations)
print("Is minimal =>", myfsm.isSurelyMinimal())
