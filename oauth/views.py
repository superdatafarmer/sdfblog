import random
import string
import time

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.http.response import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse

from .forms import ForgetPwdForm

User = auth.get_user_model()

# Create your views here.
def login(request):
    context = {
        'nav_item':'login'
    }
    if request.user.is_authenticated:
        return redirect(reverse('blog:home'))
    if request.method == 'GET':
        return render(request,'oauth/login.html',context = context)
    elif request.method == 'POST':
        email = request.POST.get('email')
        pwd = request.POST.get('password')

        # 查询邮箱对应的用户名
        if not User.objects.filter(username = email).exists():
            context['status'] = '0'
            context['error'] = '用户邮箱不存在或密码错误!'
        else:
            user = auth.authenticate(username = email,password = pwd)
            if user is None:
                context['status'] = '0'
                context['error'] = '邮箱不存在或密码错误!'
            else:
                auth.login(request,user)
                context['status'] = '1'
                if request.GET.get('from') == reverse('oauth:register'):
                    context['jump_url'] = reverse('blog:home')
                else:
                    context['jump_url'] = request.GET.get('from', reverse('blog:home'))
        return JsonResponse(context)
    else:
        context['status'] = '0'
        context['error'] = '近接受GET/POST请求!'
        return JsonResponse()

def register(request):
    context = {
        'nav_item': 'register'
    }
    if request.user.is_authenticated:
        return redirect(reverse('blog:home'))
    if request.method == 'GET':
        return render(request,'oauth/register.html',context = context)
    elif request.method == 'POST':
        email = request.POST.get('email')
        send_for = request.POST.get('send_for')
        vercode = request.POST.get('vercode')
        password = request.POST.get('password')
        confirmPassword = request.POST.get('confirmPassword')
        nickname = request.POST.get('nickname')

        # 判断验证码是否一致
        vercode_session = request.session.get(send_for,'')
        if vercode_session != vercode:
            context['status'] = '0'
            context['error'] = '验证码不正确'
            return JsonResponse(context)

        # 判断密码是否一致
        if password != confirmPassword:
            context['status'] = '0'
            context['error'] = '两次输入的密码不一致'
            return JsonResponse(context)

        # 判断邮箱是否重复
        if User.objects.filter(email = email).exists():
            context['status'] = '0'
            context['error'] = '不能重复注册，请换一个邮箱'
            return JsonResponse(context)

        user = User()
        user.username = email
        user.email = email
        user.set_password(password)
        user.nickname = nickname
        user.save()
        context['status'] = '1'
        return JsonResponse(context)
    else:
        context['status'] = '0'
        context['error'] = '近接受GET/POST请求!'
        return JsonResponse(context)

# 用forms做数据验证
def forget_pwd(request):
    context = {
    }
    if request.method == 'GET':
        return render(request,'oauth/forget_pwd.html',context = context)
    elif request.method == 'POST':
        forgetPwdForm = ForgetPwdForm(request.POST,request = request)
        if forgetPwdForm.is_valid():
            data = forgetPwdForm.cleaned_data
            user = data['user']
            pwd = data['confirmPassword']
            user.set_password(pwd)
            user.save()
            context['status'] = '1'
            return JsonResponse(context)
        else:
            context['status'] = '0'
            context['error'] = forgetPwdForm.errors['__all__'][0]  # form错误返回的是字典
            return JsonResponse(context)
    else:
        context['status'] = '0'
        context['error'] = '近接受GET/POST请求!'
        return JsonResponse(context)

@login_required(login_url='oauth:login')
def logout(request):
    jump_url = request.GET.get('from',reverse('blog:home'))
    auth.logout(request)
    return redirect(jump_url)

def send_verification_code(request):
    email = request.GET.get('email','')
    send_for = request.GET.get('send_for','')
    subject = request.GET.get('subject','')
    context = {
    }

    if email != '':
        user_exist = User.objects.filter(email=email).exists()
        if send_for == 'reset_pwd_code' and not user_exist:
            context['status'] = '0'
            context['error'] = '邮箱不存在'
        elif send_for == 'register_code' and user_exist:
            context['status'] = '0'
            context['error'] = '不能重复注册，请换一个邮箱'
        else:
            # 生成验证码
            code = ''.join(random.sample(string.ascii_letters + string.digits, 4))
            now = int(time.time())
            send_code_time = request.session.get('send_code_time', 0)
            if now - send_code_time < 30:
                context['status'] = '0'
                context['error'] = '30s内不能重复发送验证码'
            else:
                request.session[send_for] = code
                request.session['send_code_time'] = now
                context['status'] = '1'
                # 发送邮件
                send_mail(
                    subject = subject,
                    message = f'您的验证码是：{code}',
                    from_email = settings.EMAIL_HOST_USER,
                    recipient_list = [email],
                    fail_silently=False
                )
    else:
        context['status'] = '0'
        context['error'] = '邮箱不能为空'

    return JsonResponse(context)