import os
import json
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

def json_to_nfo(info_path, yaml_template, output_folder):
    with open(info_path, "r", encoding="utf-8") as f:
        info = json.load(f)

    root = Element("episodedetails")

    # 필드 처리
    for field in ["title", "showtitle", "season", "episode", "plot", "runtime", "id", "studio", "genre"]:
        if field in yaml_template:
            text = get_value(info, field) if field != "plot" else get_value(info, "description", "")
            SubElement(root, field).text = str(text)

    # 섬네일 처리
    thumb_tag = SubElement(root, "thumb")
    thumb_tag.text = find_thumbnail(info_path, info)

    # ratings
    ratings_info = yaml_template.get("ratings", [])
    for r in ratings_info:
        rating = SubElement(root, "ratings")
        sub = SubElement(rating, "rating", {
            "name": r.get("name", "youtube"),
            "max": str(r.get("max", 5)),
            "default": str(r.get("default", True)).lower()
        })
        SubElement(sub, "value").text = str(info.get("average_rating", r.get("value", 0)))
        SubElement(sub, "votes").text = str(info.get("view_count", r.get("votes", 0)))

    # uniqueid
    uid = SubElement(root, "uniqueid", {"type": "youtube", "default": "True"})
    SubElement(uid, "value").text = info.get("id", "")

    # aired, dateadded
    upload_date = info.get("upload_date")
    if upload_date:
        SubElement(root, "aired").text = datetime.strptime(upload_date, "%Y%m%d").strftime("%Y-%m-%d")
    SubElement(root, "dateadded").text = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # UTF-8 인코딩 포함
    xml_bytes = minidom.parseString(tostring(root)).toprettyxml(indent="  ", encoding="utf-8")

    # NFO 파일 생성 (output_folder)
    os.makedirs(output_folder, exist_ok=True)
    base_name = os.path.splitext(os.path.basename(info_path))[0]
    if base_name.endswith(".info"):
        base_name = base_name[:-5]
    nfo_filename = os.path.join(output_folder, base_name + ".nfo")

    with open(nfo_filename, "wb") as f:
        f.write(xml_bytes)

    print(f"NFO 생성 완료: {nfo_filename}")
