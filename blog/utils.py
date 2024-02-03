import datetime
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from .models import ViewDetail,Article

# 只要打开，阅读量+1，使用cookie方案
def set_views_once_read(request,obj):

    ct = ContentType.objects.get_for_model(obj)
    key = f"{ct.model}_{obj.pk}_read"  # cookie

    # 没有发布的文章不增加阅读量和阅读明细
    if not obj.is_publish:
        return key

    if not request.COOKIES.get(key):
        # 总阅读数
        obj.views += 1
        obj.save()

        # 当天阅读量 +1
        date = timezone.now().date()
        viewDeatil,created = ViewDetail.objects.get_or_create(content_type=ct,object_id=obj.pk,date=date)
        viewDeatil.views += 1
        viewDeatil.save()
    return key

# 过去7天的阅读量
def get_seven_days_views(content_type):
    pass

# 昨日热榜
def get_hot_articles_by_view(day_type = 'all'):
    if day_type == 'yesterday':
        dt = timezone.now().date() - datetime.timedelta(days=1)
        content_type = ContentType.objects.get_for_model(Article)
        hot_articles = ViewDetail.objects.filter(content_type=content_type,date=dt).order_by('-views').all()[:5]
    else:
        hot_articles = Article.objects.filter(is_publish=True).order_by('-views').all()[:5]
    return hot_articles