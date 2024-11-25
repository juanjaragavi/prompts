import json

# Step 2: Prepare your data
# This is a list of dictionaries, where each dictionary represents a single record
data = [
    {"text": "This is the first record.", "label": "Positive"},
    {"text": "This is the second record.", "label": "Negative"},
    # Add more records as needed
]

# Step 3: Open a file for writing
with open('data.jsonl', 'w', encoding='utf-8') as outfile:
    # Step 4: Write JSON data to the file
    for entry in data:
        json.dump(entry, outfile)
        outfile.write('\n')

# Step 5: The file is automatically closed when you exit the 'with' block

