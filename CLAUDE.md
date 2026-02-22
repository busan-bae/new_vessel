# HOS 선박정보 프로젝트

## 프로젝트 목표
- 선박 정보를 관리하는 풀스택 웹 애플리케이션 개발
- 개발 과정을 통해 풀스택 웹 개발을 학습

## 기술 스택
- **Backend**: Python Flask
- **Frontend**: HTML, CSS (Jinja2 템플릿)
- **Database**: SQLite + SQLAlchemy

## 학습자 지침
- 학습 목적 프로젝트이므로 코드에 **한글 주석**으로 설명을 포함할 것
- 새로운 개념이 등장하면 간단히 설명할 것
- 한 번에 너무 많은 변경을 하지 말고, 단계별로 진행할 것
- 코드를 직접 작성하지 말고, **채팅으로 제안 → 학습자가 직접 구현 → 리뷰** 방식으로 진행

## 프로젝트 구조
```
new_vessel/
├── CLAUDE.md            # 프로젝트 지침 & 진행 현황
├── main.py              # 앱 실행 진입점 (create_app() 호출만)
├── app.py               # create_app() 팩토리 함수 (설정, 확장, Blueprint 등록, 에러 핸들러)
├── models.py            # DB 모델 (User, Vessel, VesselDetail)
├── instance/
│   └── vessel.db        # SQLite 데이터베이스 파일
├── routes/
│   ├── __init__.py      # 패키지 선언 (빈 파일)
│   ├── main.py          # 홈 라우트 (/)
│   ├── auth.py          # 인증 라우트 (/signup, /login, /logout)
│   ├── vessel.py        # 선박 라우트 (/vessel/*)
│   └── decorators.py    # 공통 데코레이터 (login_required)
├── static/
│   ├── css/
│   │   ├── common.css        # CSS 리셋 & 공통 스타일 (header, .inner, .btn-primary, 플래시 메시지)
│   │   ├── index.css         # 메인 페이지 전용 스타일
│   │   ├── signup.css        # 회원가입 페이지 전용 스타일
│   │   ├── login.css         # 로그인 페이지 전용 스타일
│   │   ├── vessel_new.css    # 선박 등록 페이지 전용 스타일
│   │   ├── vessel_list.css   # 선박 목록 페이지 전용 스타일
│   │   ├── vessel_detail.css # 선박 상세 페이지 전용 스타일 (CSS Grid 키-값 레이아웃)
│   │   └── vessel_edit.css   # 선박 수정 페이지 전용 스타일
│   └── js/
│       └── common.js         # 공통 JS (플래시 메시지 자동 숨김 + 애니메이션)
└── templates/
    ├── base.html             # 공통 레이아웃 (header, block css, block content, 플래시 메시지)
    ├── index.html            # 메인 페이지
    ├── signup.html           # 회원가입 페이지
    ├── login.html            # 로그인 페이지
    ├── vessel_new.html       # 선박 등록 페이지 (Vessel + VesselDetail 동시 등록)
    ├── vessel_list.html      # 선박 목록 페이지 (선박명 클릭 → 상세 이동)
    ├── vessel_detail.html    # 선박 상세 페이지 (dl/dt/dd + CSS Grid)
    ├── vessel_edit.html      # 선박 수정 페이지
    ├── 404.html              # 커스텀 404 에러 페이지
    └── 500.html              # 커스텀 500 에러 페이지
```

## 추후 리팩토링 목표
- 템플릿 폴더 구조 분리 (파일이 많아지면 templates/auth/, templates/vessel/, templates/errors/ 로 분리)
- 환경변수로 설정 관리 (.env + python-dotenv)
- CSR(React 등)로 전환 시 검색은 JS 필터링 + API 방식으로 변경

## 진행 현황

### 로드맵
1. ~~CRUD 완성~~ ✅ → 2. ~~리팩토링~~ ✅ → 3. ~~검색/조회 기능~~ ✅ → 4. ~~권한 관리~~ ✅ → 5. 운항정보 API 수신 (예정)

