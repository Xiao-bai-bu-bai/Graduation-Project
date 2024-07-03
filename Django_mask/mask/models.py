from django.db import models

class Admin(models.Model):
    """管理员表"""
    username = models.CharField(verbose_name='管理员', max_length=32)
    password = models.CharField(verbose_name='密码', max_length=64)
    age = models.IntegerField(verbose_name='年龄', null=True, blank=True)
    gender = models.IntegerField(verbose_name='性别',
                                 choices=[(1, '男'), (2, '女')],
                                 default=1)
