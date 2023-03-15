from django.views import View
from django.http import JsonResponse
from api.views.login import clean_form
from django.db.models import F
from django import forms
from django.contrib import auth
from app01.models import Avatars


class EditPasswordForm(forms.Form):
    old_pwd = forms.CharField(min_length=4, error_messages={'required': '请输入之前的密码', 'min_length': '密码最低为4位'})
    pwd = forms.CharField(min_length=4, error_messages={'required': '请输入新的密码', 'min_length': '密码最低为4位'})
    re_pwd = forms.CharField(min_length=4, error_messages={'required': '请再次输入新的密码', 'min_length': '密码最低为4位'})

    # 重写init方法
    def __init__(self, *args, **kwargs):
        # 做自己想做的事情
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def clean_old_pwd(self):
        old_pwd = self.cleaned_data['old_pwd']
        user = auth.authenticate(username=self.request.user.username, password=old_pwd)
        if not user:
            self.add_error('old_pwd', '原密码输入错误')
        return old_pwd

    def clean(self):
        pwd = self.cleaned_data.get('pwd')
        re_pwd = self.cleaned_data.get('re_pwd')

        if pwd != re_pwd:
            self.add_error('re_pwd', '两次密码不一致')
        return self.cleaned_data


class EditPasswordView(View):
    def post(self, request):
        res = {
            'msg': '密码修改成功',
            'self': None,
            'code': 414
        }
        data = request.data
        form = EditPasswordForm(data, request=request)
        if not form.is_valid():
            # 验证不同通过
            res['self'], res['msg'] = clean_form(form)
            return JsonResponse(res)
        user = request.user
        user.set_password(data['pwd'])
        user.save()
        auth.logout(request)    # 退出登录
        res['code'] = 0
        return JsonResponse(res)


class EditAvatarView(View):
    def put(self, request):
        res = {
            'msg': '头像修改成功',
            'code': 414
        }
        avatar_id = request.data.get('avatar_id')

        # 判断用户的登录状态
        user = request.user
        sign_status = user.sign_status
        avatar = Avatars.objects.get(nid=avatar_id)
        if sign_status == 0:
            # 用户名密码注册
            user.avatar_id = avatar_id
        else:
            avatar_url = avatar.url.url
            user.avatar_url = avatar_url
        user.save()
        res['data'] = avatar.url.url
        res['code'] = 0
        return JsonResponse(res)
