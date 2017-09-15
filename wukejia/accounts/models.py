from django.db import models
from django.contrib.auth.models import  User

# Create your models here.

class Profile(models.Model):
    user =  models.OneToOneField(User)
    name =  models.CharField("中文名",max_length=32)
    phone = models.CharField("电话号码",max_length=20)
    weixin = models.CharField("weixinid",max_length=50)

