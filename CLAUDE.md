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
├── main.py              # Flask 앱 엔트리포인트 (라우트: /, /signup, /login, /logout, /vessel/new, /vessel/list, /vessel/<id>)
├── instance/
│   └── vessel.db        # SQLite 데이터베이스 파일
├── static/
│   ├── css/
│   │   ├── common.css        # CSS 리셋 & 공통 스타일 (header, .inner, .btn-primary, 플래시 메시지)
│   │   ├── index.css         # 메인 페이지 전용 스타일
│   │   ├── signup.css        # 회원가입 페이지 전용 스타일
│   │   ├── login.css         # 로그인 페이지 전용 스타일
│   │   ├── vessel_new.css    # 선박 등록 페이지 전용 스타일
│   │   ├── vessel_list.css   # 선박 목록 페이지 전용 스타일
│   │   └── vessel_detail.css # 선박 상세 페이지 전용 스타일 (CSS Grid 키-값 레이아웃)
│   └── js/
│       └── common.js         # 공통 JS (플래시 메시지 자동 숨김 + 애니메이션)
└── templates/
    ├── base.html             # 공통 레이아웃 (header, block css, block content, 플래시 메시지)
    ├── index.html            # 메인 페이지 (base.html 상속)
    ├── signup.html           # 회원가입 페이지 (base.html 상속)
    ├── login.html            # 로그인 페이지 (base.html 상속)
    ├── vessel_new.html       # 선박 등록 페이지 (base.html 상속, Vessel + VesselDetail 동시 등록)
    ├── vessel_list.html      # 선박 목록 페이지 (base.html 상속, 선박명 클릭 → 상세 이동)
    └── vessel_detail.html    # 선박 상세 페이지 (base.html 상속, dl/dt/dd + CSS Grid)
