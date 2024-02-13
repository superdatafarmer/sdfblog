from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse,HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator
import markdown
import datetime

# Create your views here.
from blog.models import Article,About,LikeDetail,Tag,Subject,ToolSet
from blog.utils import set_views_once_read
from comment.models import Comment


# 主题
def subject(request):
    subjects = Subject.objects.exclude(status = 'not_started')
    context = {
        'nav_item': 'subject',
        'subjects':subjects,
    }
    return render(request,'blog/subject.html',context=context)
def subject_deatil(request,slug):
    subject = Subject.objects.get(slug=slug)
    context = {
        'nav_item': 'subject',
        'subject':subject,
    }
    return render(request,'blog/subject_detail.html',context=context)

# 获取文章列表的公共方法
def get_articles(request,nav_item):
    # 读取参数
    curr = request.GET.get('curr', 1)  # 获取当前页码
    context = {}

    if nav_item == 'article':
        tag_slug = request.GET.get('tag')
        if tag_slug:
            tag = Tag.objects.get(slug=tag_slug)
            articles_all = tag.articles.filter(is_publish=True)
            context['filter'] = tag.name
        else:
            articles_all = Article.objects.filter(is_publish=True)
            context['filter'] = 'all'
        limit = request.GET.get('limit', 10)  # 获取当前每页条数
    else:
        articles_all = Article.objects.filter(is_top=True, is_publish=True)
        limit = request.GET.get('limit', 5)  # 获取当前每页条数

    paginator = Paginator(articles_all, per_page=limit)  # 分页
    count = paginator.count  # 获取总的记录数量
    articles = paginator.get_page(curr)  # 获取当前页的数据

    context['base_url'] = request.get_full_path()
    context['nav_item'] =  nav_item
    context['articles'] =  articles
    context['curr'] =  curr
    context['limit'] =  limit
    context['count'] =  count

    return context

# 主页
def home(request):
    nav_item = 'home'
    context = get_articles(request,nav_item)
    return render(request, 'blog/home.html', context = context)

# 文章列表
def article(request):
    nav_item = 'article'
    context = get_articles(request, nav_item)
    return render(request, 'blog/article.html', context=context)

# 文章详情
def detail(request,slug):
    article = Article.objects.get(slug__exact=slug)
    # 未发布的文章不允许访问
    if not article.is_publish and not article.author.is_staff:
        return HttpResponse('没权限访问!')

    view_cookie_key = set_views_once_read(request,article)  # 阅读的cookie

    # 评论相关
    ct = ContentType.objects.get_for_model(article)
    comments = Comment.objects.filter(content_type=ct,object_id=article.pk,parent=None)

    # markdown语法渲染器
    md = markdown.Markdown(
        extensions=[
            # 包含 缩写、表格等常用扩展
            'markdown.extensions.extra',
            # 语法高亮扩展
            'markdown.extensions.codehilite',
            # 目录扩展
            'markdown.extensions.toc',
        ],
    )
    # 将内容渲染替换
    article.content = md.convert(article.content)
    toc = md.toc

    # 判断是否需要vip权限
    can_access = True
    if article.topic.subject.vip:
        if request.user.is_authenticated:
            if not request.user.vip and not request.user.is_staff:
                can_access = False
        else:
            can_access = False

    context = {
        'article':article,
        'toc':toc,
        'ct':ct.model,
        'comments':comments,
        'can_access':can_access,
    }

    # 判断是否是vip专题，如果是判断登录用户是否是vip用户，是的话允许访问
    response = render(request,'blog/detail.html',context=context)

    # 设置cookie并且第二天0点过期
    next_day = datetime.datetime.now() + datetime.timedelta(days=1)
    expires = next_day.replace(hour=0,minute=0,second=0,microsecond=0)
    response.set_cookie(view_cookie_key,'true',expires=expires)  # 阅读cookie的标记
    return response


# 喜欢
def changelike(request):
    context = {}
    user = request.user
    if not user.is_authenticated:
        context['status'] = '0'
        context['error'] = '请登录后点赞'
        return JsonResponse(context)

    # 获取被点赞的文章
    article_id = request.GET.get('article_id',0)
    try:
        article = Article.objects.get(pk = article_id)
    except Exception as e:
        context['status'] = '0'
        context['error'] = '文章不存在，可能被管理员删除了，请返回首页'
        return JsonResponse(context)

    # 动作类型，1喜欢,0取消
    action = request.GET.get('action')
    if action == '1':
        like_detail,created = LikeDetail.objects.get_or_create(article = article,user = user)
        if created:
            article.likes += 1
            article.save()
            like_detail.save()
            context['status'] = '1'
            context['like_num'] = article.likes

        else:
            context['status'] = '0'
            context['error'] = '已赞过，不要重复点赞'
    elif action == '0':
        try:
            like_detail = LikeDetail.objects.get(article=article,user=user)
            like_detail.delete()
            article.likes -= 1
            article.save()
            context['status'] = '1'
            context['like_num'] = article.likes
        except Exception as e:
            print(e)
            context['status'] = '0'
            context['error'] = '未点赞过，无法取消'
    else:
        context['status'] = '0'
        context['error'] = '参数错误'

    return JsonResponse(context)

# 开发日志
def about(request):
    context = {"nav_item":"about"}
    # markdown语法渲染器
    md = markdown.Markdown(
        extensions=[
            # 包含 缩写、表格等常用扩展
            'markdown.extensions.extra',
            # 语法高亮扩展
            'markdown.extensions.codehilite',
        ],
    )
    content = md.convert(About.objects.all().first().content)
    context['content'] = content
    return render(request, 'blog/about.html', context=context)

# 工具集
def tool(request):
    context = {"nav_item":"tool"}
    toolsets = ToolSet.objects.all()
    context['toolsets'] = toolsets
    return render(request, 'blog/tool.html', context=context)