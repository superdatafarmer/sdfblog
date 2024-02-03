from django import template
from ..models import Carousel,Welcome,Article,Topic,Subject,LikeDetail,Tag
from ..utils import get_hot_articles_by_view

register = template.Library()

# 获取轮播图列表轮播图
@register.simple_tag
def get_carousel_list():
    return Carousel.objects.filter(is_show=True).all()

# 获取欢迎图
@register.simple_tag
def get_welcome_img():
    return Welcome.objects.filter(is_show=True).first()

# 点击排行
@register.simple_tag
def get_top5_views_all():
    return get_hot_articles_by_view()
@register.simple_tag
def get_top5_views_yesterday():
    return get_hot_articles_by_view(day_type = 'yesterday')

# 喜欢状态
@register.simple_tag
def like_status(article,user):
    if LikeDetail.objects.filter(article=article,user=user).exists():
        return '1'
    else:
        return '0'

# 喜欢排行
@register.simple_tag
def get_top5_likes():
    return Article.objects.filter(is_publish=True).order_by('-likes').all()[:5]


# 标签云
@register.simple_tag
def get_tags():
    return Tag.objects.all()

# 详情页左侧目录栏
@register.simple_tag
def get_ws_menu(article):
    '''
    根据博客详情获取左侧的目录 专题-主题-文章
    '''
    data = []
    topic = article.topic
    if topic is not None:
        subject = topic.subject
        topics = Topic.objects.filter(subject = subject).order_by('sort_by').all()
        for topic in topics:
            articles = Article.objects.filter(topic = topic,is_publish=True).order_by('sort_in_topic').all()
            data.append((topic.name,[(article.short_title,article.get_absolute_url()) for article in articles]))
    return data

# 详情页左侧目录栏
@register.simple_tag
def get_ws_menu_by_subject(subject):
    '''
    根据博客详情获取左侧的目录 专题-主题-文章
    '''
    data = []
    topics = Topic.objects.filter(subject = subject).order_by('sort_by').all()
    for topic in topics:
        articles = Article.objects.filter(topic = topic,is_publish=True).order_by('sort_in_topic').all()
        data.append((topic.name,[(article.title,article.get_absolute_url(),article.created) for article in articles]))
    return data