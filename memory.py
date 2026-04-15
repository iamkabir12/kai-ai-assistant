import json
import os

MEMORY_FILE = "memory.json"

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "w") as f:
            json.dump({"name": "", "preferences": {}, "reminders": []}, f)

    with open(MEMORY_FILE, "r") as f:
        return json.load(f)

def save_memory(data):
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=4)

def set_name(name):
    data = load_memory()
    data["name"] = name
    save_memory(data)

def get_name():
    return load_memory().get("name", "")

def set_preference(key, value):
    data = load_memory()
    data["preferences"][key] = value
    save_memory(data)

def get_preference(key):
    return load_memory()["preferences"].get(key, None)

def add_reminder(text, time):
    data = load_memory()
    data["reminders"].append({"text": text, "time": time})
    save_memory(data)

def get_reminders():
    return load_memory()["reminders"]