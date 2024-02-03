from django.urls import path
from . import views

app_name = 'oauth'
urlpatterns = [
    path("login/",views.login,name='login'),
    path("register/",views.register,name='register'),
    path("forget_pwd/",views.forget_pwd,name='forget_pwd'),
    path("logout/",views.logout,name='logout'),
    path("send_verification_code/",views.send_verification_code,name='send_verification_code'),
]
