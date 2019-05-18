from flask import Flask, render_template, redirect, url_for, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

app = Flask(__name__)


class Configs(object):
    """配置参数"""

    # sqlalchemy的配置参数
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:.@127.0.0.1:3306/db_YourDreams'

    # 设置sqlalchemy自动更新跟踪数据库
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # 使用form 表单必写
    SECRET_KEY = 'werqwerqe2346tyhgad'


# 应用配置文件
app.config.from_object(Configs)

# 创建数据库sqlalchemy对象
db = SQLAlchemy(app)

manager = Manager(app, db)
Migrate(app, db)
manager.add_command('db', MigrateCommand)


class Users(db.Model):
    """用户表信息"""
    __tablename__ = 'tbl_client_info'

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(32), unique=True)
    password = db.Column(db.String(32))
    email = db.Column(db.String(32), unique=True)


class RegisterForm(FlaskForm):
    """注册模型类"""
    user_name = StringField(label='帐号:', validators=[DataRequired('用户名必填')])
    password = StringField(label='密码:', validators=[DataRequired('密码必填')])
    email = StringField(label='邮箱:', validators=[DataRequired('邮箱必填')])
    submit = SubmitField(label='注册')


class LoginForm(FlaskForm):
    """登录模型类"""
    user_name = StringField(label='帐号:', validators=[DataRequired('用户名必填')])
    password = StringField(label='密码:', validators=[DataRequired('密码必填')])
    submit = SubmitField(label='登录')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """注册"""
    form = RegisterForm()
    # 查询数据库
    user_li = Users.query.all()
    if form.validate_on_submit():
        # 如果表单验证成功
        # 提取表单数据
        user_name = form.user_name.data
        password = form.password.data
        email = form.email.data

        # 保存数据库
        save_data = Users(user_name=user_name, password=password, email=email)
        db.session.add(save_data)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', user=user_li, form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """登录"""
    form = LoginForm()
    user_li = Users.query.all()

    if form.validate_on_submit():
        # 如果表单验证成功
        # 提取表单数据
        user_name = form.user_name.data
        password = form.password.data
        for i in user_li:
            if i.user_name == user_name and i.password == password:
                return render_template('index.html', user=i.user_name)
    return render_template('login.html', user=user_li, form=form)
    # return 'ok'


@app.route('/')
def index():
    return redirect(url_for('register'))


if __name__ == '__main__':
    manager.run()
