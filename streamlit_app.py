import streamlit as st
import ast
import networkx as nx
import matplotlib.pyplot as plt
from pygraphviz import AGraph

# Function to convert AST to a directed graph
def ast_to_graph(node, graph=None):
    if graph is None:
        graph = nx.DiGraph()

    graph.add_node(id(node), label=get_node_label(node))

    for child_node in ast.iter_child_nodes(node):
        graph.add_edge(id(node), id(child_node))
        ast_to_graph(child_node, graph)

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
def visualize_ast(code):
    parsed_code = ast.parse(code)
    ast_graph = ast_to_graph(parsed_code)

    # Generate DOT format string using pygraphviz
    dot = AGraph(directed=True)
    for node in ast_graph.nodes:
        dot.add_node(node, label=str(ast_graph.nodes[node]['label']))

    for edge in ast_graph.edges:
        dot.add_edge(edge[0], edge[1])

    # Save the DOT string to a PNG file
    dot_path = "ast_graph"
    dot.layout(prog="dot")
    dot.draw(f"{dot_path}.png", format="png")

    # Display the PNG image using Streamlit
    st.image(f"{dot_path}.png")

# Streamlit UI
st.title("Euclidean Division Algorithm Analysis")

# Code input area
code_input = st.text_area("Enter Python code", """
def euclidean_division(a, b):
    while b != 0:
        a, b = b, a % b
    return a
""")

# Button to visualize the AST graph
if st.button("Visualize AST"):
    visualize_ast(code_input)
