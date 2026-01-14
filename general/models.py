from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
import pyotp

class UserProfile(models.Model):
    class Type(models.TextChoices):
        reviewer = 'reviewer', 'рецензер'
        editor = 'editor', 'редактор'
    full_name = models.TextField(null = True)
    date_of_birth = models.TextField(null = True)
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    type = models.TextField(choices = Type, null = True)
    totp_key = models.TextField(null = True)
    class Meta:
        permissions = [
            ('can_create_objects', 'Может создавать объекты'),
            ('can_read_objects', 'Может просматривать информацию об объектах'),
            ('can_update_objects', 'Может обновлять объекты'),
            ('can_delete_objects', 'Может удалять объекты'),
        ]
    def save(self, *args, **kwargs):
        if self.id is None:
            self.totp_key = pyotp.random_base32()
        super().save(*args, **kwargs)

@receiver(post_save, sender = User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user = instance)