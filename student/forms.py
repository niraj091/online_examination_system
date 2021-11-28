from django import forms
from .models import StudentInfo
from django.contrib.auth.models import User

class StudentForm(forms.ModelForm):
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
    

class StudentInfoForm(forms.ModelForm):
    class Meta():
        model = StudentInfo
        fields = ['first_name','last_name','picture']
 
        
        
     