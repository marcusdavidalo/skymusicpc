import os
import time
import tkinter as tk
from tkinter import filedialog, messagebox
import json
import threading
import keyboard

SAVED_SONGS_FILE = "saved_songs.json"
LAST_LOADED_SONG_FILE = "last_loaded_song.json"

# Global variable for the delay
delay = 0.015

# Define the key mapping
keyMapping = {
    "1Key0": "y",
    "1Key1": "u",
    "1Key2": "i",
    "1Key3": "o",
    "1Key4": "p",
    "1Key5": "h",
    "1Key6": "j",
    "1Key7": "k",
    "1Key8": "l",
    "1Key9": ";",
    "1Key10": "n",
    "1Key11": "m",
    "1Key12": ",",
    "1Key13": ".",
    "1Key14": "/",
    "2Key0": "y",
    "2Key1": "u",
    "2Key2": "i",
    "2Key3": "o",
    "2Key4": "p",
    "2Key5": "h",
    "2Key6": "j",
    "2Key7": "k",
    "2Key8": "l",
    "2Key9": ";",
    "2Key10": "n",
    "2Key11": "m",
    "2Key12": ",",
    "2Key13": ".",
    "2Key14": "/"
}

# Define color themes
light_theme = {
    "bg": "white",
    "fg": "black",
    "button_bg": "#cccccc",  # Light gray for buttons
    "button_fg": "black"
}

dark_theme = {
    "bg": "#222222",
    "fg": "white",
    "button_bg": "#444444",  # Dark gray for buttons
    "button_fg": "white"
}

current_theme = dark_theme  # Set initial theme

# Initialize saved music as an empty list
saved_music = []

# Flag to track playback state
is_playing = False

# Global variables to track playback and pause state
is_playing = False
is_paused = False
current_note_index = 0  # Add a global variable to keep track of the current note index

# Create an Event object for each state
play_event = threading.Event()
stop_event = threading.Event()

# Define the initial hotkeys
hotkeys = {"play": "F1", "pause": "F2", "stop": "F10"}

def play_music(notes):
    global current_note_index
    play_event.set()  # Start playing
    stop_event.clear()  # Don't stop yet

    while current_note_index < len(notes):
        if stop_event.is_set():  # Stop playing if the stop event is set
            break

        # Get the current time and the time for the next note
        current_time = notes[current_note_index]['time']
        keys_to_press = []

        # Add all keys that should be pressed at the current time
        while current_note_index < len(notes) and notes[current_note_index]['time'] == current_time:
            key = notes[current_note_index]['key']
            mapped_key = keyMapping.get(key)
            if mapped_key:
                keys_to_press.append(mapped_key)
            current_note_index += 1

        # Press all keys
        for key in keys_to_press:
            keyboard.press(key)
        
        time.sleep(delay_slider.get())

        # Release all keys
        for key in keys_to_press:
            keyboard.release(key)

        if current_note_index < len(notes):  # If there are more notes to play
            next_time = notes[current_note_index]['time']
            delay = max(0, (next_time - current_time) / 1000 - delay_slider.get())  # Calculate the delay until the next note, subtracting the user-adjustable delay
            if delay > 0:
                time.sleep(delay)  # Wait until it's time for the next note

    if not is_paused:  # If the music wasn't paused, reset the current note index
        current_note_index = 0
    is_playing = False



def play_loaded_music():
  global loaded_notes
  if loaded_notes is not None:
    play_music(loaded_notes)  # Play the loaded notes

def stop_music():
    if play_event.is_set():  # If the music is playing
        stop_event.set()  # Stop the music

def play_or_stop_music():
    global is_playing
    if is_playing:
        stop_music()
    else:
        play_loaded_music()

keyboard.add_hotkey('F1', play_or_stop_music)

def set_hotkey(action):
    try:
        settings_window.withdraw()  # Temporarily hide settings window
        keyboard.wait("hotkey")  # Wait for user to press a hotkey
        hotkey = keyboard.get_hotkey_name().split("+")[-1]  # Get the pressed key
        keyboard.remove_hotkey(hotkeys[action])  # Remove the existing hotkey
        hotkeys[action] = hotkey  # Update the hotkey in the hotkeys dictionary
        keyboard.add_hotkey(hotkey, globals()[f"{action}_music"])  # Update the hotkey for the action
        hotkey_labels[action].config(text=f"{action} Music: {hotkey}")
        messagebox.showinfo("Hotkey Set", f"Hotkey for {action} music set to {hotkey}")
    except Exception as e:
        messagebox.showerror("Error", f"Error setting hotkey: {str(e)}")
    finally:
        settings_window.deiconify()  # Show settings window again


