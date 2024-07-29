from django.shortcuts import render,redirect
from .models import *
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url="/login/")
def receipes(request):
    if request.method=="POST":
        data=request.POST
        rec_name=data.get('rec_name')
        rec_desc=data.get('rec_desc')
        rec_image=request.FILES.get('rec_image')
        
        Receipe.objects.create(
            rec_image=rec_image,
            rec_name= rec_name,
            rec_desc= rec_desc,
        )
        return redirect('/receipes/')
    
    queryset=Receipe.objects.all()
    if request.GET.get('search'):
        queryset=queryset.filter(rec_name__icontains=request.GET.get('search'))        # print(request.GET.get('search'))

    context={'receipes':queryset}
    return render (request, 'res.html',context)

@login_required(login_url="/login/")

def delete_receipe(request,id):
    queryset= Receipe.objects.get(id=id)
    queryset.delete()
    # return HttpResponse("a")
    return redirect('/receipes/')

# authentication is given to users only
@login_required(login_url="/login/")
def update_receipe(request,id):
    queryset=Receipe.objects.get(id=id)
    if request.method=="POST":
        data=request.POST
        rec_name=data.get('rec_name')
        rec_desc=data.get('rec_desc')
        rec_image=request.FILES.get('rec_image')
        queryset.rec_name=rec_name
        queryset.rec_desc=rec_desc
        if rec_image:
            queryset.rec_image=rec_image
        queryset.save()
        return redirect('/receipes/')
    context={'receipes':queryset}
    return render(request ,'update_receipes.html',context)


def login_page(request):
    if request.method == "POST":
        username=request.POST.get('username')
        password=request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            messages.error(request,'Invalid Username')
            return redirect('/login/')
        user=authenticate(username=username, password=password)
        if user is None:
            messages.error(request,'Invalid Password')
            return redirect ('/login/')
        else:
            login(request, user)
            return redirect('/receipes/')

    return render(request, 'login.html')

def logout_page(request):
    logout(request)
    return redirect ('/login/')

def register(request):
    if request.method == "POST":
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        username=request.POST.get('username')
        password=request.POST.get('password')

        user=User.objects.filter(username=username)
        if user.exists():
            messages.info(request,'Username already exists')
            return redirect('/register/')

        user=User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username,
           )
        user.set_password(password)
        user.save()
        messages.info(request,'account created successfully')
        return redirect('/register/')
    return render(request, 'register.html')
