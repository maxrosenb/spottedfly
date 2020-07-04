from django.db import models
from django.urls import reverse # < here
from django.utils.text import slugify # < here


class Post(models.Model): # < here
    title = models.CharField(max_length=255,
                             default='',
                             blank=True)
    body = models.TextField(default='',
                            blank=True)
    slug = models.SlugField(max_length=255,
                            default='',
                            blank=True,
                            unique=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:detail',
                       args=[str(self.slug)])