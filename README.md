# v1_blog
个人博客
## 主要功能：
文章，页面，分类目录，标签的添加，删除，编辑等。文章及页面支持Markdown，支持代码高亮。
支持文章条件搜索。
主题切换功能
完整的评论功能，包括发表回复评论，支持Markdown。
侧边栏功能，最新文章，最多阅读等。
手机端适配(待完善)
## 项目截图
![image](https://user-images.githubusercontent.com/127709716/225201971-3deaa4a0-c6b7-482b-ac4e-f19081433949.png)
![image](https://user-images.githubusercontent.com/127709716/225202033-bfa58bef-e6f7-400e-9875-c119da3f5cd7.png)
![image](https://user-images.githubusercontent.com/127709716/225202075-71715a4e-db97-41ff-94a3-8d53f0a37841.png)
![image](https://user-images.githubusercontent.com/127709716/225202128-b7a646e5-78b1-4ce9-845e-2f0f585a05ad.png)
![image](https://user-images.githubusercontent.com/127709716/225202155-190221ea-dfa4-4d1b-85ab-0a022c1d7c6e.png)
![image](https://user-images.githubusercontent.com/127709716/225202438-d031903f-482a-40e6-bb64-1e1813c17549.png)
![image](https://user-images.githubusercontent.com/127709716/225202467-4c16b333-8cc7-46a0-b46a-3a6f722a89c3.png)
![image](https://user-images.githubusercontent.com/127709716/225202505-af176667-b8dc-4b6b-af67-769fd1d4d662.png)
![image](https://user-images.githubusercontent.com/127709716/225202569-2157f1e3-09b7-453c-940e-f4bb47b5d719.png)
##　项目目录
+---v1_blog  项目同名目录
|      +---__init__.py
|      +---asgi.py  asgi部署使用
|      +---wsgi.py  wsgi部署使用
|      +---settings.py  配置文件，重要
|      +---local_settings.py 本地运行时的配置
|      +---urls.py  项目路由，重要
|
+---lib  一些工具模块都在这里
|
+---api  api相关的app
|      +---migrations  数据库迁移文件
|      +---views  视图目录
|      |     +---admin_data.py  后台的一些数据接口  
|      |     +---article.py  文章接口
|      |     +---comment.py  评论接口
|      |     +---history.py  回忆录接口
|      |     +---login.py  登录注册接口
|      |     +---mood.py  心情接口
|      |     +---sites.py  网站导航接口
|      |     +---user.py  修改密码接口
|      |
|      +---__init__.py
|      +---admin.py
|      +---models.py  表结构
|      +---tests.py
|      +---urls.py  api分发的路由
+---app01 与页面相关的app
|      +---migrations
|      +---templatetags  自定义标签和过滤器
|      |      +---my_filter.py  自定义过滤器
|      |      +---my_tag.py  自定义标签
|      |     
|      +---valid  验证相关
|      |      +---auth  重写django的authenticate方法
|      |
|      +---views  视图目录
|      +---__init__.py  app01的初始化文件
|      +---admin.py  admin结构
|      +---middleware_decode.py  用于转换axios数据的中间件
|      +---models.py  表结构
|      +---tests.py
|      
+---media  用户上传文件的目录
+---static  静态文件
+---templates  模板文件
|      +---backend  后台相关的模板
|      |      +---add_article.html  添加文章
|      |      +---avatar_list.html  头像列表
|      |      +---backend.html  个人中心
|      |      +---cover_list.html  文章封面列表
|      |      +---edit_article.html  编辑文章
|      |      +---edit_avatar.html  修改头像
|      |      
|      +---my_tag   自定义
|      |      +---headers.html  banner轮播图
|      |
|      +---simple_admin
|      |      +---add_form.html  后台选择封面的模板修改
|      |
|      +---about.html  网站关于
|      +---admin_home.html  后台的首页
|      +---article.html  文章详情页
|      +---article_lock.html  加锁的文章详情页
|      +---blog.html  博客项目
|      +---history.html  建站回忆录
|      +---index.html  首页
|      +---login.html  登录
|      +---moods.html  心情页面
|      +---news.html  新闻
|      +---search.html  搜索
|      +---sign.html  注册
|      +---sites.html  网址导航
|
+---.gitignore  git忽略文件
+---README.md  说明文档
+---blog.sql  项目的数据库文件
+---manage.py  启动文件
+---requirements.txt  第三方模块
