# yt-meta2plex

## 개요
- YouTube JSON metadata 감지
- NFO 변환
- Plex 메타데이터 자동 업데이트
- FastAPI 백엔드 + React 웹 UI + Docker 지원

## 초기 세팅

### Backend (Python)
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python main.py
```

### Frontend (React)
```bash
cd web
npm install
npm start
```

### Docker
```bash
cd docker
docker-compose build
docker-compose up -d
```

