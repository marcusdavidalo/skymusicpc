import os
import time
import tkinter as tk
from tkinter import filedialog, messagebox
import json
import chardet
import threading
import keyboard

SAVED_SONGS_FILE = "saved_songs.json"
LAST_LOADED_SONG_FILE = "last_loaded_song.json"

# Global variables
delay = 0.015
auto_delay = False

# Define the key mapping
keyMapping = {
    "1Key0": "y", "1Key1": "u", "1Key2": "i", "1Key3": "o", "1Key4": "p",
    "1Key5": "h", "1Key6": "j", "1Key7": "k", "1Key8": "l", "1Key9": ";",
    "1Key10": "n", "1Key11": "m", "1Key12": ",", "1Key13": ".", "1Key14": "/",
    "2Key0": "y", "2Key1": "u", "2Key2": "i", "2Key3": "o", "2Key4": "p",
    "2Key5": "h", "2Key6": "j", "2Key7": "k", "2Key8": "l", "2Key9": ";",
    "2Key10": "n", "2Key11": "m", "2Key12": ",", "2Key13": ".", "2Key14": "/"
}

# Initialize saved music as an empty list
saved_music = []

# Flags to track playback state
is_playing = False
current_note_index = 0

# Create Event objects for each state
play_event = threading.Event()
stop_event = threading.Event()

# Define the initial hotkeys
hotkeys = {"play_stop": "F1"}

def play_music(notes):
    global current_note_index
    play_event.set()
    stop_event.clear()

    while current_note_index < len(notes):
        if stop_event.is_set():
            break

        current_time = notes[current_note_index]['time']
        keys_to_press = []

        while current_note_index < len(notes) and notes[current_note_index]['time'] == current_time:
            key = notes[current_note_index]['key']
            mapped_key = keyMapping.get(key)
            if mapped_key:
                keys_to_press.append(mapped_key)
            current_note_index += 1

        for key in keys_to_press:
            keyboard.press(key)
        
        if auto_delay and current_note_index < len(notes):
            next_time = notes[current_note_index]['time']
            calculated_delay = max(0, (next_time - current_time) / 1000 - 0.005)  # Subtract a small value to ensure overlap
            time.sleep(calculated_delay)
        else:
            time.sleep(delay_slider.get())

        for key in keys_to_press:
            keyboard.release(key)

        if not auto_delay and current_note_index < len(notes):
            next_time = notes[current_note_index]['time']
            delay = max(0, (next_time - current_time) / 1000 - delay_slider.get())
            if delay > 0:
                time.sleep(delay)

def play_loaded_music():
    global loaded_notes
    if loaded_notes is not None:
        play_music(loaded_notes)

def pause_music():
    global is_playing
    if play_event.is_set():
        stop_event.set()
        is_playing = False

def stop_music():
    global is_playing, current_note_index
    if play_event.is_set():
        stop_event.set()
    is_playing = False
    current_note_index = 0

def play_or_stop_music():
    global is_playing
    if is_playing:
        is_playing = False
        stop_music()
    else:
        is_playing = True
        play_loaded_music()

keyboard.add_hotkey('F1', play_or_stop_music)
keyboard.add_hotkey('F2', pause_music)

def set_hotkey(action):
    try:
        settings_window.withdraw()
        keyboard.wait("hotkey")
        hotkey = keyboard.get_hotkey_name().split("+")[-1]
        keyboard.remove_hotkey(hotkeys[action])
        hotkeys[action] = hotkey
        keyboard.add_hotkey(hotkey, globals()[f"{action}_music"])
        hotkey_labels[action].config(text=f"{action} Music: {hotkey}")
        messagebox.showinfo("Hotkey Set", f"Hotkey for {action} music set to {hotkey}")
    except Exception as e:
        messagebox.showerror("Error", f"Error setting hotkey: {str(e)}")
    finally:
        settings_window.deiconify()

loaded_notes = None

def detect_encoding(file_path):
    with open(file_path, 'rb') as file:
        raw_data = file.read()
        result = chardet.detect(raw_data)
        return result['encoding']

def load_music_from_file():
    global loaded_notes
    results = []
    try:
        file_types = [("SkySheet Files", "*.skysheet"), ("JSON Files", "*.json")]
        file_paths = filedialog.askopenfilenames(filetypes=file_types)
        if file_paths:
            for file_path in file_paths:
                try:
                    encoding = detect_encoding(file_path)
                    with open(file_path, 'r', encoding=encoding) as file:
                        data = json.load(file)
                    
                    if isinstance(data, list) and 'songNotes' in data[0] and isinstance(data[0]['songNotes'], list):
                        loaded_notes = data[0]['songNotes']
                        save_music_result = save_music(loaded_notes, file_path)
                        if save_music_result:
                            results.append(f"File {file_path}: Saved successfully.")
                        else:
                            results.append(f"File {file_path}: Save failed. A song with the same name is already saved.")
                    else:
                        results.append(f"File {file_path}: Invalid SkySheet file. Missing or incorrect 'songNotes' key.")
                except (UnicodeDecodeError, json.JSONDecodeError) as e:
                    results.append(f"File {file_path}: Failed to decode. Error: {str(e)}")
    except FileNotFoundError as e:
        results.append(f"Error loading music: {str(e)}")
    
    # Show summary of results
    summary = "\n".join(results)
    messagebox.showinfo("Load Music Summary", summary)

