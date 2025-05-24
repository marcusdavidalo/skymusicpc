import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
import json
import chardet
import threading
import keyboard
import uuid
import time as time_module
import random

# Localization system
TRANSLATIONS = {
    "en": {  # English (Default)
        "app_title": "SkyMusic Player",
        "app_subtitle": "Play your sky music with ease",
        "sidebar_title": "SkyMusic Player",
        "sidebar_subtitle": "SONG LIBRARY",
        "search_placeholder": "Search songs...",
        "no_songs_found": "No songs found",
        "load_music": "Load Music",
        "now_playing": "NOW PLAYING",
        "no_song_loaded": "No song loaded",
        "playback_settings": "PLAYBACK SETTINGS",
        "auto_sustain_on": "Auto Sustain: On",
        "auto_sustain_off": "Auto Sustain: Off",
        "humanizer_on": "Humanizer: On",
        "humanizer_off": "Humanizer: Off",
        "queue_mode_on": "Queue Mode: On",
        "queue_mode_off": "Queue Mode: Off",
        "playback_speed": "Playback Speed",
        "normal_speed": "Normal",
        "slower": "% Slower",
        "faster": "% Faster",
        "note_delay": "Note Delay",
        "seconds": "seconds",
        "humanize_amount": "Humanize Amount",
        "play_pause": "Play/Pause (F1)",
        "stop": "Stop (F2)",
        "queue_management": "QUEUE MANAGEMENT",
        "previous": "◀ Previous",
        "next": "Next ▶",
        "clear_queue": "Clear Queue",
        "queue_empty": "Queue is empty",
        "keyboard_shortcuts": "KEYBOARD SHORTCUTS",
        "play_pause_desc": "Play/Pause current song",
        "stop_desc": "Stop playback",
        "ms": "ms",
        "legacy_format": "Legacy Format",
        "load": "Load",
        "add_queue": "+ Queue",
        "delete": "Delete",
        "welcome": "Welcome to SkyMusic Player! Press F1 to play/pause, F2 to stop. Queue system is enabled - add songs from your library to the queue.",
        "status_playing": "▶ Playing",
        "status_paused": "⏸ Paused",
        "status_stopped": "⏹ Stopped",
        "status_finished": "⏹ Finished",
        "status_ready": "▶ Ready",
        "status_no_song": "⏹ No song loaded",
        "status_error": "⏹ Error: No notes",
        "status_queue_finished": "⏹ Queue Finished",
        "load_success": "Loaded: {name}",
        "delete_success": "Deleted: {name}",
        "queue_add_success": "Added song to queue",
        "queue_remove_success": "Removed song from queue",
        "queue_clear_success": "Queue cleared",
        "queue_mode_enabled": "Queue mode enabled",
        "queue_mode_disabled": "Queue mode disabled",
        "auto_sustain_enabled": "Auto sustain enabled. Notes will be sustained automatically.",
        "auto_sustain_disabled": "Auto sustain disabled. Use delay slider to control note duration.",
        "humanizer_enabled": "Humanizer enabled - notes will have slight timing variations",
        "humanizer_disabled": "Humanizer disabled",
        "always_on_top_on": "Always on Top: On",
        "always_on_top_off": "Always on Top: Off",
        "always_on_top_enabled": "Always on Top enabled",
        "always_on_top_disabled": "Always on Top disabled",
        "language": "English"
    },
    "zh": {  # Chinese
        "app_title": "天空音乐播放器",
        "app_subtitle": "轻松播放您的天空音乐",
        "sidebar_title": "天空音乐播放器",
        "sidebar_subtitle": "音乐库",
        "search_placeholder": "搜索歌曲...",
        "no_songs_found": "未找到歌曲",
        "load_music": "加载音乐",
        "now_playing": "正在播放",
        "no_song_loaded": "未加载歌曲",
        "playback_settings": "播放设置",
        "auto_sustain_on": "自动延音: 开",
        "auto_sustain_off": "自动延音: 关",
        "humanizer_on": "人性化演奏: 开",
        "humanizer_off": "人性化演奏: 关",
        "queue_mode_on": "队列模式: 开",
        "queue_mode_off": "队列模式: 关",
        "playback_speed": "播放速度",
        "normal_speed": "正常",
        "slower": "% 慢速",
        "faster": "% 快速",
        "note_delay": "音符间隔",
        "seconds": "秒",
        "humanize_amount": "人性化强度",
        "play_pause": "播放/暂停 (F1)",
        "stop": "停止 (F2)",
        "queue_management": "队列管理",
        "previous": "◀ 上一首",
        "next": "下一首 ▶",
        "clear_queue": "清空队列",
        "queue_empty": "队列为空",
        "keyboard_shortcuts": "键盘快捷键",
        "play_pause_desc": "播放/暂停当前歌曲",
        "stop_desc": "停止播放",
        "ms": "毫秒",
        "legacy_format": "旧格式",
        "load": "加载",
        "add_queue": "+ 队列",
        "delete": "删除",
        "welcome": "欢迎使用天空音乐播放器! 按F1播放/暂停, 按F2停止。",
        "status_playing": "▶ 播放中",
        "status_paused": "⏸ 已暂停",
        "status_stopped": "⏹ 已停止",
        "status_finished": "⏹ 已完成",
        "status_ready": "▶ 就绪",
        "status_no_song": "⏹ 未加载歌曲",
        "status_error": "⏹ 错误: 无音符",
        "status_queue_finished": "⏹ 队列已完成",
        "load_success": "已加载: {name}",
        "delete_success": "已删除: {name}",
        "queue_add_success": "已添加歌曲到队列",
        "queue_remove_success": "已从队列中移除歌曲",
        "queue_clear_success": "已清空队列",
        "queue_mode_enabled": "已启用队列模式",
        "queue_mode_disabled": "已禁用队列模式",
        "auto_sustain_enabled": "已启用自动延音。音符将自动延长。",
        "auto_sustain_disabled": "已禁用自动延音。使用延迟滑块控制音符持续时间。",
        "humanizer_enabled": "已启用人性化演奏 - 音符将有轻微的时间变化",
        "humanizer_disabled": "已禁用人性化演奏",
        "always_on_top_on": "置顶: 开",
        "always_on_top_off": "置顶: 关",
        "always_on_top_enabled": "已启用置顶",
        "always_on_top_disabled": "已禁用置顶",
        "language": "中文"
    },
    "es": {  # Spanish
        "app_title": "SkyMusic Player",
        "app_subtitle": "Reproduce tu música Sky con facilidad",
        "sidebar_title": "SkyMusic Player",
        "sidebar_subtitle": "BIBLIOTECA DE CANCIONES",
        "search_placeholder": "Buscar canciones...",
        "no_songs_found": "No se encontraron canciones",
        "load_music": "Cargar Música",
        "now_playing": "REPRODUCIENDO AHORA",
        "no_song_loaded": "Ninguna canción cargada",
        "playback_settings": "AJUSTES DE REPRODUCCIÓN",
        "auto_sustain_on": "Auto-sostenido: Activado",
        "auto_sustain_off": "Auto-sostenido: Desactivado",
        "humanizer_on": "Humanizador: Activado",
        "humanizer_off": "Humanizador: Desactivado",
        "queue_mode_on": "Modo Cola: Activado",
        "queue_mode_off": "Modo Cola: Desactivado",
        "playback_speed": "Velocidad de Reproducción",
        "normal_speed": "Normal",
        "slower": "% Más lento",
        "faster": "% Más rápido",
        "note_delay": "Retardo de Nota",
        "seconds": "segundos",
        "humanize_amount": "Cantidad de Humanización",
        "play_pause": "Reproducir/Pausar (F1)",
        "stop": "Detener (F2)",
        "queue_management": "GESTIÓN DE COLA",
        "previous": "◀ Anterior",
        "next": "Siguiente ▶",
        "clear_queue": "Limpiar Cola",
        "queue_empty": "La cola está vacía",
        "keyboard_shortcuts": "ATAJOS DE TECLADO",
        "play_pause_desc": "Reproducir/Pausar canción actual",
        "stop_desc": "Detener reproducción",
        "ms": "ms",
        "legacy_format": "Formato Antiguo",
        "load": "Cargar",
        "add_queue": "+ Cola",
        "delete": "Eliminar",
        "welcome": "¡Bienvenido a SkyMusic Player! Presiona F1 para reproducir/pausar y F2 para detener.",
        "status_playing": "▶ Reproduciendo",
        "status_paused": "⏸ Pausado",
        "status_stopped": "⏹ Detenido",
        "status_finished": "⏹ Finalizado",
        "status_ready": "▶ Listo",
        "status_no_song": "⏹ Sin canción cargada",
        "status_error": "⏹ Error: Sin notas",
        "status_queue_finished": "⏹ Cola Finalizada",
        "load_success": "Cargada: {name}",
        "delete_success": "Eliminada: {name}",
        "queue_add_success": "Canción añadida a la cola",
        "queue_remove_success": "Canción eliminada de la cola",
        "queue_clear_success": "Cola limpiada",
        "queue_mode_enabled": "Modo cola activado",
        "queue_mode_disabled": "Modo cola desactivado",
        "auto_sustain_enabled": "Auto-sostenido activado. Las notas se sostendrán automáticamente.",
        "auto_sustain_disabled": "Auto-sostenido desactivado. Usa el deslizador de retardo para controlar la duración de las notas.",
        "humanizer_enabled": "Humanizador activado - las notas tendrán ligeras variaciones de tiempo",
        "humanizer_disabled": "Humanizador desactivado",
        "always_on_top_on": "Siempre visible: Activado",
        "always_on_top_off": "Siempre visible: Desactivado",
        "always_on_top_enabled": "Siempre visible activado",
        "always_on_top_disabled": "Siempre visible desactivado",
        "language": "Español"
    },
    "ja": {  # Japanese
        "app_title": "スカイミュージックプレーヤー",
        "app_subtitle": "簡単にスカイミュージックを再生",
        "sidebar_title": "スカイミュージックプレーヤー",
        "sidebar_subtitle": "曲ライブラリ",
        "search_placeholder": "曲を検索...",
        "no_songs_found": "曲が見つかりません",
        "load_music": "音楽を読み込む",
        "now_playing": "再生中",
        "no_song_loaded": "曲が読み込まれていません",
        "playback_settings": "再生設定",
        "auto_sustain_on": "自動サステイン: オン",
        "auto_sustain_off": "自動サステイン: オフ",
        "humanizer_on": "ヒューマナイザー: オン",
        "humanizer_off": "ヒューマナイザー: オフ",
        "queue_mode_on": "キューモード: オン",
        "queue_mode_off": "キューモード: オフ",
        "playback_speed": "再生速度",
        "normal_speed": "通常",
        "slower": "% 遅く",
        "faster": "% 速く",
        "note_delay": "ノートディレイ",
        "seconds": "秒",
        "humanize_amount": "ヒューマナイズ量",
        "play_pause": "再生/一時停止 (F1)",
        "stop": "停止 (F2)",
        "queue_management": "キュー管理",
        "previous": "◀ 前へ",
        "next": "次へ ▶",
        "clear_queue": "キューをクリア",
        "queue_empty": "キューは空です",
        "keyboard_shortcuts": "キーボードショートカット",
        "play_pause_desc": "現在の曲を再生/一時停止",
        "stop_desc": "再生を停止",
        "ms": "ミリ秒",
        "legacy_format": "レガシーフォーマット",
        "load": "読込",
        "add_queue": "+ キュー",
        "delete": "削除",
        "welcome": "スカイミュージックプレーヤーへようこそ！F1で再生/一時停止、F2で停止します。",
        "status_playing": "▶ 再生中",
        "status_paused": "⏸ 一時停止中",
        "status_stopped": "⏹ 停止しました",
        "status_finished": "⏹ 終了しました",
        "status_ready": "▶ 準備完了",
        "status_no_song": "⏹ 曲が読み込まれていません",
        "status_error": "⏹ エラー: ノートがありません",
        "status_queue_finished": "⏹ キュー終了",
        "load_success": "読み込みました: {name}",
        "delete_success": "削除しました: {name}",
        "queue_add_success": "曲をキューに追加しました",
        "queue_remove_success": "曲をキューから削除しました",
        "queue_clear_success": "キューをクリアしました",
        "queue_mode_enabled": "キューモードを有効にしました",
        "queue_mode_disabled": "キューモードを無効にしました",
        "auto_sustain_enabled": "自動サステインを有効にしました。ノートは自動的に持続します。",
        "auto_sustain_disabled": "自動サステインを無効にしました。ディレイスライダーでノートの長さを調整してください。",
        "humanizer_enabled": "ヒューマナイザーを有効にしました - ノートにわずかな時間差が生じます",
        "humanizer_disabled": "ヒューマナイザーを無効にしました",
        "always_on_top_on": "常に手前に表示: オン",
        "always_on_top_off": "常に手前に表示: オフ",
        "always_on_top_enabled": "常に手前に表示を有効にしました",
        "always_on_top_disabled": "常に手前に表示を無効にしました",
        "language": "日本語"
    }
}

