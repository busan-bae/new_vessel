from flask import Flask, render_template, request,redirect, url_for,session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_seasurf import SeaSurf

# Flask 객체 생성 
# __name__ : 현재 실행중인 모듈의 이름
app = Flask(__name__)

# DB파일 위치 설정 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vessel.db'  # SQLite 데이터베이스 URI 설정

# 시크릿 키 설정 (세션 관리)
# 실제로는 안전한 키로 변경해야 함  ----> 추후 환경변수로 관리 예정 
app.config['SECRET_KEY'] = "my_secret_key_top"  

# SQLAlchemy 객체 생성
db = SQLAlchemy(app)

# csrf 객체 생성
csrf = SeaSurf(app)

# USER 모델 ㅈ클래스 정의 db 테이블 
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # 고유 ID (자동 증가)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    
class Vessel(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # 고유 ID (자동 증가)
    name = db.Column(db.String(100), nullable=False)
    imo_number = db.Column(db.String(20), unique=True, nullable=False)
    ship_type = db.Column(db.String(50), nullable=False)
    gross_tonnage = db.Column(db.Integer, nullable=False)
    flag = db.Column(db.String(50),nullable=False)
    detail = db.relationship('VesselDetail', backref='vessel', uselist=False)  # VesselDetail과 1:1 관계 설정

class VesselDetail(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # 고유 ID (자동 증가)
    vessel_id = db.Column(db.Integer, db.ForeignKey('vessel.id'), nullable=False)  # Vessel 테이블과의 외래키
    ship_code = db.Column(db.String(6), nullable=False)
    vessel_ro = db.Column(db.String(20), nullable=False)
    vessel_class = db.Column(db.String(20), nullable=False)
    built_year = db.Column(db.String(50), nullable=True)
    team = db.Column(db.String(50), nullable=False)
    crew = db.Column(db.String(50), nullable=False)

    
    
    
# 데이터베이스 테이블 생성
with app.app_context():
    db.create_all()

# 홈화면 라우트 설정
@app.route("/") 
def home():
    return render_template("index.html")  # index.html 템플릿 렌더링

@app.route("/signup", methods=["GET", "POST"]) 
def signup():
    
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        hashed_password = generate_password_hash(password)  # 비밀번호 해싱
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("home"))  # 회원가입 후 홈 화면으로 리디렉션
    
    return render_template("signup.html")  # signup.html 템플릿 렌더링

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST" :
        username = request.form.get("username")
        password = request.form.get("password")
        
        # DB에서 사용자 조회
        user = User.query.filter_by(username=username).first()
        
        # 사용자가 없거나 비밀번호가 틀린경우
        if not user or not check_password_hash(user.password, password):
            return render_template("login.html",error="아이디 또는 비밀번호가 일치하지 않습니다.")
        
        # 로그인 성공 -> 세션이 사용자 ID 저장
        session['user_id'] = user.id
        flash("로그인 성공!", "success")
        return redirect(url_for("home"))  # 로그인 성공 후 홈 화면으로 리디렉션
    
    return render_template("login.html")  # login.html 템플릿 렌더링

@app.route("/logout")
def logout():
    # 세션 전체 초기화
    session.clear()
    flash("로그아웃 되었습니다.", "info")
    return redirect(url_for("home"))

@app.route("/vessel/new", methods=["GET", "POST"])
def vessel_new():
    # 로그인 여부 확인 -> 비 로그인시 로그인 페이지 이동
    if not session.get('user_id'):
        return redirect(url_for("login"))
    
    if request.method == "POST":
        name = request.form.get("name")
        imo_number = request.form.get("imo_number")
        ship_type = request.form.get("ship_type")
        gross_tonnage = request.form.get("gross_tonnage")
        flag = request.form.get("flag")
        

        ship_code = request.form.get("ship_code")
        vessel_ro = request.form.get("vessel_ro")
        vessel_class = request.form.get("vessel_class")
        built_year = request.form.get("built_year")
        team = request.form.get("team")
        crew = request.form.get("crew")
        
    
        
        if Vessel.query.filter_by(imo_number=imo_number).first():
            flash("이미 등록된 IMO 번호입니다.", "error")
        elif Vessel.query.filter_by(name=name).first():
            flash("이미 등록된 선박 이름입니다.", "error")    
        else:
            new_vessel = Vessel(
            name=name, 
            imo_number=imo_number, 
            ship_type=ship_type, 
            gross_tonnage=gross_tonnage, 
            flag=flag
            )
            
            new_vessel_detail = VesselDetail(
            ship_code=ship_code,
            vessel_ro=vessel_ro,
            vessel_class=vessel_class,
            built_year=built_year,
            team = team,
            crew = crew
            ) 
            
            new_vessel.detail = new_vessel_detail  # Vessel과 VesselDetail 연결
            
            db.session.add(new_vessel)
            db.session.commit()
            flash("선박 등록이 완료되었습니다.", "success")
            return redirect(url_for("vessel_list"))  # 선박 등록 후 선박 목록 페이지로 리디렉션
    
    return render_template("vessel_new.html")
    

@app.route("/vessel/list", methods=["GET"])
def vessel_list():
    # 로그인 여부 확인 -> 비 로그인시 로그인 페이지 이동
    if not session.get('user_id'):
        return redirect(url_for("login"))
    
    vessels = Vessel.query.all()  # DB에서 모든 선박 정보 조회
    return render_template("vessel_list.html", vessels=vessels)  # vessel_list.html 템플릿 렌더링


@app.route("/vessel/<int:vessel_id>", methods=["GET"])
def vessel_detail(vessel_id):
    # 로그인 여부 확인 -> 비 로그인시 로그인 페이지 이동
    if not session.get('user_id'):
        return redirect(url_for("login"))
    
    vessel = Vessel.query.get_or_404(vessel_id)# DB에서 해당 ID의 선박 정보 조회, 없으면 404 에러)   
    return render_template("vessel_detail.html", vessel=vessel)  # vessel_list.html 템플릿 렌더링

@app.route("/vessel/<int:vessel_id>/edit", methods=["GET", "POST"])
def vessel_edit(vessel_id):
    # 로그인 여부 확인 -> 비 로그인시 로그인 페이지 이동
    if not session.get('user_id'):
        return redirect(url_for("login"))    
    
    vessel = Vessel.query.get_or_404(vessel_id)# DB에서 해당 ID의 선박 정보 조회, 없으면 404 에러)   

    if request.method == "POST":
        name = request.form.get("name")
        imo_number = request.form.get("imo_number")
        ship_type = request.form.get("ship_type")
        gross_tonnage = request.form.get("gross_tonnage")
        flag = request.form.get("flag")
        
        ship_code = request.form.get("ship_code")
        vessel_ro = request.form.get("vessel_ro")
        vessel_class = request.form.get("vessel_class")
        built_year = request.form.get("built_year")
        team = request.form.get("team")
        crew = request.form.get("crew")
        
        vessel.name = name
        vessel.imo_number = imo_number
        vessel.ship_type = ship_type
        vessel.gross_tonnage = gross_tonnage
        vessel.flag = flag
        vessel.detail.ship_code = ship_code
        vessel.detail.vessel_ro = vessel_ro
        vessel.detail.vessel_class = vessel_class
        vessel.detail.built_year = built_year
        vessel.detail.team = team
        vessel.detail.crew = crew
        
        vessel.detail.vessel = vessel
        db.session.commit()
        flash("선박 정보가 수정되었습니다.","success")
        return redirect(url_for("vessel_detail", vessel_id=vessel.id))  # 수정 후 선박 상세 페이지로 리디렉션
    
    return render_template("vessel_edit.html", vessel=vessel)  # vessel_edit.html 템플릿 렌더링

@app.route("/vessel/<int:vessel_id>/delete", methods=["POST"])
def vessel_delete(vessel_id):
   # 로그인 여부 확인 -> 비 로그인시 로그인 페이지 이동
    if not session.get('user_id'):
        return redirect(url_for("login"))    
    
    vessel = Vessel.query.get_or_404(vessel_id)# DB에서 해당 ID의 선박 정보 조회, 없으면 404 에러)   
    
    try:
        db.session.delete(vessel.detail)
    except:
        pass
        
    db.session.delete(vessel)
    db.session.commit()
    flash("선박 정보가 삭제되었습니다.","success")
    return redirect(url_for("vessel_list"))

# 이 파일이 직접 실행될 때만 아래 코드가 실행되도록 하는 조건문
# 즉, 다른 모듈에서 import 될 때는 실행되지 않도록 함
if __name__ == "__main__":
    app.run(debug=True)