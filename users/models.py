from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class UserProfile(models.Model):
    USER_GENDER = (
        ('male', '男'),
        ('female', '女'),
    )
    owner = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="用户")
    nike_name = models.CharField(max_length=50, verbose_name="昵称", blank=True, default='')
    birthday = models.DateField(verbose_name="生日", blank=True, null=True)
    gender = models.CharField('性别', max_length=6, choices=USER_GENDER, blank=True)
    adress = models.CharField('地址', max_length=100, blank=True)
    image = models.ImageField('用户头像', upload_to='images/%Y/%m/', default='images/2023/04/img.jpg', max_length=100)
    desc = models.TextField('个人简介', max_length=200, blank=True, default='')
    gexing = models.CharField('个性签名', max_length=100, blank=True, default='')

    class Meta:
        verbose_name = '用户数据'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.owner.username

# 邮箱校验记录

class EmailVerifyRecord(models.Model):
    """邮箱验证记录"""
    SEND_TYPE_CHOICES = (
        ('register', '注册'),
        ('forget', '找回密码'),
    )

    code = models.CharField('验证码', max_length=20)
    email = models.EmailField('邮箱', max_length=50)
    send_type = models.CharField(choices=SEND_TYPE_CHOICES, max_length=10, default='register')
    send_time = models.DateTimeField('时间', auto_now_add=True)

    class Meta:
        verbose_name = '邮箱验证码'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code