### 1단계 — CRUD 완성 ✅
- [x] Flask 기본 세팅 & DB 연동 (SQLite + SQLAlchemy)
- [x] User 모델, 회원가입/로그인/로그아웃
- [x] CSRF 보호 (flask-seasurf)
- [x] Vessel + VesselDetail 모델 (1:1 관계)
- [x] 선박 등록/목록/상세/수정/삭제 (CRUD 완성)
- [x] 플래시 메시지 & JS 애니메이션
- [x] 모바일 반응형 CSS

### 2단계 — 리팩토링 ✅
- [x] Blueprint 패턴 (routes/auth.py, routes/vessel.py, routes/main.py)
- [x] Application Factory 패턴 (create_app())
- [x] models.py 분리
- [x] login_required 데코레이터 (routes/decorators.py)
- [x] 커스텀 에러 페이지 (404, 500)

### 3단계 — 검색/조회 기능 ✅
- [x] seed.py — JSON 파일로 더미데이터 삽입 (119척)
- [x] 모델 수정 — gross_tonnage(Integer) → ship_size(String)
- [x] 선박 검색 (선박명 부분검색, 선종/기국 필터링)
- [x] 검색 후 폼 값 유지 (라우트에서 템플릿으로 값 전달)
- [x] 페이지네이션 (20척/페이지, 검색 조건 유지, 모바일 반응형)

### 4단계 — 권한 관리 (RBAC) ✅
- [x] User 모델에 role 필드 추가 (admin / viewer)
- [x] admin_required 데코레이터 (routes/decorators.py)
- [x] 등록/수정/삭제 라우트에 @admin_required 적용
- [x] context_processor로 current_user 전체 템플릿 주입 (app.py)
- [x] 헤더/메인 페이지에서 admin만 선박 등록·회원가입 버튼 노출

### 5단계 — 운항정보 API 수신 (예정)

#### 개요
- n8n이 HTTP POST로 컨테이너선 운항정보 JSON 배열을 전송
- Flask API가 수신 → DB 저장 (덮어쓰기) → 운항정보 페이지 표시

#### 데이터 형식 (n8n → Flask)
```json
[
  {
    "vessel_name": "HMM ALGECIRAS",
    "voy_no": "0019",
    "line": "FE4",
    "teu": "24K",
    "flag": "KOR",
    "captain": "이상필 (2026-02-05)",
    "chief_engineer": "문학병 (2025-10-30)",
    "safety_supervisor": "장성욱",
    "ops_supervisor": "강문수",
    "psc_inspection": { "mou_1": "Tokyo", "date_1": "2025-09-09", "mou_2": "Paris", "date_2": "2025-11-25" },
    "last_port": { "port": "SGSIN(PSA)", "etd": "2026-02-19 04:30" },
    "next_port": { "port": "GBFXT(GBR)", "eta": "2026-03-21 04:00", "etb": "2026-03-22 04:00", "etd": "2026-03-23 15:00" },
    "itinerary": "NLRTM / RWG(03/24) → DEHAM / CTB(03/30) → ..."
  }
]
```

#### 구현 순서
- [ ] `models.py` — VoyageInfo 모델 추가 (vessel_id FK, 중첩 객체 컬럼으로 펼치기, updated_at)
- [ ] `routes/api.py` — POST /api/voyage 엔드포인트 (새 파일)
- [ ] API 인증 — 1단계: API Key 방식 → 2단계: HMAC 서명 검증으로 업그레이드 예정
- [ ] `app.py` — api Blueprint 등록
- [ ] `routes/vessel.py` — 운항정보 페이지 라우트 추가
- [ ] `templates/voyage.html` — 운항정보 페이지

#### 선박 연결 방식
- `vessel_name`으로 기존 Vessel 테이블과 매칭 (이름 형식 동일)
- 매칭 실패 시 `vessel_id = None`으로 저장 (연결 없이 데이터는 보존)

#### 저장 방식
- 덮어쓰기 (upsert) — vessel_name 기준으로 기존 row 업데이트, 없으면 새로 생성
- [x] User 모델에 role 필드 추가 (admin / viewer)
- [x] admin_required 데코레이터 (routes/decorators.py)
- [x] 등록/수정/삭제 라우트에 @admin_required 적용
- [x] context_processor로 current_user 전체 템플릿 주입 (app.py)
- [x] 헤더/메인 페이지에서 admin만 선박 등록·회원가입 버튼 노출

