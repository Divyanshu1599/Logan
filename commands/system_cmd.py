import platform
import psutil
import os
from datetime import datetime

def handle_system_command(text: str):
    """Retrieve and display system information."""
    info = {
        "OS": platform.system(),
        "OS Version": platform.version(),
        "Platform": platform.platform(),
        "Architecture": platform.machine(),
        "Processor": platform.processor(),
        "Python Version": platform.python_version(),
        "Hostname": platform.node(),
        "CPU Count": psutil.cpu_count(logical=False),
        "Total Memory": f"{psutil.virtual_memory().total / (1024**3):.2f} GB",
        "Available Memory": f"{psutil.virtual_memory().available / (1024**3):.2f} GB",
        "CPU Usage": f"{psutil.cpu_percent(interval=1)}%",
        "Disk Usage": f"{psutil.disk_usage('/').percent}%",
    }
    return info


def display_system_cmd():
    """Display formatted system information."""
    info = handle_system_command("")
    print("\n" + "="*40)
    print("SYSTEM INFORMATION")
    print("="*40)
    for key, value in info.items():
        print(f"{key:.<25} {value}")
    print("="*40 + "\n")


if __name__ == "__main__":
    display_system_cmd()