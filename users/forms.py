from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, UserInformation

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    
class UserInformationForm(forms.ModelForm):
    class Meta:
        model = UserInformation
        fields = (
            'profile_pic',
            'phone_number',
            'gender',
            'date_of_birth',
            'branch',
        )
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }
