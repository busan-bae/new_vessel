from flask import Flask, render_template,session
from flask_seasurf import SeaSurf
from models import db, User
from routes.main import main_bp
from routes.auth import auth_bp
from routes.vessel import vessel_bp

def create_app():
    app = Flask(__name__)
    
    # DB파일 위치 설정 
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vessel.db'  # SQLite 데이터베이스 URI 설정

    # 시크릿 키 설정 (세션 관리)
    # 실제로는 안전한 키로 변경해야 함  ----> 추후 환경변수로 관리 예정 
    app.config['SECRET_KEY'] = "my_secret_key_top"  
    
    db.init_app(app)
    SeaSurf(app)
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(vessel_bp) 
    
    with app.app_context():
        db.create_all()
    
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("404.html"), 404
    
    @app.errorhandler(500)
    def server_error(e):
        return render_template("500.html"), 500
    
    @app.context_processor
    def inject_user():
        user = User.query.get(session.get('user_id'))  # 현재 로그인 유저 조회
        return dict(current_user=user)  
    
    return app