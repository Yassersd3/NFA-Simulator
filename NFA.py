import matplotlib.pyplot as plt
import matplotlib.patches as patches
from collections import defaultdict
import tkinter as tk
from tkinter import messagebox

transitions = defaultdict(lambda: defaultdict(set))

def addTransition(from_state, symbol, to_state):
    transitions[from_state][symbol].add(to_state)

def move(state, symbol):
    return transitions[state].get(symbol, set())

class TraceNode:
    def __init__(self, state, step=0):
        self.state = state
        self.step = step
        self.input_parents = []
        self.lambda_parents = []
        self.x = 0
        self.y = 0

def draw_nfa_input(alphabet, numberOfStates, startStates, finalStates, input_string):
    layers = []

    layer0 = {}
    for s in startStates:
        layer0[s] = TraceNode(s, 0)
    layers.append(layer0)

    def expand_lambdas_in_place(current_layer_dict):
        while True:
            changes_made = False
            current_states = list(current_layer_dict.values())
            for node in current_states:
                dests = move(node.state, "#")
                for d in dests:
                    if d not in current_layer_dict:
                        new_node = TraceNode(d, node.step)
                        current_layer_dict[d] = new_node
                        changes_made = True
                    target_node = current_layer_dict[d]
                    if node not in target_node.lambda_parents and node != target_node:
                        target_node.lambda_parents.append(node)
                        changes_made = True
            if not changes_made:
                break

    expand_lambdas_in_place(layers[0])

    for i, symbol in enumerate(input_string):
        current_layer_dict = layers[-1]
        next_layer_dict = {}
        
        for state_id, parent_node in current_layer_dict.items():
            dests = move(state_id, symbol)
            for d in dests:
                if d not in next_layer_dict:
                    next_layer_dict[d] = TraceNode(d, len(layers))
                next_layer_dict[d].input_parents.append(parent_node)
        
        layers.append(next_layer_dict)
        
        if not next_layer_dict:
            break
            
        expand_lambdas_in_place(layers[-1])

    Y_STEP = -2.5
    CIRCLE_RAD = 0.4
    
    all_nodes = []
    for step_idx, layer_dict in enumerate(layers):
        y = step_idx * Y_STEP
        for node in layer_dict.values():
            node.x = node.state * 2.5
            node.y = y
            all_nodes.append(node)

    if not all_nodes:
        min_x, max_x = 0, 5
        min_y, max_y = 0, 0
    else:
        min_x = min(n.x for n in all_nodes)
        max_x = max(n.x for n in all_nodes)
        min_y = min(n.y for n in all_nodes)
        max_y = max(n.y for n in all_nodes)

    padding_x = 2.0
    padding_y = 1.0
    
    plot_width = (max_x - min_x) + (padding_x * 2)
    plot_height = (max_y - min_y) + (padding_y * 2)
    fig_w = max(8, plot_width * 0.5)
    fig_h = max(6, abs(plot_height) * 0.5)

    fig, ax = plt.subplots(figsize=(fig_w, fig_h))
    ax.set_aspect('equal')
    ax.axis('off')
    
    left_limit = min_x - padding_x
    right_limit = max_x + padding_x
    ax.set_xlim(left_limit, right_limit)
    ax.set_ylim(min_y - padding_y - 1, max_y + padding_y)

    for i in range(len(input_string)):
        if i >= len(layers) - 1: break
        symbol = input_string[i]
        y_line = (i * Y_STEP) + (Y_STEP / 2)
        ax.plot([left_limit, right_limit], [y_line, y_line], color='black', linewidth=1, alpha=0.3)
        ax.text(left_limit + 0.5, y_line, symbol, fontsize=14, fontweight='bold', 
                va='center', ha='left', color='blue')

    for layer_dict in layers:
        for node in layer_dict.values():
            for parent in node.input_parents:
                ax.annotate("", 
                            xy=(node.x, node.y + CIRCLE_RAD + 0.1), 
                            xytext=(parent.x, parent.y - CIRCLE_RAD),
                            arrowprops=dict(arrowstyle="->", color="black", lw=1.5))
            for parent in node.lambda_parents:
                is_left_arrow = (node.state < parent.state)
                start_x = parent.x - CIRCLE_RAD if is_left_arrow else parent.x + CIRCLE_RAD
                end_x = node.x + CIRCLE_RAD if is_left_arrow else node.x - CIRCLE_RAD
                
                ax.annotate("", 
                            xy=(end_x, node.y), 
                            xytext=(start_x, parent.y),
                            arrowprops=dict(arrowstyle="->", color="red", lw=1.5, ls="--"))
                
                mid_x = (start_x + end_x) / 2
                ax.text(mid_x, node.y + 0.25, "λ", color="red", fontsize=10, fontweight='bold', ha='center')

    accepted_nodes = set()
    last_layer = layers[-1] if layers else {}
    
    if len(layers) == len(input_string) + 1:
        for n in last_layer.values():
            if n.state in finalStates:
                accepted_nodes.add(n)
    
    is_accepted = (len(accepted_nodes) > 0)

    for layer_dict in layers:
        for node in layer_dict.values():
            fill_color = 'white'
            edge_color = 'black'
            width = 1.5
            
            is_final = node.state in finalStates
            is_in_last_layer = (node in last_layer.values())

            if is_in_last_layer and is_final and is_accepted:
                fill_color = '#ccffcc'
                edge_color = 'green'
                width = 3.0
            elif is_final:
                width = 2.5

            circle = patches.Circle((node.x, node.y), CIRCLE_RAD, 
                                    edgecolor=edge_color, facecolor=fill_color, linewidth=width, zorder=10)
            ax.add_patch(circle)
            ax.text(node.x, node.y, str(node.state), 
                    ha='center', va='center', fontsize=12, fontweight='bold', zorder=11)

    final_y = (len(layers) - 1) * Y_STEP - 1.5
    res_text = "ACCEPTED" if is_accepted else "REJECTED"
    res_col = "green" if is_accepted else "red"
    
    center_x = (min_x + max_x) / 2
    ax.text(center_x, final_y, res_text, ha='center', fontsize=20, fontweight='bold', color=res_col)
    
    plt.title(f"Input: {input_string}", fontsize=16)
    plt.show()

