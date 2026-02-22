from flask import session, redirect, url_for, flash, request
from functools import wraps
from models import User

def login_required(func): # 함수를 인자로 받음
    @wraps(func)
    def wrapper(*args,**kwargs):
        if not session.get('user_id'): # 로그인 체크
            return redirect(url_for("auth.login"))
        return func(*args,**kwargs) # 로그인 됐으면 원래 함수 실행
    return wrapper
    
def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user = User.query.get(session.get('user_id'))  # 현재 로그인 유저 조회
        if not user or user.role != "admin":            # admin이 아니면 차단
            flash("접근 권한이 없습니다.", "error")
            return redirect(request.referrer or url_for("vessel.vessel_list"))
        return func(*args, **kwargs)
    return wrapper