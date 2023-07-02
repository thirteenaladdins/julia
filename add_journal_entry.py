import subprocess
import json
import os
from datetime import date

filename = "journal_entries.json"

# Check if the JSON file exists
if os.path.exists(filename):
    # File exists, so read its contents
    with open(filename, "r") as file:
        data = json.load(file)
    print("File exists. Contents:")
    print(data)
else:
    # File doesn't exist, so create it with an empty dictionary
    data = {}
    with open(filename, "w") as file:
        json.dump(data, file)
    print("File created with initial data.")

# Get today's date in ISO format (YYYY-MM-DD)
today = str(date.today())

# Check if today's entry already exists
if today in data:
    print(f"Existing entry found for {today}. Modifying entry...")
    entry = data[today]["entry"]
else:
    print(f"No entry found for {today}. Creating new entry...")
    entry = "New entry"

# Create a temporary file to store the relevant JSON content
temp_filename = "temp.txt"  # changing from json to txt, nano is better for text editing

# Write the entry content to the temporary file
with open(temp_filename, "w") as file:
    file.write(entry)  # writing entry string, not JSON data

# Open the temporary file in nano
subprocess.call(["nano", temp_filename])

# Read the updated entry from the temporary file
with open(temp_filename, "r") as file:
    updated_entry = file.read().strip()  # reading entry string, not JSON data

# Update the entry in the data dictionary
data[today] = {"entry": updated_entry}

# Write the updated data back to the JSON file
with open(filename, "w") as file:
    json.dump(data, file, indent=4)

# Remove the temporary file
os.remove(temp_filename)

print("Entry updated and JSON file updated.")
