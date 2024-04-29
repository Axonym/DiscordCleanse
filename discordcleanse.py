import requests
import tkinter as tk
import customtkinter as ctk
import time
import random
from tkinter import filedialog
import os
import csv
import json

directory = filedialog.askdirectory(title="Select the Package folder")

if os.path.exists(os.path.join(directory, "messages")):
    messagedir = os.path.join(directory, "messages")
else:
    print(
        "Please select the folder that has subfolders 'account', 'messages' etc in it"
    )
    exit()


def log_message(message):
    # Enable the text widget to allow text insertion
    log_text.configure(state="normal")
    # Append the message to the text widget
    log_text.insert(tk.END, message + "\n")
    # Scroll to the end of the text widget
    log_text.see(tk.END)
    # Disable the text widget again to prevent manual edits
    log_text.configure(state="disabled")


def clear_log():
    log_text.configure(state="normal")
    log_text.delete(1.0, tk.END)
    log_text.configure(state="disabled")


# Function to toggle password visibility
def toggle_password_visibility(event=None):
    show_char = "*" if password_var.get() == 1 else ""
    authorization_entry.configure(show=show_char)
    channel_id_entry.configure(show=show_char)


def slider_event(value):
    delay_var.set(f"Delay: {value} ms")
    global delay
    delay = int(value) / 1000  # Convert milliseconds to seconds

    if delay < 2.5:
        delay_var.set(f"NOT RECOMMENDED! Delay: {value} ms")
        delay_value_label.configure(text_color="red")
    if delay >= 2.5:
        delay_value_label.configure(text_color="white")


def read_csv_file(file_path):
    message_ids = []
    with open(file_path, newline="") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            # Check if the third or fourth column has something in them
            if row[2] or row[3]:
                message_ids.append(row[0])
    return message_ids


def read_json_file(file_path):
    message_ids = []
    with open(file_path, "r", encoding="utf-8") as jsonfile:
        data = json.load(jsonfile)
        for message in data:
            if "ID" in message:
                message_ids.append(message["ID"])
    return message_ids


