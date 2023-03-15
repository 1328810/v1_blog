import os

if __name__ == '__main__':
    # 加载django项目的配置信息
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "v1_blog.settings")
    # 导入django，并且启动django项目
    import django
    django.setup()
    from app01.models import Articles, Comment
    # 方案一
    """
    [
        父评论1_nid{
            sub_comment:[
                {},{},{}
            ]
        }
        父评论2_nid{}
    ]
    """
    def find_root_comment(comment: Comment):
        # 找comment的最终根评论
        if comment.parent_comment:
            # 不是根评论
            # 递归去找他的根评论
            return find_root_comment(comment.parent_comment)
        # 是根评论
        return comment
    comment_dict = {

    }
    # 找到某个文章的所有评论
    comment_query = Comment.objects.filter(article_id=33)
    for comment in comment_query:
        # 如果他的父亲是none，就说明是根评论
        if not comment.parent_comment:
            # 把根评论放入字典
            comment_dict[comment.nid] = comment
            # 给根评论添加自定义属性，将所有的子评论放进去
            comment.sub_comment = []
            continue
    for comment in comment_query:
        # 一定是某个父评论的子评论
        for sub_comment in comment.comment_set.all():
            # 遍历该评论下面的所有子评论
            # 找到这个子评论的最终根评论
            # find_root_comment:找到这个子评论得到最终根评论，放回根评论对象
            root_comment = find_root_comment(sub_comment)
            # 把子评论添加到属于自己的根品论里面
            comment_dict[root_comment.nid].sub_comment.append(sub_comment)
    for k, v in comment_dict.items():
        print(v, '根评论')
        for comment in v.sub_comment:
            print('  ', comment, '子评论')

