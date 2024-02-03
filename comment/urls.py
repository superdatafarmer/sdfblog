from django.urls import path
from . import views

app_name = 'comment'
urlpatterns = [
    path('add_comment/',views.add_comment,name='add_comment'),
    path('del_comment/',views.del_comment,name='del_comment'),
]