# Default language
current_language = "en"

# Function to get translated text
def _(key, **kwargs):
    """Get translated text for the given key in the current language"""
    if current_language in TRANSLATIONS and key in TRANSLATIONS[current_language]:
        text = TRANSLATIONS[current_language][key]
        # Format the text with the provided kwargs if any
        if kwargs:
            return text.format(**kwargs)
        return text
    # Fallback to English
    if key in TRANSLATIONS["en"]:
        text = TRANSLATIONS["en"][key]
        if kwargs:
            return text.format(**kwargs)
        return text
    # If key doesn't exist, return the key itself
    return key

# Function to switch language
def switch_language(lang):
    """Switch the application language and update all UI elements"""
    global current_language
    if lang in TRANSLATIONS:
        current_language = lang
        update_ui_language()
        return True
    return False

# Define the update_ui_language function that updates all UI text when language changes
def update_ui_language():
    """Update all UI text elements to the current language"""
    # Update window title
    root.title(_("app_title"))
    
    # Update header
    app_title.config(text=_("app_title"))
    app_subtitle.config(text=_("app_subtitle"))
    load_button.config(text=_("load_music"))
    
    # Update sidebar
    sidebar_title.config(text=_("sidebar_title"))
    sidebar_subtitle.config(text=_("sidebar_subtitle"))
    
    # Update search placeholder if it's the default
    if search_entry.get() == "Search songs..." or search_entry.get() == "搜索歌曲...":
        search_entry.delete(0, "end")
        search_entry.insert(0, _("search_placeholder"))
    
    # Update Now Playing section
    now_playing_title.config(text=_("now_playing"))
    if current_song_label.cget("text") == "No song loaded" or current_song_label.cget("text") == "未加载歌曲":
        current_song_label.config(text=_("no_song_loaded"))
    
    # Update playback controls
    play_button.config(text=_("play_pause"))
    stop_button.config(text=_("stop"))
    
    # Update settings section
    settings_title.config(text=_("playback_settings"))
    
    # Update auto-sustain checkbox
    if auto_sustain:
        auto_sustain_checkbox.config(text=_("auto_sustain_on"))
    else:
        auto_sustain_checkbox.config(text=_("auto_sustain_off"))
    
    # Update humanizer checkbox
    if humanizer_enabled:
        humanizer_checkbox.config(text=_("humanizer_on"))
    else:
        humanizer_checkbox.config(text=_("humanizer_off"))
    
    # Update humanizer settings
    humanizer_strength_label.config(text=_("humanize_amount"))
    humanizer_strength_value.config(text=f"{humanizer_strength} {_('ms')}")
    
    # Update queue checkbox
    if queue_enabled:
        queue_checkbox.config(text=_("queue_mode_on"))
    else:
        queue_checkbox.config(text=_("queue_mode_off"))
    
    # Update always on top checkbox
    if always_on_top:
        always_on_top_checkbox.config(text=_("always_on_top_on"))
    else:
        always_on_top_checkbox.config(text=_("always_on_top_off"))

    # Update speed settings
    speed_label.config(text=_("playback_speed"))
    update_speed_label(speed_slider.get())  # This will refresh the speed label text
    
    # Update delay settings
    delay_title.config(text=_("note_delay"))
    update_delay_label(delay_slider.get())  # This will refresh the delay label text
    
    # Update queue management section
    if queue_enabled:
        queue_title.config(text=_("queue_management"))
        prev_queue_btn.config(text=_("previous"))
        next_queue_btn.config(text=_("next"))
        clear_queue_btn.config(text=_("clear_queue"))
        update_queue_display()  # This will refresh all queue items
    
    # Update keyboard shortcuts section
    keyboard_title.config(text=_("keyboard_shortcuts"))
    f1_desc.config(text=_("play_pause_desc"))
    f2_desc.config(text=_("stop_desc"))
    
    # Update sidebar items
    update_sidebar()

# Update the speed_label formatting function to use translations
def update_speed_label(val):
    val_float = float(val)
    if val_float < -0.33:
        # Slower
        slowdown = int(abs(val_float) * 100)
        label_text = f"{slowdown}{_('slower')}"
    elif val_float > 0.33:
        # Faster
        speedup = int(val_float * 100)
        label_text = f"{speedup}{_('faster')}"
    else:
        label_text = _("normal_speed")
    speed_value_label.config(text=label_text)

# Update the delay_label formatting function to use translations
def update_delay_label(val):
    val_float = float(val)
    delay_value_label.config(text=f"{val_float:.2f} {_('seconds')}")
    # Also update the global delay variable
    global delay
    delay = val_float

SAVED_SONGS_FILE = "saved_songs.json"
LAST_LOADED_SONG_FILE = "last_loaded_song.json"

# Global variables
delay = 0.030
auto_sustain = True
speed = 0
hotkey = "F1"
humanizer_enabled = False
humanizer_strength = 10  # Milliseconds of maximum random variation
queue_enabled = True
always_on_top = False # New global variable for always on top
play_queue = []  # List to hold song IDs in the queue
current_queue_index = -1  # Current position in the queue

# Define the key mapping
keyMapping = {
    "1Key0": "y", "1Key1": "u", "1Key2": "i", "1Key3": "o", "1Key4": "p",
    "1Key5": "h", "1Key6": "j", "1Key7": "k", "1Key8": "l", "1Key9": ";",
    "1Key10": "n", "1Key11": "m", "1Key12": ",", "1Key13": ".", "1Key14": "/",
    "2Key0": "y", "2Key1": "u", "2Key2": "i", "2Key3": "o", "2Key4": "p",
    "2Key5": "h", "2Key6": "j", "2Key7": "k", "2Key8": "l", "2Key9": ";",
    "2Key10": "n", "2Key11": "m", "2Key12": ",", "2Key13": ".", "2Key14": "/"
}

saved_music = []
is_playing = False
current_note_index = 0
play_event = threading.Event()
stop_event = threading.Event()
pause_event = threading.Event()
player_thread = None

