from django.shortcuts import render, redirect
from app01.models import *


def backend(request):
    if not request.user.username:
        # 没有登录
        return redirect('/')
    return render(request, 'backend/backend.html', locals())


def add_article(request):
    # 拿到所有分类、标签
    tag_list = Tags.objects.all()
    # 拿到所有的文章封面
    cover_list = Cover.objects.all()
    c_l = []
    for cover in cover_list:
        c_l.append({
            'url': cover.url.url,
            'nid': cover.nid
        })
    category_list = Articles.category_choice
    return render(request, 'backend/add_article.html', locals())


# 编辑头像
def edit_avatar(request):
    avatar_url = request.user.avatar_url
    # 如果是用户名注册
    avatar_id = request.user.avatar.nid
    # 查询所有头像
    avatar_list = Avatars.objects.all()
    for i in avatar_list:
        if i.url.url == avatar_url:
            print(i.nid)
            avatar_id = i.nid
    return render(request, 'backend/edit_avatar.html', locals())


def reset_password(request):
    return render(request, 'backend/reset_password.html', locals())


def edit_article(request, nid):
    article_obj = Articles.objects.get(nid=nid)
    tags = [str(tag.nid) for tag in article_obj.tag.all()]
    # 拿到所有分类、标签
    tag_list = Tags.objects.all()
    # 拿到所有的文章封面
    cover_list = Cover.objects.all()
    c_l = []
    for cover in cover_list:
        c_l.append({
            'url': cover.url.url,
            'nid': cover.nid
        })
    category_list = Articles.category_choice
    return render(request, 'backend/edit_article.html', locals())


def admin_home(request):
    return render(request, 'admin_home.html')