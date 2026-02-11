 **NFA Simulator with λ-Transitions and Visual Trace**

**Overview**
This project implements a Non-Deterministic Finite Automaton (NFA) simulator with lambda (λ) transitions and provides a graphical visualization of the execution trace.
It allows users to define custom NFAs, input strings, and visually observe how the automaton processes the string step-by-step.

The simulator includes:

Support for λ-transitions (#)
Full execution trace visualization
Acceptance / rejection detection
Interactive GUI for user-friendly input

**Project Objectives**
Simulate NFA behavior including λ-transitions
Visualize state transitions dynamically
Understand nondeterministic computation
Enhance learning of automata theory concepts
Provide intuitive graphical trace output
**Core Concepts**
Non-Deterministic Finite Automata (NFA)
λ-transitions (epsilon transitions)
State transition tracing
Acceptance and rejection detection
Graph-based visualization of computation paths
**Simulation Logic**
The simulator processes the input string in layers:

Each layer represents a computation step.
All reachable states are computed.
λ-transitions are expanded recursively.
State connections are drawn dynamically.
The final layer is checked for the existence of at least one accepting state to determine whether the input is accepted.

**Graphical Visualization**
States are represented as nodes (circles).
Transitions are drawn as arrows.
λ-transitions are drawn using dashed red arrows.
Input steps are separated by horizontal layers.
Final result (ACCEPTED / REJECTED) is displayed clearly.
Accepted states in the final layer are highlighted.
**GUI Features**
Interactive NFA definition
Transition input field
Automatic validation
Built-in testing example
Visual trace rendering
Clear error handling
**File Structure**
nfa_simulator.py // NFA simulation logic, GUI, and visualization

**Input Format**
Alphabet
Space-separated symbols. Example: a b

Number of States
Single integer. Example: 4

Transitions
Each transition in the format: from_state symbol to_state

Use # to represent λ-transition.

Example: 0 a 0 0 b 0 0 b 1 1 a 2 1 # 2 2 b 3 3 a 3 3 b 3

Start States
Space-separated integers. Example: 0

Final States
Space-separated integers. Example: 3

Input String
Any string formed from the given alphabet. Example: ababba

**How to Run**
Install required libraries: pip install matplotlib

Run the simulator: python nfa_simulator.py

Use the GUI to:

Enter NFA details
Define transitions
Input the test string
Click Visualize Trace
Optionally click Testing Example to load a predefined example.
**Output**
Graphical trace showing:
State transitions
λ-transitions
Execution flow
Final result:
ACCEPTED (green)
REJECTED (red)
**Notes**
States must be numbered starting from 0.
λ-transitions are represented using #.
The simulator explores all possible paths simultaneously.
Visualization dynamically scales to fit all states.
**Learning Objectives**
Understand nondeterministic automata behavior
Visualize λ-closure expansion
Analyze state transition graphs
Gain hands-on experience with automata simulation
Strengthen theoretical understanding through visualization
🚀 Future Improvements
Support for DFA simulation
Step-by-step animation control
Export trace visualization as image
Highlight active states per step
Add regular expression to NFA conversion
