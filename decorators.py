
import imp
from flask import g,redirect,url_for
from functools import wraps


def login_required(func):
    # 装饰器
    @wraps(func)
    def wrapper(*arg,**kwargs):
        if hasattr(g,'user'):
            return func(*arg,**kwargs)
        else:
            return redirect(url_for('user.login'))

    return wrapper
