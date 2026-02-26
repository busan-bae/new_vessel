# HOS 선박정보 프로젝트 — 배포 설계 기록

## 배포 목표
- 미니PC(Ubuntu)에서 Docker 컨테이너로 Flask 앱 배포
- DDNS로 도메인 연결 후 HTTPS 적용

---

## 최종 구성

```
인터넷
  ↓
[Caddy]       ← 이미 실행 중, HTTPS 자동 처리 (Nginx 불필요)
  ↓
[Gunicorn + Flask 컨테이너]  ← Docker로 관리
```

| 역할 | 도구 |
|------|------|
| HTTPS + 리버스 프록시 | Caddy (이미 설치됨) |
| Flask 프로덕션 실행 | Gunicorn |
| 컨테이너 관리 | Docker Compose |
| SSL 인증서 | Caddy 자동 처리 |
| 도메인 | DDNS (추후 연결) |
| 배포 환경 | 미니PC — Ubuntu |

## 미니PC 실행 중인 서비스
| 컨테이너 | 포트 | 용도 |
|---------|------|------|
| n8n | 5678 (내부) | 워크플로우 자동화 (5단계 연동 예정) |
| Uptime Kuma | 3001 | 서버 모니터링 |
| PostgreSQL | 5432 (내부) | n8n용 DB |
| Redis | 6379 (내부) | n8n용 캐시 |
| Caddy | 80, 443 | 리버스 프록시 + HTTPS |

→ Flask 컨테이너는 **5000번 포트** 사용 (비어있음)

---

## 배포 흐름

```
이 PC                         미니PC (Ubuntu)
------                        ---------------
코드 작성
git push              →       git pull
                              docker compose up --build
                              (브라우저로 접속)
```

---

## 학습 단계

### 1단계 — Dockerfile 작성 ✅
- [x] `requirements.txt` 에 gunicorn 추가
- [x] `Dockerfile` 작성
- [x] `.dockerignore` 작성

### 2단계 — docker-compose.yml 작성 ✅
- [x] Flask 서비스 구성
- [x] 볼륨 마운트 (SQLite DB 파일 유지)
- [x] 포트 설정 (5000번)
- [x] 미니PC 배포 및 브라우저 접속 확인

### 3단계 — HTTPS 적용 ✅
- [x] DDNS 도메인 연결 (hos.hangbae.dedyn.io)
- [x] Caddy API로 Flask 프록시 라우트 추가 (기존 설정 파일 수정 없이)
- [x] HTTPS 접속 확인

---

## 파일 구조 (현재)

```
new_vessel/
├── Dockerfile        ✅
├── docker-compose.yml ✅
├── .dockerignore     ✅
├── DEPLOY.md         ✅
└── (기존 Flask 파일들...)
```

---

## 학습 메모

### Docker
- `FROM python:3.13-slim` — 슬림 버전: 불필요한 OS 패키지 제거, 이미지 크기 최소화
- `WORKDIR /app` — 컨테이너 안 작업 디렉토리 (없으면 자동 생성)
- `COPY requirements.txt .` → `RUN pip install` — 레이어 캐시 최적화 (코드 변경 시 패키지 재설치 방지)
- `CMD ["gunicorn", ...]` — 컨테이너 시작 시 실행할 명령어
- `volumes: - ./data:/app/instance` — 미니PC 폴더와 컨테이너 폴더를 연결 (DB 영구 보존)
- Docker가 생성한 폴더는 root 소유 → `sudo chown -R user:user ./data/` 로 권한 변경 필요

### DB 마이그레이션
- `instance/`는 `.gitignore`에 포함 → git으로 전송 불가
- FileZilla(SFTP) 또는 scp로 직접 전송 (미니PC SSH 포트: 2222)
- 전송 후 `docker compose restart` 로 컨테이너 재시작 필요

### Caddy API
- Caddy 관리자 API: `localhost:2019` (로컬에서만 접근 가능)
- 파일 수정 없이 라우트 추가: `curl -X POST localhost:2019/config/apps/http/servers/srv0/routes/0`
- 라우트 삭제: `curl -X DELETE localhost:2019/config/apps/http/servers/srv0/routes/[인덱스]`
- 현재 라우트 확인: `curl -s localhost:2019/config/apps/http/servers/srv0/routes/ | python3 -m json.tool | grep -A2 '"host"'`

### Gunicorn
- Flask 내장 서버는 개발용 (단일 스레드, 느림)
- Gunicorn은 프로덕션용 WSGI 서버 (멀w티 워커, 안정적)
- `--bind 0.0.0.0:5000` — 모든 외부 요청을 5000번 포트로 수신
- `app:create_app()` — app.py의 create_app() 팩토리 함수 호출

### n8n → Flask API 연동
- n8n과 Flask가 다른 docker-compose 프로젝트면 기본적으로 다른 네트워크 → 컨테이너 이름으로 직접 통신 불가
- 같은 네트워크로 묶으려면 shared external network 필요 (복잡)
- 간단한 대안: 외부 도메인 URL 사용 (`https://hos.hangbae.dedyn.io/api/voyage`) — 같은 서버 내에서 돌아오지만 트래픽이 적으면 충분

### 가상환경 (venv)
- conda는 데이터사이언스용, venv는 웹개발/배포에 적합
- `pip freeze`는 가상환경 활성화 후 사용해야 정확한 목록 생성
- Docker 빌드 시 requirements.txt 기준으로 패키지 설치

---

## 현재 진행 현황

- [x] venv 생성 및 requirements.txt 작성
- [x] 배포 아키텍처 설계 완료
- [x] Dockerfile 작성
- [x] .dockerignore 작성
- [x] docker-compose.yml 작성
- [x] 미니PC 배포 완료 (http://192.168.0.13:5000)
- [x] DDNS 연결 및 HTTPS 적용 (https://hos.hangbae.dedyn.io)
- [x] 기존 개발 DB 데이터 마이그레이션 (vessel.db → 미니PC data/ 폴더)
- [x] python-dotenv 추가 및 requirements.txt 갱신 (venv 기반으로 정리)
- [x] .env 파일 FileZilla로 미니PC 전송
- [x] n8n → Flask API 연동 (https://hos.hangbae.dedyn.io/api/voyage)
- [ ] deSEC 토큰으로 IP 자동 업데이트 설정 (IP 고정이라 나중에 필요 시)