# Minimalist Zinc Gray Color Palette
COLOR_BG = "#27272A"  # Zinc 800 - Main background
COLOR_SECONDARY_BG = "#3F3F46"  # Zinc 700 - Sidebar, cards, secondary elements
COLOR_FG = "#FAFAFA"  # Zinc 50 - Primary text
COLOR_ACCENT = "#A1A1AA"  # Zinc 400 - Accent for titles, active states, highlights
COLOR_ACCENT_SECONDARY = "#71717A"  # Zinc 600 - Lighter accent for hover/pressed
COLOR_HOVER = "#52525B"  # Zinc 600 - Hover effect for interactive elements
COLOR_SUCCESS = "#4CAF50"  # Green for success
COLOR_WARNING = "#FFC107"  # Amber for warnings
COLOR_ERROR = "#F44336"  # Red for errors
COLOR_BUTTON_BG = "#52525B"  # Zinc 600 - Button background
COLOR_BUTTON_FG = "#FAFAFA"  # Zinc 50 - Button text
COLOR_BORDER = "#3F3F46"  # Zinc 700 - Border color
COLOR_CARD_BG = "#3F3F46"  # Zinc 700 - Card/panel background
COLOR_INACTIVE = "#A1A1AA"  # Zinc 400 - Inactive element color

# Function to release all keys
def release_all_keys():
    for key in "yuiop;hjkl,./nm":
        keyboard.release(key)

def toggle_play_pause():
    global is_playing, player_thread
    if not is_playing:
        # Start playing
        play_loaded_music()
    else:
        # Pause
        pause_music()

def stop_music_wrapper():
    global is_playing, current_note_index, speed, player_thread
    
    # Prevent duplicate calls - return immediately if not playing
    if not is_playing:
        return
    
    # Set the stop event which will be checked by the player thread
    stop_event.set()
    # Wait briefly to ensure thread sees the event
    time_module.sleep(0.1)
    # Update UI
    play_status_label.config(text=_("status_stopped"), foreground=COLOR_INACTIVE)
    # Reset state
    is_playing = False
    current_note_index = 0
    speed = 0
    speed_slider.set(0)
    # Release all pressed keys
    release_all_keys()
    
    # If the thread is still running, join it with a timeout
    if player_thread and player_thread.is_alive():
        player_thread.join(0.5)
    
    # Reset events
    stop_event.clear()
    play_event.clear()
    pause_event.clear()

# Clear any existing hotkeys
try:
    # Try to remove individual hotkeys instead of all at once
    try:
        keyboard.remove_hotkey("F1")
        print("F1 hotkey removed successfully.")
    except:
        pass
    
    try:
        keyboard.remove_hotkey("F2")
        print("F2 hotkey removed successfully.")
    except:
        pass
except Exception as e:
    print(f"Error removing hotkeys: {e}")

# Add new hotkeys
try:
    keyboard.add_hotkey("F1", toggle_play_pause)
    keyboard.add_hotkey("F2", stop_music_wrapper)
    print("Hotkeys added successfully.")
except Exception as e:
    print(f"Error adding hotkeys: {e}")
    messagebox.showwarning("Hotkey Warning", "Could not register keyboard shortcuts. You may still use the buttons.")

def player_thread_func(notes):
    global current_note_index, is_playing, speed
    
    # Safety check for empty notes
    if not notes or len(notes) == 0:
        print("No notes to play")
        is_playing = False
        root.after(0, lambda: play_status_label.config(text=_("status_error"), foreground=COLOR_ERROR))
        return
    
    # Check if we're dealing with the old format (list of integers)
    if isinstance(notes[0], int):
        # Convert old format to new format
        converted_notes = []
        for i in range(0, len(notes), 2):
            if i + 1 < len(notes):
                key = f"1Key{notes[i] % 15}"
                note_time = notes[i + 1] if notes[i + 1] >= 0 else -notes[i + 1]
                converted_notes.append({"key": key, "time": note_time})
        notes = converted_notes

    time_threshold = 20  # Threshold in milliseconds for grouping notes
    note_groups = []
    current_group = []

    # Group notes by their time, considering a time threshold for grouping
    for note in notes:
        note_time = note['time']
        if not current_group or note_time - current_group[-1]['time'] <= time_threshold:
            current_group.append(note)
        else:
            note_groups.append(current_group)
            current_group = [note]
    if current_group:
        note_groups.append(current_group)

    start_time = time_module.time()  # Record the start time
    current_note_index = 0
    paused_elapsed = 0  # Track elapsed time when paused

    while current_note_index < len(note_groups):
        # Check for stop request
        if stop_event.is_set():
            release_all_keys()
            return
        
        # Check for pause
        if pause_event.is_set():
            if not paused_elapsed:
                paused_elapsed = time_module.time() - start_time
            time_module.sleep(0.1)  # Sleep while paused
            continue
        
        # If we were paused and now resumed, adjust the start time
        if paused_elapsed > 0:
            start_time = time_module.time() - paused_elapsed
            paused_elapsed = 0
        
        # Current note group
        group = note_groups[current_note_index]
        group_times = [note['time'] for note in group]
        current_time = min(group_times) / 1000  # Convert to seconds
        
        # Get current speed - make sure to get it on each iteration
        speed = speed_slider.get()
        
        # Calculate time adjustment based on speed
        speed_factor = 1.0
        if speed > 0:
            # Faster: reduce the effective time (speeds up playback)
            speed_factor = 1.0 - (speed * 0.5)  # At max speed (1.0), time is halved
        elif speed < 0:
            # Slower: increase the effective time (slows down playback)
            speed_factor = 1.0 + (abs(speed) * 0.5)  # At min speed (-1.0), time is 1.5x
        
        # Apply speed factor to calculate how much time should have passed
        adjusted_current_time = current_time * speed_factor
        
        # Calculate wait time based on adjusted time
        elapsed_time = time_module.time() - start_time
        wait_time = adjusted_current_time - elapsed_time

        # Wait if needed
        if wait_time > 0:
            time_module.sleep(wait_time)
        
        # Check again for stop/pause after waiting
        if stop_event.is_set():
            release_all_keys()
            return
        if pause_event.is_set():
            if not paused_elapsed:
                paused_elapsed = time_module.time() - start_time
            continue

        # Press all keys for the current time group
        keys_to_press = set(keyMapping.get(note['key']) for note in group if keyMapping.get(note['key']))
        
        # Apply humanizer if enabled - press keys with slight random timing differences
        if humanizer_enabled and len(keys_to_press) > 1:
            # Convert to list to maintain order for consistent randomization
            keys_list = list(keys_to_press)
            
            # Randomize the order slightly for more human-like playing
            if random.random() < 0.3:  # 30% chance to change order
                random.shuffle(keys_list)
            
            # Press each key with a small random delay
            for key in keys_list:
                keyboard.press(key)
                if len(keys_list) > 1:  # Only add delay if there are multiple keys
                    # Random delay between key presses (0-X ms based on humanizer strength)
                    random_delay = random.uniform(0, humanizer_strength / 1000.0)
                    time_module.sleep(random_delay)
        else:
            # Standard key press (all at once)
            for key in keys_to_press:
                keyboard.press(key)

        # Calculate the delay for the next group of notes
        if current_note_index < len(note_groups) - 1:
            next_group = note_groups[current_note_index + 1]
            next_times = [note['time'] for note in next_group]
            next_time = min(next_times) / 1000
            note_delay = next_time - current_time
        else:
            note_delay = delay_slider.get()

        # Apply speed adjustment to the delay
        note_delay = note_delay * speed_factor
        
        # Adjust for auto-sustain
        if auto_sustain:
            # Hold the notes slightly less than the full delay
            sustain_time = max(0.02, note_delay - 0.01)  # At least 20ms, with 10ms gap
            time_module.sleep(sustain_time)
        else:
            # Use the manual delay setting
            manual_delay = delay_slider.get()
            time_module.sleep(manual_delay)
        
        # Check for stop/pause after delay
        if stop_event.is_set():
            release_all_keys()
            return
        
        # Release keys with humanized timing if enabled
        if humanizer_enabled and len(keys_to_press) > 1:
            # Convert to list to maintain order
            keys_list = list(keys_to_press)
            
            # Randomize the release order slightly for more human-like playing
            if random.random() < 0.4:  # 40% chance to change release order
                random.shuffle(keys_list)
            
            # Release each key with a small random delay
            for key in keys_list:
                keyboard.release(key)
                if len(keys_list) > 1:  # Only add delay if there are multiple keys
                    # Random delay between key releases (0-X ms based on humanizer strength)
                    random_delay = random.uniform(0, humanizer_strength / 1000.0)
                    time_module.sleep(random_delay)
        else:
            # Standard key release (all at once)
            for key in keys_to_press:
                keyboard.release(key)

        # Move to the next group
        current_note_index += 1
        
    # After all notes are played
    is_playing = False
    
    # Check if we should play the next song in queue
    if queue_enabled and current_queue_index < len(play_queue) - 1:
        # Schedule the next song to play after a short delay
        # Avoid triggering immediate UI updates that could cause refresh loops
        root.after(500, play_next_in_queue)
    else:
        if queue_enabled and len(play_queue) > 0:
            # Show a status message to indicate queue has finished
            root.after(100, lambda: play_status_label.config(text=_("status_queue_finished"), foreground=COLOR_INACTIVE))
        else:
            # Update UI to show finished state - use root.after to avoid refresh loops
            root.after(100, lambda: play_status_label.config(text=_("status_finished"), foreground=COLOR_INACTIVE))

def play_music(notes):
    global current_note_index, is_playing, player_thread
    
    # Stop any existing playback
    if is_playing:
        stop_music_wrapper()
    
    # Reset state
    is_playing = True
    play_event.set()
    stop_event.clear()
    pause_event.clear()
    
    # Start a new thread for playback
    player_thread = threading.Thread(target=player_thread_func, args=(notes,))
    player_thread.daemon = True
    player_thread.start()

def play_loaded_music():
    global loaded_notes, is_playing
    if loaded_notes is not None:
        play_music(loaded_notes)
        # Update the status text
        play_status_label.config(text=_("status_playing"), foreground=COLOR_SUCCESS)
        is_playing = True
    else:
        # No song loaded - show an error message
        play_status_label.config(text=_("status_no_song"), foreground=COLOR_ERROR)
        show_status_message(_("no_song_loaded"), "error")

