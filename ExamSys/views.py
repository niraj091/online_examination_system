from django.shortcuts import render
from django.contrib import messages
from django.core.mail import EmailMessage,send_mail

def index(request):
    return render(request,'index.html')
    
def contact(request):
	if request.method == "POST":
		name= request.POST.get("name")
		email = request.POST.get("email")
		msg = request.POST.get("msg")
		
		data = {
		        'name':name,
		        'email':email,
		        'msg':msg,
		}
		message = "Name:{}\nMessage: {}\nFrom: {}".format(data['name'],data["msg"],data["email"])
		send_mail("Feedback",message,"",["neerajjha091@gmail.com"])
		
		
		
		
	return  render(request,"contact.html")