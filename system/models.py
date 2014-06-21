from django.db import models

class Keyword(models.Model):
    word = models.CharField(max_length=50, unique=True)

class Post(models.Model):
    post_id = models.CharField(max_length=50, unique=True)
    text = models.CharField(max_length=250, unique=True)
    keyword = models.ForeignKey('Keyword')
    label = models.CharField(max_length=5)
    positive = models.IntegerField()
    negative = models.IntegerField()
    neutral = models.IntegerField()
    created_at = models.DateTimeField()

