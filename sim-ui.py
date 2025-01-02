import tkinter as tk
from tkinter import ttk
import re
import time

# Function to parse the log file
def parse_log(file_path):
    events = []
    with open(file_path, "r") as log_file:
        lines = log_file.readlines()

    current_time = None
    for line in lines:
        # Extract current time
        time_match = re.search(r"Current Time:\s+([\d.]+)", line)
        if time_match:
            current_time = float(time_match.group(1))
            continue

        # Extract model events (e.g., transitions, outputs)
        if "TRANSITION" in line or "Received data" in line or "Sending" in line:
            events.append((current_time, line.strip()))
    
    return events

# Function to update the UI based on selected time
def display_event(event_listbox, event_details, events):
    selected_index = event_listbox.curselection()
    if not selected_index:
        return
    selected_index = selected_index[0]
    current_event = events[selected_index]
    event_details.config(state="normal")
    event_details.delete(1.0, tk.END)
    event_details.insert(tk.END, f"Time: {current_event[0]}\nEvent: {current_event[1]}")
    event_details.config(state="disabled")

# Main UI
def create_ui(events):
    root = tk.Tk()
    root.title("Simulation Log Viewer")
    root.geometry("800x600")

    # Frame for the timeline and details
    timeline_frame = ttk.Frame(root)
    timeline_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Event Timeline (Listbox)
    event_listbox = tk.Listbox(timeline_frame, width=40)
    event_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Scrollbar for the timeline
    scrollbar = ttk.Scrollbar(timeline_frame, orient=tk.VERTICAL, command=event_listbox.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    event_listbox.config(yscrollcommand=scrollbar.set)

    # Populate the timeline with events
    for time, event in events:
        event_listbox.insert(tk.END, f"Time {time:.2f}: {event}")

    # Event Details
    event_details = tk.Text(root, state="disabled", wrap="word", height=15)
    event_details.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    # Bind event selection
    event_listbox.bind(
        "<<ListboxSelect>>", lambda e: display_event(event_listbox, event_details, events)
    )

    # Diagram canvas for system visualization (placeholder)
    diagram_frame = ttk.Frame(root)
    diagram_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    diagram_label = ttk.Label(diagram_frame, text="System Diagram Placeholder", anchor="center")
    diagram_label.pack(fill=tk.BOTH, expand=True)

    root.mainloop()

# Main execution
if __name__ == "__main__":
    # Parse the log file
    log_file = "/Users/likhithkanigolla/IIITH/code-files/Digital-Twin/DEVS/detail-model-v1/simulation_output/water-quality.txt"  # Replace with the path to your log file
    events = parse_log(log_file)

    # Create the UI
    create_ui(events)
