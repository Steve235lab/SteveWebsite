from django.db import models
from django.contrib.auth.models import User

# 定义功能数据库
# 用户信息
class Userinfo(models.Model):
    headImg = models.ImageField()
    nickName = models.CharField()
    belong = models.OneToOneField(User)
    def __init__(self):
        return self.id

# 栏目
# 树形结构，采用递归的查询方法
class Category(models.Model):
    name = models.CharField()
    belong = models.ForeignKey(self)
    def __init__(self):
        return self.id
    
# 文章
class Article(models.Model):
    title = models.CharField()
    cover = models.CharField()
    text = models.TextField()
    belong = models.ForeignKey(Userinfo)
    def __init__(self):
        return self.id
    
# 收藏
class Favourite(models.Model):
    belong_user = models.ForeignKey(Userinfo)
    belong_art = models.ForeignKey(Article)
    def __init__(self):
        return self.id
    
# 点赞
class Like(models.Model):
    belong_user = models.ForeignKey(Userinfo)
    belong_art = models.ForeignKey(Article)
    #num = models.IntegerField()
    def __init__(self):
        return self.id
    
# 打赏
class PayOrder(models.Model):
    order = models.CharField()
    price = models.CharField()
    status = models.BooleanField()
    def __init__(self):
        return self.id

