import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from .json_to_nfo import json_to_nfo

class NFOHandler(FileSystemEventHandler):
    def __init__(self, plex_client):
        self.plex_client = plex_client

    def on_created(self, event):
        path = Path(event.src_path)
        if path.suffix == ".json":
            print(f"[watcher] JSON detected: {path}")
            nfo_path = json_to_nfo(path)
            print(f"[watcher] NFO created: {nfo_path}")
            self.plex_client.refresh_metadata()

def start_watching(dirs, plex_client, interval=10):
    observer = Observer()
    handler = NFOHandler(plex_client)
    for d in dirs:
        observer.schedule(handler, d, recursive=True)
    observer.start()
    print(f"[watcher] Watching: {dirs}")
    try:
        while True:
            time.sleep(interval)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
