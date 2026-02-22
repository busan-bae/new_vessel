from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# USER 모델 ㅈ클래스 정의 db 테이블 
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # 고유 ID (자동 증가)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20),nullable=False, default="viewer")

class Vessel(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # 고유 ID (자동 증가)
    name = db.Column(db.String(100), nullable=False)
    imo_number = db.Column(db.Integer, unique=True, nullable=False)
    ship_type = db.Column(db.String(50), nullable=False)
    ship_size = db.Column(db.String(20), nullable=False)
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