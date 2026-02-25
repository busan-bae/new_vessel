from flask import Blueprint, render_template,request,redirect,url_for,session,flash
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User

auth_bp = Blueprint('auth',__name__)

@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        # username 중복 체크
        if User.query.filter_by(username=username).first():
            flash("이미 사용 중인 아이디입니다.", "error")
            return render_template("signup.html")
        
        hashed_password = generate_password_hash(password)  # 비밀번호 해싱
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("main.home"))  # 회원가입 후 홈 화면으로 리디렉션
    
    return render_template("signup.html")  # signup.html 템플릿 렌더링

@auth_bp.route("/login", methods=["GET", "POST"])
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
        return redirect(url_for("main.home"))  # 로그인 성공 후 홈 화면으로 리디렉션
    
    return render_template("login.html")  # login.html 템플릿 렌더링

@auth_bp.route("/logout")
def logout():
    # 세션 전체 초기화
    session.clear()
    flash("로그아웃 되었습니다.", "info")
    return redirect(url_for("main.home"))