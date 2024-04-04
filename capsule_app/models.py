from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.

class Creator(models.Model):

    name = models.CharField(max_length=200, blank = False)
    email = models.EmailField(max_length=100)

    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('creator-detail', args=[str(self.id)])


class Capsule(models.Model):
    
    EDUCATION = (
        ('MS', 'Middle School'),
        ('HS', 'High School'),
        ('AD', 'Associate Degree'),
        ('BD', 'Bachelor\'s Degree'),
        ('MD', 'Master\'s Degree'),
        ('DD', 'Doctoral Degree'),
    )

    title = models.CharField(max_length = 200, default = 'Capsule Name', blank=False)
    is_primary = models.BooleanField(default = False)
    synopsis = models.TextField(blank = True)
    education = models.CharField(max_length = 200, choices=EDUCATION, blank = True)
    profession = models.CharField(max_length = 200, blank = True)
    fav_book = models.CharField(max_length = 200, blank = True)
    fav_movie = models.CharField(max_length = 200, blank = True)
    fav_quote = models.TextField(blank = True)
    user = models.ForeignKey(Creator, on_delete = models.CASCADE)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('capsule-detail', args=[str(self.id)])
    

    