from django.views import View
from django.http import JsonResponse
from api.views.login import clean_form
from django.db.models import F
from django import forms
from app01.models import Avatars, Moods, MoodComment
import random


class AddMoodsForm(forms.Form):
    name = forms.CharField(error_messages={'required': '请输入用户名'})
    content = forms.CharField(error_messages={'required': '请输入心情内容'})
    avatar_id = forms.CharField(required=False)      # 不进行为空验证
    drawing = forms.CharField(required=False)  # 不进行为空验证

    def clean_avatar_id(self):
        avatar_id = self.cleaned_data.get('avatar_id')
        if avatar_id:
            return avatar_id
        # 随机选择头像
        avatar_list = [i.nid for i in Avatars.objects.all()]
        avatar_id = random.choice(avatar_list)
        return avatar_id


def mood_digg(model_obj, nid):
    res = {
        'msg': '点赞成功',
        'code': 412,
    }
    mood_query = model_obj.objects.filter(nid=nid)
    mood_query.update(digg_count=F('digg_count') + 1)
    res['data'] = mood_query.first().digg_count
    res['code'] = 0
    return JsonResponse(res)


class MoodsView(View):
    def post(self, request):
        res = {
            'msg': '心情发布成功',
            'code': 412,
            'self': None
        }
        data = request.data
        form = AddMoodsForm(data)
        if not form.is_valid():
            res['self'], res['msg'] = clean_form(form)
            return JsonResponse(res)

        Moods.objects.create(**form.cleaned_data)
        res['code'] = 0
        return JsonResponse(res)

    def delete(self, request, nid):
        res = {
            'msg': '心情删除成功',
            'code': 412,
        }
        if not request.user.is_superuser:
            res['msg'] = '用户验证失败'
            return JsonResponse(res)
        mood_query = Moods.objects.filter(nid=nid)
        if not mood_query:
            res['msg'] = '心情不存在'
            return JsonResponse(res)
        mood_query.delete()
        res['code'] = 0
        return JsonResponse(res)

    # 点赞
    def put(self, request, nid):
        return mood_digg(Moods, nid)


class MoodCommentsView(View):
    def post(self, request, nid):
        res = {
            'msg': '回复成功',
            'code': 412,
            'self': None
        }
        data = request.data
        form = AddMoodsForm(data)
        if not form.is_valid():
            res['self'], res['msg'] = clean_form(form)
            return JsonResponse(res)
        form.cleaned_data['mood_id'] = nid
        form.cleaned_data.pop('drawing')
        MoodComment.objects.create(**form.cleaned_data)
        Moods.objects.filter(nid=nid).update(comment_count=F('comment_count') + 1)
        res['code'] = 0
        return JsonResponse(res)

    def delete(self, request, nid):
        res = {
            'msg': '评论删除成功',
            'code': 412,
            'daya': 0
        }
        if not request.user.is_superuser:
            res['msg'] = '用户验证失败'
            return JsonResponse(res)
        mood_id = request.data.get('mood_id')
        MoodComment.objects.filter(nid=nid).delete()

        mood_query = Moods.objects.filter(nid=mood_id)
        mood_query.update(comment_count=F('comment_count') - 1)
        res['data'] = mood_query.first().comment_count

        res['code'] = 0
        print(res)
        return JsonResponse(res)

    # 点赞
    def put(self, request, nid):
        return mood_digg(MoodComment, nid)