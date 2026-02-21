from flask import Blueprint,render_template

main_bp = Blueprint('main', __name__)

@main_bp.route("/") #app 대신 main_bp 사용
def home():
    return render_template("index.html")  # index.html 템플릿 렌더링
