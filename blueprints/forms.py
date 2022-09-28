import wtforms
from wtforms.validators import email,length,EqualTo
from blueprints import user

from models import EmailCaptchaModel, UserModel


class RegisterForm(wtforms.Form):
    username=wtforms.StringField(validators=[length(min=3,max=20)])
    email=wtforms.StringField(validators=[email()])
    captcha=wtforms.StringField(validators=[length(min=4,max=4)])
    password=wtforms.StringField(validators=[length(min=6,max=20)])
    password_confirm=wtforms.StringField(validators=[EqualTo("password")])

    def validate_captcha(self,field):
        captcha=field.data
        email=self.email.data
        captcha_model=EmailCaptchaModel.query.filter_by(email=email).first()
        if not captcha_model or captcha_model.captcha.lower() != captcha.lower():
            raise  wtforms.ValidationError("验证码错误！")

    def validate_email(self,field):
        email=field.data
        user_model=UserModel.query.filter_by(email=email).first()
        if user_model:
            raise wtforms.ValidationError("邮箱已经存在！")

    # def validate_username(self,field):
    #     username=field.data
    #     user_model=UserModel.query.filter_by(username=username).first()
    #     if user_model:
    #         raise wtforms.ValidationError("用户名已经存在！")