from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login , logout, authenticate

def user_logout(request):
    logout(request)
    return redirect("login")


def user_profile(request):
    user=request.user
    return render(request,"./user/profile.html",{"user":user})

def user_login(request):
    message=""
    if request.method =="POST":
        if request.POST.get('register'):
            return redirect('register')
        username=request.POST.get("username")
        password=request.POST.get("password")

        print(username,password)
        if not User.objects.filter(username=username):
            message="查無此帳號"
        else:
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                message="登入成功!"
                return redirect("profile")
            else:
                message="密碼錯誤!"
            
    return render(request,"./user/login.html",{"message":message})
# Create your views here.
def user_register(request):
    message=''
    if request.method == "POST":
        username=request.POST.get('username')
        password1=request.POST.get('password1')
        password2=request.POST.get('password2')

        if len(password1)<8:
            message= "密碼過短"
        elif password1!=password2:
            message= "兩次密碼不相同"
        else:
            if User.objects.filter(username=username):
                message = "帳號已經註冊過"
            else:
                user=User.objects.create_user(username=username,password=password1)
                user.save()
                message="帳號註冊成功!"
                login(request,user)
                return redirect("profile")
        print(username,password1,password2)

    form= UserCreationForm()
    return render(request,"./user/register.html",{"form":form, "message":message})


