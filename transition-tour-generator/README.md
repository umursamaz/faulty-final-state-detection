This repository contains a Python implementation of exact and heuristic transition tour algorithms for strongly connected finite state machines (FSMs).

# TT/CPT Generation for FSM

## Overview

TT/CPT-Method for minimizing the length of $TT$ (Transition Tour) in the context of the Chinese Postman Problem (CPP). The goal is to find a minimum-cost tour that traverses every edge in a directed graph (digraph) at least once.

When dealing with a strongly connected digraph $G(V, E)$ representing a Finite State Machine $FSM(M)$, the objective is to minimize the length of $TT$ for $M$. This reduction can be achieved by finding a CPT of $G$.

### Symmetric Graphs

If $G$ is symmetric, the problem simplifies to finding an Euler tour of $G$. The condition for $G$ to contain an Euler tour is that it must be strongly connected and symmetric.

### Non-Symmetric Graphs

In cases where $G$ is not symmetric, every edge $e \in E$ must be included at least once, potentially more, in a minimal-cost tour. Finding a CPT of $G$ involves:

- Constructing a symmetric augmentation $G'$ of $G$, ensuring $G'$ is symmetric and strongly connected with minimal replicated edges.
- Finding an Euler tour of $G'$, which serves as a CPT for $G$.

## A Non-optimized Approach

The algorithm generates a tour that covers all transitions (edges) in a given FSM, starting from an initial state and forming a path that visits all edges at least once. It uses a heuristic approach to prioritize uncovered edges and completes the tour by returning to the starting state.

## Features

- Reads FSM structure from a text file
- Implements a heuristic transition tour algorithm
- Handles strongly connected FSMs
- Outputs the transition tour as a sequence of states

## Usage

1. Ensure you have Python 3.x installed on your system.
2. Clone this repository.
3. Prepare your FSM input file (e.g., `fsm.txt`) in the following format:

n
m
u1 v1 c1
u2 v2 c2
...
um vm cm

Where:
- `n` is the number of vertices
- `m` is the number of edges
- Each subsequent line represents an edge with its start vertex (`u`), end vertex (`v`), and cost (`c`)
- For the same vertex each consecutive edge corresponds to an input of FSM

4. Run the script: `python transition_tour.py`
5. The algorithm will output the transition tour as a sequence of states.

## Input File Format

The first line contains the number of vertices $(n)$.
The second line contains the number of edges $(m)$.
Each of the next $m$ lines contains three integers $u$, $v$, and $c$, representing an edge from vertex $u$ to vertex $v$ with cost $c$.

## Limitations

- The algorithm uses a heuristic approach and may not always find the optimal tour.
- It assumes the input FSM is strongly connected.

## Contributing

Contributions, issues, and feature requests are welcome. Feel free to check [issues page](https://github.com/kgnakbas/transition-tour-generator-fsm/issues) if you want to contribute.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.