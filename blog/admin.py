from django.contrib import admin
from .models import Topic,Subject,Tag,Category,Article,Carousel,Welcome,About,LikeDetail,ToolSet,Tool

# Register your models here.
# 自定义管理站点的名称和URL标题
admin.site.site_header = '网站管理'
admin.site.site_title = '博客后台管理'

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    date_hierarchy = 'created'
    list_display = ('id', 'name', 'slug', 'cover', 'sort_by', 'status','vip')
    list_editable = ('sort_by', 'status','vip')
    list_display_links = ('name',)
    list_filter = ('created', 'status')

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    date_hierarchy = 'created'
    list_display = ('id', '__str__', 'created', 'updated', 'sort_by', 'subject')
    list_editable = ('sort_by',)
    list_display_links = ('__str__',)
    list_filter = ('created', 'sort_by', 'subject')

    # 设置搜索字段
    search_fields = ['name', 'subject__name']

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name','slug')
    list_editable = ('name','slug')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name','slug')
    list_editable = ('slug',)
    list_display_links = ('name',)

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    # 筛选器
    # date_hierarchy = 'created'

    # 排除
    # exclude = ('views',)

    # 列表
    list_display = ('id','title','short_title','is_top','is_publish','topic','sort_in_topic')

    # 编辑页，字段归类显示
    fieldsets = (
        ('文章信息',{'fields':(('title','short_title','slug'),'summary','content','cover',('is_top','is_publish'))}),
        ('文章关系',{'fields':('author','category','tags')}),
        ('文章专题',{'fields':('topic','sort_in_topic')}),
    )

    # 允许直接编辑的字段
    list_editable = ('short_title','is_top','is_publish','topic','sort_in_topic')

    # 设置需要添加<a>标签的字段
    list_display_links = ('title',)

    # 激活过滤器
    list_filter = ('created', 'topic__subject', 'category', 'is_top', 'is_publish')

    # 控制每页显示的对象数量，默认是100
    list_per_page = 10

    # 给多选增加一个左右添加的框
    filter_horizontal = ('tags',)

    # 搜索，可以搜查本身字段也可以搜索外键的字段
    search_fields = ('author__username', 'title', 'topic__name')

# 轮播图
@admin.register(Carousel)
class CarouselAdmin(admin.ModelAdmin):
    list_display = ('id','title','sort_by','img_url','jump_url','is_show')
    list_editable = ('is_show','sort_by')

# 欢迎图
@admin.register(Welcome)
class WelcomeAdmin(admin.ModelAdmin):
    list_display = ('id','title','img_url','jump_url','is_show')
    list_editable = ('is_show',)

# 关于
admin.site.register(About)

# 喜欢列表
admin.site.register(LikeDetail)


# 工具
@admin.register(ToolSet)
class ToolSetAdmin(admin.ModelAdmin):
    list_display = ('id','name','sort_by')
    list_editable = ('name','sort_by')

@admin.register(Tool)
class ToolAdmin(admin.ModelAdmin):
    list_display = ('id','name','url','toolset','sort_by')
    list_display_links = ('name',)
    list_editable = ('url','toolset','sort_by')