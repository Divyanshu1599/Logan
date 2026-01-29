from datetime import datetime

def handle_time_command(text:str):
    now = datetime.now().strftime("%I:%M %P")
    return f"The time is {now}"

