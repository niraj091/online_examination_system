from django.shortcuts import render,redirect
from django.views import View
from .forms import FacultyForm,FacultyInfoForm
from datetime import  datetime
from .models import FacultyInfo
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required,user_passes_test
from django.core.mail import EmailMessage
import threading
from django.contrib.sites.shortcuts import get_current_site
from student.views import EmailThread
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from questions.views import has_group

def is_faculty(user):
    return user.groups.filter(name='Professor').exists()
@login_required(login_url='faculty-login')
@user_passes_test(is_faculty)
def index(request):
    students = User.objects.filter(groups__name = "Student")
    
    
    current_time = datetime.now().strftime('%H')
    current_time = int(current_time)
    if 0 <= current_time <= 12:
    	context={
    "greet":"Good Morning",
    "stu":students.all().count()
   }
    if 12 <= current_time <= 18:
    	context={
    "greet":"Good Afternoon",
    "stu":students.all().count()
    }
    if 18 <= current_time <= 24:
    	context={
    "greet":"Good Evening",
    "stu":students.all().count()
    }
    	
    return render(request,'faculty/index.html',context)

class Register(View):
    def get(self,request):
        faculty_form = FacultyForm()
        faculty_info_form = FacultyInfoForm()
        return render(request,'faculty/register.html',{'faculty_form':faculty_form,'faculty_info_form':faculty_info_form})
    
    def post(self,request):
        faculty_form = FacultyForm(data=request.POST)
        faculty_info_form = FacultyInfoForm(data=request.POST)
        email = request.POST['email']

        if faculty_form.is_valid() and faculty_info_form.is_valid() and faculty_form.cleaned_data['password'] == faculty_form.cleaned_data['confirm_password']:
            faculty = faculty_form.save()
            faculty.set_password(faculty.password)
            faculty.is_active = True
            faculty.is_staff = True
            faculty.save()

            domain = get_current_site(request).domain
            email_subject = 'Activate your Exam Portal Faculty account'
            email_body = "Hi. Please contact the admin team of "+domain+". To register yourself as a professor."+ ".\n\n You are receiving this message because you registered on " + domain +". If you didn't register please contact support team on " + domain 
            fromEmail = 'noreply@exam.com'
            email = EmailMessage(
				email_subject,
				email_body,
				fromEmail,
				[email],
            )
            student_info = faculty_info_form.save(commit=False)
            student_info.user = faculty
            if 'picture' in request.FILES:
                student_info.picture = request.FILES['picture']
            student_info.save()
            messages.success(request,"Registered Succesfully. Check Email for confirmation")
            EmailThread(email).start()
            return redirect('faculty-login')
        elif faculty_form.cleaned_data['password'] != faculty_form.cleaned_data['confirm_password']:
        	messages.error(request,"The passwords do not match.")
        	return render(request,'faculty/register.html',{'faculty_form':faculty_form, 'faculty_info_form':faculty_info_form})
        else:
            print(faculty_form.errors,faculty_info_form.errors)
            return render(request,'faculty/register.html',{'faculty_form':faculty_form,'faculty_info_form':faculty_info_form})
    
class LoginView(View):
	def get(self,request):
		return render(request,'faculty/login.html')
	def post(self,request):
		username = request.POST['username']
		password = request.POST['password']
		has_grp = False
		if username and password:
			user = auth.authenticate(username=username,password=password)
			exis = User.objects.filter(username=username).exists()
			if exis:
				user_ch = User.objects.get(username=username)
				has_grp = has_group(user_ch,"Professor")
			if user and user.is_active and exis and has_grp:
				auth.login(request,user)
				return redirect('faculty-index')
			elif not has_grp and exis:
				messages.error(request,'You dont have permssions to login as faculty. If You think this is a mistake please contact admin')	
				return render(request,'faculty/login.html')
                
			else:
				messages.error(request,'Invalid credentials')	
				return render(request,'faculty/login.html')
            
            

		messages.error(request,'Please fill all fields')
		return render(request,'faculty/login.html')

class LogoutView(View):
	def post(self,request):
		auth.logout(request)
		messages.success(request,'Logged Out')
		return redirect('faculty-login')