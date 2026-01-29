import json
import os

MEMORY_FILE = "memory.json"

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {}
    with open(MEMORY_FILE, "r") as f:
        return json.load(f)
    
def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)

def get_memory(key: str, value: str):
    memory = load_memory()
    memory[key] = value
    save_memory(memory)

def fetch_memory(key: str):
    memory = load_memory()
    return memory.get(key)
