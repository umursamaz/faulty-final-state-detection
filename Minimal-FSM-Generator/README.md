# Minimal-FSM-Generator

*This is a work in progress*


## Important notes

The FSM.draw() function requires the package graphviz.

Check out [graphviz website](https://graphviz.gitlab.io/download/) and [pypi.org](https://pypi.org/project/graphviz/) for detailed information

You can use `pip install graphviz` but you also need to make sure that the executables of graphviz is in your **System Path**

## Functions for general usage

- **FSM(** *number of states*, *number of inputs*, *number of outputs* **)**
  - Initializes the finite state machine object with the given attributes

- FSM.**generate()**
  - Generates a random finite state machine.
  - Does not guarantee minimality
  
- FSM.**generateMinimal()**
  - Generates a random *minimal* finite state machine.
  
- FSM.**clear()**
  - Clears the FSM object
  - Cleared object can be used to create another random FSM

- FSM.**isMinimal()**
  - Applies a minimality check to the FSM object 
  - Returns True if the FSM is minimal, False otherwise
  
- FSM.**isMinimalGraph()**
  - Applies a graph based minimality check to the FSM object
  - Returns True if the FSM is minimal, False otherwise
  
- FSM.**isSurelyMinimal()**
  - Applies both minimality checks together.
  - Returns True if the FSM is minimal, False otherwise

- FSM.**generateRandomTrace(** *length=10*, *startNode=-1* **)**
  - Randomly moves on the FSM for *length* steps and generates a trace
  - Returns a *List* containing tuples in the form (input, output)
  - e.g `[(0, 0), (4, 1), (1, 0), (3, 1), (4, 0)]`
  - You can choose which node to start with startNode. If the node you choose is not valid or *-1 (default)*, chooses a random node.
  
- FSM.**show()**
  - Prints the nodes of FSM in a formatted way
  
- FSM.**draw(** *_filename="fsm"* *makePng=False* **)**
  - Uses the graphviz package to draw the graph.
  - The name of the generated file is *_filename.gv*
  - Default output (only output for now) is pdf
  - If makePng is True, will also try to create a png file
  
## Example use

```
from randomfsmgenerator import FSM

myFsm = FSM(10, 5, 2)

myFsm.generate()
myFsm.show()

myFsm.clear()

myFsm.generateMinimal()
if not myFsm.isSurelyMinimal():
  print("We have a big problem")
```
