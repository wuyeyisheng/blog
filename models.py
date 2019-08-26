# coding: utf-8
from sqlalchemy import Column, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.mysql import INTEGER, LONGTEXT, TINYINT
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class ArticleType(Base):
    __tablename__ = 'article_type'

    id = Column(INTEGER(11), primary_key=True)
    name = Column(String(25))
    time = Column(DateTime)
    father_type = Column(INTEGER(11))


class Paper(Base):
    __tablename__ = 'paper'

    id = Column(INTEGER(11), primary_key=True)
    picture = Column(String(255))


class User(Base):
    __tablename__ = 'user'

    id = Column(INTEGER(11), primary_key=True)
    name = Column(String(20))
    info = Column(LONGTEXT)
    time = Column(DateTime)
    is_super = Column(TINYINT(1))
    is_delete = Column(TINYINT(1))


class Photo(User):
    __tablename__ = 'photo'

    id = Column(ForeignKey('user.id'), primary_key=True)
    info = Column(Text)
    picture = Column(String(255))
    time = Column(DateTime)
    type = Column(INTEGER(11))


class Article(Base):
    __tablename__ = 'article'

    id = Column(INTEGER(11), primary_key=True)
    userid = Column(ForeignKey('user.id'), index=True)
    title = Column(String(20))
    text = Column(LONGTEXT)
    time = Column(DateTime)
    picture = Column(ForeignKey('paper.id'), index=True)
    type = Column(ForeignKey('article_type.id'), index=True)
    is_recommand = Column(TINYINT(1))

    paper = relationship('Paper')
    article_type = relationship('ArticleType')
    user = relationship('User')


class Command(Base):
    __tablename__ = 'command'

    id = Column(INTEGER(11), primary_key=True)
    userid = Column(ForeignKey('user.id'), index=True)
    visitid = Column(ForeignKey('user.id'), index=True)
    command_user = Column(INTEGER(11))
    info = Column(String(255))
    time = Column(DateTime)

    user = relationship('User', primaryjoin='Command.userid == User.id')
    user1 = relationship('User', primaryjoin='Command.visitid == User.id')
