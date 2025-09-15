import sys
import os
import yaml

# 프로젝트 루트 추가
PROJECT_ROOT = os.getcwd()
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from backend.converter.converter import json_to_nfo

# 테스트용 JSON 폴더
TEST_JSON_FOLDER = os.path.join(PROJECT_ROOT, "_test", "converter", "input")
if not os.path.exists(TEST_JSON_FOLDER):
    raise FileNotFoundError(f"{TEST_JSON_FOLDER} 폴더가 존재하지 않습니다. JSON 파일을 넣어주세요.")

# YAML 템플릿 파일
YAML_FILE = os.path.join(PROJECT_ROOT, "backend", "converter", "custom_extractor.yaml")
if not os.path.exists(YAML_FILE):
    raise FileNotFoundError(f"{YAML_FILE} 파일이 존재하지 않습니다.")

# YAML 로드
with open(YAML_FILE, "r", encoding="utf-8") as f:
    yaml_template = yaml.safe_load(f)

# JSON → NFO 변환
for file in os.listdir(TEST_JSON_FOLDER):
    if file.endswith(".json"):
        json_path = os.path.join(TEST_JSON_FOLDER, file)
        json_to_nfo(json_path, yaml_template)

print("✅ converter 테스트 완료!")
