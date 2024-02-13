from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.shortcuts import reverse
from django.contrib import auth
from django.utils import timezone
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from uuslug import slugify
from mdeditor.fields import MDTextField

# 内容体系
# 专题-主题-文章
# 分类-文章
# 标签-文章
User = auth.get_user_model()

# Create your models here.
# 专题
class Subject(models.Model):
    STATUS_CHOICES = (
        ('not_started', '未开始'),
        ('ongoing', '连载中'),
        ('completed', '已完结'),
    )

    name = models.CharField(max_length=50,verbose_name='专题名称')
    slug = models.SlugField(unique=True, editable=True,null=True,blank=True, verbose_name='英文短标题')
    status = models.CharField(max_length=20,verbose_name='状态',choices=STATUS_CHOICES,default='not_started')
    description = models.TextField(max_length=250, verbose_name='描述')
    sort_by = models.IntegerField(default=999,help_text='作为专题列表页的排序',verbose_name='排序')
    created = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='创建时间', auto_now=True)
    cover = ProcessedImageField(
        upload_to='cover',
        default='cover/default.png',
        processors=[ResizeToFill(250, 150)],
        help_text='5:3上传比例',
        verbose_name='专题封面'
    )
    vip = models.BooleanField(default=False,verbose_name='vip')

    class Meta:
        verbose_name = '专题'
        verbose_name_plural = verbose_name
        ordering = ['sort_by']

    def __str__(self):
        return self.name

    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Subject,self).save(*args,**kwargs)

    def get_article_count(self):
        count = 0
        for topic in self.topics.all():
            count += topic.articles.count()
        return count

# 主题
class Topic(models.Model):
    name = models.CharField(max_length=50,verbose_name='专题名称')
    sort_by = models.IntegerField(default=999,help_text='专题中的排序字段',verbose_name='排序')
    created = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='创建时间', auto_now=True)
    subject = models.ForeignKey(Subject,on_delete=models.PROTECT,related_name='topics',verbose_name='专题')

    class Meta:
        verbose_name = '主题'
        verbose_name_plural = verbose_name
        ordering = ['sort_by']

    def __str__(self):
        return f'[{self.subject.name}]{self.name}'


# 标签
class Tag(models.Model):
    name = models.CharField(max_length=20,verbose_name='标签')
    slug = models.SlugField(unique=True,editable=True,null=True,blank=True,verbose_name='英文短标题')
    description = models.TextField(max_length=240,verbose_name='描述',default='分类描述')

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.name

    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Tag,self).save(*args,**kwargs)

# 分类
class Category(models.Model):
    name = models.CharField(max_length=20,verbose_name='分类')
    slug = models.SlugField(unique=True,editable=True,null=True,blank=True,verbose_name='英文短标题')
    description = models.TextField(max_length=240,verbose_name='描述',default='分类描述')

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.name

    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Category,self).save(*args,**kwargs)

# 文章
class Article(models.Model):
    title = models.CharField(max_length=40,verbose_name='标题')
    short_title = models.CharField(max_length=20,verbose_name='文章短标题',null=True)
    slug = models.SlugField(max_length=250,unique=True,editable=True,null=True,blank=True,verbose_name='英文短标题')
    summary = models.TextField(max_length=250,verbose_name='摘要')
    content = MDTextField(verbose_name='内容')
    cover = ProcessedImageField(
        upload_to='cover',
        default='cover/default.png',
        processors=[ResizeToFill(250, 150)],
        help_text='5:3上传比例',
        verbose_name='封面',
        blank=True
    )
    created = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='创建时间', auto_now=True)
    is_top = models.BooleanField(default=False,verbose_name='是否置顶')
    is_publish = models.BooleanField(default=True,verbose_name='是否发布')
    views = models.IntegerField(default=0,verbose_name='浏览量')
    likes = models.IntegerField(default=0,verbose_name='喜欢')

    author = models.ForeignKey(User, default= 1, on_delete=models.PROTECT, verbose_name='作者')
    category = models.ForeignKey(Category,on_delete=models.PROTECT,verbose_name='分类')
    tags = models.ManyToManyField(Tag,related_name='articles',verbose_name='标签')

    # 专题-主题-文章
    topic = models.ForeignKey(Topic,on_delete=models.SET_NULL,null=True,blank=True,related_name='articles',verbose_name='主题')
    sort_in_topic = models.IntegerField(default=999,null=True,blank=True,verbose_name='主题内的排序')

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-created']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """优先使用专题地址"""
        return reverse('blog:detail', kwargs={'slug': self.slug})

    def get_absolute_subject_url(self):
        """优先使用专题地址"""
        return reverse('blog:subject_deatil', kwargs={'slug': self.topic.subject.slug})

    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Article,self).save(*args,**kwargs)

# 阅读明细，记录每天阅读的数量，采用content_type实现
class ViewDetail(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    date = models.DateField(default=timezone.now)
    views = models.IntegerField(default=0)


# 喜欢明细
class LikeDetail(models.Model):
    article = models.ForeignKey(Article,on_delete=models.CASCADE,verbose_name='文章')
    user = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='被谁喜欢')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '喜欢明细'
        verbose_name_plural = verbose_name

# 轮播图
class Carousel(models.Model):
    title = models.CharField(max_length=20,verbose_name='轮播图标题')
    description = models.TextField(max_length=240,verbose_name='描述',default='轮播图描述')
    sort_by = models.IntegerField(default=999, help_text='展示顺序', verbose_name='排序')
    is_show = models.BooleanField(default=True,verbose_name='是否展示')
    img_url = ProcessedImageField(
        upload_to='carousel',
        processors=[ResizeToFill(1000, 400)],
        help_text='5:2上传比例',
        verbose_name='轮播图'
    )
    jump_url = models.CharField(max_length=100,default='#',verbose_name='跳转链接',help_text='默认值#号不跳转')

    class Meta:
        verbose_name = '轮播图'
        verbose_name_plural = verbose_name
        ordering = ['sort_by']

    def __str__(self):
        return self.title


# welcome
class Welcome(models.Model):
    title = models.CharField(max_length=20, verbose_name='欢迎图标题')
    is_show = models.BooleanField(default=True, verbose_name='是否展示')
    img_url = ProcessedImageField(
        upload_to='welcome',
        processors=[ResizeToFill(500, 300)],
        help_text='5:3上传比例',
        verbose_name='轮播图'
    )
    jump_url = models.CharField(max_length=100, default='#', verbose_name='跳转链接', help_text='默认值#号不跳转')

    class Meta:
        verbose_name = '欢迎图'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.title

# 关于
class About(models.Model):
    content = MDTextField(verbose_name="描述内容")

    class Meta:
        verbose_name = '关于'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '关于'


class ToolSet(models.Model):
    name = models.CharField(max_length=10, verbose_name='名称')
    sort_by = models.IntegerField(default=999,verbose_name='排序')

    class Meta:
        verbose_name = '工具集合'
        verbose_name_plural = verbose_name
        ordering = ('sort_by',)

    def __str__(self):
        return self.name

class Tool(models.Model):

    name = models.CharField(max_length=10,verbose_name='名称')
    url = models.CharField(max_length=250,verbose_name='链接地址')
    description = models.TextField(max_length=250,verbose_name='描述')
    sort_by = models.IntegerField(default=999, verbose_name='排序')
    toolset = models.ForeignKey(ToolSet,on_delete=models.CASCADE,related_name='tools',verbose_name='合集')

    class Meta:
        verbose_name = '工具'
        verbose_name_plural = verbose_name
        ordering = ('sort_by',)

    def __str__(self):
        return self.name