```

## 아키텍처 방향 (추후 리팩토링 목표)
- Blueprint + Application Factory 패턴 적용 예정
- 기능별 라우트 파일 분리 (routes/main.py, routes/vessel.py, routes/auth.py)
- 템플릿 base.html 공통 레이아웃 분리
- CSS 파일도 페이지별로 분리

## 진행 현황

### 완료
- [x] Flask 기본 세팅 (main.py)
- [x] CSS 리셋 (common.css)
- [x] 헤더 레이아웃 (네비게이션: 선박 리스트, 선박 등록, 로그인/로그아웃)
- [x] 히어로 섹션 (title-container: h1 + 버튼, flex column 세로 정렬)
- [x] 공통 버튼 스타일 (.btn-primary → common.css)
- [x] 메인 페이지 카드 섹션 (선박 등록, 선박 조회, 회원 가입 카드 3개)
- [x] 카드 호버 효과 (box-shadow, transform: translateY, transition)
- [x] 모바일 반응형 (미디어 쿼리 768px, 카드 세로 정렬, 메뉴 폰트 축소)
- [x] 카드 클릭 링크 연결 (url_for 활용)
- [x] 회원가입 페이지 HTML (signup.html)
- [x] 회원가입 라우트 (GET /signup)
- [x] 폼 스타일 (flex column, input 크기, :focus 효과)
- [x] CSS 구조 분리 (common.css / index.css / signup.css)
- [x] base.html 공통 레이아웃 (Jinja2 템플릿 상속)
- [x] SQLite + SQLAlchemy DB 연동 (User 모델, vessel.db 생성)
- [x] 회원가입 POST 처리 & DB 저장
- [x] 비밀번호 해시 처리 (werkzeug generate_password_hash)
- [x] HTML 유효성 검사 (required, minlength, maxlength)
- [x] 로그인 페이지 & 기능 (세션 개념 학습)
- [x] 로그아웃 기능 (session.clear())
- [x] 헤더 로그인/로그아웃 조건부 표시 (session.get('user_id'))
- [x] CSRF 보호 — flask-seasurf 적용 (폼에 _csrf_token hidden input 추가)
- [x] Vessel 모델 (name, imo_number, ship_type, gross_tonnage, flag)
- [x] 선박 등록 페이지 & 기능 (/vessel/new, GET/POST, 로그인 체크)
- [x] select 드롭다운 placeholder (value="" disabled selected + select:invalid CSS)
- [x] 선박 목록 페이지 & 기능 (/vessel/list, Vessel.query.all(), Jinja2 for 반복문)
- [x] 테이블 스타일 (border-collapse, th/td padding, tr:hover)
- [x] 플래시 메시지 기능 (flash(), get_flashed_messages(), 카테고리 success/info)
- [x] JS 파일 분리 (static/js/common.js)
- [x] 플래시 메시지 애니메이션 (@keyframes slideDown/slideUp, 3초 후 자동 퇴장)
- [x] 플래시 메시지 고정 위치 (position: fixed, left: 50%, translateX(-50%))
- [x] 선박 등록 후 리다이렉트 개선 (홈 → 선박 목록)
- [x] 중복 IMO 번호 등록 방지 (사전 조회 후 flash 에러 메시지)
- [x] 중복 선박명 등록 방지
- [x] 에러 시 등록 페이지 유지 (목록 리다이렉트 → render_template으로 변경)
- [x] flash-error 카테고리 스타일 추가 (common.css)
- [x] VesselDetail 모델 (ship_code, vessel_ro, vessel_class, built_year, team, crew)
- [x] Vessel ↔ VesselDetail 1:1 관계 설정 (ForeignKey, relationship)
- [x] 선박 등록 시 VesselDetail 동시 저장
- [x] 선박 상세 페이지 (/vessel/<int:vessel_id>, get_or_404, 로그인 체크)
- [x] vessel_detail.html (dl/dt/dd 구조, CSS Grid 키-값 레이아웃)
- [x] vessel_detail.css (Grid 레이아웃, 행 구분선, 모바일 반응형)
- [x] 선박 목록에서 선박명 클릭 → 상세 페이지 링크 연결

### 학습 메모
- `inline` vs `inline-block` vs `block` 차이 학습
- `flex-direction: column`으로 세로 배치 학습
- `box-shadow`, `transform`, `transition`으로 인터랙션 효과 학습
- `rgba(r, g, b, a)` — a는 투명도 (0 완전투명 ~ 1 완전불투명)
- `@media (max-width: 768px)` 미디어 쿼리로 모바일 반응형 학습
- `url_for('함수명')` — Flask가 경로를 자동 생성, 경로 변경에도 링크 유지
- `:focus` 가상 선택자로 input 포커스 스타일 적용
- `method="POST"` — 폼 데이터를 서버로 전송하는 방식
- `{% extends %}` / `{% block %}` — Jinja2 템플릿 상속으로 공통 레이아웃 관리
- `{% block css %}` — 페이지별 CSS를 base.html의 head에 추가하는 패턴
- `db.Model` — Python 클래스로 DB 테이블 정의 (ORM)
- `db.session.add()` / `db.session.commit()` — DB 저장 방식
- `generate_password_hash` / `check_password_hash` — werkzeug 비밀번호 해시
- `required`, `minlength`, `maxlength` — HTML 클라이언트 유효성 검사
- `session['key'] = value` — 딕셔너리처럼 사용하는 서버 메모장
- `session.clear()` — 로그아웃 시 세션 전체 초기화
- `session.get('user_id')` — Jinja2 템플릿에서 로그인 상태 확인
- `not user or not check_password_hash(...)` — 방어적 조건문 (인증 실패 처리)
- `SECRET_KEY` — 세션 쿠키 서명에 사용되는 비밀 키
- CSRF — 악성 사이트가 사용자 브라우저를 통해 위조 요청을 보내는 공격
- `_csrf_token` hidden input — 서버가 발급한 토큰으로 정상 폼 요청인지 검증
- `flask-seasurf` — Flask CSRF 보호 라이브러리, SeaSurf(app)으로 초기화
- `if not session.get('user_id')` — 접근 제어 패턴 (비로그인 시 로그인 페이지로 강제 이동)
- `<option value="" disabled selected>` — select 드롭다운 placeholder 구현 방법
- `select:invalid { color: #999 }` — placeholder 상태일 때 회색 글자 표시
- `Vessel.query.all()` — DB 전체 행 조회 (리스트 반환)
- `{% for vessel in vessels %} ... {% endfor %}` — Jinja2 반복문으로 목록 렌더링
- `border-collapse: collapse` — 테이블 셀 이중 테두리 제거
- `flash("메시지", "카테고리")` — 일회성 알림 메시지, 세션에 임시 저장
- `get_flashed_messages(with_categories=True)` — 템플릿에서 메시지 꺼내기, 꺼내면 자동 삭제
- `{% with messages = ... %}` — Jinja2 임시 변수 블록
- `setTimeout(함수, 시간)` — JS에서 일정 시간(ms) 후 함수 실행
- `document.querySelectorAll('.클래스')` — CSS 선택자로 여러 요소 한 번에 선택
- `forEach(function(item) {...})` — 리스트 각 요소를 순회 (Python for 루프와 동일 개념)
- `classList.add('클래스명')` — JS로 클래스를 동적으로 추가
- `@keyframes 이름 { from {...} to {...} }` — CSS 다단계 애니메이션 정의
- `animation: 이름 시간 easing forwards` — keyframes 애니메이션 적용, forwards는 끝 상태 유지
- `cubic-bezier(0.22, 1, 0.36, 1)` — 자연스러운 감속 곡선 easing
- `position: fixed` + `left: 50%` + `translateX(-50%)` — 뷰포트 기준 가운데 고정 정렬
- 마진 병합(Margin Collapsing) — 부모/자식 간 경계 없을 때 마진이 합쳐지는 현상, 큰 값이 적용됨
- `Vessel.query.filter_by(imo_number=...).first()` — 중복 체크 패턴 (저장 전 사전 조회)
- `db.ForeignKey('vessel.id')` — 두 테이블을 연결하는 외래키
- `db.relationship('VesselDetail', backref='vessel', uselist=False)` — 1:1 관계 설정, uselist=False가 핵심
- `new_vessel.detail = new_vessel_detail` — relationship으로 연결 후 add 하나만으로 두 테이블 동시 저장
- `@app.route("/vessel/<int:vessel_id>")` — 동적 라우트, URL의 숫자를 인자로 받음
- `Vessel.query.get_or_404(id)` — 단건 조회, 없으면 자동 404 반환
- `vessel.detail.ship_code` — relationship으로 연결된 테이블 데이터 접근
- `{{ value or "-" }}` — Jinja2에서 None/빈값일 때 기본값 표시
- `url_for('vessel_detail', vessel_id=vessel.id)` — 동적 라우트에 인자 전달
- `display: grid` + `grid-template-columns: 1fr 2fr` — CSS Grid로 키-값 레이아웃 구현
- `fr` — fraction(분수), 남은 공간을 비율로 나누는 Grid 단위
- `value="{{ vessel.xxx }}"` — input pre-fill로 기존 값 표시 (수정 폼에서 활용)
- `{% if vessel.field == "값" %}selected{% endif %}` — select 현재 값 표시 패턴
- `db.session.delete(객체)` — DB 행 삭제, 자식 테이블 먼저 삭제 후 부모 삭제
- `addEventListener('submit', ...)` — 폼 제출 이벤트를 JS에서 감지
- `event.preventDefault()` — 브라우저 기본 동작(폼 제출 등) 취소
- 인라인 이벤트 핸들러(`onsubmit="..."`) 대신 JS 파일에서 `addEventListener`로 관리하는 것이 원칙

### 다음 단계

#### 로드맵
1. CRUD 완성 → 2. 리팩토링 → 3. 검색/조회 기능

#### 1단계 — CRUD 완성
- [x] 선박 수정 기능 (/vessel/<id>/edit, GET/POST, Vessel + VesselDetail 동시 수정)
- [x] 선박 삭제 기능 (/vessel/<id>/delete, POST, VesselDetail 먼저 삭제 후 cascade)

#### 2단계 — 리팩토링 (Blueprint 패턴)
- [ ] Blueprint 적용 (routes/auth.py, routes/vessel.py, routes/main.py)
- [ ] Application Factory 패턴 (create_app())

#### 3단계 — 검색/조회 기능
- [ ] 선박 검색 (선박명, 선종, 기국 등 필터링)
- [ ] 페이지네이션

#### 4단계 — 권한 관리 (RBAC)
- [ ] User 모델에 role 필드 추가 (admin / manager / viewer)
- [ ] 역할별 접근 제어 (등록/수정/삭제는 admin, 조회는 viewer도 가능)
