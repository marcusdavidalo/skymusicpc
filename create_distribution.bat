@echo off
echo Creating distribution package for SkyMusic Player...

REM Create distribution folder if it doesn't exist
mkdir SkyMusicPlayer_Distribution 2>nul

REM Copy the executable
copy "dist\SkyMusic Player.exe" SkyMusicPlayer_Distribution\ /Y

REM Create empty JSON files for first-time users
echo {} > SkyMusicPlayer_Distribution\saved_songs.json
echo {} > SkyMusicPlayer_Distribution\last_loaded_song.json

REM Copy the icon
copy ei.ico SkyMusicPlayer_Distribution\ /Y

REM Create a simple readme
echo SkyMusic Player > SkyMusicPlayer_Distribution\README.txt
echo ===================== >> SkyMusicPlayer_Distribution\README.txt
echo. >> SkyMusicPlayer_Distribution\README.txt
echo Thank you for using SkyMusic Player! >> SkyMusicPlayer_Distribution\README.txt
echo. >> SkyMusicPlayer_Distribution\README.txt
echo To get started: >> SkyMusicPlayer_Distribution\README.txt
echo 1. Simply double-click on "SkyMusic Player.exe" to launch the application >> SkyMusicPlayer_Distribution\README.txt
echo 2. Use the "Add Music" button to load your music files >> SkyMusicPlayer_Distribution\README.txt
echo 3. Enjoy your music! >> SkyMusicPlayer_Distribution\README.txt
echo. >> SkyMusicPlayer_Distribution\README.txt
echo Note: Your music library will be saved in saved_songs.json >> SkyMusicPlayer_Distribution\README.txt
echo. >> SkyMusicPlayer_Distribution\README.txt

echo Distribution package created successfully!
echo Located in: SkyMusicPlayer_Distribution folder 