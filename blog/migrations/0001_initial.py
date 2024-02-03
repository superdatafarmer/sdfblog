# Generated by Django 4.2 on 2024-01-12 23:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import imagekit.models.fields
import mdeditor.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("contenttypes", "0002_remove_content_type_name"),
    ]

    operations = [
        migrations.CreateModel(
            name="About",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=20, verbose_name="时间或标题")),
                ("content", models.TextField(max_length=250, verbose_name="描述内容")),
                (
                    "sort_by",
                    models.IntegerField(
                        default=999, help_text="展示顺序", verbose_name="排序"
                    ),
                ),
            ],
            options={
                "verbose_name": "关于",
                "verbose_name_plural": "关于",
                "ordering": ["-sort_by"],
            },
        ),
        migrations.CreateModel(
            name="Article",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=20, verbose_name="标题")),
                (
                    "slug",
                    models.SlugField(
                        blank=True,
                        max_length=250,
                        null=True,
                        unique=True,
                        verbose_name="英文短标题",
                    ),
                ),
                ("summary", models.TextField(max_length=250, verbose_name="摘要")),
                ("content", mdeditor.fields.MDTextField(verbose_name="内容")),
                (
                    "cover",
                    imagekit.models.fields.ProcessedImageField(
                        blank=True,
                        default="article/default.jpg",
                        help_text="5:4上传比例",
                        upload_to="article/cover",
                        verbose_name="封面",
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(auto_now_add=True, verbose_name="创建时间"),
                ),
                ("updated", models.DateTimeField(auto_now=True, verbose_name="创建时间")),
                ("is_top", models.BooleanField(default=False, verbose_name="是否置顶")),
                ("is_publish", models.BooleanField(default=True, verbose_name="是否发布")),
                ("views", models.IntegerField(default=0, verbose_name="浏览量")),
                ("likes", models.IntegerField(default=0, verbose_name="喜欢")),
                (
                    "sort_in_topic",
                    models.IntegerField(
                        blank=True, default=999, null=True, verbose_name="主题内的排序"
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="作者",
                    ),
                ),
            ],
            options={
                "verbose_name": "文章",
                "verbose_name_plural": "文章",
                "ordering": ["-created"],
            },
        ),
        migrations.CreateModel(
            name="Carousel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=20, verbose_name="轮播图标题")),
                (
                    "description",
                    models.TextField(
                        default="轮播图描述", max_length=240, verbose_name="描述"
                    ),
                ),
                (
                    "sort_by",
                    models.IntegerField(
                        default=999, help_text="展示顺序", verbose_name="排序"
                    ),
                ),
                ("is_show", models.BooleanField(default=True, verbose_name="是否展示")),
                (
                    "img_url",
                    imagekit.models.fields.ProcessedImageField(
                        help_text="5:2上传比例", upload_to="carousel", verbose_name="轮播图"
                    ),
                ),
                (
                    "jump_url",
                    models.CharField(
                        default="#",
                        help_text="默认值#号不跳转",
                        max_length=100,
                        verbose_name="跳转链接",
                    ),
                ),
            ],
            options={
                "verbose_name": "轮播图",
                "verbose_name_plural": "轮播图",
                "ordering": ["sort_by"],
            },
        ),
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=20, verbose_name="分类")),
                (
                    "slug",
                    models.SlugField(
                        blank=True, null=True, unique=True, verbose_name="英文短标题"
                    ),
                ),
                (
                    "description",
                    models.TextField(default="分类描述", max_length=240, verbose_name="描述"),
                ),
            ],
            options={
                "verbose_name": "分类",
                "verbose_name_plural": "分类",
                "ordering": ["id"],
            },
        ),
        migrations.CreateModel(
            name="Subject",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50, verbose_name="专题名称")),
                (
                    "slug",
                    models.SlugField(
                        blank=True, null=True, unique=True, verbose_name="英文短标题"
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("not_started", "未开始"),
                            ("ongoing", "连载中"),
                            ("completed", "已完结"),
                        ],
                        default="not_started",
                        max_length=20,
                        verbose_name="状态",
                    ),
                ),
                ("description", models.TextField(max_length=250, verbose_name="描述")),
                (
                    "sort_by",
                    models.IntegerField(
                        default=999, help_text="作为专题列表页的排序", verbose_name="排序"
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(auto_now_add=True, verbose_name="创建时间"),
                ),
                ("updated", models.DateTimeField(auto_now=True, verbose_name="创建时间")),
                (
                    "cover",
                    imagekit.models.fields.ProcessedImageField(
                        default="subject/default.png",
                        help_text="5：3上传比例",
                        upload_to="subject/cover",
                        verbose_name="专题封面",
                    ),
                ),
            ],
            options={
                "verbose_name": "专题",
                "verbose_name_plural": "专题",
                "ordering": ["sort_by"],
            },
        ),
        migrations.CreateModel(
            name="Tag",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=20, verbose_name="标签")),
                (
                    "slug",
                    models.SlugField(
                        blank=True, null=True, unique=True, verbose_name="英文短标题"
                    ),
                ),
                (
                    "description",
                    models.TextField(default="分类描述", max_length=240, verbose_name="描述"),
                ),
            ],
            options={
                "verbose_name": "标签",
                "verbose_name_plural": "标签",
                "ordering": ["id"],
            },
        ),
        migrations.CreateModel(
            name="Welcome",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=20, verbose_name="欢迎图标题")),
                ("is_show", models.BooleanField(default=True, verbose_name="是否展示")),
                (
                    "img_url",
                    imagekit.models.fields.ProcessedImageField(
                        help_text="5:3上传比例", upload_to="welcome", verbose_name="轮播图"
                    ),
                ),
                (
                    "jump_url",
                    models.CharField(
                        default="#",
                        help_text="默认值#号不跳转",
                        max_length=100,
                        verbose_name="跳转链接",
                    ),
                ),
            ],
            options={
                "verbose_name": "欢迎图",
                "verbose_name_plural": "欢迎图",
                "ordering": ["id"],
            },
        ),
        migrations.CreateModel(
            name="ViewDetail",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("object_id", models.PositiveIntegerField()),
                ("date", models.DateField(default=django.utils.timezone.now)),
                ("views", models.IntegerField(default=0)),
                (
                    "content_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="contenttypes.contenttype",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Topic",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50, verbose_name="专题名称")),
                (
                    "sort_by",
                    models.IntegerField(
                        default=999, help_text="专题中的排序字段", verbose_name="排序"
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(auto_now_add=True, verbose_name="创建时间"),
                ),
                ("updated", models.DateTimeField(auto_now=True, verbose_name="创建时间")),
                (
                    "subject",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="topics",
                        to="blog.subject",
                        verbose_name="专题",
                    ),
                ),
            ],
            options={
                "verbose_name": "主题",
                "verbose_name_plural": "主题",
                "ordering": ["sort_by"],
            },
        ),
        migrations.CreateModel(
            name="LikeDetail",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                (
                    "article",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="blog.article",
                        verbose_name="文章",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="被谁喜欢",
                    ),
                ),
            ],
            options={"verbose_name": "喜欢明细", "verbose_name_plural": "喜欢明细",},
        ),
        migrations.AddField(
            model_name="article",
            name="category",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                to="blog.category",
                verbose_name="分类",
            ),
        ),
        migrations.AddField(
            model_name="article",
            name="tags",
            field=models.ManyToManyField(
                related_name="articles", to="blog.tag", verbose_name="标签"
            ),
        ),
        migrations.AddField(
            model_name="article",
            name="topic",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="articles",
                to="blog.topic",
                verbose_name="主题",
            ),
        ),
    ]
