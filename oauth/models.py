from django.db import models
from django.contrib.auth.models import AbstractUser
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

# Create your models here.
class Ouser(AbstractUser):
    avatar = ProcessedImageField(upload_to='avatar/%Y%m%d',
                                 default='avatar/default.png',
                                 verbose_name='头像',
                                 processors=[ResizeToFill(80,80)]
                                 )
    nickname = models.CharField(max_length=10,default='访客')
    vip = models.BooleanField(default=False,verbose_name='用户是否是vip')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def __str__(self):
        return f'User: {self.username}'