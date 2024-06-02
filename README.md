# SkyMusic

SkyMusic is a Python application for playing music on Sky: Children of the Light

## Requirements

This app uses the following Python packages:

```
keyboard==0.13.5
MouseInfo==0.1.3
pillow==10.2.0
PyAutoGUI==0.9.54
PyGetWindow==0.0.9
PyMsgBox==1.0.9
pyperclip==1.8.2
PyRect==0.2.0
PyScreeze==0.1.30
pytweening==1.2.0
chardet
```

These can be installed using the `requirements.txt` file provided.

## Installation

1. **Clone the repository:**

   ```sh
   git clone https://github.com/marcusdavidalo/skymusicpc.git
   cd skymusicpc
   ```

2. **Create a virtual environment:**

   ```sh
   python -m venv venv
   ```

3. **Activate the virtual environment:**

   - On Windows:

     ```sh
     venv\Scripts\activate
     ```

   - On macOS and Linux:

     ```sh
     source venv/bin/activate
     ```

4. **Install the required packages:**

   ```sh
   pip install -r requirements.txt
   ```

## Running the Application

To run the application, execute the main script:

```sh
python skympc.py
```

## Building an Executable

To build a standalone executable of the application, use `pyinstaller`. Ensure `pyinstaller` is installed in your virtual environment:

```sh
pip install pyinstaller
```

Then run the following command:

```sh
pyinstaller -n skyplayer --onefile --windowed --icon=ei.ico --strip skympc.py
```

This will create a single executable file named `skyplayer` in the `dist` directory.

## Features

- **Load Music**: Load music files in SkySheet or JSON format.
- **Save Music**: Save loaded music for easy access later.
- **Play Music**: Play loaded music by simulating keyboard inputs.
- **Pause/Stop Music**: Control the playback with F1 to play and F2 to stop.
- **Adjust Playback Speed**: Control playback speed with a slider.
- **Auto Delay**: Automatically adjust delay between notes.

## Hotkeys

- **F1**: Play loaded music. (works)
- **F2**: Stop playing music. (currently does not work yet)

## GUI

The app uses Tkinter for its graphical user interface. The main window includes controls for loading, saving, and playing music, as well as sliders for adjusting delay and playback speed.

## Known Bugs

- Stopping from Sky doesn't work when pressing F2; you need to alt-tab to the app to manually press the stop button on the UI to stop playing.

## Planned Improvements

- Improve the playback speed controller for smoother and more accurate speed adjustments.
- Enhance the auto delay/auto release logic for better timing and performance.
- Add more hotkeys for additional controls and functionality.
- Implement a more user-friendly and responsive GUI design.

## License

This project is licensed under the MIT License.

## Contributing

If you would like to contribute, please fork the repository and submit a pull request.

---

There are still a lot of improvements that can be made to this application. Your contributions and suggestions are very VERY welcome!
