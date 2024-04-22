from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from guardian.shortcuts import assign_perm
from .validators import *
from django.core.validators import *


# Create your models here.

class Video(models.Model):
    caption = models.CharField(max_length=200, default = 'Video')
    video = models.FileField(upload_to="video/%y/%m/%d/")

    def __str__(self):
        return self.caption


class Creator(models.Model):

    name = models.CharField(max_length=200, default = 'name', blank = False)
    email = models.EmailField(max_length=100)

    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE, unique = True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('creator-detail', args=[str(self.id)])


class Capsule(models.Model):

    title = models.CharField("Capsule Title", max_length = 200, default = 'Capsule Name', blank=False)
    is_primary = models.BooleanField("Primary Capsule?", default = False)
    synopsis = models.TextField("Life Story", blank = True)
    video = models.FileField(upload_to="video/%y/%m/%d", blank = True, validators=[validate_video, file_size])
    education = models.CharField("Education", max_length = 200, blank = True)
    profession = models.CharField("Profession", max_length = 200, blank = True)
    fav_book = models.CharField("Favorite Book", max_length = 200, blank = True)
    fav_movie = models.CharField("Favorite Movie", max_length = 200, blank = True)
    fav_quote = models.TextField("Favorite Quote", blank = True)
    creator = models.ForeignKey(Creator, on_delete = models.CASCADE)
    
    class Meta:
        permissions = (
            ('create_capsule', 'Create Capsule'),
        )

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('capsule-detail', args=[str(self.id)])
    
@receiver(post_save, sender=Capsule)
def set_permission(sender, instance, **kwargs):
    assign_perm('add_capsule', instance.creator.user, instance)
    assign_perm('change_capsule', instance.creator.user, instance)
    assign_perm('delete_capsule', instance.creator.user, instance)
    assign_perm('view_capsule', instance.creator.user, instance)