def pause_music():
    global is_playing
    if is_playing:
        if pause_event.is_set():
            # Resume
            pause_event.clear()
            play_status_label.config(text=_("status_playing"), foreground=COLOR_SUCCESS)
        else:
            # Pause
            pause_event.set()
            play_status_label.config(text=_("status_paused"), foreground=COLOR_WARNING)
            # Release all keys when pausing
            release_all_keys()

def stop_music():
    global is_playing, current_note_index, speed
    # Use the wrapper function
    stop_music_wrapper()

def play_or_pause_music():
    toggle_play_pause()

loaded_notes = None

def detect_encoding(file_path):
    with open(file_path, 'rb') as file:
        raw_data = file.read()
        result = chardet.detect(raw_data)
        return result['encoding']

def load_music_from_file():
    global loaded_notes, saved_music
    success_count = 0
    failure_count = 0
    
    try:
        file_types = [("SkySheet Files", "*.skysheet"), ("JSON Files", "*.json"), ("Text Files", "*.txt")]
        file_paths = filedialog.askopenfilenames(filetypes=file_types)
        if file_paths:
            for file_path in file_paths:
                try:
                    encoding = detect_encoding(file_path)
                    with open(file_path, 'r', encoding=encoding) as file:
                        data = json.load(file)
                    
                    if isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict):
                        song_data = data[0]
                        if 'songNotes' in song_data:
                            loaded_notes = song_data['songNotes']
                            
                            # Generate an ID if it doesn't exist
                            if 'id' not in song_data:
                                song_data['id'] = str(uuid.uuid4())
                            
                            # Use 'name' if it exists, otherwise use the filename
                            song_name = song_data.get('name', os.path.basename(file_path))
                            song_data['name'] = song_name

                            # Check if it's the old format and convert if necessary
                            if isinstance(loaded_notes[0], int):
                                song_data['oldFormat'] = True
                            else:
                                song_data['oldFormat'] = False

                            save_music_result = save_music(song_data, file_path)
                            if save_music_result:
                                # Explicitly set last loaded song
                                load_music(song_data)
                                # Reload saved songs and update sidebar
                                load_saved_songs()
                                success_count += 1
                            else:
                                failure_count += 1
                                show_status_message(f"Song '{song_name}' already exists in library", "warning")
                        else:
                            failure_count += 1
                            show_status_message(f"Invalid SkySheet file: Missing notes data", "error")
                    else:
                        failure_count += 1
                        show_status_message(f"Invalid SkySheet file format", "error")
                except (UnicodeDecodeError, json.JSONDecodeError) as e:
                    failure_count += 1
                    show_status_message(f"Failed to decode file: {str(e)[:50]}...", "error")
    except FileNotFoundError as e:
        show_status_message(f"Error loading music: {str(e)}", "error")
    
    # Show a summary notification if multiple files were loaded
    if success_count > 0 and failure_count > 0:
        show_status_message(f"Loaded {success_count} songs, {failure_count} failed", "info")
    elif success_count > 1:
        show_status_message(f"Successfully loaded {success_count} songs", "success")
    # For single file success, the load_music function already shows a notification

def save_music(song_data, file_path):
    global loaded_notes
    if os.path.exists(SAVED_SONGS_FILE):
        with open(SAVED_SONGS_FILE, "r") as file:
            saved_songs = json.load(file)
    else:
        saved_songs = []

    # Check for duplicate song name or ID
    for song in saved_songs:
        if song["name"] == song_data["name"] or song["id"] == song_data["id"]:
            return False  # Song already exists

    saved_songs.append(song_data)

    with open(SAVED_SONGS_FILE, "w") as file:
        json.dump(saved_songs, file, indent=4)

    # Save the last loaded song to a separate file
    last_loaded_song = {
        "name": song_data["name"],
        "id": song_data["id"],
        "file_path": file_path
    }
    with open(LAST_LOADED_SONG_FILE, "w") as file:
        json.dump(last_loaded_song, file, indent=4)

    return True
    
def load_saved_songs():
    if os.path.exists(SAVED_SONGS_FILE):
        with open(SAVED_SONGS_FILE, 'r') as f:
            global saved_music
            saved_music = json.load(f)
            update_sidebar(saved_music)

