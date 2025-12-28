from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

class UserProfile(models.Model):
    class Type(models.TextChoices):
        reviewer = 'reviewer', 'рецензер'
        editor = 'editor', 'редактор'
    full_name = models.TextField(null = True)
    date_of_birth = models.TextField(null = True)
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    type = models.TextField(choices = Type, null = True)

@receiver(post_save, sender = User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user = instance)