from datetime import datetime
import email
import json
import random
from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session, flash
from flask_mail import Message
from exts import mail, db
import string
from models import EmailCaptchaModel, UserModel
from werkzeug.security import generate_password_hash, check_password_hash
from .forms import LoginForm, RegisterForm

bp = Blueprint("user", __name__, url_prefix="/user")


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('user.login'))


@bp.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            user = UserModel.query.filter_by(email=email).first()
            if user and check_password_hash(user.password, password):
                session['user_id'] = user.id
                return redirect("/")
            else:
                flash("邮箱或密码错误！")
                return redirect(url_for('user.login'))
        else:
            flash("邮箱或密码格式错误！")
            return redirect(url_for('user.login'))


@bp.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        print(request.args)
        form = RegisterForm(request.form)
        if form.validate():
            username = form.username.data
            email = form.email.data
            password = form.password.data
            hash_password = generate_password_hash(password)

            user = UserModel(username=username, email=email,
                             password=hash_password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('user.login'))
        else:
            return redirect(url_for('user.register'))


@bp.route("/captcha", methods=['POST'])
def get_captcha():
    letters = string.ascii_letters+string.digits
    captcha = "".join(random.sample(letters, 4))
    # get用args post用forms
    # email = request.args.get('email')
    email = request.form.get('email')

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
        return jsonify({"code": 200})
    else:
        return jsonify({"code": 400, "message": "请先传递邮箱"})