def show_error_message(message):
    error_window = tk.Toplevel(root)
    error_window.title("Error")
    error_window.configure(bg=COLOR_BG)
    error_window.grab_set()  # Make the window modal
    
    # Center the error window on the main window
    window_width = 300
    window_height = 150
    position_x = root.winfo_x() + (root.winfo_width() // 2) - (window_width // 2)
    position_y = root.winfo_y() + (root.winfo_height() // 2) - (window_height // 2)
    error_window.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")
    
    frame = ttk.Frame(error_window, style="Dialog.TFrame")
    frame.pack(fill="both", expand=True, padx=15, pady=15)
    
    error_label = ttk.Label(frame, text=message, style="Dialog.TLabel", wraplength=250)
    error_label.pack(pady=(0, 20))
    
    ok_button = ttk.Button(frame, text="OK", command=error_window.destroy, style="Accent.TButton", width=10)
    ok_button.pack()

def load_music(notes):
    global loaded_notes, current_loaded_song_id
    loaded_notes = notes['songNotes']
    
    # Check if we're loading the same song - no need to update UI
    same_song = current_loaded_song_id == notes.get('id', '')
    
    # Store the current song ID for highlighting in sidebar
    current_loaded_song_id = notes.get('id', '')
    
    with open(LAST_LOADED_SONG_FILE, 'w') as f:
        json.dump(notes, f)
    
    # Update the current song display
    current_song_label.config(text=f"{notes.get('name', 'Unnamed Song')}")
    
    # Reset play status
    play_status_label.config(text=_("status_ready"), foreground=COLOR_INACTIVE)
    
    # Show status message
    show_status_message(_("load_success", name=notes.get('name', 'Unnamed Song')), "success")
    
    # Only update sidebar if we're loading a different song
    if not same_song:
        update_sidebar()

def load_last_song():
    if os.path.exists(LAST_LOADED_SONG_FILE):
        with open(LAST_LOADED_SONG_FILE, 'r') as f:
            music = json.load(f)
            load_music(music)

def delete_music(index):
    global saved_music
    if index < len(saved_music):
        song_name = saved_music[index].get("name", "Unnamed Song")
        del saved_music[index]
        with open(SAVED_SONGS_FILE, 'w') as f:
            json.dump(saved_music, f)
        update_sidebar()
        show_status_message(f"Deleted: {song_name}", "warning")

def load_specific_sidebar_music(frame):
    song = getattr(frame, "song", None)
    if song:
        load_music(song)

def add_to_queue_from_sidebar(frame):
    song = getattr(frame, "song", None)
    if song:
        song_id = song.get('id', '')
        if song_id:
            add_to_queue(song_id)

def delete_specific_sidebar_music(frame):
    song = getattr(frame, "song", None)
    if song:
        song_id = song.get('id', '')
        if song_id:
            delete_song_by_id(song_id)

def search_songs(event=None):
    # Reset the canvas scroll position to the top when searching
    canvas.yview_moveto(0)
    # The actual filtering is now done in the update_sidebar function
    update_sidebar()

def load_sidebar_music(index, current_songs=None):
    songs_to_use = current_songs if current_songs is not None else saved_music
    if index < len(songs_to_use):
        music = songs_to_use[index]
        load_music(music)

def toggle_auto_sustain(state):
    global auto_sustain
    auto_sustain = state
    
    # Update UI based on auto_sustain state
    if auto_sustain:
        delay_frame.grid_forget()
        auto_sustain_checkbox.configure(text=_("auto_sustain_on"))
    else:
        delay_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=5)
        auto_sustain_checkbox.configure(text=_("auto_sustain_off"))
    
    # Update status message
    if auto_sustain:
        show_status_message(_("auto_sustain_enabled"), "info")
    else:
        show_status_message(_("auto_sustain_disabled"), "info")

def show_status_message(message, message_type="info"):
    """Display a status message in the status bar with appropriate styling"""
    status_label.config(text=message)
    if message_type == "success":
        status_frame.configure(style="Success.TFrame")
        status_label.configure(style="Success.TLabel")
    elif message_type == "error":
        status_frame.configure(style="Error.TFrame")
        status_label.configure(style="Error.TLabel")
    elif message_type == "warning":
        status_frame.configure(style="Warning.TFrame")
        status_label.configure(style="Warning.TLabel")
    else:
        status_frame.configure(style="Status.TFrame")
        status_label.configure(style="Status.TLabel")
    
    # Make the status message visible
    status_frame.pack(fill="x", padx=30, pady=(0, 10))
    
    # Determine display duration based on message type and content
    display_time = 3000  # Default: 3 seconds
    
    # Longer display time for errors and warnings
    if message_type == "error" or message_type == "warning":
        display_time = 5000  # 5 seconds
    
    # Even longer for loading-related messages (they typically show file info)
    if "loaded" in message.lower() or "failed" in message.lower() or "invalid" in message.lower():
        display_time = 6000  # 6 seconds
    
    # Schedule the message to disappear
    root.after(display_time, lambda: status_frame.pack_forget())

def play_next_in_queue():
    """Play the next song in the queue"""
    global current_queue_index, play_queue
    
    if not queue_enabled or not play_queue:
        return
    
    # Move to the next song in queue
    current_queue_index += 1
    
    # Check if we've reached the end of the queue
    if current_queue_index >= len(play_queue):
        current_queue_index = len(play_queue) - 1
        play_status_label.config(text=_("status_queue_finished"), foreground=COLOR_INACTIVE)
        return
    
    # Get the song ID of the next song in queue
    song_id = play_queue[current_queue_index]
    
    # Find the song in the saved_music list
    for song in saved_music:
        if song.get('id', '') == song_id:
            # Load and play the song
            load_music(song)
            play_loaded_music()
            # Update queue display
            update_queue_display()
            return
    
    # If we get here, the song was not found
    show_status_message(f"Song ID {song_id} not found in library", "error")

def play_previous_in_queue():
    """Play the previous song in the queue"""
    global current_queue_index, play_queue
    
    if not queue_enabled or not play_queue:
        return
    
    # Move to the previous song in queue
    current_queue_index -= 1
    
    # Check if we've reached the beginning of the queue
    if current_queue_index < 0:
        current_queue_index = 0
        show_status_message("Already at the beginning of the queue", "info")
        return
    
    # Get the song ID of the previous song in queue
    song_id = play_queue[current_queue_index]
    
    # Find the song in the saved_music list
    for song in saved_music:
        if song.get('id', '') == song_id:
            # Load and play the song
            load_music(song)
            play_loaded_music()
            # Update queue display
            update_queue_display()
            return
    
    # If we get here, the song was not found
    show_status_message(f"Song ID {song_id} not found in library", "error")

def add_to_queue(song_id):
    """Add a song to the queue"""
    global play_queue
    
    # Check if the song exists in the library
    song_exists = False
    song_name = "Unknown Song"
    for song in saved_music:
        if song.get('id', '') == song_id:
            song_exists = True
            song_name = song.get("name", "Unknown Song")
            break
    
    if not song_exists:
        show_status_message("Cannot add song to queue - song not found", "error")
        return False
    
    # Add the song to the queue
    play_queue.append(song_id)
    
    # Update the queue display
    update_queue_display()
    show_status_message(f"Added to queue: {song_name}", "success")
    return True

def remove_from_queue(index):
    """Remove a song from the queue"""
    global play_queue, current_queue_index
    
    if index < 0 or index >= len(play_queue):
        show_status_message("Invalid queue index", "error")
        return False
    
    # Remove the song from the queue
    removed_id = play_queue.pop(index)
    
    # Adjust the current index if needed
    if current_queue_index >= index:
        current_queue_index = max(0, current_queue_index - 1)
    
    # Update the queue display
    update_queue_display()
    show_status_message(_("queue_remove_success"), "info")
    return True

def clear_queue():
    """Clear the entire queue"""
    global play_queue, current_queue_index
    
    # Clear the queue
    play_queue = []
    current_queue_index = -1
    
    # Update the queue display
    update_queue_display()
    show_status_message(_("queue_clear_success"), "info")

def toggle_queue():
    """Toggle queue mode on/off"""
    global queue_enabled
    queue_enabled = not queue_enabled
    
    # Update UI
    queue_var.set(queue_enabled)
    if queue_enabled:
        queue_checkbox.configure(text=_("queue_mode_on"))
        show_status_message(_("queue_mode_enabled"), "success")
    else:
        queue_checkbox.configure(text=_("queue_mode_off"))
        show_status_message(_("queue_mode_disabled"), "info")
    
    # Update the queue display
    update_queue_display()

def update_queue_display():
    """Update the queue list display"""
    # Clear existing items in the queue display
    for widget in queue_list_frame.winfo_children():
        widget.destroy()
    
    if not play_queue:
        # No songs in queue
        empty_label = ttk.Label(queue_list_frame, text=_("queue_empty"), style="TLabel", foreground=COLOR_INACTIVE)
        empty_label.pack(pady=10, padx=10)
        return
    
    # Add a heading to show which song is next
    if current_queue_index < len(play_queue) - 1:
        next_song_id = play_queue[current_queue_index + 1]
        next_song_name = "Unknown Song"
        for song in saved_music:
            if song.get('id', '') == next_song_id:
                next_song_name = song.get('name', "Unknown Song")
                break
        
        next_song_heading = ttk.Label(queue_list_frame, text=f"Next: {next_song_name}", 
                                    style="TLabel", foreground=COLOR_SUCCESS, font=('Segoe UI', 9, 'bold'))
        next_song_heading.pack(fill="x", pady=(0, 10), padx=5)
    
    # Add each song in the queue to the display
    for i, song_id in enumerate(play_queue):
        # Find the song in the saved_music list
        song_name = "Unknown Song"
        for song in saved_music:
            if song.get('id', '') == song_id:
                song_name = song.get('name', f"Song {i+1}")
                break
        
        # Create a frame for each queue item
        item_frame = ttk.Frame(queue_list_frame, style="Card.TFrame")
        item_frame.pack(fill="x", padx=5, pady=2)
        
        # Indicate if this is the current song
        prefix = "▶ " if i == current_queue_index else f"{i+1}. "
        color = COLOR_SUCCESS if i == current_queue_index else COLOR_FG
        
        # Create a container for the song info
        info_frame = ttk.Frame(item_frame, style="Card.TFrame")
        info_frame.pack(side="left", fill="x", expand=True, padx=5, pady=5)
        
        # Display the song name
        song_label = ttk.Label(info_frame, text=prefix + song_name, style="TLabel", foreground=color)
        song_label.pack(side="left")
        
        # Add buttons container on the right
        buttons_frame = ttk.Frame(item_frame, style="Card.TFrame")
        buttons_frame.pack(side="right", padx=5, pady=5)
        
        # Add up/down buttons
        if i > 0:
            up_btn = ttk.Button(buttons_frame, text="▲", width=2, 
                              command=lambda idx=i: move_up_in_queue(idx),
                              style="TButton")
            up_btn.pack(side="left", padx=2)
        
        if i < len(play_queue) - 1:
            down_btn = ttk.Button(buttons_frame, text="▼", width=2, 
                                command=lambda idx=i: move_down_in_queue(idx),
                                style="TButton")
            down_btn.pack(side="left", padx=2)
        
        # Add a remove button
        remove_btn = ttk.Button(buttons_frame, text="✕", width=2, 
                              command=lambda idx=i: remove_from_queue(idx),
                              style="Error.TButton")
        remove_btn.pack(side="left", padx=2)

def toggle_humanizer():
    """Toggle humanizer mode on/off"""
    global humanizer_enabled
    humanizer_enabled = not humanizer_enabled
    
    # Update UI
    humanizer_var.set(humanizer_enabled)
    if humanizer_enabled:
        humanizer_checkbox.configure(text=_("humanizer_on"))
        humanizer_strength_frame.pack(fill="x", padx=10, pady=(5, 10))
        show_status_message(_("humanizer_enabled"), "success")
    else:
        humanizer_checkbox.configure(text=_("humanizer_off"))
        humanizer_strength_frame.pack_forget()
        show_status_message(_("humanizer_disabled"), "info")

def update_humanizer_strength(val):
    """Update the humanizer strength value"""
    global humanizer_strength
    strength = int(float(val))
    humanizer_strength = strength
    humanizer_strength_value.config(text=f"{strength} {_('ms')}")

def toggle_always_on_top():
    """Toggle always on top mode for the main window"""
    global always_on_top
    always_on_top = not always_on_top
    root.wm_attributes("-topmost", always_on_top)
    
    # Update UI
    always_on_top_var.set(always_on_top)
    if always_on_top:
        always_on_top_checkbox.configure(text=_("always_on_top_on"))
        show_status_message(_("always_on_top_enabled"), "success")
    else:
        always_on_top_checkbox.configure(text=_("always_on_top_off"))
        show_status_message(_("always_on_top_disabled"), "info")

# UI setup
root = tk.Tk()
root.title("SkyMusic Player")
root.config(bg=COLOR_BG)
root.geometry("800x600") # Set a larger default window size
root.resizable(True, True) # Make window resizable

# Use the ei.ico file directly instead of base64 encoded icon
icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ei.ico")
if os.path.exists(icon_path):
    root.iconbitmap(icon_path)
else:
    print("Warning: Icon file 'ei.ico' not found.")

icon_data = ''

# Configure ttk styles for a modern, sleek dark enterprise look
style = ttk.Style()
style.theme_use('clam')

# Base styles
style.configure("TFrame", background=COLOR_BG)
style.configure("TButton", background=COLOR_BUTTON_BG, foreground=COLOR_BUTTON_FG, 
                padding=(8, 4), font=('Segoe UI', 9), relief="flat", borderwidth=0)
style.map("TButton", 
          background=[('active', COLOR_HOVER), ('pressed', COLOR_ACCENT)],
          foreground=[('pressed', COLOR_BUTTON_FG)])
style.configure("TLabel", background=COLOR_BG, foreground=COLOR_FG, 
                padding=2, font=('Segoe UI', 9))
style.configure("TEntry", fieldbackground=COLOR_SECONDARY_BG, foreground=COLOR_FG, 
                padding=4, font=('Segoe UI', 9), borderwidth=0, relief="flat")
style.map("TEntry", 
          fieldbackground=[('focus', COLOR_SECONDARY_BG)],
          bordercolor=[('focus', COLOR_ACCENT)])
style.configure("Vertical.TScrollbar", background=COLOR_SECONDARY_BG, 
                troughcolor=COLOR_BG, bordercolor=COLOR_SECONDARY_BG, 
                arrowcolor=COLOR_FG, relief="flat", borderwidth=0)
style.map("Vertical.TScrollbar", 
          background=[('active', COLOR_ACCENT), ('pressed', COLOR_ACCENT_SECONDARY)])
style.configure("TCheckbutton", background=COLOR_BG, foreground=COLOR_FG, 
                font=('Segoe UI', 9))
style.map("TCheckbutton", 
          background=[('active', COLOR_BG)],
          indicatorcolor=[('selected', COLOR_ACCENT)])
style.configure("Horizontal.TScale", background=COLOR_BG, troughcolor=COLOR_SECONDARY_BG, 
                sliderlength=16, sliderthickness=10, borderwidth=0)
style.map("Horizontal.TScale", 
          background=[('active', COLOR_ACCENT)],
          troughcolor=[('active', COLOR_SECONDARY_BG)])

# Specialized button styles
style.configure("Accent.TButton", background=COLOR_ACCENT, foreground=COLOR_BUTTON_FG)
style.map("Accent.TButton", 
          background=[('active', COLOR_ACCENT_SECONDARY), ('pressed', COLOR_ACCENT)])
style.configure("Success.TButton", background=COLOR_SUCCESS, foreground=COLOR_BUTTON_FG)
style.map("Success.TButton", 
          background=[('active', "#35E073"), ('pressed', COLOR_SUCCESS)])
style.configure("Warning.TButton", background=COLOR_WARNING, foreground="#000000")
style.map("Warning.TButton", 
          background=[('active', "#FFE345"), ('pressed', COLOR_WARNING)])
style.configure("Error.TButton", background=COLOR_ERROR, foreground=COLOR_BUTTON_FG)
style.map("Error.TButton", 
          background=[('active', "#FF4D6B"), ('pressed', COLOR_ERROR)])

# Sidebar-specific styles
style.configure("Sidebar.TFrame", background=COLOR_SECONDARY_BG)
style.configure("Sidebar.TButton", background=COLOR_SECONDARY_BG, foreground=COLOR_FG, 
                padding=8, font=('Segoe UI', 9))
style.map("Sidebar.TButton", 
          background=[('active', COLOR_HOVER), ('pressed', COLOR_ACCENT)])
style.configure("Sidebar.TLabel", background=COLOR_SECONDARY_BG, foreground=COLOR_FG, 
                padding=5, font=('Segoe UI', 9))

# Selected item in sidebar
style.configure("Selected.Sidebar.TFrame", background=COLOR_HOVER, relief="flat")
style.configure("Selected.Sidebar.TLabel", background=COLOR_HOVER, foreground=COLOR_FG)

# Card styles for visual grouping
style.configure("Card.TFrame", background=COLOR_CARD_BG, relief="flat", borderwidth=0)

# Title and heading styles
style.configure("Title.TLabel", background=COLOR_BG, foreground=COLOR_FG, 
                font=('Segoe UI', 16, 'bold')) # Slightly larger for prominence
style.configure("Subtitle.TLabel", background=COLOR_BG, foreground=COLOR_FG, 
                font=('Segoe UI', 10, 'bold')) # Slightly smaller
style.configure("SectionTitle.TLabel", background=COLOR_BG, foreground=COLOR_ACCENT, 
                font=('Segoe UI', 11, 'bold')) # Slightly larger

# Status message styles
style.configure("Status.TFrame", background=COLOR_SECONDARY_BG)
style.configure("Status.TLabel", background=COLOR_SECONDARY_BG, foreground=COLOR_FG)
style.configure("Success.TFrame", background=COLOR_SUCCESS)
style.configure("Success.TLabel", background=COLOR_SUCCESS, foreground="#FFFFFF")
style.configure("Error.TFrame", background=COLOR_ERROR)
style.configure("Error.TLabel", background=COLOR_ERROR, foreground="#FFFFFF")
style.configure("Warning.TFrame", background=COLOR_WARNING)
style.configure("Warning.TLabel", background=COLOR_WARNING, foreground="#000000")

# Dialog styles
style.configure("Dialog.TFrame", background=COLOR_BG)
style.configure("Dialog.TLabel", background=COLOR_BG, foreground=COLOR_FG, 
                font=('Segoe UI', 10))

# Create main frames with better structure
main_container = ttk.Frame(root, style="TFrame")
main_container.pack(fill="both", expand=True)

# Configure main grid layout
main_container.grid_rowconfigure(0, weight=1)
main_container.grid_columnconfigure(0, weight=0)  # Sidebar doesn't expand
main_container.grid_columnconfigure(1, weight=1)  # Main content expands

# Create sidebar and main content frames
sidebar_frame = ttk.Frame(main_container, style="Sidebar.TFrame")
main_frame = ttk.Frame(main_container, style="TFrame")

# Pack main frames
sidebar_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5)) # Add some right padding to sidebar
main_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 0)) # Add some left padding to main frame

