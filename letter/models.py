import uuid

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone


# Create your models here.
class Letter(models.Model):

    class Audience(models.TextChoices):
        PUBLIC_ANON = 'public, but as anon'
        PRIVATE = 'private'

    id = models.UUIDField(unique=True, primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    content = models.TextField()
    delivery_date = models.DateField()
    date_posted = models.DateTimeField(default=timezone.now)
    email_address = models.EmailField()
    audience = models.CharField(max_length=20, choices=Audience.choices)
    delivered = models.BooleanField(default=False)

    class Meta:
        ordering = ('-date_posted',)

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse('letter:letter_detail', kwargs={'pk': self.id})


class Comment(models.Model):
    
    user = models.CharField(max_length=100, null=True)
    comment = models.TextField()
    letter = models.ForeignKey(Letter, on_delete=models.CASCADE)
    parent_comment = models.ForeignKey('self', null=True, on_delete=models.SET_NULL, related_name='replies')
    date_posted = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f'Comment by {self.user if self.user else "Anonymous"}'
    