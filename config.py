import yaml
from pathlib import Path

def load_config(path="yt-meta2plex.yaml"):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)
