#!/bin/bash
set -e

echo "=== yt-meta2plex setup 시작 ==="

# ----------------------------
# 1. python3-venv 설치 확인/설치
# ----------------------------
if ! python3 -m venv --help >/dev/null 2>&1; then
    echo "python3-venv가 설치되어 있지 않습니다. 설치 중..."
    sudo apt update
    sudo apt install -y python3-venv python3-pip
    echo "python3-venv 설치 완료!"
fi

# ----------------------------
# 2. 가상환경 생성 (없으면)
# ----------------------------
if [ ! -d "venv" ]; then
    echo "가상환경 생성 중..."
    if ! python3 -m venv venv; then
        echo "가상환경 생성 실패! python3-venv 설치 확인 필요."
        exit 1
    fi
    echo "가상환경 생성 완료: venv/"
fi

# ----------------------------
# 3. 가상환경 활성화
# ----------------------------
if [ -f "venv/bin/activate" ]; then
    echo "가상환경 활성화..."
    source venv/bin/activate
else
    echo "venv/bin/activate 파일이 없습니다. 가상환경 생성 확인 필요."
    exit 1
fi

# ----------------------------
# 4. pip 업그레이드
# ----------------------------
echo "pip 업그레이드 중..."
pip install --upgrade pip

# ----------------------------
# 5. 필요 패키지 설치
# ----------------------------
if [ ! -f "requirements.txt" ]; then
    echo "requirements.txt가 없습니다. 최소 패키지 설치 중..."
    pip install PyYAML watchdog fastapi uvicorn SQLAlchemy
else
    echo "requirements.txt에서 패키지 설치 중..."
    pip install -r requirements.txt
fi

# ----------------------------
# 6. converter 테스트 실행 (예제)
# ----------------------------
if [ -f "_test/test_converter.py" ]; then
    echo "converter 테스트 실행..."
    python3 _test/test_converter.py
else
    echo "_test/test_converter.py 파일이 없습니다. 테스트 건너뜀."
fi

echo "=== setup.sh 완료! 가상환경과 패키지 설치가 준비되었습니다. ==="