## 학습 메모

### Flask & Python
- `url_for('Blueprint이름.함수명')` — Blueprint 사용 시 url_for 형식
- `Blueprint('이름', __name__)` — 이름은 문자열, url_for에서 이 이름 사용
- `db = SQLAlchemy()` → `db.init_app(app)` — Application Factory 패턴에서 db 연결 방식
- `app.register_blueprint(bp)` — Blueprint를 앱에 등록해야 라우트가 활성화됨
- `@app.errorhandler(404)` — 에러 핸들러 등록, create_app() 안에서 사용
- `__init__.py` — 폴더를 Python 패키지로 인식시키는 파일 (내용 없어도 됨)
- `from routes.auth import auth_bp` — 하위 폴더 import 시 경로 명시 필요
- 데코레이터 — 함수에 기능을 추가하는 장치 (`@login_required`)
- `@wraps(func)` — 데코레이터 사용 시 원래 함수 이름 보존 (Flask 이름 충돌 방지)
- `debug=False` 로 실행해야 커스텀 500 에러 페이지 확인 가능

### CSS & JS
- `inline` vs `inline-block` vs `block` 차이
- `flex-direction: column` — 세로 배치
- `box-shadow`, `transform`, `transition` — 인터랙션 효과
- `@media (max-width: 768px)` — 모바일 반응형
- `display: grid` + `grid-template-columns: 1fr 2fr` — CSS Grid 키-값 레이아웃
- `@keyframes` + `animation` — CSS 애니메이션
- `position: fixed` + `left: 50%` + `translateX(-50%)` — 뷰포트 가운데 고정
- `addEventListener` — 인라인 이벤트 핸들러 대신 JS 파일에서 관리하는 것이 원칙

### DB & 보안
- `db.Model` — Python 클래스로 DB 테이블 정의 (ORM)
- `db.ForeignKey` + `db.relationship(uselist=False)` — 1:1 관계 설정
- `generate_password_hash` / `check_password_hash` — 비밀번호 해시
- `session['key']` — 서버 메모장, `session.clear()`로 로그아웃
- CSRF — 위조 요청 공격, flask-seasurf로 보호 (GET 방식은 CSRF 불필요)
- `Vessel.query.filter_by(...).first()` — 중복 체크 패턴
- `Vessel.query.get_or_404(id)` — 단건 조회, 없으면 자동 404
- `Vessel.query.filter(Vessel.name.like(f"%{keyword}%"))` — 부분 검색 (LIKE)
- `query.filter(...).filter(...)` — 필터 중첩 (AND 조건)
- `request.args.get("key", "")` — GET 쿼리 파라미터 읽기, 없으면 기본값 반환
- seed.py — `create_app()` + `app_context()`로 스크립트에서 DB 접근하는 패턴
- SSR 검색은 SQL 필터링, CSR 전환 시 JS 필터링으로 변경 예정
- `query.paginate(page=page, per_page=20, error_out=False)` — 페이지 단위 데이터 조회
- `pagination.items` — 현재 페이지 데이터 목록
- `pagination.iter_pages()` — 페이지 번호 목록 생성, 생략 구간은 None 반환
- `<input type="hidden" name="page" value="1">` — 검색 시 항상 1페이지로 초기화
- `url_for()`에 검색 파라미터 함께 전달 — 페이지 이동 시 검색 조건 유지

### 권한 관리 (RBAC)
- `role = db.Column(db.String(20), nullable=False, default="viewer")` — 모델에 역할 컬럼 추가
- `@admin_required` — 데코레이터로 라우트 단위 권한 제어
- `request.referrer or url_for(...)` — 권한 없을 때 이전 페이지로 리디렉션, 없으면 폴백
- `@app.context_processor` — 모든 템플릿에 변수를 자동 주입하는 기능
- `current_user` — context_processor로 주입된 현재 유저 객체 (비로그인 시 None)
- `{% if current_user and current_user.role == "admin" %}` — 템플릿에서 역할별 UI 분기