def delete_messages():
    clear_log()
    authorization = authorization_entry.get()
    channel_id = channel_id_entry.get()
    if not authorization or not channel_id:
        log_message("Authorization or Channel ID is empty. Please fill in both fields.")
        return
    testurl = f"https://discord.com/api/v9/channels/{channel_id}/messages?limit=50"
    headers = {"Authorization": authorization}

    response = requests.get(testurl, headers=headers)

    if response.status_code == 401:
        log_message("Incorrect authorization cookie")
        return
    elif response.status_code == 404:
        log_message("Channel doesn't exist or incorrect channel ID")
        return
    elif response.status_code != 200:
        log_message("No permission to the channel")
        return

    csv_file_path = os.path.join(
        messagedir, f"c{channel_id}", "messages.csv"
    )  # Construct the file path using the channel ID
    json_file_path = os.path.join(messagedir, f"c{channel_id}", "messages.json")
    if os.path.exists(csv_file_path):
        # Read the CSV file and extract message IDs
        message_ids = read_csv_file(csv_file_path)
    elif os.path.exists(json_file_path):
        # Read the JSON file and extract message IDs
        message_ids = read_json_file(json_file_path)
    else:
        log_message("Incorrect Channel ID/channel ID not found from package")

    all_successful = True
    total_messages = len(message_ids)

    log_message("Starting to delete messages")

    estimated_time = (
        total_messages * delay
    )  # Calculate the total estimated time in seconds

    # Convert the estimated time to hours, minutes, and seconds
    hours, remainder = divmod(estimated_time, 3600)
    minutes, seconds = divmod(remainder, 60)

    # Conditionally format the estimated time
    if hours > 0:
        formatted_time = (
            f"{int(hours)} hours, {int(minutes)} minutes, and {int(seconds)} seconds"
        )
    elif minutes > 0:
        formatted_time = f"{int(minutes)} minutes and {int(seconds)} seconds"
    else:
        formatted_time = f"{int(seconds)} seconds"

    estimated_time_text = f"Estimated time: {formatted_time}"
    log_message(estimated_time_text)
    root.update()

    successful_deletions = 0  # Initialize a counter for successful deletions

    for index, message_id in enumerate(message_ids):
        url = f"https://discord.com/api/v9/channels/{channel_id}/messages/{message_id}"
        res = requests.delete(url, headers=headers)
        status = res.status_code

        if status == 204:
            successful_deletions += (
                1  # Increment the counter if the deletion is successful
            )
        elif status == 403:
            all_successful = False
            log_message(
                "Unable to delete system message or message sent by someone else"
            )
            time.sleep(1)
            continue
        else:
            all_successful = False
            log_message(f"Something went wrong for message ID {message_id}")
            time.sleep(1)
            continue

        # Calculate the remaining time by subtracting the total delay applied so far
        remaining_time = estimated_time - ((index + 1) * delay)

        # Convert the remaining time to hours, minutes, and seconds
        hours, remainder = divmod(remaining_time, 3600)
        minutes, seconds = divmod(remainder, 60)

        # Conditionally format the remaining time
        if hours > 0:
            formatted_time = f"{int(hours)} hours, {int(minutes)} minutes, and {int(seconds)} seconds"
        elif minutes > 0:
            formatted_time = f"{int(minutes)} minutes and {int(seconds)} seconds"
        else:
            formatted_time = f"{int(seconds)} seconds"

        estimated_time_text = f"Time left: {formatted_time}"
        log_message(f"{index+1}/{total_messages} {estimated_time_text}")
        root.update()

        # Apply the delay after calculating the remaining time, except for the last message
        if index < total_messages - 1:
            # Add random delay between 0 and 300 ms
            random_delay = random.uniform(
                0, 0.3
            )  # Generate a random float between 0 and 0.3
            time.sleep(delay + random_delay)  # Add the random delay to the base delay

    if all_successful:
        log_message("All messages were deleted successfully")
    else:
        log_message(
            f"Was able to delete {successful_deletions}/{total_messages} messages"
        )


# Create the main window
root = ctk.CTk()
root.title("Discord Cleanse")
root.geometry("600x500")

# Create labels and entries for inputs
authorization_label = ctk.CTkLabel(root, text="Authorization Cookie Value:")
authorization_label.pack()
authorization_entry = ctk.CTkEntry(root)
authorization_entry.pack()

channel_id_label = ctk.CTkLabel(root, text="Channel ID:")
channel_id_label.pack()
channel_id_entry = ctk.CTkEntry(root)
channel_id_entry.pack()

# Create a checkbox to toggle password visibility
password_var = tk.IntVar()  # Create an IntVar to track the checkbox state
password_checkbox = ctk.CTkCheckBox(
    root,
    text="Hide values",
    variable=password_var,
    command=toggle_password_visibility,
)
password_checkbox.pack(pady=10)

# Initialize delay variable
delay = 2.5

# Create a slider for setting the delay
delay_label = ctk.CTkLabel(root, text="Adjust delay between deletions")
delay_label.pack()
delay_var = tk.StringVar()
delay_var.set("Delay: 2500.0 ms")
delay_slider = ctk.CTkSlider(
    root, from_=0, to=5000, command=slider_event, number_of_steps=50
)
delay_slider.pack()

delay_slider.set(delay * 1000)

# Display the current slider value
delay_value_label = ctk.CTkLabel(root, textvariable=delay_var, text_color="white")
delay_value_label.pack()

# Create a button to execute the deletion
delete_button = ctk.CTkButton(root, text="Delete Messages", command=delete_messages)
delete_button.pack()

# Create a label to display the result
result_label = ctk.CTkLabel(root, text="")
result_label.pack()

log_text = ctk.CTkTextbox(
    root,
    fg_color="#242424",
    border_color="#1f6aa5",
    border_width=1.5,
    font=("Inter", 12),
    wrap=tk.WORD,
    height=150,
    width=400,
    state="disabled",
)
log_text.pack()

# Start the main loop
root.mainloop()
