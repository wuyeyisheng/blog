# 模型
import datetime

from .exts import db


# commend = db.Table(
#     'commend',
#     db.Column(db.Integer, primary_key=True, autoincrement=True),
#     db.Column('user_id', db.Integer, db.ForeignKey("User.id")),
#     db.Column('article_id', db.Integer, db.ForeignKey("Article.id")),
#     db.Column('info', db.TEXT, default=''),
#     db.Column('time', db.DateTime, default=datetime.datetime.now())
# )


class User(db.Model):
    '''
        用户表
    '''
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(255))
    info = db.Column(db.TEXT)
    icon = db.Column(db.String(255))  # 用户的图像。
    time = db.Column(db.DateTime)
    is_super = db.Column(db.Boolean)
    is_delete = db.Column(db.Boolean)

    articles = db.relationship('Article', backref='ariticle_user', lazy=True)
    comments = db.relationship('Commend', backref='comment_user', lazy=True)


class AriticleType(db.Model):
    '''
        文章类型
    '''
    __tablename__ = 'articletype'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(25))
    othername = db.Column(db.String(25))  # 别名
    time = db.Column(db.DateTime)
    # 父类的ID
    father_type = db.Column(db.Integer, default=False)

    articles = db.relationship('Article', backref='ariticletype', lazy=True)


class Article(db.Model):
    '''
        文章表
    '''
    __tablename__ = "article"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userid = db.Column(db.Integer, db.ForeignKey(User.id))
    title = db.Column(db.String(50))
    text = db.Column(db.TEXT)
    time = db.Column(db.DateTime)
    picture = db.Column(db.String(255))
    num = db.Column(db.Integer) # 点击量
    introduce = db.Column(db.String(255)) # 简介
    type = db.Column(db.Integer, db.ForeignKey(AriticleType.id))

    is_recommand = db.Column(db.Boolean)
    # 评论的字段
    commend = db.relationship('Commend', backref='article', lazy=True)


class Photo(db.Model):
    '''
        用户发布的照片墙。
    '''
    __tablename__ = 'photo'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    info = db.Column(db.TEXT)
    picture = db.Column(db.String(255))
    time = db.Column(db.DateTime)
    type = db.Column(db.Integer)


class Commend(db.Model):
    '''
        用户评论表
    '''
    __tablename__ = 'commend'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userid = db.Column(db.Integer, db.ForeignKey(User.id))
    articleid = db.Column(db.Integer, db.ForeignKey(Article.id))

    info = db.Column(db.TEXT)
    time = db.Column(db.DateTime)