def save_music(notes, path):
    global saved_music
    name = os.path.basename(path)
    for music in saved_music:
        if music["name"] == name:
            return False  # Indicate that saving failed due to duplicate name
    
    saved_music.append({"notes": notes, "name": name})
    update_sidebar(saved_music)
    
    # Save the music data to files
    with open(SAVED_SONGS_FILE, 'w') as f:
        json.dump(saved_music, f)
    with open(LAST_LOADED_SONG_FILE, 'w') as f:
        json.dump({"notes": notes, "name": name}, f)
    
    return True  # Indicate that saving was successful

def show_error_message(message):
    messagebox.showerror("Error", message)

def load_music(notes):
    global loaded_notes
    loaded_notes = notes

def load_saved_songs():
    if os.path.exists(SAVED_SONGS_FILE):
        with open(SAVED_SONGS_FILE, 'r') as f:
            global saved_music
            saved_music = json.load(f)
            update_sidebar(saved_music)

def load_last_song():
    if os.path.exists(LAST_LOADED_SONG_FILE):
        with open(LAST_LOADED_SONG_FILE, 'r') as f:
            music = json.load(f)
            load_music(music["notes"])

def load_sidebar_music(index):
    if index < len(saved_music):
        music = saved_music[index]
        load_music(music["notes"])

def delete_music(index):
    if index < len(saved_music):
        del saved_music[index]
        update_sidebar(saved_music)

# Define color themes
light_theme = {"bg": "white", "fg": "black", "button_bg": "#cccccc", "button_fg": "black"}
dark_theme = {"bg": "#222222", "fg": "white", "button_bg": "#444444", "button_fg": "white"}
current_theme = dark_theme  # Set initial theme

def update_sidebar(notes=None):
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
    current_theme = light_theme if current_theme == dark_theme else dark_theme
    update_theme()

def update_theme():
    root.config(bg=current_theme["bg"])
    for child in root.winfo_children():
        child.config(fg=current_theme["fg"], bg=current_theme["bg"])
    load_button.config(bg=current_theme["button_bg"], fg=current_theme["button_fg"])
    stop_button.config(bg=current_theme["button_bg"], fg=current_theme["button_fg"])
    hotkey_button.config(bg=current_theme["button_bg"], fg=current_theme["button_fg"])
    theme_button.config(bg=current_theme["button_bg"], fg=current_theme["button_fg"])
    settings_button.config(bg=current_theme["button_bg"], fg=current_theme["button_fg"])
    delay_slider.config(fg=current_theme["fg"], bg=current_theme["bg"], highlightbackground=current_theme["bg"])
    auto_delay_checkbox.config(fg=current_theme["fg"], bg=current_theme["bg"], highlightbackground=current_theme["bg"])

def toggle_auto_delay(state):
    global auto_delay
    auto_delay = state
    if auto_delay:
        delay_slider.pack_forget()
    else:
        delay_slider.pack(pady=10)

root = tk.Tk()
root.title("SkyMusic")
root.config(bg=current_theme["bg"])

sidebar = tk.Frame(root, width=200, bg=current_theme["bg"])
sidebar.pack(side=tk.LEFT, fill=tk.Y)

load_button = tk.Button(root, text="Load Music", command=load_music_from_file, bg=current_theme["button_bg"], fg=current_theme["button_fg"])
load_button.pack(pady=10)

delay_slider = tk.Scale(root, from_=0.001, to_=1.0, resolution=0.001, orient=tk.HORIZONTAL, label="Delay (seconds)", fg=current_theme["fg"], bg=current_theme["bg"])
delay_slider.set(delay)
delay_slider.pack(pady=10)

auto_delay = True  # Set initial auto delay
auto_delay_var = tk.BooleanVar()
auto_delay_checkbox = tk.Checkbutton(root, text="Auto Delay", variable=auto_delay_var, command=lambda: toggle_auto_delay(auto_delay_var.get()), fg=current_theme["fg"], bg=current_theme["bg"], selectcolor=current_theme["bg"])
auto_delay_checkbox.pack()

hotkey_button = tk.Button(root, text="Hotkey Settings", command=lambda: settings_window.deiconify(), bg=current_theme["button_bg"], fg=current_theme["button_fg"])
hotkey_button.pack(pady=10)

theme_button = tk.Button(root, text="Toggle Theme", command=toggle_theme, bg=current_theme["button_bg"], fg=current_theme["button_fg"])
theme_button.pack(pady=10)

stop_button = tk.Button(root, text="Stop Music", command=stop_music, bg=current_theme["button_bg"], fg=current_theme["button_fg"])
stop_button.pack(pady=10)

settings_button = tk.Button(root, text="Settings", command=lambda: settings_window.deiconify(), bg=current_theme["button_bg"], fg=current_theme["button_fg"])
settings_button.pack(pady=10)

settings_window = tk.Toplevel(root)
settings_window.title("Settings")
settings_window.withdraw()
settings_window.protocol("WM_DELETE_WINDOW", settings_window.withdraw)
settings_window.config(bg=current_theme["bg"])

hotkey_labels = {}
for action in ["play_stop"]:
    hotkey_labels[action] = tk.Label(settings_window, text=f"{action} Music: {hotkeys[action]}", fg=current_theme["fg"], bg=current_theme["bg"])
    hotkey_labels[action].pack()
    set_hotkey_button = tk.Button(settings_window, text=f"Set {action} Hotkey", command=lambda action=action: set_hotkey(action), bg=current_theme["button_bg"], fg=current_theme["button_fg"])
    set_hotkey_button.pack()

load_saved_songs()
load_last_song()
update_sidebar()

root.mainloop()
