from core.memory_sqlite import get_memory, fetch_memory

def normalize_key(raw_key: str) -> str:
    raw_key = raw_key.strip().lower()
    raw_key = raw_key.replace("my ", "")
    return raw_key

def handle_memory_command(text: str):
    text = text.lower()

    # remember my name is divyanshu
    if text.startswith("remember") and "is" in text: 
        try:
            key_part, value = text.split(" is", 1)
            key = key_part.replace("remember", "").strip()
            key = normalize_key(key)
            get_memory(key, value)
            return f"Okay, I will remember that your {key} is {value}."
        except Exception:
            return "Sorry, I couldn't understand what to remember."
        
    # what is my name
    if text.startswith("what is my"):
        key = text.replace("what is my", "").strip()
        key = normalize_key(key)
        value = fetch_memory(key)
        if value:
            return f"Your {key} is {value}."
        else:
            return f"I don't have any memory of your {key}."    
        
    return None