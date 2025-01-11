from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class SingUpForm(UserCreationForm):
    email = forms.EmailField(required=False, help_text= 'Email not required')
    gender_type = ( ('male', 'Male'), ('female', 'Female'), )
    gender = forms.CharField(max_length=6, widget=forms.Select(choices=gender_type))
    age = forms.CharField(max_length=30)
    
    class Meta:
        model = User 
        fields = ('username','email', 'password1', 'password2')  

class UserForm(forms.ModelForm):
    class Meta:
        model = User 
        fields = ['username', 'email']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile  
        fields = ['about', 'gender', 'age', 'medical_history','ProfileImg']  
