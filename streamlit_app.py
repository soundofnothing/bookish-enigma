import streamlit as st
import ast
import networkx as nx
import matplotlib.pyplot as plt

# Function to convert AST to a directed graph
def ast_to_graph(node, graph=None, depth=2):
    if graph is None:
        graph = nx.DiGraph()

    if depth == 0:
        return graph

    node_id = id(node)
    label = get_node_label(node)
    graph.add_node(node_id, label=label)

    for child_node in ast.iter_child_nodes(node):
        child_id = id(child_node)
        graph.add_edge(node_id, child_id)
        ast_to_graph(child_node, graph, depth=depth-1)

    return graph

# Function to get a label for each node in the graph
def get_node_label(node):
    if isinstance(node, ast.FunctionDef):
        return f"Function: {node.name}"
    elif isinstance(node, ast.For):
        return "For Loop"
    elif isinstance(node, ast.While):
        return "While Loop"
    elif isinstance(node, ast.If):
        return "If Statement"
    elif isinstance(node, ast.BinOp):
        return "Binary Operation"
    else:
        return type(node).__name__

# Function to visualize the AST graph using Streamlit
def visualize_ast(code, depth=2):
    parsed_code = ast.parse(code)
    ast_graph = ast_to_graph(parsed_code, depth=depth)

    # Draw the graph using Matplotlib
    pos = nx.spring_layout(ast_graph)
    
    plt.figure(figsize=(10, 6))
    nx.draw(ast_graph, pos, with_labels=True, labels=get_node_labels(ast_graph), font_size=8, font_color="black", font_weight="bold", arrowsize=10)
    plt.show()

# Function to get node labels for the graph
def get_node_labels(graph):
    labels = {}
    for node in graph.nodes:
        labels[node] = str(graph.nodes[node].get('label', ''))
    return labels

# Streamlit UI
st.title("Euclidean Division Algorithm Analysis")

# Code input area
code_input = st.text_area("Enter Python code", """
def euclidean_division(a, b):
    while b != 0:
        a, b = b, a % b
    return a
""")

# Depth input area
depth_input = st.slider("Select AST Depth", min_value=1, max_value=5, value=2)

# Button to visualize the AST graph
if st.button("Visualize AST"):
    visualize_ast(code_input, depth=depth_input)
