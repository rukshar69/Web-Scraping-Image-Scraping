import json

# Replace 'data.json' with the actual path to your JSON file
json_file_path = 'o.json'

# Read the JSON file
with open(json_file_path, 'r') as json_file:
    data = json.load(json_file)

# Check the number of dictionaries in the list
number_of_dictionaries = len(data)

print("Number of dictionaries:", number_of_dictionaries)
