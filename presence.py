import re
import sys
import time
import os
import json
from pypresence import Presence
import threading
import psutil

class TimestampedWriter:
    def __init__(self, file):
        self.file = file
        self.at_line_start = True

    def write(self, message):
        for char in message:
            if self.at_line_start and char != "\n":
                timestamp = time.strftime("[%d.%m.%Y %H:%M:%S] ")
                self.file.write(timestamp)
                self.at_line_start = False
            self.file.write(char)
            if char == "\n":
                self.at_line_start = True

    def flush(self):
        self.file.flush()

GAME_PROCESS_NAMES = ["PagodaSteam-Win64-Shipping.exe", "PagodaSteamDemo-Win64-Shipping.exe"]


def is_game_running():
    for proc in psutil.process_iter(["name"]):
        try:
            if proc.info["name"] in GAME_PROCESS_NAMES:
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return False


def watch_game_and_exit():
    MAX_WAIT_MINUTES = 5
    waited_seconds = 0

    while not is_game_running():
        time.sleep(1)
        waited_seconds += 1
        if waited_seconds >= MAX_WAIT_MINUTES * 60:
            print(f"No game detected within {MAX_WAIT_MINUTES} minutes. Closing application.")
            os._exit(0)

    misses = 0
    REQUIRED_MISSES = 3
    CHECK_INTERVAL = 1

    while True:
        if is_game_running():
            misses = 0
        else:
            misses += 1
            if misses >= REQUIRED_MISSES:
                break
        time.sleep(CHECK_INTERVAL)

    print("Dead as Disco was closed. Closing application...")
    time.sleep(1)
    os._exit(0)

CLIENT_ID = "1545751092116066344"


def get_base_dir():
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


BASE_DIR = get_base_dir()

if getattr(sys, "frozen", False):
    log_path = os.path.join(BASE_DIR, "presence_log.txt")

    MAX_LOG_AGE_DAYS = 7
    if os.path.exists(log_path):
        age_days = (time.time() - os.path.getmtime(log_path)) / 86400
        if age_days > MAX_LOG_AGE_DAYS:
            os.remove(log_path)

    log_file = open(log_path, "a", encoding="utf-8", buffering=1)
    sys.stdout = TimestampedWriter(log_file)
    sys.stderr = TimestampedWriter(log_file)

SONGS_FILE = os.path.join(BASE_DIR, "songs.json")
LOG_PATH = os.path.expandvars(r"%LOCALAPPDATA%\Pagoda\Saved\Logs\Pagoda.log")

DEFAULT_SONGS = {
    "PS_Echolokators_152": ("Deckard Voltair", "Echolokators (Boss Remix)"),
    "PS_Doll_AltStruct_123": ("Arora", "Rhythm Divine (Boss Remix)"),
    "PS_Mission_155": ("Prophet", "Mission (Boss Remix)"),
    "PS_Maniac_165": ("Hemlock", "Maniac (Boss Remix)")
}


def load_songs():
    if not os.path.exists(SONGS_FILE):
        with open(SONGS_FILE, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_SONGS, f, indent=2, ensure_ascii=False)
        return DEFAULT_SONGS
    try:
        with open(SONGS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"couldn't read songs.json ({e}), using fallback list.")
        return DEFAULT_SONGS


SONG_OVERRIDES = load_songs()

KNOWN_PREFIXES = ["PS_", "ED_"]
MAP_PATTERN = re.compile(r"LogLoad: LoadMap: (.+)$")
SONG_STARTED_PATTERN = re.compile(r"OnSongStartedEvent, song asset (.+)$")


def clean_internal_name(raw):
    name = raw
    changed = True
    while changed:
        changed = False
        for prefix in KNOWN_PREFIXES:
            if name.startswith(prefix):
                name = name[len(prefix):]
                changed = True
    name = re.sub(r"[_ ]?\d+\s*bpm$", "", name, flags=re.IGNORECASE)
    name = re.sub(r"_\d+$", "", name)
    name = name.replace("_", " ")
    name = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", " ", name)
    name = re.sub(r"(?<=[A-Z])(?=[A-Z][a-z])", " ", name)
    name = re.sub(r"\s+", " ", name).strip()
    return name


def parse_artist_song(asset_string):
    asset_string = asset_string.strip()
    if asset_string in SONG_OVERRIDES:
        artist, song = SONG_OVERRIDES[asset_string]
        return artist, song
    if " - " in asset_string:
        artist, song = asset_string.rsplit(" - ", 1)
        return artist.strip(), song.strip()
    return None, clean_internal_name(asset_string)


def classify_map(path):
    if "DiveBar" in path:
        return "bar"
    if "LevelSelect" in path or "Main_Menu" in path:
        return "menu"
    return "level"

def connect_discord():
    print("Connecting with Discord...")
    while True:
        try:
            rpc = Presence(CLIENT_ID)
            rpc.connect()
            print("Connected with Discord.")
            return rpc
        except Exception as e:
            print(f"Couldn't connect to Discord ({e}), retry again in 5s...")
            time.sleep(5)


def wait_for_log():
    print("Discord Rich Presence started and active.")
    while not os.path.exists(LOG_PATH):
        time.sleep(2)


def tail_log(path):
    f = open(path, "r", encoding="utf-8", errors="ignore")
    f.seek(0, os.SEEK_END)
    while True:
        line = f.readline()
        if line:
            yield line.rstrip("\n")
            continue
        time.sleep(0.5)
        try:
            current_size = os.path.getsize(path)
        except FileNotFoundError:
            continue
        if current_size < f.tell():
            print("Dead as Disco started, loading logfile...")
            f.close()
            f = open(path, "r", encoding="utf-8", errors="ignore")


watcher_started = False


def main():
    global watcher_started

    print("=== Dead as Disco - Discord Rich Presence ===")
    print("================= by Anomyt =================")

    rpc = connect_discord()
    wait_for_log()

    if not watcher_started:
        watcher_started = True
        watcher = threading.Thread(target=watch_game_and_exit, daemon=True)
        watcher.start()

    current_map_type = "menu"
    current_song = None

    def push_update():
        try:
            if current_map_type == "bar":
                rpc.update(details="Chilling at the bar", start=int(time.time()))
            elif current_map_type == "menu":
                rpc.update(details="Idle", start=int(time.time()))
            elif current_song:
                artist, song = current_song
                if artist:
                    rpc.update(details=artist, state=song, start=int(time.time()))
                else:
                    rpc.update(details=song, start=int(time.time()))
            else:
                rpc.update(details="Idle", start=int(time.time()))
        except Exception as e:
            print(f"Presence-Update failed: {e}")

    push_update()

    for line in tail_log(LOG_PATH):
        map_match = MAP_PATTERN.search(line)
        if map_match:
            current_map_type = classify_map(map_match.group(1))
            current_song = None
            push_update()
            continue

        if "OnSongStartedEvent" in line:
            match = SONG_STARTED_PATTERN.search(line)
            if match:
                artist, song = parse_artist_song(match.group(1))
                current_song = (artist, song)
                push_update()
            continue

        if "OnSongStoppedEvent" in line:
            current_song = None
            push_update()


if __name__ == "__main__":
    try:
        while True:
            try:
                main()
            except Exception as e:
                print(f"Unexpected error: {e}. Restarting in 5s...")
                time.sleep(5)
    except Exception:
        import traceback
        traceback.print_exc()
        time.sleep(10)
