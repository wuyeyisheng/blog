# url+视图函数
import random
from operator import or_

from flask import Blueprint, render_template, jsonify, request, redirect, url_for, session
from sqlalchemy import desc

from App.exts import cache
from .models import *

blog = Blueprint('blog', __name__)
admin = Blueprint('admin', __name__)


@blog.route('/')
def home():
    # 用户的个人信息
    user = User.query.all()[0]
    # 查询所有的文章

    arts = Article.query.order_by(desc('is_recommand'))
    # 查询图片
    ablums = PhotoMain.query.all()
    # 查看自己分类
    types = AriticleType.query.all()

    data = {
        "user": user,
        "arts": arts,

        "ablums": ablums,
        "types": types,
    }

    return render_template('blog/index.html', **data)


@blog.route("/info/<id>", methods=["GET", "POST", "PUT", "DELETE"])
def info(id):
    '''
    文章详细内容
    :return:
    '''
    if request.method == "GET":
        article = Article.query.get(id)
        #
        print(article.visit)

        if article.visit:
            article.visit += 1
        else:
            article.visit = 1
        db.session.commit()

        # 获取上一篇和下一篇的内容
        if id != 1:
            prvart = Article.query.filter(Article.id.__lt__(id)).first()
        else:
            prvart = None

        nextart = Article.query.filter(Article.id.__gt__(id)).first()

        # 查询所有的文章
        arts = Article.query.all()
        # 查看自己分类
        types = AriticleType.query.all()
        commands = Commend.query.filter(Commend.articleid == article.id).order_by(desc("time"))

        tags = article.tag.split("、")
        typeclass = []
        tmp = article.ariticletype
        flags = 1
        while flags:
            typeclass.append(tmp.name)
            if tmp.father_type:
                print(tmp.father_type)
                tmp = AriticleType.query.get(tmp.father_type)
            else:
                flags = 0
        print(typeclass)

        data = {
            "prvart": prvart,
            "nextart": nextart,

            "article": article,
            "typeclass": typeclass,

            "tags": tags,
            "arts": arts,
            "commands": list(commands),

            "types": types,
        }
        return render_template("blog/info.html", **data)

    elif request.method == "PUT":
        '''
            修改点赞量。
        '''
        if cache.get(request.remote_addr) != id:
            try:
                id = request.form.get("id")
                cache.set(request.remote_addr, id, 5)
                art = Article.query.get(id)
                art.num += 1
                db.session.commit()
                return jsonify({"code": 1, "art_num": art.num})
            except:
                return jsonify({"code": 0})
        else:
            cache.set(request.remote_addr, id, 5)
            return jsonify({"code": 2})

    elif request.method == "POST":

        try:
            id = request.cookies.get("user") or "1"
            nameip = request.remote_addr
            artid = request.form.get("artid")
            name = request.form.get("name") or nameip
            info = request.form.get("info")

            user = User()

            user.name = name
            user.icon = "http://img4.imgtn.bdimg.com/it/u=2641899507,2178808967&fm=26&gp=0.jpg"
            user.time = datetime.datetime.now()
            db.session.add(user)
            db.session.commit()

            commend = Commend()
            # 反向插入id必须找到对方的值。
            commend.comment_user = user
            commend.articleid = artid
            commend.info = info
            commend.time = datetime.datetime.now()

            db.session.add(commend)
            db.session.commit()

            return jsonify({"code": 1})
        except:
            return jsonify({"code": 0})


@blog.route("/yzm/")
def yzm():
    num = random.choices("0123456789qwertyuiopasdfghjklzxcvbnm", k=4)
    return jsonify({"code": 1, "yzm": "".join(num)})


@blog.route("/share/")
def share():
    '''
    图片壁纸的分类
    :return:
    '''

    pages = request.args.get("page", 1)
    per_page = request.args.get("per_page", 12)

    phage = PhotoMain.query.filter_by().paginate(int(pages), int(per_page), error_out=False)
    print(pages)
    data = {
        "phage": phage,
        "selected2": "selected"
    }
    return render_template("blog/share.html", **data)


@blog.route("/share/<id>")
def infopic(id):
    '''
    图片壁纸的分类
    :return:
    '''

    # 用户的个人信息
    user = User.query.all()[0]
    # 查询所有的文章
    arts = Article.query.all()
    # 查询图片
    ablums = PhotoMain.query.all()
    # 查看自己分类
    types = AriticleType.query.all()

    photo = PhotoMain.query.get(id)

    data = {
        "photo": photo,
        "selected2": "selected",

        "user": user,
        "arts": arts,
        "ablums": ablums,
        "types": types,
    }
    return render_template("blog/infopic.html", **data)


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
        "selected3": "selected"

    }
    return render_template("blog/about.html", **data)


@blog.route("/gbook/")
def gbook():
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
        "selected4": "selected"

    }
    return render_template("blog/gbook.html", **data)


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

    page = request.args.get("pages", 1)
    per_page = request.args.get("per_page", 5)
    print(page, per_page)

    artspg = Article.query.paginate(int(page), int(per_page), False).items

    arts_list = [art.to_dict() for art in artspg]
    types_list = [type.to_dict() for type in types]
    data = {
        "types": types_list,
        "arts": arts_list,
        # "artspg":artspg
    }

    return jsonify(data)


# 文章搜索
@blog.route("/searchkey/")
def searchkey():
    # 查询所有的文章
    key = request.args.get("key")
    page = request.args.get("pages", 1)
    per_page = request.args.get("per_page", 5)

    artspg = Article.query.filter(or_(Article.title.contains(key), Article.text.contains(key))).paginate(int(page),
                                                                                                         int(per_page),
                                                                                                         False).items

    arts_list = [art.to_dict() for art in artspg]
    data = {
        "arts": arts_list,
    }

    return jsonify(data)


# ===============管理员摄图===============================

# 管理员的登录页面
@admin.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "GET":
        return render_template("admin/login.html")
    elif request.method == "POST":
        info = request.form
        username = info.get("username")
        userpwd = info.get("userpwd")

        user = list(User.query.filter_by(name=username, password=userpwd))

        if user:
            if user[0].is_super == 1:
                print(user[0].id)

                session["uid"] = user[0].id
                return redirect(url_for('admin.amdin_index'))
            else:
                return render_template("admin/login.html", errors="不是管理员")
        else:
            return render_template("admin/login.html", errors="用户没有注册。")


# 退出登录
@admin.route("/admin/logout", methods=["GET", "POST"])
def admin_logout():
    if request.method == "GET":
        session.pop('uid')
        return redirect(url_for('admin.admin_login'))


# 管理首页
@admin.route('/admin/')
def amdin_index():
    # 获取全部的文章

    if not session.get("uid"):
        return redirect(url_for('admin.admin_login'))

    userid = session.get("uid") or "1"
    uname = User.query.get(userid).name
    comment = Commend.query.all()

    arts = Article.query.filter_by(userid=userid)

    ip = request.remote_addr
    nums = 0
    for num in list(arts):
        nums += num.num

    data = {
        "nums": nums,
        "comment": comment,
        "uname": uname,
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
        per_page = int(request.args.get("per_page", 4))
        arts = Article.query.filter_by(userid=userid).paginate(page, per_page, error_out=False)

        data = {
            "arts": list(arts.items),
            "pgs": arts

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
            "arts": AriticleType.query.all(),
            "arttype": art.to_dict(),
            "fart": fart
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
