import xml.etree.ElementTree as ET
import json
from pathlib import Path

def json_to_nfo(json_path: Path):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    root = ET.Element("movie")
    ET.SubElement(root, "title").text = data.get("title")
    ET.SubElement(root, "plot").text = data.get("description")
    ET.SubElement(root, "originalurl").text = data.get("webpage_url")
    nfo_path = json_path.with_suffix(".nfo")
    ET.ElementTree(root).write(nfo_path, encoding="utf-8", xml_declaration=True)
    return nfo_path
