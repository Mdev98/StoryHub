from django.db import models
from django.db.models import Count

from authentication.models import User


# Create your models here.

class Story(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stories')
    tag = models.ManyToManyField('Tag', related_name='stories')

    def __str__(self):
        return self.title

    def get_comment_count(self):
        return self.comments.count()

    def get_like_count(self):
        return self.likes.count()

    def get_tags(self):
        return ', '.join([tag.name for tag in self.tag.all()])

    def has_liked(self, user):
        return self.likes.filter(user=user).exists()

    def get_comments(self):
        return self.comments.order_by('-created_at')

    @classmethod
    def get_top_stories(cls):
        return cls.objects.annotate(like_count=Count('likes')).order_by('-like_count')


class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    def get_story_count(self):
        return self.stories.count()

    @classmethod
    def get_most_popular_tag(cls):
        return cls.objects.annotate(story_count=Count('stories')).order_by('-story_count')


class Comment(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.author} commented on {self.story}'


class Like(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['story', 'user'], name='unique_like')
        ]

    def __str__(self):
        return f'{self.user} liked {self.story}'
