import random
from django.views import View
from django.http import JsonResponse
from django import forms
from api.views.login import clean_form
from markdown import markdown
from pyquery import PyQuery
from app01.models import Tags, Articles, Cover
from django.db.models import F


# 添加文章
class AddArticleFrom(forms.Form):
    title = forms.CharField(error_messages={'required': '请输入文章标题'})
    content = forms.CharField(error_messages={'required': '请输入文章内容'})
    abstract = forms.CharField(required=False)      # 不进行为空验证
    cover_id = forms.IntegerField(required=False)
    category = forms.IntegerField(required=False)
    pwd = forms.CharField(required=False)
    recommend = forms.BooleanField(required=False)
    status = forms.IntegerField(required=False)


    # 全局钩子 分类 文章密码
    def clean(self):
        category = self.cleaned_data['category']
        if not category:
            self.cleaned_data.pop('category')
        pwd = self.cleaned_data['pwd']
        if not pwd:
            self.cleaned_data.pop('pwd')

    # 文章简介
    def clean_abstract(self):
        abstract = self.cleaned_data['abstract']
        if abstract:
            return abstract
        # 截取正文的前30个字
        content = self.cleaned_data.get('content')
        if content:
            abstract = PyQuery(markdown(content)).text()[:90]
            return abstract

    # 文章封面
    def clean_cover_id(self):
        cover_id = self.cleaned_data['cover_id']
        if cover_id:
            return cover_id
        cover_set = Cover.objects.all().values('nid')
        cover_id = random.choice(cover_set)['nid']
        return cover_id


# 给文章添加标签
def add_article_tag(tags, article_obj):
    for tag in tags:
        if tag.isdigit():
            article_obj.tag.add(tag)
        else:
            # 先创建，再多对多关联
            tab_obj = Tags.objects.create(title=tag)
            article_obj.tag.add(tab_obj.nid)


# 文章
class ArticleView(View):
    # 添加文章
    def post(self, request):
        res = {
            'msg': '文章发布成功',
            'code': 412,
            'data': None
        }
        data = request.data
        data['status'] = 1
        form = AddArticleFrom(data)
        if not form.is_valid():
            res['self'], res['msg'] = clean_form(form)
            return JsonResponse(res)
        # 校验通过
        form.cleaned_data['author'] = 'aze'
        form.cleaned_data['source'] = '奇点个人博客'
        print(form.cleaned_data)
        article_obj = Articles.objects.create(**form.cleaned_data)
        tags = data.get('tags')
        # 添加标签
        add_article_tag(tags, article_obj)
        res['code'] = 0
        res['data'] = article_obj.nid
        return JsonResponse(res)

    # 编辑文章
    def put(self, request, nid):
        res = {
            'msg': '文章编辑成功',
            'code': 412,
            'data': None
        }
        article_query = Articles.objects.filter(nid=nid)
        if not article_query:
            res['msg']: '请求错误'
            return JsonResponse(res)
        data = request.data
        data['status'] = 1
        form = AddArticleFrom(data)
        if not form.is_valid():
            res['self'], res['msg'] = clean_form(form)
            return JsonResponse(res)
        # 校验通过
        form.cleaned_data['author'] = 'aze'
        form.cleaned_data['source'] = '奇点个人博客'
        article_query.update(**form.cleaned_data)
        tags = data.get('tags')
        # 标签修改
        article_query.first().tag.clear()
        # 添加标签
        add_article_tag(tags, article_query.first())
        res['code'] = 0
        res['data'] = article_query.first().nid
        return JsonResponse(res)

# 给文章点赞
class ArticleDiggView(View):
    def post(self, request, nid):
        res = {
            'msg': '文章点赞成功',
            'code': 412,
            'data': 0
        }
        comment_query = Articles.objects.filter(nid=nid)
        comment_query.update(digg_count=F('digg_count') + 1)
        digg_count = comment_query.first().digg_count
        res['code'] = 0
        res['data'] = digg_count
        return JsonResponse(res)
# 文章收藏
class ArticleCollectsView(View):
    def post(self, request, nid):
        res = {
            'msg': '文章收藏成功',
            'code': 412,
            'isCollects': True,
            'data': 0
        }
        # 判断登录
        # 一个用户只能收藏一次，同样的操作收藏变取消
        if not request.user.username:
            res['msg'] = '请先登录'
            return JsonResponse(res)

        # 判断用户是否收藏过该文章
        flag = request.user.collects.filter(nid=nid)
        num = 1
        res['code'] = 0
        if flag:
            # 用户已经收藏了文章，再次点击会取消收藏
            res['msg'] = '文章取消收藏成功'
            res['isCollects'] = False
            request.user.collects.remove(nid)
            num = -1
        else:
            request.user.collects.add(nid)
        article_query = Articles.objects.filter(nid=nid)
        article_query.update(collects_count=F('collects_count')+num)
        collects_count = article_query.first().collects_count
        res['data'] = collects_count
        return JsonResponse(res)
