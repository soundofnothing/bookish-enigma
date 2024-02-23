import streamlit as st
import ast
import networkx as nx
import matplotlib.pyplot as plt
from streamlit import GraphvizChart

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

    # Visualize the graph using Streamlit
    st.graphviz_chart(nx.drawing.nx_pydot.to_pydot(ast_graph).to_string())

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
