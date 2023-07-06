import subprocess
import json
import os
from InquirerPy import prompt
from datetime import date

filename = "journal_entries.json"

# Check if the JSON file exists
if os.path.exists(filename):
    # File exists, so read its contents
    with open(filename, "r") as file:
        data = json.load(file)
else:
    # File doesn't exist, so create it with an empty dictionary
    data = {}
    with open(filename, "w") as file:
        json.dump(data, file)

# Get today's date in ISO format (YYYY-MM-DD)
today = str(date.today())

# Fetch these to display them to the user
five_most_recent_keys = list(data.keys())[::-1][:5]

# Add the option to create a new entry
five_most_recent_keys.append("Create new entry")

# Display those options to the user in a terminal list
questions = [
    {
        "type": "list",
        "message": "Select an entry:",
        "choices": five_most_recent_keys,
        "name": "selected_key",
    },
]

# Fetch selection
answers = prompt(questions)
selected_entry = answers["selected_key"]

# If the user selected "Create new entry", create a new one for today
if selected_entry == "Create new entry":
    selected_entry = today
    if selected_entry not in data:
        print(f"No entry found for {today}. Creating new entry...")
        entry = ""
    else:
        print(f"Existing entry found for {today}. Modifying entry...")
        entry = data[selected_entry]["entry"]
else:
    print(f"Existing entry found for {selected_entry}. Modifying entry...")
    entry = data[selected_entry]["entry"]

# Create a temporary file to store the relevant text content
temp_filename = "temp.txt"

# Write the entry content to the temporary file
with open(temp_filename, "w") as file:
    file.write(entry)

# Open the temporary file in nano
subprocess.call(["nano", temp_filename])

# Read the updated entry from the temporary file
with open(temp_filename, "r") as file:
    updated_entry = file.read().strip()

# Update the entry in the data dictionary
data[selected_entry] = {"entry": updated_entry}

# Write the updated data back to the JSON file
with open(filename, "w") as file:
    json.dump(data, file, indent=4)

# Remove the temporary file
os.remove(temp_filename)

print("Entry updated and JSON file updated.")
