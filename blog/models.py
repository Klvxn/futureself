from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


# Create your models here.
class Blog(models.Model):

    class Status(models.TextChoices):
        PENDING = 'under review'
        PUBLISHED = 'published'

    title = models.CharField(max_length=100, unique=True)
    content = models.TextField()
    slug = models.SlugField(unique=True, max_length=100)
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="blog/")
    status = models.CharField(max_length=15, choices=Status.choices, default=Status.PENDING)

    class Meta:
        ordering = ('-date_posted',)
        
    def __str__(self) -> str:
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:blog_detail', args=[self.slug, self.date_posted.year, self.date_posted.month])
    