# url+视图函数
from flask import Blueprint, render_template
from .models import *

blog = Blueprint('blog', __name__)
admin = Blueprint('admin', __name__)


@blog.route('/')
def home():
    return 'HOME'


@blog.route('/index/')
def index():
    return render_template('blog/index.html')


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

