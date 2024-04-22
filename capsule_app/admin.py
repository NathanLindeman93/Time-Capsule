from django.contrib import admin
from .models import *
from guardian.admin import GuardedModelAdmin

# Register your models here.

class CapsuleAdmin(GuardedModelAdmin):
    pass

admin.site.register(Capsule, CapsuleAdmin)
admin.site.register(Creator)
admin.site.register(Video)
