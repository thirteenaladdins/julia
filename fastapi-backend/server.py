from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import uvicorn
from datetime import date
import os

app = FastAPI()

# Configure CORS settings
origins = [
    "http://localhost:5173",  # Allow Svelte app to access the API.
    # Add any other origins that need to access the API.
    # "*" would mean all origins are allowed but it's not recommended for security reasons.
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods.
    allow_headers=["*"],  # Allows all headers.
)

class Entry(BaseModel):
    date: str
    entry: str

@app.get("/journal")
async def read_entries():
    if os.path.exists('data/journal_entries.json'):
        with open('data/journal_entries.json', 'r') as file:
            data = json.load(file)
            return data
    else:
        return {"message": "No entries found"}

@app.get("/journal/{entry_date}")
async def read_entry(entry_date: str):
    with open('data/journal_entries.json', 'r') as file:
        data = json.load(file)
        if entry_date in data:
            return data[entry_date]
        else:
            return {"message": f"No entry found for date {entry_date}"}

@app.post("/journal")
async def create_entry(entry: Entry):
    new_entry = entry.dict()
    if os.path.exists('data/journal_entries.json'):
        with open('journal_entries.json', 'r') as file:
            data = json.load(file)
    else:
        data = {}
    data[new_entry['date']] = new_entry['entry']
    with open('data/journal_entries.json', 'w') as file:
        json.dump(data, file, indent=4)
    return new_entry

@app.post("/journal/{entry_date}")
async def create_entry(entry_date: str, entry: Entry):
    with open('data/journal_entries.json', 'r') as file:
        data = json.load(file)
        
        # Check if entry for this date already exists
        if entry_date in data:
            return {"message": f"Entry for date {entry_date} already exists"}
        
        # If not, create new entry
        data[entry_date] = entry.dict()['entry']
        with open('data/journal_entries.json', 'w') as file:
            json.dump(data, file, indent=4)
        return {entry_date: data[entry_date]}


@app.put("/journal/{entry_date}")
async def update_entry(entry_date: str, entry: Entry):
    with open('data/journal_entries.json', 'r') as file:
        data = json.load(file)
        if entry_date in data:
            data[entry_date] = entry.dict()['entry']
            with open('data/journal_entries.json', 'w') as file:
                json.dump(data, file, indent=4)
            return {entry_date: data[entry_date]}
        else:
            return {"message": f"No entry found for date {entry_date}"}

if __name__ == "__main__":
    # os.system("uvicorn server:app --host 0.0.0.0 --port 8001 --reload")
    uvicorn.run("server:app", host="0.0.0.0", port=8001, reload=True)
