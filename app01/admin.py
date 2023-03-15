from django.contrib import admin
from app01.models import *
from django.utils.safestring import mark_safe


# Register your models here.
# 文章表
class ArticleAdmin(admin.ModelAdmin):
    def get_cover(self):
        if self.cover:
            return mark_safe(f'<img src="{self.cover.url.url}" style="height:60px; border-radius:5px">')
        return
    get_cover.short_description = '文章封面'

    def get_tag(self):
        tag_list = ', '.join(i.title for i in self.tag.all())
        return tag_list
    get_tag.short_description = '文章标签'

    def get_title(self):
        return mark_safe(f'<a href="/article/{self.nid}" target="_blank">{self.title}</a>')
    get_title.short_description = '文章'

    def get_edit_delete_btn(self):
        return mark_safe(f"""
        <a href="/backend/edit_article/{self.nid}/" target="_blank">编辑</a>
        <a href="/admin/app01/articles/{self.nid}/delete/">删除</a>
        """)
    get_edit_delete_btn.short_description = '操作'

    list_display = [get_title,
                    get_cover,
                    get_tag,
                    'category',
                    'look_count', 'digg_count', 'comment_count', 'collects_count', 'word',
                    'change_date',
                    get_edit_delete_btn]

    def action_word(self, request, queryset):
        for obj in queryset:
            word = len(obj.content)
            obj.word = word
            obj.save()

    action_word.short_description = '获取文章字数'
    action_word.type = 'success'
    actions = [action_word]


admin.site.register(Articles, ArticleAdmin)
admin.site.register(Tags)
admin.site.register(Cover)
admin.site.register(Comment)
admin.site.register(Avatars)
admin.site.register(UserInfo)


# 广告信息
class AdvertAdmin(admin.ModelAdmin):

    def get_href(self):
        return mark_safe(f"""<a href="{self.href}" target="_blank">跳转链接</a>""")
    get_href.short_description = '跳转链接'

    def get_img_list(self):
        # 解析分号
        # 解析换行符
        html_s: str = self.img_list
        html_new = html_s.replace(';', '；').replace('\n', ';')
        img_list = html_new.split(';')

        html_str = ''
        for i in img_list:
            html_str += f'<img src="{i}" style="height:60px; border-radius:5px; margin-right:10px">'
        return mark_safe(html_str)
    get_img_list.short_description = '广告图组'

    def get_img(self):
        if self.img:
            print(self.img.url)
            return mark_safe(f'''<img src="{self.img.url}" style="height:60px; border-radius:5px;">''')
    get_img.short_description = '用户上传'

    list_display = ['title', get_img, 'is_show', 'author', get_img_list,  get_href]


admin.site.register(Advert, AdvertAdmin)