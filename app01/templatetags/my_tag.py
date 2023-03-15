from django import template
from app01.utils.search import Search
from django.utils.safestring import mark_safe
from app01.models import Tags

# 注册
register = template.Library()


# 自定义过滤器
@register.inclusion_tag('my_tag/headers.html')
# 轮播图
def banner(menu_name, article=None):
    img_list = [
        "http://www.fengfengzhidao.com/media/site_bg/wallhaven-l3geq2.jpg",
        "http://www.fengfengzhidao.com/media/site_bg/wallhaven-k75977.jpg",
        "http://www.fengfengzhidao.com/media/site_bg/3-1.jpg"
    ]
    if article:
        print(article)
        # 拿到文档的封面
        cover = article.cover.url.url
        print(cover)
        img_list = [cover]
        pass
    return {'img_list': img_list}


# 生成标签
@register.simple_tag
def generate_order_html(request, key):
    order = request.GET.get(key, '')
    order_list = []
    if key == 'order':
        order_list = [
            ('', '综合排序'),
            ('-create_date', '最新发布'),
            ('-look_count', '最多浏览'),
            ('-digg_count', '最多点赞'),
            ('-collects_count', '最多收藏'),
            ('-comment_count', '最多评论')
        ]
    elif key == 'word':
        order = request.GET.getlist(key, '')
        order_list = [
            ('', '全部字数'),
            (['0', '1000'], '1000字以内'),
            (['1000', '3000'], '3000字以内'),
            (['3000', '5000'], '5000字以内'),
            (['5000', '10000'], '10000字以内'),
            (['10000', '20000'], '20000字以内'),
            (['20000', '100000'], '20000字以上')
        ]
    elif key == 'tag':
        tag_list = Tags.objects.exclude(articles__isnull=True)
        order_list.append(('', '全部标签'))
        for tag in tag_list:
            order_list.append((tag.title, tag.title))
    query_params = request.GET.copy()
    order = Search(
        key=key,
        order=order,
        order_list=order_list,
        query_params=query_params
    )
    return mark_safe(order.order_html())


# 动态导航栏
@register.simple_tag
def dynamic_navigation(request):
    path = request.path_info
    path_dict = {
        '/': '首页',
        '/news/': '新闻',
        '/moods/': '心情',
        '/history/': '回忆录',
        '/sites/': '网站导航',
        '/about/': '关于',
    }
    nav_list = []
    for k, v in path_dict.items():
        if k == path:
            nav_list.append(f'<a href="{k}" class="active">{v}</a>')
            continue
        nav_list.append(f'<a href="{k}">{v}</a>')
    return mark_safe(''.join(nav_list))


# 生成广告
@register.simple_tag
def generate_advert(advert_list):
    html_list = []
    for i in advert_list:
        if i.img:
            # 上传的文件
            html_list.append(
                f"<div><a href='{i.href}' title={i.title} target='_blank'><img src='{i.img.url}'></a></div>"
            )
            continue
        html_s: str = i.img_list
        html_new = html_s.replace(';', '；').replace('\n', ';')
        img_list = html_new.split(';')
        for url in img_list:
            html_list.append(
                f"<div><a href='{i.href}' title={i.title} target='_blank'><img src='{url}'></a></div>"
            )
    print(html_list)
    return mark_safe(''.join(html_list))


# 遍历配图
@register.simple_tag
def generate_drawing(drawing: str):
    if not drawing:
        return ''
    drawing = drawing.replace(';', '；').replace('\n', ';')
    drawing_list = drawing.split(';')
    html_s = ''
    for i in drawing_list:
        html_s += f'<img src="{i}" alt="">'
    return mark_safe(html_s)
