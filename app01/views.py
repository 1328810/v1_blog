from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from app01.utils.random_code import random_code
from django.contrib import auth
from app01.models import UserInfo
from app01.models import *
from app01.utils.sub_comment import sub_comment_list
from django.db.models import F
from app01.utils.pagination import Pagination

# Create your views here.


def index(request):
    article_list = Articles.objects.filter(status=1).order_by('-change_date')
    frontend_list = Articles.objects.filter(category=1)[:6]
    backend_list = Articles.objects.filter(category=2)[:6]
    # 分页器
    query_params = request.GET.copy()
    pager = Pagination(
        current_page=request.GET.get('page'),
        all_count=article_list.count(),
        base_url=request.path_info,
        query_params=query_params,
        per_page=5,
        pager_page_count=7
    )
    article_list = article_list[pager.start:pager.end]

    advert_list = Advert.objects.filter(is_show=True )

    return render(request, 'index.html', locals())


def search(request):
    search_key = request.GET.get('key', '')
    order = request.GET.get('order', '')
    word = request.GET.getlist('word')
    tag = request.GET.get('tag', '')
    query_params = request.GET.copy()
    article_list = Articles.objects.filter(title__contains=search_key)

    # 字数搜索
    if len(word) == 2:
        article_list = article_list.filter(word__range=word)

    # 标签搜索
    if tag:
        article_list = article_list.filter(tag__title=tag)
    if order:
        try:
            article_list = article_list.order_by(order)
        except Exception:
            pass
    # 分页器
    pager = Pagination(
        current_page=request.GET.get('page'),
        all_count=article_list.count(),
        base_url=request.path_info,
        query_params=query_params,
        per_page=10,
        pager_page_count=7
    )
    article_list = article_list[pager.start:pager.end]

    return render(request, 'search.html', locals())


def article(request, nid):
    article_query = Articles.objects.filter(nid=nid)
    article_query.update(look_count=F('look_count') + 1)
    if not article_query:
        return redirect('/')
    article = article_query.first()
    comment_list = sub_comment_list(nid)
    return render(request, 'article.html', locals())


def news(request):
    return render(request, 'news.html')


def moods(request):
    # 查询所有头像
    avatar_list = Avatars.objects.all()

    # 搜索
    key = request.GET.get('key', '')

    mood_list = Moods.objects.filter(content__contains=key).order_by('-create_date')

    query_params = request.GET.copy()
    # 分页器
    pager = Pagination(
        current_page=request.GET.get('page'),
        all_count=mood_list.count(),
        base_url=request.path_info,
        query_params=query_params,
        per_page=5,
        pager_page_count=7
    )
    mood_list = mood_list[pager.start:pager.end]

    return render(request, 'moods.html', locals())


def history(request):
    return render(request, 'history.html')


def about(request):
    return render(request, 'about.html')


def sites(request):
    return render(request, 'sites.html')


def login(request):
    return render(request, 'login.html')


# 获取随机验证码
def get_random_code(request):
    data, valid_code = random_code()
    request.session['valid_code'] = valid_code
    return HttpResponse(data)


def register(request):
    return render(request, 'register.html')


def logout(request):
    auth.logout(request)
    return redirect('/')


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