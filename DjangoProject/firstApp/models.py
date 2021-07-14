from django.db import models


# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=150, verbose_name='title')
    body = models.TextField(verbose_name='content')
    creator = models.ForeignKey('auth.User', verbose_name='creator', on_delete=models.PROTECT)
    time = models.DateTimeField(auto_now_add=True, verbose_name='created on')
    intro_image = models.ImageField(verbose_name='Post Image', blank=True, null=True)
    likes = models.IntegerField(verbose_name='likes', default=0)
    categories = models.ManyToManyField('firstApp.Category')

    class Meta:
        ordering = ('title',)
        verbose_name = 'post'
        verbose_name_plural = 'posts'

    def __str__(self):
        return f'{self.title}'


class Category(models.Model):
    """
    Categories for posts
    """
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=20, unique=True, null=False, blank=False)

    class Meta:
        permissions = []
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name
