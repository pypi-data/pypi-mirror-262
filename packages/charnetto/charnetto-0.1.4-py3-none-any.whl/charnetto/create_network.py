from collections import Counter
import networkx as nx
import json
import numpy as np


def create_graph(char_list, pairs):
    """Generate a weighted networkx graph"""
    G = nx.Graph()
    G.add_nodes_from(char_list)
    G.add_weighted_edges_from(pairs)
    return G


def create_charnet(pairs, min_pairs, alias_df=None, char_list=None):
    """Create a character network based on a list of pairs.

    The pairs represent cooccurrences within the text, and
    a threshold can be fixed to ensure each cooccurrence
    appears at least min_pairs times.
    
    If no list of characters is provided, the nodes will be deduced
    from the list of pairs (thus ignoring characters whose number of 
    cooccurrences is below the threshold).
    
    If desired, a dataframe of occurrences can be provided: the weight
    of each node will then be computed based on the total number of 
    occurrences of the related character, and added as a node attribute 'weight'.

    Parameters
    ----------
    pairs: list of lists
        The list of cooccurrences between two characters.
    min_pairs: int
        Threshold for minimum amount of occurrences of the same pair.
    alias_df: pandas.DataFrame
        (optional) The dataframe of all named entities occurrences, already mapped
        with the list of characters. Must contain a column labeled 'alias'
    char_list: list
        (optional) The clean list of all desired characters.
    """
    pairs = [sorted(pair) for pair in pairs]
    counter = Counter(map(tuple, pairs))

    char_nodes = []
    triplets = []
    
    for (a, b), value in counter.items():
        if value >= min_pairs:
            triplet = a, b, value
            triplets.append(triplet)
            char_nodes.append(a)
            char_nodes.append(b)
    char_nodes = np.unique(char_nodes)
    
    #use char_list if provided, allowing for nodes without edges
    if char_list:
        char_nodes = char_list
    
    G = create_graph(char_nodes, triplets)                
    
    #add weight of nodes if alias_df profided
    if alias_df is not None:
        weights = dict()
        for node in G.nodes():
            weight = alias_df['alias'].value_counts()[node]
            weights[node] = weight
        nx.set_node_attributes(G, weights, name="weight")  

    return G
