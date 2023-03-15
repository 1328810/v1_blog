import os

if __name__ == '__main__':
    # 加载django项目的配置信息
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "v1_blog.settings")
    # 导入django，并且启动django项目
    import django
    django.setup()
    from app01.models import Articles, Comment
    # 方案二
    """
    思想：根据根评论去递归查找下面的所以子评论
    要把他放入根评论的一个空间中
    """

    def find_root_sub_comment(root_comment, sub_comment_list):
        for sub_comment in root_comment.comment_set.all():
            # 找根评论的子评论
            sub_comment_list.append(sub_comment)
            find_root_sub_comment(sub_comment, sub_comment_list)
        return

    # 找到某个文章的所有评论
    comment_query = Comment.objects.filter(article_id=33)
    # 把评论存储到列表
    comment_list = []
    for comment in comment_query:
        # 如果他的父亲是none，就说明是根评论
        if not comment.parent_comment:
            # 递归查找这个根评论下面的所有子评论
            lis = []
            find_root_sub_comment(comment, lis)
            comment.sub_comment = lis
            comment_list.append(comment)
            continue
    for comment in comment_list:
        print(comment)
        for sub_comment in comment.sub_comment:
            print(sub_comment)