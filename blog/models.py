from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

TOPIC_CHOICES = ((x, x) for x in ["travel", "food", "sport"])


# створення класу-моделі для "посту"
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.CharField(choices=TOPIC_CHOICES,
                             default='Travel', max_length=50)
    title = models.CharField(max_length=200)
    post_img = models.ImageField(blank=True, null=True)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now())
    published_date = models.DateTimeField(auto_now_add=True)
    link = models.CharField(max_length=500, blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


# Comment model class
class Comment(models.Model):
    comment_to = models.ForeignKey("Post", on_delete=models.CASCADE)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    comment_text = models.TextField()
    data = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return "{} ".format(self.comment_text)
