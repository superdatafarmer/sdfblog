from django import forms
from django.contrib import auth

class ForgetPwdForm(forms.Form):
    email = forms.EmailField()
    send_for = forms.CharField()
    vercode = forms.CharField()
    password = forms.CharField()
    confirmPassword = forms.CharField()

    def __init__(self,*args, **kwargs):
        # 初始化表单的时候，需要将request传进来，获取session中验证码
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(ForgetPwdForm,self).__init__(*args, **kwargs)

    def clean(self):
        User = auth.get_user_model()

        # 判断邮箱是否存在
        email = self.cleaned_data['email']
        if not User.objects.filter(username = email).exists():
            raise forms.ValidationError('用户邮箱不存在')

        # 判断验证码是否正确
        send_for = self.cleaned_data['send_for']
        vercode_session = self.request.session.get(send_for,'')
        vercode = self.cleaned_data['vercode']
        if vercode_session != vercode:
            raise forms.ValidationError('验证码不正确')

        user = User.objects.get(username = email)
        self.cleaned_data['user'] = user

        return self.cleaned_data

    def clean_confirmPassword(self):
        confirmPassword = self.cleaned_data['confirmPassword']
        password = self.cleaned_data['password']
        if confirmPassword != '' and confirmPassword != password:
            raise ValueError('两次输入的密码不一致')
        return confirmPassword