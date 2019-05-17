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

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:.@127.0.0.1:3306/db_YourDreams'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = 'skdfpoisdg8sdfgsdf8gdfg'


app.config.from_object(Configs)
db = SQLAlchemy(app)
manager = Manager(app, db)
Migrate(app, db)
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
    lead = db.Column(db.String(32))
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
    form = AuthorBookForm()
    if form.validate_on_submit():
        author_name = form.author_name.data
        book_name = form.book_name.data
        email_addres = form.email_address.data
        leader = form.lead.data
        author = Author(name=author_name, email=email_addres)
        db.session.add(author)
        db.session.commit()
        book = Book(name=book_name, lead=leader, author_id=author.id)
        db.session.add(book)
        db.session.commit()

    # 查询数据库
    author_li = Author.query.all()
    return render_template('author_book.html', author=author_li, form=form)


@app.route('/delete_book', methods=['GET'])
def delete_book():
    """get请求方式删除数据,接收前端发送回来的url"""
    book_id = request.args.get('page')
    book = Book.query.get(book_id)
    author = Author.query.get(book.author_id)
    db.session.delete(author)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    manager.run()