# Global variable to store the loaded notes
loaded_notes = None

def load_music_from_file():
    global loaded_notes  # Use the global loaded_notes variable
    try:
        file_types = [("SkySheet Files", "*.skysheet"), ("JSON Files", "*.json")]
        file_paths = filedialog.askopenfilenames(filetypes=file_types)  # Change this line
        if file_paths:
            for file_path in file_paths:  # Iterate over all selected files
                with open(file_path, 'r', encoding='utf-8') as file:
                    file_data = file.read()
                    print(file_data)  # Print out the data read from the file
                    data = json.loads(file_data)  # Use json.loads instead of json.load
                    # Check if the "songNotes" key exists and is a list
                    if 'songNotes' in data[0] or data and isinstance(data[0]['songNotes'], list):
                        loaded_notes = data[0]['songNotes'] or data['songNotes'] # Store the loaded notes
                        save_music(loaded_notes, file_path)  # Save the loaded music
                    else:
                        messagebox.showerror("Error", "Invalid SkySheet file. Missing or incorrect 'songNotes' key.")
    except FileNotFoundError as e:
        error_message = f"Error loading music: {str(e)}"
        show_error_message(error_message)

    loaded_notes = data[0]['songNotes']  # Store the loaded notes

def load_music(notes):  # This function now only loads music from a list of notes
    global loaded_notes
    loaded_notes = notes

def save_music(notes, path):
    # Extract the filename from the path
    name = os.path.basename(path)
    # Check if a song with the same name is already in the saved_music list
    for music in saved_music:
        if music["name"] == name:
            messagebox.showinfo("Save Failed", "A song with the same name is already saved.")
            return  # If a song with the same name is found, don't add the new song
    saved_music.append({"notes": notes, "name": name})
    update_sidebar(saved_music)
    messagebox.showinfo("Save Successful", "Music saved successfully.")
    with open(SAVED_SONGS_FILE, 'w') as f:
        json.dump(saved_music, f)
    with open(LAST_LOADED_SONG_FILE, 'w') as f:
        json.dump({"notes": notes, "name": name}, f)

# Load saved songs when the program starts
def load_saved_songs():
    if os.path.exists(SAVED_SONGS_FILE):
        with open(SAVED_SONGS_FILE, 'r') as f:
            global saved_music
            saved_music = json.load(f)
            update_sidebar(saved_music)

# Load the last song when the program starts
def load_last_song():
    if os.path.exists(LAST_LOADED_SONG_FILE):
        with open(LAST_LOADED_SONG_FILE, 'r') as f:
            music = json.load(f)
            load_music(music["notes"])

def load_sidebar_music(index):
    if index < len(saved_music):  # Check if the selected song is in the saved_music list
        music = saved_music[index]
        load_music(music["notes"])

def delete_music(index):
    if index < len(saved_music):  # Check if the selected song is in the saved_music list
        del saved_music[index]  # Delete the song from the saved_music list
        update_sidebar(saved_music)  # Update the sidebar

def update_sidebar(notes=None):
    # Delete all existing widgets in the sidebar
    for widget in sidebar.winfo_children():
        widget.destroy()

    if notes is None:
        notes = saved_music
    if not notes:
        sidebar.insert(tk.END, "No Songs Saved")
    else:
        for i, music in enumerate(notes):
            frame = tk.Frame(sidebar, bg=current_theme["bg"])
            frame.pack(fill=tk.X)
            label = tk.Label(frame, text=music["name"], fg=current_theme["fg"], bg=current_theme["bg"])
            label.pack(side=tk.LEFT)
            load_button = tk.Button(frame, text="Load", command=lambda i=i: load_sidebar_music(i), bg=current_theme["button_bg"], fg=current_theme["button_fg"])
            load_button.pack(side=tk.RIGHT)
            delete_button = tk.Button(frame, text="Delete", command=lambda i=i: delete_music(i), bg=current_theme["button_bg"], fg=current_theme["button_fg"])
            delete_button.pack(side=tk.RIGHT)

def show_error_message(message):
    error_window = tk.Toplevel(root)
    error_window.title("Error")
    error_label = tk.Label(error_window, text=message, fg=current_theme["fg"], bg=current_theme["bg"])
    error_label.pack(padx=10, pady=10)
    ok_button = tk.Button(error_window, text="OK", command=error_window.destroy, bg=current_theme["button_bg"], fg=current_theme["button_fg"])
    ok_button.pack()


