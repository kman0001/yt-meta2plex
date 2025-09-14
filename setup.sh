#!/bin/bash
set -e

# ----------------------------
# 1. 가상환경 생성 (없으면)
# ----------------------------
if [ ! -d "venv" ]; then
    echo "가상환경 생성 중..."
    python3 -m venv venv
    echo "가상환경 생성 완료: venv/"
fi

# ----------------------------
# 2. 가상환경 활성화
# ----------------------------
echo "가상환경 활성화..."
source venv/bin/activate

# ----------------------------
# 3. pip 업그레이드
# ----------------------------
echo "pip 업그레이드 중..."
pip install --upgrade pip

# ----------------------------
# 4. 필요 패키지 설치
# ----------------------------
# requirements.txt가 없으면 최소 패키지 설치
if [ ! -f "requirements.txt" ]; then
    echo "requirements.txt가 없습니다. 최소 패키지 설치 중..."
    pip install PyYAML watchdog fastapi uvicorn SQLAlchemy
else
    echo "requirements.txt에서 패키지 설치 중..."
    pip install -r requirements.txt
fi

# ----------------------------
# 5. converter 테스트 실행 (예제)
# ----------------------------
if [ -f "_test/converter/test_converter.py" ]; then
    echo "converter 테스트 실행..."
    python3 _test/converter/test_converter.py
else
    echo "_test/converter/test_converter.py 파일이 없습니다. 테스트 건너뜀."
fi

echo "setup.sh 완료! 가상환경과 패키지 설치가 준비되었습니다."
