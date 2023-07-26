from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse,reverse_lazy
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.translation import gettext_lazy as _


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self) -> str:
        return self.name



class Post(models.Model):
    # CHOICES = (
    #     ('New', 'New'),
    #     ('Accepted', 'Accepted'),
    #     ('Completed', 'Completed'),
    #     ('Cancelled', 'Cancelled'),
    # )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank= True)
    title = models.CharField(max_length=250)
    category = models.ManyToManyField(Category)
    text = RichTextUploadingField()
    created_date = models.DateTimeField(default = timezone.now)
    published = models.BooleanField(default=False)
    published_date = models.DateTimeField(null=True, blank=True)
    def approved_comments(self):
        return self.comments.filter(approve_comment = True)

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail',kwargs={'pk':self.pk})

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post,related_name='comments', on_delete=models.CASCADE)
    text = models.CharField(max_length=250)
    created_date = models.DateTimeField(default= timezone.now)
    approve_comment = models.BooleanField(default=False)

    def comment_approve(self):
        self.approve_comment = True
        self.save()
