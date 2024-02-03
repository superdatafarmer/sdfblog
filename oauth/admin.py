from django.contrib import admin
from .models import Ouser

# Register your models here.
@admin.register(Ouser)
class OuserAdmin(admin.ModelAdmin):
    # 列表页字段
    list_display = ('username', 'email', 'nickname', 'is_staff', 'is_active', 'date_joined','vip')
    # 允许直接编辑的字段
    list_editable = ('is_staff','vip')
    # 编辑页分组配置
    fieldsets = (
        ('基础信息', {'fields': (('username', 'email', 'nickname'), ('avatar',))}),
        ('权限信息', {'fields': (('is_active', 'is_staff', 'is_superuser'), 'groups', 'user_permissions')}),
        ('重要日期', {'fields': (('last_login', 'date_joined'),)}),
    )
    filter_horizontal = ('groups', 'user_permissions',)
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'email')