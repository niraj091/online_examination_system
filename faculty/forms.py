from django import forms 
from .models import FacultyInfo
from django.contrib.auth.models import User

class FacultyForm(forms.ModelForm):
    confirm_password=forms.CharField(widget=forms.PasswordInput())
   
    class Meta:
        model = User
        fields = ['first_name','last_name','username', 'email', 'password']
        widgets = {
         'first_name' : forms.TextInput(attrs = {'id':'firstnamefield','class':'form-control'}),
          'last_name' : forms.TextInput(attrs = {'id':'lastnamefield','class':'form-control'}),
            'password': forms.PasswordInput(attrs = {'id':'passwordfield','class':'form-control'}),
            'email' : forms.EmailInput(attrs = {'id':'emailfield','class':'form-control'}),
            'username' : forms.TextInput(attrs = {'id':'usernamefield','class':'form-control'})
        }

class FacultyInfoForm(forms.ModelForm):
    class Meta():
        model = FacultyInfo
        fields = ['first_name','last_name','picture','subject','picture']
        widgets = {
            'subject' : forms.TextInput(attrs = {'class':'form-control'})
        }