# Add a logo/title area at the top of the sidebar
sidebar_header = ttk.Frame(sidebar_frame, style="Sidebar.TFrame")
sidebar_header.pack(fill='x', pady=(10, 5))

sidebar_title = ttk.Label(sidebar_header, text=_("sidebar_title"), style="Sidebar.TLabel", 
                          font=('Segoe UI', 10, 'bold'))
sidebar_title.pack(fill='x', padx=10, pady=0)

sidebar_subtitle = ttk.Label(sidebar_header, text=_("sidebar_subtitle"), style="Sidebar.TLabel", 
                           font=('Segoe UI', 8), foreground=COLOR_ACCENT)
sidebar_subtitle.pack(fill='x', padx=10, pady=(0, 5))

# Add a separator below the title
title_separator = ttk.Separator(sidebar_frame, orient="horizontal")
title_separator.pack(fill='x', padx=10, pady=0)

# Create a search bar with modern styling
search_frame = ttk.Frame(sidebar_frame, style="Sidebar.TFrame")
search_frame.pack(fill='x', padx=10, pady=8)

search_var = tk.StringVar()
search_entry = ttk.Entry(search_frame, textvariable=search_var, style="TEntry")
search_entry.pack(side='left', fill='x', expand=True)
search_entry.bind("<KeyRelease>", search_songs)
search_entry.insert(0, _("search_placeholder"))
search_entry.bind("<FocusIn>", lambda e: search_entry.delete(0, "end") if search_entry.get() == _("search_placeholder") else None)
search_entry.bind("<FocusOut>", lambda e: search_entry.insert(0, _("search_placeholder")) if search_entry.get() == "" else None)

# Create a canvas in the sidebar frame
canvas = tk.Canvas(sidebar_frame, bg=COLOR_SECONDARY_BG, highlightthickness=0)
canvas.pack(side="left", fill="both", expand=True, padx=0, pady=(0, 0))

# Add a scrollbar to the canvas
scrollbar = ttk.Scrollbar(sidebar_frame, orient="vertical", command=canvas.yview, style="Vertical.TScrollbar")
scrollbar.pack(side="right", fill="y")
canvas.configure(yscrollcommand=scrollbar.set)

# Create a frame inside the canvas to contain sidebar content
sidebar_inner_frame = ttk.Frame(canvas, style="Sidebar.TFrame")
canvas_window = canvas.create_window((0, 0), window=sidebar_inner_frame, anchor="nw", width=canvas.winfo_reqwidth())

# Bind the scrollbar to the canvas
sidebar_inner_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

# Make the canvas expand with the window
def on_window_resize(event):
    canvas.itemconfig(canvas_window, width=sidebar_frame.winfo_width())
    canvas.configure(scrollregion=canvas.bbox("all"))

canvas.bind('<Configure>', on_window_resize)

# Create a header for the main content area
header_frame = ttk.Frame(main_frame, style="TFrame")
header_frame.pack(fill="x", pady=(5, 5), padx=10)

app_title = ttk.Label(header_frame, text=_("app_title"), style="Title.TLabel")
app_title.pack(side="left")

app_subtitle = ttk.Label(header_frame, text=_("app_subtitle"), style="TLabel", foreground=COLOR_INACTIVE)
app_subtitle.pack(side="left", padx=(5, 0))

# Add language switcher dropdown to the right of the header
language_frame = ttk.Frame(header_frame, style="TFrame")
language_frame.pack(side="right", padx=(10, 0))

# Create a styled frame for the language selector
language_selector_frame = ttk.Frame(language_frame, style="Card.TFrame")
language_selector_frame.pack(side="right", padx=(5, 0))

# Map language codes to their display names
language_display = {
    "en": "ENGLISH",
    "zh": "中文",
    "es": "ESPAÑOL",
    "ja": "日本語"
}

language_var = tk.StringVar(value=current_language)

# Function to update language display name
def update_language_display(*args):
    lang = language_var.get()
    if lang in language_display:
        language_button.config(text=language_display[lang])

# Trace changes to the language variable
language_var.trace_add("write", update_language_display)

# Create a button that when clicked shows the dropdown
language_button = ttk.Button(
    language_selector_frame, 
    text=language_display[current_language],
    style="Language.TButton",
    width=10
)

# Define custom styling for the language button and dropdown
style.configure("Language.TButton", 
                background=COLOR_SECONDARY_BG, 
                foreground=COLOR_FG,
                padding=(5, 2),
                font=('Segoe UI', 9))
style.map("Language.TButton", 
          background=[('active', COLOR_HOVER), ('pressed', COLOR_ACCENT)])

# Function to show dropdown on button click
def show_language_dropdown(event=None):
    # Get position of button
    x = language_button.winfo_rootx()
    y = language_button.winfo_rooty() + language_button.winfo_height()
    
    # Create dropdown menu
    menu = tk.Menu(root, tearoff=0, bg=COLOR_SECONDARY_BG, fg=COLOR_FG, 
                  activebackground=COLOR_HOVER, activeforeground=COLOR_FG,
                  bd=0, relief="flat")
    
    # Add language options
    for lang_code, lang_name in language_display.items():
        menu.add_command(
            label=lang_name, 
            command=lambda lc=lang_code: set_language(lc),
            font=('Segoe UI', 9)
        )
    
    # Show the menu
    menu.tk_popup(x, y)

def set_language(lang_code):
    language_var.set(lang_code)
    switch_language(lang_code)

# Bind the button click to show dropdown
language_button.bind("<Button-1>", show_language_dropdown)
language_button.pack(side="right")

