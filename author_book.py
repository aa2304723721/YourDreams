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
    SECRET_KEY = 'skdfpoisdg8sdfgsdf8gdfg'


# 应用配置文件
app.config.from_object(Configs)

# 创建数据库sqlalchemy对象
db = SQLAlchemy(app)

# 创建flask脚本管理工具对象
manager = Manager(app, db)

# 创建数据库迁移工具对象
Migrate(app, db)

# 向manager对象中添加数据库的操作命令
manager.add_command('db', MigrateCommand)


class Author(db.Model):
    """作者表"""
    __tablename__ = 'tbl_authors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    email = db.Column(db.String(128), unique=True)
    books = db.relationship('Book', backref='author')


class Book(db.Model):
    """图书表"""
    __tablename__ = 'tbl_books'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    author_id = db.Column(db.Integer, db.ForeignKey('tbl_authors.id'))


class AuthorBookForm(FlaskForm):
    """作者数据表单模型类"""
    author_name = StringField(label='作者:', validators=[DataRequired('作者必填')])
    book_name = StringField(label='书名:', validators=[DataRequired('书名必填')])
    email_address = StringField(label='邮箱:', validators=[DataRequired('邮箱必填')])
    lead = StringField(label='人物:', validators=[DataRequired('人物必填')])
    submit = SubmitField(label='提交')


@app.route('/', methods=['GET', 'POST'])
def index():
    """主页"""
    # 创建表单对象
    form = AuthorBookForm()

    if form.validate_on_submit():
        # 如果表单验证成功
        # 提取表单数据
        author_name = form.author_name.data
        book_name = form.book_name.data
        email_addres = form.email_address.data
        leader = form.lead.data

        # 保存数据库
        author = Author(name=author_name, email=email_addres)
        db.session.add(author)
        db.session.commit()

        # 通过Book的author_id拿取作者id
        book = Book(name=book_name, lead=leader, author_id=author.id)
        # 通过Author的backref反向拿取作者id
        # book = Book(name=book_name,lead=lead,author=author)
        db.session.add(book)
        db.session.commit()

    # 查询数据库
    author_li = Author.query.all()
    return render_template('author_book.html', author=author_li, form=form)


# @app.route('/delete_book',methods=['POST'])
# def delete_book():
#     """post请求方式删除数据,接收前端发送回来的json数据"""
#     # 提取参数
#     # 如果前端发送的请求体数据是json格式,get_json会解析成字典
#     req_dict = request.get_json()
#     book_id = req_dict.get('book_id')
#
#     # 删除数据
#     # 获取书籍信息
#     book = Book.query.get(book_id)
#     # 获取作者信息
#     author = Author.query.get(book.author_id)
#     # 删除作者
#     db.session.delete(author)
#     # 删除书籍
#     db.session.delete(book)
#     # 提交操作
#     db.session.commit()
#
#     # 前端返回的数据类型为"Content-Type":"application/json"
#     return jsonify(code=0,message='OK')

# /delete_book?book_id=1

@app.route('/delete_book', methods=['GET'])
def delete_book():
    """get请求方式删除数据,接收前端发送回来的url"""
    # 提取参数
    # 直接拿区前端发送回来的url中的book_id
    book_id = request.args.get('page')

    # 删除数据
    # 获取书籍信息
    book = Book.query.get(book_id)
    # 获取作者信息
    author = Author.query.get(book.author_id)
    # 删除作者
    db.session.delete(author)
    # 删除书籍
    db.session.delete(book)
    # 提交操作
    db.session.commit()

    return redirect(url_for('index'))


if __name__ == '__main__':
    # # 删除数据库所有数据
    # db.drop_all()
    # db.create_all()
    #
    # # 生成数据
    # au_xi = Author(name='我吃西红柿', email='xihongshi@163.com')
    # au_qian = Author(name='萧潜', email='xiaoqian@126.com')
    # au_san = Author(name='唐家三少', email='sanshao@163.com')
    # db.session.add_all([au_xi, au_qian, au_san])
    # db.session.commit()
    #
    # bk_xi = Book(name='吞噬星空', lead='罗峰', author_id=au_xi.id)
    # bk_xi2 = Book(name='寸芒', lead='李杨', author_id=au_qian.id)
    # bk_qian = Book(name='飘渺之旅', lead='李强', author_id=au_qian.id)
    # bk_san = Book(name='冰火魔厨', lead='融念冰', author_id=au_san.id)
    # db.session.add_all([bk_xi, bk_xi2, bk_qian, bk_san])
    # db.session.commit()

    # app.run(debug=True)
    manager.run()
