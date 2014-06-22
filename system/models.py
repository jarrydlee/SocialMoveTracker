from django.db import models

class Keyword(models.Model):
    word = models.CharField(max_length=50, unique=True)

class Post(models.Model):
    post_id = models.CharField(max_length=50, unique=True)
    text = models.CharField(max_length=250, unique=True)
    keyword = models.ForeignKey('Keyword')
    semantic = models.IntegerField()
    confidence = models.FloatField()
    created_at = models.DateTimeField()

    def as_json(self):
        return dict(
            id=self.id,
            text=self.text,
            keyword=self.keyword.word,
            semantic=self.semantic,
            confidence=self.confidence,
            time=str(self.created_at.strftime("%H:%M"))


        )

