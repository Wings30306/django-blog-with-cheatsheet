"""
Models for blog
"""

from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

# Create your models here.
STATUS = ((0, "Draft"), (1, "Published"))


class Post(models.Model):
    """
    Users should be able to post blog posts.
    This class will be used to store blog posts
    """
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="blog_posts")
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()
    featured_image = CloudinaryField('image', default='placeholder')
    excerpt = models.TextField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    likes = models.ManyToManyField(User, related_name='blog_likes', blank=True)

    class Meta:
        """ Meta class for ordering by date - most recent first """
        ordering = ['-created_on']

    def __str__(self):
        return f"{self.title}"

    def number_of_likes(self):
        """
        Count number of likes on a post
        """
        return self.likes.count()


class Comment(models.Model):
    """
    Users should be able to comment on posts.
    This class will save users' comments
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name="comments")
    name = models.CharField(max_length=100)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        """ Meta class for ordering by date - most recent first """
        ordering = ['-created_on']

    def __str__(self):
        return f"Comment by {self.name} on post {self.post}: {self.body}"
