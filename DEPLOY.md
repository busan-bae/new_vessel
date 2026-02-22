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

### 1단계 — Dockerfile 작성 ⬅ 현재
- [ ] `requirements.txt` 에 gunicorn 추가
- [ ] `Dockerfile` 작성
- [ ] `.dockerignore` 작성

### 2단계 — docker-compose.yml 작성
- [ ] Flask + Nginx 서비스 구성
- [ ] 볼륨 마운트 (SQLite DB 파일 유지)
- [ ] 포트 설정

### 3단계 — Nginx 설정 (HTTP)
- [ ] `nginx.conf` 작성
- [ ] Flask → Nginx 프록시 연결 확인

### 4단계 — HTTPS 적용
- [ ] DDNS 도메인 연결
- [ ] Let's Encrypt 인증서 발급 (Certbot)
- [ ] Nginx HTTPS 설정

---

## 파일 구조 (완성 목표)

```
new_vessel/
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── nginx/
│   └── nginx.conf
└── (기존 Flask 파일들...)
```

---

## 학습 메모

### Docker
- `FROM python:3.11-slim` — 슬림 버전: 불필요한 OS 패키지 제거, 이미지 크기 최소화
- `WORKDIR /app` — 컨테이너 안 작업 디렉토리 (없으면 자동 생성)
- `COPY requirements.txt .` → `RUN pip install` — 레이어 캐시 최적화 (코드 변경 시 패키지 재설치 방지)
- `CMD ["gunicorn", ...]` — 컨테이너 시작 시 실행할 명령어

### Gunicorn
- Flask 내장 서버는 개발용 (단일 스레드, 느림)
- Gunicorn은 프로덕션용 WSGI 서버 (멀티 워커, 안정적)
- `--bind 0.0.0.0:5000` — 모든 외부 요청을 5000번 포트로 수신
- `app:create_app()` — app.py의 create_app() 팩토리 함수 호출

### 가상환경 (venv)
- conda는 데이터사이언스용, venv는 웹개발/배포에 적합
- `pip freeze`는 가상환경 활성화 후 사용해야 정확한 목록 생성
- Docker 빌드 시 requirements.txt 기준으로 패키지 설치

---

## 현재 진행 현황

- [x] venv 생성 및 requirements.txt 작성 (13개 패키지)
- [x] 배포 아키텍처 설계 완료
- [ ] Dockerfile 작성 중
