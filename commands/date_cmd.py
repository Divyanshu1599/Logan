from datetime import datetime

def handle_date_command(text: str):
    """Handles the date command by returning the current date and time."""
    now = datetime.now()
    date_str = now.strftime("%A, %B %d, %Y")
    time_str = now.strftime("%I:%M %p")
    return f"Today is {date_str} and the current time is {time_str}."