from django.contrib import admin

# Register your models here.

from .models import Capsule
admin.site.register(Capsule)

from .models import Creator
admin.site.register(Creator)

