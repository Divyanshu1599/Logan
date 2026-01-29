import psutil

def handle_battery_command(text: str):
    battery = psutil.sensors_battery()

    if battery is None:
        return "Battery information is not available on this system."

    percent = battery.percent
    plugged = battery.power_plugged

    if plugged:
        return f"Battery is at {percent} percent and charging."
    else:
        return f"Battery is at {percent} percent."
