# 模型

from .exts import db


class User(db.Model):
    # 表名
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(255))
    info = db.Column(db.TEXT)
    time = db.Column(db.DateTime)
    is_super = db.Column(db.Boolean)
    is_delete = db.Column(db.Boolean)


class Ariticle(db.Model):
    # 文章表
    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name =




