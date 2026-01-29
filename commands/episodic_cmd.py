from core.episodic_memory import (get_recent_events, get_events_today, get_events_since)

def handle_episodic_command(text: str):
    text = text.lower().strip()

    # --Today--
    if "today" in text:
        events = get_events_today()
        label = "Events from Today"

    # --Recent (last few hours)--
    elif "recent" in text or "lately" in text:
        events = get_events_since(6)  # Last 6 hours
        label = "Recent Events (Last 6 Hours)"

    # --last night--
    elif "last night" in text:
        events = get_events_since(12)  # Last 12 hours
        label = "Events from Last Night"

    # --generic--
    elif text in ["what did i do", "what have i done", "show my activities"]:
        events = get_recent_events(5)
        label = "Recent activities"

    else:
        return None
    
    if not events:
        return f"No episodic events found for: {label}"
    
    response = f"Here is what you did {label}:\n"
    for _, details, timestamp in events:
        response += f"- {details} at {timestamp}\n"

    return response

