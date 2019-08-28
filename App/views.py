# url+视图函数
from flask import Blueprint, render_template, jsonify
from .models import *

blog = Blueprint('blog', __name__)
admin = Blueprint('admin', __name__)


@blog.route('/')
def home():
    # 用户的个人信息
    user = User.query.all()[0]
    # 查询所有的文章
    arts = Article.query.all()
    # 查询图片
    ablums = Photo.query.all()
    # 查看自己分类
    types = AriticleType.query.all()

    data = {
        "user":user,
        "arts":arts,
        "ablums":ablums,
        "types":types,
    }

    return render_template('blog/index.html', **data)

@blog.route("/info/<id>")
def info(id):
    '''
    文章详细内容
    :return:
    '''
    article = Article.query.get(id)
    # 查询所有的文章
    arts = Article.query.all()
    # 查看自己分类
    types = AriticleType.query.all()
    data = {
        "article":article,
        "arts":arts,
        "types": types,
    }
    return render_template("blog/info.html", **data)

@blog.route("/share/")
def share():
    '''
    图片壁纸的分类
    :return:
    '''
    return render_template("blog/share.html")

@blog.route("/about/")
def about():
    '''
    关于我
    :return:
    '''
    return render_template("blog/about.html")

@blog.route("/gbook/")
def gbook():
    '''
    关于我
    :return:
    '''
    return render_template("blog/gbook.html")


@blog.route("/type/<id>")
def clicktype(id):
    '''
    点击分类的接口
    :param id:
    :return:
    '''
    data = {

    }
    return jsonify()



@blog.route("/articleType/")
def articleType():

    return jsonify()


# ===============管理员摄图===============================


# 管理首页
@admin.route('/admin/')
def amdin_index():
    return render_template('admin/index.html')


# 文章管理
@admin.route('/article/')
def amdin_article():
    return render_template('admin/article.html')


# 栏目管理
@admin.route('/category/')
def amdin_category():
    return render_template('admin/category.html')

