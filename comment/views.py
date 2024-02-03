from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from .models import Comment

# Create your views here.
@login_required(login_url = 'oauth:login')
def add_comment(request):
    ct = request.POST.get('ct')
    object_id = request.POST.get('object_id')
    parent_id = request.POST.get('parent_id')
    text = request.POST.get('comment')
    context = {}
    try:
        model_class = ContentType.objects.get(model=ct).model_class()
        content_object = model_class.objects.get(pk=object_id)
    except ObjectDoesNotExist:
        context['status'] = '0'
        context['error'] = '评论对象不存在'

    # 获取评论对象
    # 如果直接评论的博客，则 root parent reply_to 都为空
    # 如果评论的是评论：root是直接回复博客的评论id
    comment = Comment()
    comment.content_object = content_object
    comment.text = text
    comment.user = request.user
    context['user'] = request.user.nickname
    context['text'] = text
    if parent_id == '0':
        comment.save()
        # 返回数据
        context['status'] = '1'
        context['created'] = comment.created.strftime('%Y-%m-%d %H:%M:%S')
        context['reply_to'] = ''
        context['root_id'] = ''
        context['pk'] = comment.pk
    elif Comment.objects.filter(pk = parent_id).exists():
        parent = Comment.objects.get(pk = parent_id)
        comment.root = parent.root if parent.root is not None else parent
        comment.parent = parent
        comment.reply_to = parent.user
        comment.save()
        # 返回数据
        context['status'] = '1'
        context['created'] = comment.created.strftime('%Y-%m-%d %H:%M:%S')
        context['reply_to'] = comment.reply_to.nickname
        context['root_id'] = comment.root.pk
        context['pk'] = comment.pk
    else:
        context['status'] = '0'
        context['error'] = '评论对象不存在'

    return JsonResponse(context)

@login_required(login_url = 'oauth:login')
def del_comment(request):
    context = {}
    id = request.GET.get('pk')
    try:
        comment = Comment.objects.get(pk = id)
        if request.user == comment.user or request.user.is_staff:
            comment.delete()
            context['status'] = '1'
        else:
            context['status'] = '0'
            context['error'] = '没有权限删除评论'
    except:
        context['status'] = '0'
        context['error'] = '评论不存在，删除错误'
    return JsonResponse(context)