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
├── models.py            # DB 모델 (User, Vessel, VesselDetail, VoyageInfo)
├── .env                 # 환경변수 (SECRET_KEY, API_KEY) — Git 제외
├── instance/
│   └── vessel.db        # SQLite 데이터베이스 파일
├── routes/
│   ├── __init__.py      # 패키지 선언 (빈 파일)
│   ├── main.py          # 홈 라우트 (/)
│   ├── auth.py          # 인증 라우트 (/signup, /login, /logout)
│   ├── vessel.py        # 선박 라우트 (/vessel/*, /voyage/*)
│   ├── api.py           # API 라우트 (POST /api/voyage)
│   └── decorators.py    # 공통 데코레이터 (login_required, admin_required)
├── static/
│   ├── css/
│   │   ├── common.css        # CSS 리셋 & 공통 스타일
│   │   ├── index.css
│   │   ├── signup.css
│   │   ├── login.css
│   │   ├── vessel_new.css
│   │   ├── vessel_list.css
│   │   ├── vessel_detail.css
│   │   ├── vessel_edit.css
│   │   ├── voyage_list.css
│   │   └── voyage_detail.css
│   └── js/
│       └── common.js         # 공통 JS (플래시 메시지 자동 숨김 + 애니메이션)
└── templates/
    ├── base.html
    ├── index.html
    ├── auth/
    │   ├── signup.html
    │   └── login.html
    ├── vessel/
    │   ├── vessel_new.html
    │   ├── vessel_list.html
    │   ├── vessel_detail.html
    │   ├── vessel_edit.html
    │   ├── voyage_list.html      # 운항정보 목록 (검색 + 페이지네이션)
    │   └── voyage_detail.html    # 운항정보 상세
    └── errors/
        ├── 404.html
        └── 500.html
```

## TODO

현재 처리할 항목 없음. 사용하면서 개선점 발견 시 추가.

## 진행 현황

### 로드맵
1. ~~CRUD 완성~~ ✅
2. ~~리팩토링~~ ✅
3. ~~검색/조회 기능~~ ✅
4. ~~권한 관리~~ ✅
5. ~~운항정보 API 수신~~ ✅
6. ~~운항정보 상세 페이지~~ ✅
7. ~~운항정보 검색~~ ✅
8. ~~운항정보 페이지네이션~~ ✅
9. ~~코드 품질 개선 & 구조 리팩토링~~ ✅
10. 실사용 후 개선

## 학습 메모

### Flask & Python
- `url_for('Blueprint이름.함수명')` — Blueprint 사용 시 url_for 형식
- `Blueprint('이름', __name__)` — 이름은 문자열, url_for에서 이 이름 사용
- `db = SQLAlchemy()` → `db.init_app(app)` — Application Factory 패턴에서 db 연결 방식
- `app.register_blueprint(bp)` — Blueprint를 앱에 등록해야 라우트가 활성화됨
- `@app.errorhandler(404)` — 에러 핸들러 등록, create_app() 안에서 사용
- `__init__.py` — 폴더를 Python 패키지로 인식시키는 파일 (내용 없어도 됨)
- 데코레이터 — 함수에 기능을 추가하는 장치 (`@login_required`)
- `@wraps(func)` — 데코레이터 사용 시 원래 함수 이름 보존 (Flask 이름 충돌 방지)
- `if __name__ == "__main__"` — 파일을 직접 실행할 때만 동작 (Gunicorn import 시 실행 안 됨)

### CSS & JS
- `@media (max-width: 768px)` — 모바일 반응형
- `display: grid` + `grid-template-columns: 1fr 2fr` — CSS Grid 키-값 레이아웃
- `position: fixed` + `left: 50%` + `translateX(-50%)` — 뷰포트 가운데 고정
- `addEventListener` — 인라인 이벤트 핸들러 대신 JS 파일에서 관리하는 것이 원칙

### DB & 보안
- `db.ForeignKey` + `db.relationship(uselist=False)` — 1:1 관계 설정
- `generate_password_hash` / `check_password_hash` — 비밀번호 해시
- `session['key']` — 서버 메모장, `session.clear()`로 로그아웃
- CSRF — 위조 요청 공격, flask-seasurf로 보호 (GET 방식은 CSRF 불필요)
- `Vessel.query.filter_by(...).first()` — 중복 체크 패턴
- `Vessel.query.get_or_404(id)` — 단건 조회, 없으면 자동 404
- `Vessel.query.filter(Vessel.name.like(f"%{keyword}%"))` — 부분 검색 (LIKE)
- `query.filter(...).filter(...)` — 필터 중첩 (AND 조건)
- `query.filter((A) | (B))` — OR 조건 검색
- `request.args.get("key", "")` — GET 쿼리 파라미터 읽기
- `query.paginate(page=page, per_page=20, error_out=False)` — 페이지 단위 데이터 조회
- `try/except` + `db.session.rollback()` — DB 에러 발생 시 변경사항 되돌리기

### 권한 관리 (RBAC)
- `role = db.Column(db.String(20), nullable=False, default="viewer")` — 모델에 역할 컬럼 추가
- `@admin_required` — 데코레이터로 라우트 단위 권한 제어
- `@app.context_processor` — 모든 템플릿에 변수를 자동 주입하는 기능
- `{% if current_user and current_user.role == "admin" %}` — 템플릿에서 역할별 UI 분기

### API & 외부 연동
- `jsonify({'key': 'value'})` — Python 딕셔너리를 JSON 응답으로 변환
- `request.get_json()` — POST 요청의 JSON 바디를 Python 객체로 파싱
- `request.headers.get('X-API-Key')` — 요청 헤더에서 값 읽기
- `current_app.config['KEY']` — Blueprint 안에서 앱 설정값 읽는 방법
- `csrf.exempt_urls(('/api/',))` — CSRF 검증 예외 경로 등록
- truncate and insert 패턴 — `Model.query.delete()` 후 전체 새로 삽입
- `os.environ.get('KEY')` + `load_dotenv()` — 환경변수로 민감한 설정 관리

### 코드 품질 & 보안
- `except:` (bare except) — `KeyboardInterrupt`, `SystemExit`까지 잡아버림 → 반드시 `except Exception:`으로 좁힐 것
- 에러 메시지 외부 노출 — `str(e)` 그대로 반환하면 DB 구조 등 내부 정보 유출 → `'Internal server error'`로 고정
- `load_dotenv()` 위치 — 모듈 레벨보다 `create_app()` 안 첫 줄이 더 안전 (테스트 시 타이밍 문제 방지)
- `render_template("folder/file.html")` — 템플릿 하위 폴더 구조 사용 가능, 경로 문자열로 구분
- `url_for`는 **함수 이름**을 받음, 파일 경로 아님 — 템플릿 폴더 분리 시 `url_for`는 건드리지 않음
- `g` 객체 — 요청 1번 동안만 살아있는 임시 저장소, `before_request`와 함께 요청 초반에 데이터 세팅하는 패턴
- 최적화 판단 — 기본키 조회(`User.query.get(id)`) 중복은 소규모에서 성능 영향 없음, 복잡도 증가가 더 큰 손해일 수 있음
