"""v1_blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from app01 import views
from django.conf import settings
from django.views.static import serve
urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin_home/', views.admin_home),
    path('', views.index),
    path('news/', views.news),
    path('moods/', views.moods),
    path('history/', views.history),
    path('about/', views.about),
    path('sites/', views.sites),
    path('search/', views.search),
    path('login/', views.login),
    path('login/random_code/', views.get_random_code),
    path('register/', views.register),
    path('logout/', views.logout),


    path('backend/', views.backend),                        # 后台个人中心
    path('backend/add_article/', views.add_article),        # 后台添加文章
    path('backend/reset_password/', views.reset_password),  # 后台修改密码
    path('backend/edit_avatar/', views.edit_avatar),        # 后台修改头像


    re_path(r'^backend/edit_article/(?P<nid>\d+)/', views.edit_article),    # 编辑文章
    re_path(r'^article/(?P<nid>\d+)/', views.article),  # 文章详情页
    re_path(r'^api/', include('api.urls')),     # 路由分发  将所有以api开头的请求分类发到api这个urls.py中
    re_path(r'media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT})  # 用户上传文件路由配置
]
