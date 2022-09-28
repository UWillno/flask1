
from datetime import datetime
import email
import random
from flask import Blueprint, render_template, request, redirect, url_for
from flask_mail import Message
from exts import mail, db
import string
from models import EmailCaptchaModel, UserModel

from .forms import RegisterForm

bp = Blueprint("user", __name__, url_prefix="/user")


@bp.route("/login")
def login():
    return render_template('login.html')


@bp.route("/register",methods=['GET','POST'])
def register():
    if request.method=='GET':
        return render_template('register.html')
    else:
        print(request.args)
        form = RegisterForm(request.form)
        if form.validate():
            username = form.username.data
            email = form.email.data
            password = form.password.data
            user = UserModel(username=username, email=email, password=password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('user.login'))
        else:
            return redirect(url_for('user.register'))


@bp.route("/captcha")
def get_captcha():
    letters = string.ascii_letters+string.digits
    captcha = "".join(random.sample(letters, 4))

    email = request.args.get('email')

    if email:
        message = Message(subject="test", recipients=[
            email], body=f"注册验证码为：{captcha}", sender="44910244@qq.com")
        mail.send(message)

        captcha_model = EmailCaptchaModel.query.filter_by(email=email).first()
        if captcha_model:
            captcha_model.captcha = captcha
            captcha_model.create_time = datetime.now()
            db.session.commit()
        else:
            captcha_model = EmailCaptchaModel(email=email, captcha=captcha)
            db.session.add(captcha_model)
            db.session.commit()
        return "success"
    else:
        return "没有邮箱"
