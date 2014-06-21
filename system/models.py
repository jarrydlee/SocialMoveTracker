from django.db import models

class Post(models.Model):
    post_id = models.CharField(max_length=50, unique=True)
    text = models.CharField(max_length=250)
    keyword = models.ForeignKey(Keyword)
    label = models.CharField(max_length=5)
    positive = models.IntegerField()
    negative = models.IntegerField()
    neutral = models.IntegerField()

class Keyword(models.Model):
    word = models.CharField(max_length=50)