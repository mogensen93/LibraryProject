from django.shortcuts import render, reverse
from django.contrib.auth import authenticate, login as dj_login, logout as dj_logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import RequestPasswordReset, User_Access_Level 

# Create your views here.
def login(request):
    context = {}
    if request.method == 'POST':
        username = request.POST["user"]
        password = request.POST["pass"]

        user = authenticate(request, username = username, password = password)
        if user:
            dj_login(request, user)
            return HttpResponseRedirect(reverse('library_app:index'))
        else: 
            context = {
                'error': 'Wrong username or password'
            }

    return render(request, 'login_app/login.html', context)

def sign_up(request):
    user_acess_level = User_Access_Level()
    context = {
        'access_level': user_acess_level
    }
    if request.method == 'POST':
        user_name = request.POST["user"]
        email = request.POST["email"]
        password = request.POST["pass"]
        confirm_password = request.POST["repeat_pass"]
        type_of_user = request.POST["user_type"]
        

        if password == confirm_password: 
            if User.objects.create_user(user_name, email, password):
                new_user = User.objects.get(username=user_name)
                user_access = User_Access_Level()
                user_access.user = new_user
                user_access.access_level = type_of_user
                user_access.save()
                
                return HttpResponseRedirect(reverse('login_app:login'))
            else: 
                context = {
                'error':'Something went wrong'
                }
        else: 
            context = {
                'error':'Passwords did not match'
            }
    return render(request, 'login_app/sign_up.html', context)

@login_required
def change_password(request):
    current_password = request.user.password

    context = {

        'current_pass': current_password

    }
    if request.method == "POST":
        old_pass = request.POST['old_pass']
        new_pass1 = request.POST['new_pass1']
        new_pass2 = request.POST['new_pass2']

        if not old_pass == new_pass1:
            if new_pass1 == new_pass2:
                    user = request.user
                    user.set_password(new_pass1)
                    user.save()
                    context = {
                        'error': 'Password has been changed succesfully'
                    }
            else:
                context = {
                    'error': 'New passwords didnt match'
                }

        else: 
            context = {
                'error': 'New password and old must not be the same.'
            }
    return render(request, 'login_app/change_password.html', context)

def request_password_reset(request):
    context = {}
    if request.method == "POST":
        post_user = request.POST["user"]
        
        user = None

        if post_user:
            try:
                user = User.objects.get(username=post_user)
            except:
                print (f"Invalid password request: {post_user}")

        else: 
            post_user = request.POST['email']
            try: 
                user = User.objects.get(email = post_user)
            except:
                print(f"invalid password request: {post_user}")
        print(user)
        if user: 
            
            
            rpr = RequestPasswordReset()
            rpr.user = user
            rpr.save()
            print(rpr)

            context = {
                'token': rpr.token
            }

           
            return render (request, 'login_app/password_reset.html', context)

    return render (request, 'login_app/request_password_reset.html')

def password_reset(request):
    
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        token = request.POST['token']

        if password == confirm_password:
            try:
                rpr = RequestPasswordReset.objects.get(token=token)
                rpr.save()
            except: 
                print("Invalid password attempt")
                return render(request, 'login_app/password_reset.html')
            user = rpr.user
            user.set_password(password)
            user.save()
            return HttpResponseRedirect(reverse('login_app:login'))

    return render(request, 'login_app/password_reset.html')
    
@login_required
def logout(request):
    dj_logout(request)
    return render(request, 'login_app/login.html')
