import os
import json
import yaml
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

def json_to_nfo(info_path: str, yaml_template: str):
    """
    JSON 파일을 NFO로 변환
    Args:
        info_path (str): JSON 파일 경로
        yaml_template (str): YAML 템플릿 경로
    """
    with open(info_path, "r", encoding="utf-8") as f:
        info = json.load(f)

    with open(yaml_template, "r", encoding="utf-8") as f:
        template = yaml.safe_load(f)

    root = Element("episodedetails")

    # 필드 처리
    for field in ["title", "showtitle", "season", "episode", "plot", "runtime", "id", "studio", "genre"]:
        if field in template:
            text = get_value(info, field) if field != "plot" else get_value(info, "description", "")
            SubElement(root, field).text = str(text)

    # 썸네일 처리
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

    # NFO 파일명 생성
    base_name = os.path.splitext(info_path)[0]
    if base_name.endswith(".info"):
        base_name = base_name[:-5]
    nfo_filename = base_name + ".nfo"

    with open(nfo_filename, "wb") as f:
        f.write(xml_bytes)

    logger.info(f"NFO 생성 완료: {nfo_filename}")
    return nfo_filename

def batch_convert(json_folder: str, yaml_template: str):
    """
    폴더 내 모든 JSON 파일 변환
    """
    for file in os.listdir(json_folder):
        if file.endswith(".json"):
            json_path = os.path.join(json_folder, file)
            json_to_nfo(json_path, yaml_template)
