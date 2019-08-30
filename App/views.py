# url+视图函数
from flask import Blueprint, render_template, jsonify, request, redirect, url_for
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
        "user": user,
        "arts": arts,
        "ablums": ablums,
        "types": types,
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
        "article": article,
        "arts": arts,
        "types": types,
    }
    return render_template("blog/info.html", **data)


@blog.route("/share/")
def share():
    '''
    图片壁纸的分类
    :return:
    '''
    photos = Photo.query.all()
    data = {
        "photos": photos,
    }
    return render_template("blog/share.html", **data)


@blog.route("/about/")
def about():
    '''
    关于我
    :return:
    '''
    # 用户的个人信息
    user = User.query.all()[0]
    # 查询图片
    ablums = Photo.query.all()
    data = {
        "user": user,

        "ablums": ablums,

    }
    return render_template("blog/about.html", **data)


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
    articles = AriticleType.query.get(id)
    return jsonify(articles.to_dict())


@blog.route("/articleType/")
def articleType():
    # 查看自己分类
    types = AriticleType.query.all()
    # 查询所有的文章
    arts = Article.query.all()
    arts_list = [art.to_dict() for art in arts]
    types_list = [type.to_dict() for type in types]
    data = {
        "types": types_list,
        "arts": arts_list,
    }

    return jsonify(data)


# ===============管理员摄图===============================


# 管理首页
@admin.route('/admin/')
def amdin_index():
    # 获取全部的文章
    userid = request.cookies.get("user") or "1"

    arts = Article.query.filter_by(userid=userid)

    ip = request.remote_addr

    data = {
        "arts": list(arts),
        "time": str(datetime.datetime.now())[:str(datetime.datetime.now()).rfind(".")],
        "ip": ip,
    }

    return render_template('admin/index.html', **data)


# 文章管理| 删除操作
@admin.route('/article/', methods=["GET", "POST", "PUT", "DELETE"])
def amdin_article():
    if request.method == "GET":
        userid = request.cookies.get("user") or "1"

        page = int(request.args.get("pg", 1))
        per_page = int(request.args.get("per_page", 3))
        arts = Article.query.filter_by(userid=userid).paginate(page, per_page, error_out=False)

        data = {
            "arts": list(arts.items),
            "pgs":arts


        }
        return render_template('admin/article.html', **data)
    elif request.method == "POST":
        try:
            infos = request.form.getlist("checkbox[]")
            for art in infos:
                artid = Article.query.get(art)
                db.session.delete(artid)
                db.session.commit()

            return redirect("/article/")
        except:
            return redirect('/article/?error=删除错误')


# 文章修改管理
@admin.route('/update/<id>', methods=["GET", "POST", "PUT", "DELETE"])
def amdin_update(id):
    if request.method == "GET":
        userid = request.cookies.get("user") or "1"

        arts = Article.query.get(id)
        print(arts)
        data = {
            "arts": arts.to_dict(),
            "arttype": AriticleType.query.all()
        }

        return render_template('admin/update-article.html', **data)

    elif request.method == "POST":
        info = request.form
        title = Article.query.get(info.get("articleid"))
        title.title = info.get("title")
        title.text = info.get("content")
        title.tag = info.get("keywords")
        title.picture = info.get("titlepic")
        title.introduce = info.get("describe")
        title.type = info.get("category")

        title.time = datetime.datetime.now()

        db.session.commit()

        return redirect(url_for("admin.amdin_article"))


# 文章添加管理
@admin.route('/add/', methods=["GET", "POST", "PUT", "DELETE"])
def add_article():
    if request.method == "GET":
        userid = request.cookies.get("user") or "1"

        data = {
            "arttype": AriticleType.query.all()
        }

        return render_template('admin/add-article.html', **data)

    elif request.method == "POST":
        userid = request.cookies.get("user") or "1"
        info = request.form
        title = Article()
        title.userid = userid
        title.title = info.get("title")
        title.text = info.get("content")
        title.time = datetime.datetime.now()

        title.tag = info.get("keywords")
        title.picture = info.get("titlepic")
        title.introduce = info.get("describe")
        title.num = 0
        title.is_recommand = 0
        title.type = info.get("category")

        db.session.add(title)
        db.session.commit()

        return redirect(url_for("admin.amdin_article"))


# 栏目管理 | 增| 删| 查
@admin.route('/category/', methods=["GET", "POST", "PUT", "DELETE"])
def amdin_category():
    if request.method == "GET":
        data = {
            "arttypes": AriticleType.query.all()
        }
        return render_template('admin/category.html', **data)
    elif request.method == "POST":
        info = request.form
        titletype = AriticleType()
        titletype.name = info.get("name")
        titletype.othername = info.get("alias")
        titletype.time = datetime.datetime.now()

        titletype.father_type = info.get("fid")

        db.session.add(titletype)
        db.session.commit()

        return redirect(url_for("admin.amdin_category"))

    elif request.method == "PUT":
        pass
    elif request.method == "DELETE":
        try:
            info = request.form
            tittype = AriticleType.query.get(info.get("id"))
            db.session.delete(tittype)
            db.session.commit()
            return jsonify({"code": 1})
        except:
            return jsonify({"code": 0})

@admin.route('/category_update/<id>', methods=["GET", "POST", "PUT", "DELETE"])
def amdin_category_update(id):
    if request.method == "GET":
        art = AriticleType.query.get(id)
        try:
            print(art.father_type)
            fart = AriticleType.query.get(art.father_type)

        except:
            fart = "暂无父节点"
        print(fart)
        data = {
            "arts":AriticleType.query.all(),
            "arttype": art.to_dict(),
            "fart":fart
        }
        return render_template('admin/update-category.html', **data)

    elif request.method == "POST":
        info = request.form
        titletype = AriticleType.query.get(id)
        titletype.name = info.get("name")
        titletype.othername = info.get("alias")

        titletype.father_type = info.get("fid")

        db.session.commit()

        return redirect(url_for("admin.amdin_category"))