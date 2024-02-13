from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path("home/",views.home,name='home'),
    path("subject/",views.subject,name='subject'),
    path("subject/<slug:slug>/",views.subject_deatil,name='subject_deatil'),
    path("article/",views.article,name='article'),
    path("article/<slug:slug>/",views.detail,name='detail'),
    path("article/changelike/",views.changelike,name='changelike'),
    path("tool/",views.tool,name = "tool"),
    path("about/",views.about,name = "about"),
]
