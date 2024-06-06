"""
BGP Adjacency Creator

1) Take input list of .csv files
2) Identify a complete set of AS adjacencies
3) Export a .csv file
"""

# IMPORTS
import pandas as pd
import sys

# Inputs
FILES_IN = str(sys.argv[1]) # List of CSV files to process
ADJACENCY_OUT = str(sys.argv[2]) # Adjacency CSV output

print("Loading from", FILES_IN, "\nOutput to", ADJACENCY_OUT)

as_topology = set()

with open(FILES_IN, 'r') as f:
    files_list = f.readlines()

for file in files_list:
    # Each collector input
    print("Loading from", file.strip("\n"))

    file_data = pd.read_csv(file.strip("\n"), header=0, dtype=str)
    ases = file_data['as_path'].tolist()
    del file_data

    for path in ases:
        as_list = str(path).split(' ')
        for i in range(0, len(as_list) - 1):
            if (as_list[i] != as_list[i+1] and '{' not in as_list[i+1]):
                as_topology.add(tuple(sorted([as_list[i], as_list[i+1]])))

print("Creating topology list")
adjacency_list = list(as_topology)
adjacency_export = pd.DataFrame(adjacency_list)

print("Exporting")
adjacency_export.to_csv(ADJACENCY_OUT, index=False, header=False)

print("Completed")
