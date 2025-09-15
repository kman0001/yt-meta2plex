import os
import json
import yaml
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom
from datetime import datetime

def get_value(info, key, default=""):
    return info.get(key, default)

def find_thumbnail(info_path, info):
    base_name = os.path.splitext(info_path)[0]
    if base_name.endswith(".info"):
        base_name = base_name[:-5]

    for ext in [".jpg", ".jpeg", ".png", ".webp"]:
        candidate = base_name + ext
        if os.path.exists(candidate):
            return os.path.basename(candidate)
    return get_value(info, "thumbnail", "")

def json_to_nfo(info_path, yaml_template):
    # yaml_template가 dict이면 그대로, 아니면 파일에서 로드
    if isinstance(yaml_template, dict):
        template = yaml_template
    else:
        with open(yaml_template, "r", encoding="utf-8") as f:
            template = yaml.safe_load(f)

    with open(info_path, "r", encoding="utf-8") as f:
        info = json.load(f)

    root = Element("episodedetails")

    # 필드 처리
    for field in ["title", "showtitle", "season", "episode", "plot", "runtime", "id", "studio", "genre"]:
        if field in template:
            text = get_value(info, field) if field != "plot" else get_value(info, "description", "")
            SubElement(root, field).text = str(text)

    # 섬네일 처리
    thumb_tag = SubElement(root, "thumb")
    thumb_tag.text = find_thumbnail(info_path, info)

    # ratings
    ratings_info = template.get("ratings", [])
    for r in ratings_info:
        rating = SubElement(root, "ratings")
        sub = SubElement(rating, "rating", {
            "name": r.get("name", "youtube"),
            "max": str(r.get("max", 5)),
            "default": str(r.get("default", True)).lower()
        })
        SubElement(sub, "value").text = s
