from django.forms import ModelForm
from .models import Capsule, Creator
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CapsuleForm(ModelForm):
    class Meta:
        model = Capsule
        fields = '__all__'
        exclude = ('creator',)
    
class CreatorForm(ModelForm):
    class Meta:
        model = Creator
        fields = '__all__'
        exclude = ('user',)


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']