def toggle_theme():
    global current_theme
    if current_theme == light_theme:
        current_theme = dark_theme
    else:
        current_theme = light_theme
    update_theme()


def update_theme():
    root.config(bg=current_theme["bg"])
    for child in root.winfo_children():
        child.config(fg=current_theme["fg"], bg=current_theme["bg"])
    load_button.config(bg=current_theme["button_bg"], fg=current_theme["button_fg"])
    hotkey_button.config(bg=current_theme["button_bg"], fg=current_theme["button_fg"])
    theme_button.config(bg=current_theme["button_bg"], fg=current_theme["button_fg"])
    sidebar.config(bg=current_theme["bg"], fg=current_theme["fg"], selectbackground=current_theme["bg"], selectforeground=current_theme["fg"])


hotkey_labels = {}

settings_window = None

def open_settings():
    global settings_window
    if not settings_window:  # Check if a settings window is already open
        settings_window = tk.Toplevel(root, bg=current_theme["bg"])
        settings_window.title("Settings")

        hotkey_label = tk.Label(settings_window, text="Hotkeys:", fg=current_theme["fg"], bg=current_theme["bg"])
        hotkey_label.pack(pady=(10, 5))

        # Create labels and buttons for each hotkey
        for action, key in hotkeys.items():
            label = tk.Label(settings_window, text=f"{action} Music: {key if key else '(Not set)'}", fg=current_theme["fg"], bg=current_theme["bg"])
            label.pack()
            button = tk.Button(settings_window, text="Set", command=lambda a=action: set_hotkey(a), bg=current_theme["button_bg"], fg=current_theme["button_fg"])
            button.pack()
            hotkey_labels[action] = label  # Store labels for later updates

        default_button = tk.Button(settings_window, text="Set Defaults", command=set_default_hotkeys, bg=current_theme["button_bg"], fg=current_theme["button_fg"])
        default_button.pack(pady=10)

def set_hotkey(action):
    try:
        settings_window.withdraw()  # Temporarily hide settings window
        keyboard.wait("hotkey")  # Wait for user to press a hotkey
        hotkey = keyboard.get_hotkey_name().split("+")[-1]  # Get the pressed key
        hotkeys[action] = hotkey
        hotkey_labels[action].config(text=f"{action} Music: {hotkey}")
        messagebox.showinfo("Hotkey Set", f"Hotkey for {action} music set to {hotkey}")
    except Exception as e:
        messagebox.showerror("Error", f"Error setting hotkey: {str(e)}")
    finally:
        settings_window.deiconify()  # Show settings window again

def set_default_hotkeys():
    global hotkeys
    hotkeys = {"play": "F1", "pause": "F2", "stop": "F10"}
    for action, label in hotkey_labels.items():
        label.config(text=f"{action} Music: {hotkeys[action]}")
    messagebox.showinfo("Default Hotkeys Set", "Hotkeys have been set to their defaults.")

# Create the main application window
root = tk.Tk()
root.title("Sky Music Player")
root.geometry("400x400")  # Set a fixed window size

# Create buttons with improved styling
load_button = tk.Button(root, text="Load Music", command=load_music_from_file, bg=current_theme["button_bg"], fg=current_theme["button_fg"])
load_button.pack(pady=10, fill="both", expand=True)

hotkey_button = tk.Button(root, text="Settings", command=open_settings, bg=current_theme["button_bg"], fg=current_theme["button_fg"])
hotkey_button.pack(pady=5, fill="both", expand=True)

# Create toggle theme button
theme_button = tk.Button(root, text="Toggle Theme", command=toggle_theme, bg=current_theme["button_bg"], fg=current_theme["button_fg"])
theme_button.pack(pady=5, fill="both", expand=True)

# Create a slider for the delay
delay_slider = tk.Scale(root, from_=0, to=0.2, resolution=0.001, length=400, orient=tk.HORIZONTAL, label="Delay", bg=current_theme["button_bg"], fg=current_theme["button_fg"])
delay_slider.set(delay)  # Set the initial value
delay_slider.pack(pady=10, fill="both", expand=True)


# Create stop button
stop_button = tk.Button(root, text="Stop Music", command=stop_music, bg=current_theme["button_bg"], fg=current_theme["button_fg"])
stop_button.pack(pady=10, fill="both", expand=True)

# Create sidebar to display saved music
sidebar = tk.Listbox(root)
sidebar.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
sidebar.bind("<<ListboxSelect>>", load_sidebar_music)

# Apply the initial theme
update_theme()
update_sidebar()

load_saved_songs()
load_last_song()

# Start the Tkinter event loop
root.mainloop()
