from django.db import models
from django.utils import timezone
from django.urls import reverse
# Create your models here.
class Post(models.Model):
    author = models.ForeignKey('auth.User',on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    published_date = models.DateTimeField(blank=True,null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def get_absolute_url(self):
        return reverse('blogapp:post_detail',kwargs={'pk':self.pk})

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey('Post',on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    author = models.ForeignKey('auth.User',on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('blogapp:post_list')

    def __str__(self):
        return self.text
