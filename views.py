from django.shortcuts import render,redirect
from .models import *
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required(login_url="/login-page")
def receipes(request):
    if request.method=='POST':

        data=request.POST
        receipe_image=request.FILES.get('receipe_image')
        receipe_name=data.get('receipe_name')
        receipe_description=data.get('receipe_description')

        Receipe.objects.create(
            receipe_image=receipe_image,
            receipe_name=receipe_name,
            receipe_description=receipe_description,
        )

        return redirect('/receipe-page')
    queryset=Receipe.objects.all()

    if request.GET.get('search'):
        queryset=queryset.filter(receipe_name__icontains=request.GET.get('search'))
    context={'receipes':queryset}

    return render(request,'receipes.html',context)


@login_required(login_url="/login-page")
def update_receipe(request,id):
    queryset=Receipe.objects.get(id=id)


    if request.method=='POST':

        data=request.POST

        receipe_image=request.FILES.get('receipe_image')
        receipe_name=data.get('receipe_name')
        receipe_description=data.get('receipe_description')

        queryset.receipe_name=receipe_name
        queryset.receipe_description=receipe_description
        if receipe_image:
            queryset.receipe_image=receipe_image
        queryset.save()
        return redirect('/receipe-page')

    context={'receipe':queryset}

    return render(request,'updated_receipes.html',context)

@login_required(login_url="/login-page")
def delete_receipe(request,id):
    queryset=Receipe.objects.get(id=id)
    queryset.delete()
    return redirect('/receipe-page')

# login-page

def login_page(request):

    
    if request.method=="POST":
           
        username=request.POST.get('username')
        password=request.POST.get('password')
        print(username)
        print(password)
        if not  User.objects.filter(username=username).exists():
            messages.error(request,"invalid user Credentials")
            return redirect("/login-page")
        
        user=authenticate(username=username,password=password)
        if user is None:
            messages.error(request,"invalid user Credentials")
            return redirect("/login-page")
        else:
            login(request,user)
            return redirect('/receipe-page') 
        



    return render(request,'login.html')

def logout_page(request):
    logout(request)
    return redirect('/login-page')


def register_page(request):

    if request.method=="POST":
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        email=request.POST.get('email')
        username=request.POST.get('username')
        password=request.POST.get('password')

        user=User.objects.filter(username=username)

        if user.exists():
            messages.info(request,'OOPS !! Username already Taken ')
            return redirect('/register-page')


        user=User.objects.create(first_name=first_name,
                                 last_name=last_name,
                                 email=email,
                                 username=username,
                                 )
        user.set_password(password)
        user.save()
        messages.info(request,'Account Created Successfully')
        return redirect('/register-page')        

    return render(request,'register.html')




