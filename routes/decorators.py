from flask import session, redirect, url_for
from functools import wraps

def login_required(func): # 함수를 인자로 받음
    @wraps(func)
    def wrapper(*args,**kwargs):
        if not session.get('user_id'): # 로그인 체크
            return redirect(url_for("auth.login"))
        return func(*args,**kwargs) # 로그인 됐으면 원래 함수 실행
    return wrapper
    
