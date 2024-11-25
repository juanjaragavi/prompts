"""
This module contains a script for converting data from an external file to a JSONL file.
"""

import pandas as pd
import jsonlines

# Load the data
data = pd.read_csv('your_data.csv')

# Convert the data to a list of dictionaries
data_dict = data.to_dict(orient='records')

# Write the data to a jsonl file
with jsonlines.open('output.jsonl', mode='w') as writer:
    writer.write_all(data_dict)
