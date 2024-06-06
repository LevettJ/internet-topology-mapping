import networkx as nx, pandas as pd, gc
import numpy as np
from itertools import groupby, chain
from ast import literal_eval
import sys

# Input/output
ADJ_INPUT = str(sys.argv[1]) # Adjacencies as CSV
TIMESTAMP = str(sys.argv[2]) # Timestamp for nodes
COUNTRY_DATA = str(sys.argv[3]) # Country data as CSV
GRAPH_OUT = str(sys.argv[4]) # Output GEXF
GRAPH_OUT_ML = str(sys.argv[5]) # Output GRAPHML

print("Input:", ADJ_INPUT, "| Output:", GRAPH_OUT)

# Get a list of adjacencies
with open(ADJ_INPUT, 'r') as f:
    adjacencies = f.read().splitlines()

# Create adjacencies graph
G = nx.Graph()
for peers in adjacencies:
    peers = peers.split(',')
    nx.add_star(G, peers)

# Import and clean metadata
country_data = pd.read_csv(
    COUNTRY_DATA,
    names=[
        'country_code',
        'country_name',
        'avg_long',
        'avg_lat',
        'colour',
        'asn'],
    skiprows=1)
country_data['asn'] = country_data['asn'].replace(np.nan, '[]')
country_data = country_data.replace(np.nan, '')

# Convert from string of resources to usable list of ASN integers
country_data['asn'] = country_data['asn'].apply(literal_eval).apply(lambda x: [int(i) for i in x])

# Explode such that the list is code<->ASN pairs
country_data = country_data.explode('asn')

# Set blank node attributes, to be updated later
nx.set_node_attributes(G, '', 'country_code')
nx.set_node_attributes(G, '', 'country_name')
nx.set_node_attributes(G, '', 'avg_long')
nx.set_node_attributes(G, '', 'avg_lat')
nx.set_node_attributes(G, '', 'colour')

# Set common node attributes
nx.set_node_attributes(G, TIMESTAMP, 'timestamp')

# Set common edge attributes
nx.set_edge_attributes(G, TIMESTAMP, 'timestamp')

# Add metadata for each node
for asn in G.nodes():
    try:
        country_code = country_data.loc[country_data['asn'] == int(asn)]['country_code'].values[0]
        country_name = country_data.loc[country_data['asn'] == int(asn)]['country_name'].values[0]
        avg_long = country_data.loc[country_data['asn'] == int(asn)]['avg_long'].values[0]
        avg_lat = country_data.loc[country_data['asn'] == int(asn)]['avg_lat'].values[0]
        colour = country_data.loc[country_data['asn'] == int(asn)]['colour'].values[0]
        G.nodes[asn]['country_code'] = country_code
        G.nodes[asn]['country_name'] = country_name
        G.nodes[asn]['avg_long'] = avg_long
        G.nodes[asn]['avg_lat'] = avg_lat
        G.nodes[asn]['colour'] = colour
    except:
        print("Error:", asn)

nx.write_gexf(G, GRAPH_OUT)
print(".GEXF")

nx.write_graphml(G, GRAPH_OUT_ML)
print(".GRAPHML")

