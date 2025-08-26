from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class SignUpForm(UserCreationForm):
    pass

    first_name = forms.CharField(max_length=30, required=False, help_text='Optional')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional')
    email = forms.EmailField(max_length=100, help_text='Enter a valid email address')

class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        ]
class User_form(forms.ModelForm):
     class meta:
          model = User
          fields = ['username', 'first_name', 'last_name', 'email']

class Edit_Profile_form(forms.ModelForm):
    
    gend = [
        ("Male", "Male"),
        ("Female", "Female")
    ]
    profile_picture = forms.ImageField(required=False, label="Your Passport")
    means_of_identity = forms.ImageField(required=False, label="Means of Identity")
    gender = forms.ChoiceField(choices=gend, required=True, widget=forms.RadioSelect)
    particulars = forms.FileField(required=False, label="Particulars")
    status = forms.ChoiceField(required=False)
    position = forms.ChoiceField(required=False)


    class Meta:
        model = Profile
        fields = [

         
        'address',
        'phone',
        'date_of_birth',
        'gender',
        'nationality',
        'state',
        'means_of_identity',
        'particulars',
        'profile_picture',
        'position',
        'department',
        'marital_status',
        'status',
        'staff',
        ]
        widgets = {
            'date_of_birth': forms.NumberInput(attrs = {'type': 'date'}),
        }      
  
    