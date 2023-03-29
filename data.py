import psutil
import time
import sys
import datetime
import subprocess
import psutil
import tkinter as tk
from rich.console import Console



console = Console()

root = tk.Tk()
root.overrideredirect(True)


# Create a label to display the network usage
label = tk.Label(root, text="", font=("Arial", 12), bg="black", fg="white")
label.pack()

# Place the window in the top left corner of the screen
root.geometry("+0+0")


# Get the initial network usage statistics
net_io_counters = psutil.net_io_counters()
bytes_sent_start = net_io_counters.bytes_sent
bytes_recv_start = net_io_counters.bytes_recv

# Load the total data usage from the file
total_data_used_today = 0
date_today = datetime.datetime.now().date()
try:
    with open("total_data_usage.txt", "r") as file:
        line = file.readline().strip()
        if line:
            saved_date_str, total_data_str = line.split(",")
            saved_date = datetime.datetime.strptime(saved_date_str, "%Y-%m-%d").date()
            if saved_date == date_today:
                total_data_used_today = float(total_data_str)
except FileNotFoundError:
    pass

# Loop indefinitely to display network usage in real-time
while True:
    # Get the current network usage statistics
    net_io_counters = psutil.net_io_counters()
    bytes_sent = net_io_counters.bytes_sent - bytes_sent_start
    bytes_recv = net_io_counters.bytes_recv - bytes_recv_start

    # Convert bytes to megabytes
    mb_sent = bytes_sent / 1000000
    mb_recv = bytes_recv / 1000000

    # Calculate the total data used today
    total_data_used_today += mb_sent + mb_recv

    # Clear any extra text from the screen
    result = subprocess.run(['clear'], stdout=subprocess.PIPE)

    # Save the total data usage to the file
    with open("total_data_usage.txt", "w") as file:
        file.write(f"{date_today},{total_data_used_today}")

    # Print the current network usage statistics and the total data used today to the terminal
    print(result.stdout.decode('utf-8'))

    

    # Write the rich text object and the rest of the text to the terminal
    label.config(text=f"Sent: {mb_sent:.2f} MB | Received: {mb_recv:.2f} MB ")

    # Update the window
    root.update()
    # Wait for one second before updating again
    time.sleep(1)





