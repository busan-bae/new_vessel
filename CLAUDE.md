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
1. ~~CRUD 완성~~ ✅ → 2. ~~리팩토링~~ ✅ → 3. ~~검색/조회 기능~~ (진행중) → 4. 권한 관리

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

### 3단계 — 검색/조회 기능 (진행중)
- [x] seed.py — JSON 파일로 더미데이터 삽입 (119척)
- [x] 모델 수정 — gross_tonnage(Integer) → ship_size(String)
- [x] 선박 검색 (선박명 부분검색, 선종/기국 필터링)
- [x] 검색 후 폼 값 유지 (라우트에서 템플릿으로 값 전달)
- [ ] 페이지네이션

### 4단계 — 권한 관리 (RBAC)
- [ ] User 모델에 role 필드 추가 (admin / manager / viewer)
- [ ] 역할별 접근 제어 (등록/수정/삭제는 admin, 조회는 viewer도 가능)

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
