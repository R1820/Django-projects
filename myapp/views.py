from django.shortcuts import render, redirect
from .models import *
from django.core.mail import send_mail
from django.conf import settings
import random
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def index(request):
    return render(request, 'index.html')

def vindex(request):
    return render(request, 'Vindex.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def signup(request):
    if request.method == "POST":
        try:
            user = User.objects.get(email = request.POST['email'])
            msg = "User already exist!!"
            return render(request, 'signup.html',{'msg':msg})
        except:
               if request.POST['password'] == request.POST['confirm_password']:
                   User.objects.create(
                       name = request.POST['name'],
                       email = request.POST['email'],
                       mobile = request.POST['mobile'],
                       password = request.POST['password'],
                       uprofile = request.FILES['profile'],
                       usertype = request.POST['usertype']
                   )
                   msg = "Signup Successfully!!"
                   return render(request, 'signup.html',{'msg':msg})
               else:
                   msg = "Password & confirm password does not match!!"
                   return render(request, 'signup.html',{'msg':msg}) 
    else:
        return render(request, 'signup.html')   
    
# @csrf_exempt    
def login(request):
    if request.method == "POST":
        try:
            user = User.objects.get(email = request.POST['email'])
            if user.password == request.POST['password']:
                request.session['email'] = user.email
                request.session['profile'] = user.profile.url
                if user.usertype == "customer":
                    return redirect('index')
                else:
                    return redirect('vindex')
            else:
                msg = "Password does not match!!"
                return render(request, 'login.html',{'msg':msg}) 
        except:
            msg = "Email does not match!!"
            return render(request, 'login.html',{'msg':msg})        
    else:
        return render(request, 'login.html')
     
def logout(request):
    del request.session['email']
    del request.session['profile']
    return redirect('login')

def cpass(request):
    if request.method == "POST":
        try:
            user = User.objects.get(email = request.session['email'])
            if user.password == request.POST['opassword']:
                if request.POST['npassword'] == request.POST['cnpassword']:
                    user.password = request.POST['npassword']
                    user.save()
                    return redirect('logout')
                else:
                    msg = "new password & confirm new password does not match!!"
                    return render(request, 'cpass.html',{'msg':msg})
            else:
                msg = "Old password does not match!!"
                return render(request, 'cpass.html',{'msg':msg})
        except:
            pass
    else:
        return render(request, 'cpass.html')
    
def fpass(request):
    if request.method == 'POST':
        try:
            user = User.objects.get(email = request.POST['email'])
            subject = 'OTP for forget-password'
            otp = random.randint(1001, 9999)
            message = 'Hi' +user.name+ 'your otp is : '+str(otp)
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email,]
            send_mail(subject,message,email_from,recipient_list)
            request.session['email'] = user.email
            request.session['otp'] = otp
            return render(request, 'otp.html')
        except:
            msg = "Email does not exist!!"
            return render(request, 'fpass.html',{'msg':msg})
        
    else: 
        return render(request, 'fpass.html')

def otp(request):

    try:
        otp = int(request.session['otp'])
        uotp = int(request.POST['uotp'])
        if otp == uotp:
            del request.session['otp']
            return redirect('newpass')
        else:
            msg = "Invalid otp!!"
            return render(request, 'otp.html',{'msg':msg})
    except Exception as e:
        print("***",e)
        return render(request, 'otp.html')
   
def newpass(request):
   if request.method == 'POST':
        try:
            user = User.objects.get(email = request.session['email'])
            if request.POST['npassword'] == request.POST['cnpassword']:
                user.password = request.POST['npassword']
                user.save()
                del request.session['email']
                return redirect('login')
            else:
                msg = "New password & confirm new password does not match!!"
                return render(request, 'newpass.html',{'msg':msg})
        except:
            pass
   else:
       return render(request, 'newpass.html')
   
def uprofile(request):
    user = User.objects.get(email = request.session['email'])
    return render(request, 'uprofile.html', {'user': user})

def Error(request):
    return render(request, 'Error.html')
    
def feature(request):
    return render(request, 'feature.html')

def service(request):
    return render(request, 'service.html')

def project(request):
    return render(request, 'project.html')

def team(request):
    return render(request, 'team.html')

def testimonial(request):
    return render(request, 'testimonial.html')