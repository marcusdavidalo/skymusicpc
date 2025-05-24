# SkyMusic Player

A professional music player for playing Sky: Children of the Light music with advanced features.

## Features

- Clean, compact enterprise UI design
- Support for multiple languages (English, Chinese, Spanish, Japanese)
- Library management for your song collection
- Song queue management
- Playback controls with speed adjustment
- Humanizer feature for more natural playback
- Hotkey controls (F1 for play/pause, F2 for stop)
- Tag-based filtering for easy song discovery

## Project Structure

The application is organized in a modular structure:

```
skymusicpc/
├── core/            # Core functionality
│   ├── player.py    # Music playback engine
│   └── library.py   # Song library management
├── ui/              # User interface components
│   ├── theme.py     # Theming and styling
│   ├── sidebar.py   # Library sidebar
│   ├── playback.py  # Playback controls
│   └── language.py  # Language selector
├── utils/           # Utility modules
│   ├── constants.py # Application constants
│   ├── helpers.py   # Helper functions
│   └── localization.py # Localization system
└── resources/       # Resources like icons
```

## Installation

1. Make sure you have Python 3.6+ installed
2. Clone this repository
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run the application:
   ```
   python run.py
   ```

## Usage

1. Start the application
2. Load a song from the library by clicking on it
3. Use the play/pause button or press F1 to start playback
4. Adjust playback settings as needed
5. Use tags to filter your song collection

## Adding Songs

Songs are stored in the `saved_songs.json` file. The format for a song is:

```json
{
  "id": "song_1234567890",
  "title": "Song Title",
  "notes": [
    {"timestamp": 0.0, "note": "1Key0"},
    {"timestamp": 0.5, "note": "1Key1"},
    ...
  ],
  "tags": ["tag1", "tag2"]
}
```

## License

This project is open source and available under the MIT License.
