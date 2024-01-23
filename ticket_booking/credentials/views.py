from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.http import request
from django.shortcuts import render, redirect


# Create your views here.
def register(request):

    if request.method == 'POST':

        uname = request.POST['reg_uname']
        fname = request.POST['reg_fname']
        lname = request.POST['reg_lname']
        email = request.POST['reg_email']
        rpass = request.POST['reg_pass']
        cpass = request.POST['reg_cpass']
        if rpass == cpass:
            if User.objects.filter(username=uname):
                messages.info(request, "username taken")
                return redirect('register')
            elif User.objects.filter(email=email):
                messages.info(request, "email taken")
                return redirect('register')
            else:
                user = User.objects.create_user(username=uname, first_name=fname, last_name=lname, email=email, password=rpass)
                user.save()
                return redirect('login')
        else:
            messages.info(request, "password does not match")
            return redirect('register')
    return render(request, "register.html")

def login(request):
    if request.method == 'POST':
        uname=request.POST['uname']
        password=request.POST['pass']
        user=auth.authenticate(username=uname,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request,"invalid credential")
            return redirect('login')
    return render(request,'login.html')

def logout(request):
    auth.logout(request)
    return redirect('/')