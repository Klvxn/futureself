import uuid

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone


# Create your models here.
class Letter(models.Model):

    class AudienceChoices(models.TextChoices):
        PUBLIC = 'public, but as anon'
        PRIVATE = 'private'

    id = models.UUIDField(unique=True, primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    content = models.TextField()
    delivery_date = models.DateField()
    date_posted = models.DateTimeField(default=timezone.now)
    email_address = models.EmailField()
    audience = models.CharField(max_length=20, choices=AudienceChoices.choices)
    delivered = models.BooleanField(default=False)

    class Meta:
        ordering = ('-date_posted',)

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse('letter:letter_detail', kwargs={'pk': self.id})