# Add load button to the right of the header
load_button = ttk.Button(header_frame, text=_("load_music"), command=load_music_from_file, style="Accent.TButton")
load_button.pack(side="right", padx=(0, 10))

# Main content area with cards layout
content_frame = ttk.Frame(main_frame, style="TFrame")
content_frame.pack(fill="both", expand=True, padx=10, pady=(0, 5))

# Now Playing section - Card 1
now_playing_card = ttk.Frame(content_frame, style="Card.TFrame")
now_playing_card.pack(fill="x", pady=(0, 8), ipady=4)

now_playing_title = ttk.Label(now_playing_card, text=_("now_playing"), style="SectionTitle.TLabel")

# Current song info display
current_song_frame = ttk.Frame(now_playing_card, style="Card.TFrame")
current_song_frame.pack(fill="x", padx=12, pady=(0, 5))

current_song_label = ttk.Label(current_song_frame, text=_("no_song_loaded"), style="TLabel", font=('Segoe UI', 10))
current_song_label.pack(anchor="w", padx=0, pady=2)

# Status indicator (playing/paused)
status_indicator_frame = ttk.Frame(now_playing_card, style="Card.TFrame")
status_indicator_frame.pack(fill="x", padx=12, pady=(0, 5))

play_status_label = ttk.Label(status_indicator_frame, text="▶ Ready", style="TLabel", foreground=COLOR_INACTIVE)
play_status_label.pack(side="left", padx=0, pady=2)

# Playback controls in a horizontal layout
playback_frame = ttk.Frame(now_playing_card, style="Card.TFrame")
playback_frame.pack(fill="x", padx=12, pady=5)

play_button = ttk.Button(playback_frame, text=_("play_pause"), command=toggle_play_pause, style="Success.TButton")
play_button.pack(side="left", padx=(0, 5))

stop_button = ttk.Button(playback_frame, text=_("stop"), command=stop_music, style="Error.TButton")
stop_button.pack(side="left")

# Settings section - Card 2
settings_card = ttk.Frame(content_frame, style="Card.TFrame")
settings_card.pack(fill="x", pady=(0, 8), ipady=8)

settings_title = ttk.Label(settings_card, text=_("playback_settings"), style="SectionTitle.TLabel")
settings_title.pack(anchor="w", padx=12, pady=(8, 5))

# Two-column grid for settings
settings_grid = ttk.Frame(settings_card, style="Card.TFrame")
settings_grid.pack(fill="x", padx=12, pady=5)
settings_grid.columnconfigure(0, weight=1)
settings_grid.columnconfigure(1, weight=1)

# Auto sustain checkbox with modern styling
auto_sustain_var = tk.BooleanVar(value=auto_sustain)
auto_sustain_frame = ttk.Frame(settings_grid, style="Card.TFrame")
auto_sustain_frame.grid(row=0, column=0, sticky="ew", padx=(0, 5), pady=2)

auto_sustain_checkbox = ttk.Checkbutton(auto_sustain_frame, 
                                       text=_("auto_sustain_on") if auto_sustain else _("auto_sustain_off"), 
                                       variable=auto_sustain_var, 
                                       command=lambda: toggle_auto_sustain(auto_sustain_var.get()),
                                       style="TCheckbutton")
auto_sustain_checkbox.pack(anchor="w", padx=5, pady=5)

# Humanizer checkbox with modern styling
humanizer_var = tk.BooleanVar(value=humanizer_enabled)
humanizer_frame = ttk.Frame(settings_grid, style="Card.TFrame")
humanizer_frame.grid(row=0, column=1, sticky="ew", padx=(5, 0), pady=2)

humanizer_checkbox = ttk.Checkbutton(humanizer_frame, 
                                    text=_("humanizer_on") if humanizer_enabled else _("humanizer_off"), 
                                    variable=humanizer_var, 
                                    command=toggle_humanizer,
                                    style="TCheckbutton")
humanizer_checkbox.pack(anchor="w", padx=5, pady=5)

# Humanizer strength slider (initially hidden)
humanizer_strength_frame = ttk.Frame(humanizer_frame, style="Card.TFrame")
humanizer_strength_header = ttk.Frame(humanizer_strength_frame, style="Card.TFrame")
humanizer_strength_header.pack(fill="x", expand=True)

humanizer_strength_label = ttk.Label(humanizer_strength_header, text=_("humanize_amount"), style="TLabel")
humanizer_strength_label.pack(side="left", anchor="w", padx=0, pady=(0, 2))

humanizer_strength_value = ttk.Label(humanizer_strength_header, text=f"{humanizer_strength} {_('ms')}", style="TLabel", foreground=COLOR_ACCENT)
humanizer_strength_value.pack(side="right", anchor="e", padx=0, pady=(0, 2))

humanizer_strength_slider = ttk.Scale(humanizer_strength_frame, from_=1, to=50, orient=tk.HORIZONTAL, 
                                     style="Horizontal.TScale", command=update_humanizer_strength)
humanizer_strength_slider.set(humanizer_strength)
humanizer_strength_slider.pack(fill="x", pady=(0, 0))

# Initially hide the humanizer strength slider
if not humanizer_enabled:
    humanizer_strength_frame.pack_forget()

# Queue checkbox for continuous playback
queue_var = tk.BooleanVar(value=queue_enabled)
queue_settings_frame = ttk.Frame(settings_grid, style="Card.TFrame")
queue_settings_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(5, 0))

queue_checkbox = ttk.Checkbutton(queue_settings_frame, 
                                text=_("queue_mode_on") if queue_enabled else _("queue_mode_off"), 
                                variable=queue_var, 
                                command=toggle_queue,
                                style="TCheckbutton")
queue_checkbox.pack(anchor="w", padx=5, pady=5)

# Always on Top checkbox
always_on_top_var = tk.BooleanVar(value=always_on_top)
always_on_top_frame = ttk.Frame(settings_grid, style="Card.TFrame")
always_on_top_frame.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(5, 0))

always_on_top_checkbox = ttk.Checkbutton(always_on_top_frame,
                                         text=_("always_on_top_on") if always_on_top else _("always_on_top_off"),
                                         variable=always_on_top_var,
                                         command=toggle_always_on_top,
                                         style="TCheckbutton")
always_on_top_checkbox.pack(anchor="w", padx=5, pady=5)

# Speed setting in a cleaner layout
speed_frame = ttk.Frame(settings_grid, style="Card.TFrame")
speed_frame.grid(row=4, column=0, sticky="ew", padx=(0, 5), pady=2)

speed_label = ttk.Label(speed_frame, text=_("playback_speed"), style="TLabel")
speed_label.pack(anchor="w", padx=5, pady=(5, 2))

speed_value_label = ttk.Label(speed_frame, text=_("normal_speed"), style="TLabel", foreground=COLOR_ACCENT)
speed_value_label.pack(anchor="w", padx=5, pady=(0, 2))

speed_slider = ttk.Scale(speed_frame, from_=-1.0, to_=1.0, orient=tk.HORIZONTAL, 
                        style="Horizontal.TScale", command=update_speed_label)
speed_slider.set(speed)
speed_slider.pack(fill="x", padx=5, pady=(0, 5))

# Delay settings
delay_frame = ttk.Frame(settings_grid, style="Card.TFrame")
delay_frame.grid(row=4, column=1, sticky="ew", padx=(5, 0), pady=2)

delay_header = ttk.Frame(delay_frame, style="Card.TFrame")
delay_header.pack(fill="x", expand=True)

delay_title = ttk.Label(delay_header, text=_("note_delay"), style="TLabel")
delay_title.pack(side="left", anchor="w", padx=5, pady=(5, 2))

delay_value_label = ttk.Label(delay_header, text=f"{delay:.2f} {_('seconds')}", style="TLabel", foreground=COLOR_ACCENT)
delay_value_label.pack(side="right", anchor="e", padx=5, pady=(5, 2))

delay_slider = ttk.Scale(delay_frame, from_=0.01, to_=1.0, orient=tk.HORIZONTAL, 
                        style="Horizontal.TScale", command=update_delay_label)
delay_slider.set(delay)
delay_slider.pack(fill="x", padx=5, pady=(0, 5))

# Queue Management Card
queue_card = ttk.Frame(content_frame, style="Card.TFrame")
queue_card.pack(fill="x", pady=(0, 8), ipady=8)

queue_title = ttk.Label(queue_card, text=_("queue_management"), style="SectionTitle.TLabel")
queue_title.pack(anchor="w", padx=12, pady=(8, 5))

# Queue controls
queue_controls_frame = ttk.Frame(queue_card, style="Card.TFrame")
queue_controls_frame.pack(fill="x", padx=12, pady=(0, 3))

prev_queue_btn = ttk.Button(queue_controls_frame, text=_("previous"), command=play_previous_in_queue, style="TButton", width=10)
prev_queue_btn.pack(side="left", padx=(0, 3))

next_queue_btn = ttk.Button(queue_controls_frame, text=_("next"), command=play_next_in_queue, style="TButton", width=10)
next_queue_btn.pack(side="left", padx=(0, 3))

clear_queue_btn = ttk.Button(queue_controls_frame, text=_("clear_queue"), command=clear_queue, style="Error.TButton", width=10)
clear_queue_btn.pack(side="right")

# Add queue information to the welcome message in the English translations
TRANSLATIONS["en"]["welcome"] = "Welcome to SkyMusic Player! Press F1 to play/pause, F2 to stop. Queue system is enabled - add songs from your library to the queue."

# Update the show_status_message function to show a quick help message about queuing when the application starts
root.after(1000, lambda: show_status_message("Queue system is enabled. Use '+ Queue' buttons to add songs to the queue.", "info"))