class NFA_GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("NFA Simulator w/λ Transition")
        self.root.geometry("500x700")

        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Testing Example", command=self.load_example_1, bg="gray63").pack(side=tk.TOP, padx=5)

        tk.Label(root, text="Alphabet (Space Separated):").pack(anchor="w", padx=20)
        self.entry_alphabet = tk.Entry(root, width=50)
        self.entry_alphabet.pack(padx=20, pady=5)

        tk.Label(root, text="Number of States:").pack(anchor="w", padx=20)
        self.entry_num_states = tk.Entry(root, width=50)
        self.entry_num_states.pack(padx=20, pady=5)

        tk.Label(root, text="Transitions (Format: 0 a 1) (States start from 0 !):").pack(anchor="w", padx=20)
        tk.Label(root, text="(Use # for lambda. One per line)", font=("Arial", 8)).pack(anchor="w", padx=20)
        
        self.text_transitions = tk.Text(root, height=10, width=50)
        self.text_transitions.pack(padx=20, pady=5)

        tk.Label(root, text="Start States (Space Separated):").pack(anchor="w", padx=20)
        self.entry_start = tk.Entry(root, width=50)
        self.entry_start.pack(padx=20, pady=5)

        tk.Label(root, text="Final States (Space Separated):").pack(anchor="w", padx=20)
        self.entry_final = tk.Entry(root, width=50)
        self.entry_final.pack(padx=20, pady=5)

        tk.Label(root, text="Input String to Test:").pack(anchor="w", padx=20)
        self.entry_string = tk.Entry(root, width=50)
        self.entry_string.pack(padx=20, pady=5)

        tk.Button(root, text="Visualize Trace", command=self.run_simulation, bg="gray63", fg="black", font=("Arial", 12, "bold"), height=2).pack(pady=20, fill=tk.X, padx=20)

    def set_text(self, entry, text):
        entry.delete(0, tk.END)
        entry.insert(0, text)

    def load_example_1(self):
        self.set_text(self.entry_alphabet, "a b")
        self.set_text(self.entry_num_states, "4")
        self.set_text(self.entry_start, "0")
        self.set_text(self.entry_final, "3")
        self.set_text(self.entry_string, "ababba")
        self.text_transitions.delete("1.0", tk.END)
        self.text_transitions.insert(tk.END, "0 a 0\n0 b 0\n0 b 1\n1 a 2\n1 # 2\n2 b 3\n3 a 3\n3 b 3")

    def run_simulation(self):
        transitions.clear()
        
        try:
            alphabet = self.entry_alphabet.get().split()
            num_states = int(self.entry_num_states.get())
            start_states = set(map(int, self.entry_start.get().split()))
            final_states = set(map(int, self.entry_final.get().split()))
            input_str = self.entry_string.get()
            
            raw_trans = self.text_transitions.get("1.0", tk.END).strip().split('\n')
            
            for line in raw_trans:
                if not line.strip(): continue
                parts = line.split()
                if len(parts) != 3:
                    messagebox.showerror("Error", f"Invalid transition format: {line}")
                    return
                f, s, t = parts
                addTransition(int(f), s, int(t))

            draw_nfa_input(alphabet, num_states, start_states, final_states, input_str)
            
        except ValueError as e:
            messagebox.showerror("Error", "Please check your input (States must be numbers).")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = NFA_GUI(root)
    root.mainloop()
