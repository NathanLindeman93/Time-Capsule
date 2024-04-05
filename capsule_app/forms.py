from django.forms import ModelForm
from .models import Capsule, Creator
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CapsuleForm(ModelForm):
    class Meta:
        model = Capsule
        fields = '__all__'
    
class CreatorForm(ModelForm):
    class Meta:
        model = Creator
        fields = '__all__'