# Add a function to show a quick help about the queue when queue is enabled
def show_queue_help():
    help_text = """Queue System Help:
    
1. Add songs to queue using '+ Queue' buttons in the song library
2. Use Previous/Next buttons to navigate the queue
3. Reorder songs with ▲ and ▼ buttons
4. Remove songs with ✕ button
5. Clear the entire queue with 'Clear Queue' button
6. Turn queue mode on/off with the checkbox in settings
    
When queue mode is enabled, songs will play one after another automatically."""
    
    help_window = tk.Toplevel(root)
    help_window.title("Queue Help")
    help_window.configure(bg=COLOR_BG)
    help_window.grab_set()  # Make the window modal
    
    # Set window size and position
    window_width = 500
    window_height = 280
    position_x = root.winfo_x() + (root.winfo_width() // 2) - (window_width // 2)
    position_y = root.winfo_y() + (root.winfo_height() // 2) - (window_height // 2)
    help_window.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")
    
    # Create a styled frame for the help content
    frame = ttk.Frame(help_window, style="Dialog.TFrame")
    frame.pack(fill="both", expand=True, padx=15, pady=15)
    
    # Add help title
    help_title = ttk.Label(frame, text="Queue System Help", style="Dialog.TLabel", 
                          font=('Segoe UI', 12, 'bold'), foreground=COLOR_ACCENT)
    help_title.pack(pady=(0, 15))
    
    # Add help text
    help_label = ttk.Label(frame, text=help_text, style="Dialog.TLabel", wraplength=450, justify="left")
    help_label.pack(pady=(0, 20))
    
    # Add close button
    ok_button = ttk.Button(frame, text="OK", command=help_window.destroy, style="Accent.TButton", width=10)
    ok_button.pack()

# Add a help button to the queue controls section
help_btn = ttk.Button(queue_controls_frame, text="?", width=2, command=show_queue_help, style="TButton")
help_btn.pack(side="left", padx=(5, 0))

# Queue list
queue_list_frame = ttk.Frame(queue_card, style="Card.TFrame")
queue_list_frame.pack(fill="both", expand=True, padx=12, pady=5)

# Initialize queue display
update_queue_display()

# Add keyboard shortcuts card
keyboard_card = ttk.Frame(content_frame, style="Card.TFrame")
keyboard_card.pack(fill="x", pady=(0, 8), ipady=8)

keyboard_title = ttk.Label(keyboard_card, text=_("keyboard_shortcuts"), style="SectionTitle.TLabel")
keyboard_title.pack(anchor="w", padx=12, pady=(8, 5))

shortcut_frame = ttk.Frame(keyboard_card, style="Card.TFrame")
shortcut_frame.pack(fill="x", padx=12, pady=(0, 8))

# Create a grid for shortcuts
shortcut_frame.columnconfigure(0, weight=0)  # Key column
shortcut_frame.columnconfigure(1, weight=1)  # Description column

# F1 shortcut
f1_key = ttk.Label(shortcut_frame, text="F1", style="TLabel", foreground=COLOR_ACCENT, font=('Segoe UI', 9, 'bold'))
f1_key.grid(row=0, column=0, sticky="w", padx=(0, 15), pady=2)
f1_desc = ttk.Label(shortcut_frame, text=_("play_pause_desc"), style="TLabel")
f1_desc.grid(row=0, column=1, sticky="w", pady=2)

# F2 shortcut
f2_key = ttk.Label(shortcut_frame, text="F2", style="TLabel", foreground=COLOR_ACCENT, font=('Segoe UI', 9, 'bold'))
f2_key.grid(row=1, column=0, sticky="w", padx=(0, 15), pady=2)
f2_desc = ttk.Label(shortcut_frame, text=_("stop_desc"), style="TLabel")
f2_desc.grid(row=1, column=1, sticky="w", pady=2)

# Add status frame for feedback messages
status_frame = ttk.Frame(main_frame, style="Status.TFrame")
status_label = ttk.Label(status_frame, text="", style="Status.TLabel", anchor="center")
status_label.pack(fill="both", expand=True, padx=3, pady=3)
# Status frame is hidden initially and will be shown when needed

# Make scrollbar respond to mouse wheel events
def _on_mousewheel(event):
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

canvas.bind_all("<MouseWheel>", _on_mousewheel)

def on_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

# Update the update_sidebar function to create more visually appealing song entries
def update_sidebar(notes=None):
    # Clear existing widgets in the sidebar
    for widget in sidebar_inner_frame.winfo_children():
        widget.destroy()
    
    # Load saved songs
    global saved_music, current_loaded_song_id
    
    # Initialize current_loaded_song_id if it doesn't exist
    if 'current_loaded_song_id' not in globals():
        current_loaded_song_id = ""
    
    # Filter songs based on search query
    search_query = search_var.get().lower()
    if search_query == _("search_placeholder").lower():
        search_query = ""
    
    filtered_songs = []
    for song in saved_music:
        if search_query in song.get("name", "").lower():
            filtered_songs.append(song)
    
    if not filtered_songs:
        no_songs_label = ttk.Label(sidebar_inner_frame, text=_("no_songs_found"), style="Sidebar.TLabel")
        no_songs_label.pack(pady=10, padx=10)
        # Make sure to update the scrollregion after changes
        sidebar_inner_frame.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))
        return
    
    # Add each song to the sidebar with improved styling
    for i, song in enumerate(filtered_songs):
        # Check if this is the currently loaded song
        is_current_song = song.get('id', '') == current_loaded_song_id
        song_style = "Selected.Sidebar.TFrame" if is_current_song else "Sidebar.TFrame"
        label_style = "Selected.Sidebar.TLabel" if is_current_song else "Sidebar.TLabel"
        
        song_frame = ttk.Frame(sidebar_inner_frame, style=song_style)
        song_frame.pack(fill="x", padx=10, pady=(0, 1))
        
        # Song container
        song_container = ttk.Frame(song_frame, style=song_style)
        song_container.pack(fill="x", expand=True, padx=0, pady=0)
        
        # Song name with ellipsis for long names
        song_name = song.get("name", f"Song {i+1}")
        if len(song_name) > 25:
            song_name = song_name[:22] + "..."
        
        # Add a playing indicator if this is the current song
        prefix = "► " if is_current_song else ""
        song_label = ttk.Label(song_container, text=f"{prefix}{song_name}", style=label_style, anchor="w")
        song_label.pack(fill="x", padx=8, pady=(8, 1))
        
        # Song metadata (show 'old format' indicator if applicable)
        format_text = _("legacy_format") if song.get("oldFormat", False) else ""
        format_label = ttk.Label(song_container, text=format_text, style=label_style, 
                                foreground=COLOR_INACTIVE, font=('Segoe UI', 7))
        format_label.pack(fill="x", padx=8, pady=(0, 3))
        
        # Buttons container
        button_frame = ttk.Frame(song_container, style=song_style)
        button_frame.pack(fill="x", padx=8, pady=(0, 5))
        
        # Load button - Fix: Use the filtered_songs index instead of i
        load_btn = ttk.Button(button_frame, text=_("load"), 
                             command=lambda song=song: load_music(song), 
                             style="Sidebar.TButton", width=6)
        load_btn.pack(side="left", padx=(0, 3))
        
        # Queue button - always show the queue button
        queue_btn = ttk.Button(button_frame, text=_("add_queue"), 
                             command=lambda song_id=song.get('id', ''): add_to_queue(song_id), 
                             style="Sidebar.TButton", width=6)
        queue_btn.pack(side="left", padx=(0, 3))
        
        # Delete button - Fix: Use the song's ID to safely delete
        delete_btn = ttk.Button(button_frame, text=_("delete"), 
                               command=lambda song_id=song.get('id', ''): delete_song_by_id(song_id), 
                               style="Sidebar.TButton", width=6)
        delete_btn.pack(side="left")
        
        # Store the song reference in the frame for reference
        song_frame.song = song
        
        # Add a separator after each song except the last one
        if i < len(filtered_songs) - 1:
            separator = ttk.Separator(sidebar_inner_frame, orient="horizontal")
            separator.pack(fill="x", padx=5)
    
    # Make sure to update the scrollregion after changes
    sidebar_inner_frame.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))

# Add a new function to delete song by ID rather than by index
def delete_song_by_id(song_id):
    global saved_music
    song_name = "Unknown Song"
    for i, song in enumerate(saved_music):
        if song.get('id', '') == song_id:
            song_name = song.get("name", f"Song {i+1}")
            del saved_music[i]
            break
    
    with open(SAVED_SONGS_FILE, 'w') as f:
        json.dump(saved_music, f)
    update_sidebar()
    show_status_message(_("delete_success", name=song_name), "warning")

# Initialize the UI
load_saved_songs()
load_last_song()
update_sidebar()
toggle_auto_sustain(auto_sustain)

# Show a welcome message
show_status_message(_("welcome"), "info")

# Add functions to reorder queue items
def move_up_in_queue(index):
    """Move a song up in the queue"""
    global play_queue, current_queue_index
    
    if index <= 0 or index >= len(play_queue):
        return False
    
    # Swap the item with the one above it
    play_queue[index], play_queue[index-1] = play_queue[index-1], play_queue[index]
    
    # Adjust current queue index if needed
    if current_queue_index == index:
        current_queue_index -= 1
    elif current_queue_index == index - 1:
        current_queue_index += 1
    
    # Update the queue display
    update_queue_display()
    return True

def move_down_in_queue(index):
    """Move a song down in the queue"""
    global play_queue, current_queue_index
    
    if index < 0 or index >= len(play_queue) - 1:
        return False
    
    # Swap the item with the one below it
    play_queue[index], play_queue[index+1] = play_queue[index+1], play_queue[index]
    
    # Adjust current queue index if needed
    if current_queue_index == index:
        current_queue_index += 1
    elif current_queue_index == index + 1:
        current_queue_index -= 1
    
    # Update the queue display
    update_queue_display()
    return True

root.mainloop()
