#!/usr/bin/env python3
import os
import argparse
import yaml
from backend.converter.converter import json_to_nfo

def main():
    parser = argparse.ArgumentParser(description="JSON → NFO 변환기")
    parser.add_argument(
        "--json-folder",
        required=True,
        help="변환할 JSON 파일이 들어 있는 폴더"
    )
    parser.add_argument(
        "--yaml",
        required=True,
        help="사용할 YAML 템플릿 파일 경로"
    )
    args = parser.parse_args()

    json_folder = os.path.abspath(args.json_folder)
    yaml_file = os.path.abspath(args.yaml)

    if not os.path.exists(json_folder):
        raise FileNotFoundError(f"JSON 폴더가 존재하지 않습니다: {json_folder}")
    if not os.path.exists(yaml_file):
        raise FileNotFoundError(f"YAML 파일이 존재하지 않습니다: {yaml_file}")

    # YAML 로드
    with open(yaml_file, "r", encoding="utf-8") as f:
        yaml_template = yaml.safe_load(f)

    # JSON → NFO 변환
    for file in os.listdir(json_folder):
        if file.endswith(".json"):
            json_path = os.path.join(json_folder, file)
            json_to_nfo(json_path, yaml_template)

    print("✅ 모든 JSON 파일 NFO 변환 완료!")

if __name__ == "__main__":
    main()
