from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        print(f"the current user is {request.user}")
    return render(request, "recipes/index.html")

def register(request):
    if(request.method == "POST"):
        # if fields are empty, redirect back to the register page
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        password_confirmation = request.POST.get("password-confirmation", "")
        email = request.POST.get("email", "")
        email_confirmation = request.POST.get("email-confirmation", "")
        if len(username) == 0 or len(password) == 0 or len(password_confirmation) == 0 or len(email) == 0 or len (email_confirmation) == 0:
            return render(request, "recipes/register.html", status=406)
    
        # if passwords do not match, do not continue
        if password != password_confirmation:
            return render(request, "recipes/register.html", status=406)

        # if emails do not match, do not continue
        if email != email_confirmation:
            return render(request, "recipes/register.html", status=406)
        
        #try to create a new user    
        try:
            user = User.objects.create_user(username=username,
                                password=password,
                                email=email)
            auth_login(request,user)
            return HttpResponseRedirect(reverse("index"))
        # # if new user cannot be created, handle the problem by rendering the page again
        except:
            return render(request, "recipes/register.html", status=409)

    return render(request, "recipes/register.html")

def login(request):
    if request.user.is_authenticated:
        print(request.user.username)
    if(request.method == "POST"):
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        if len(username) == 0 or len(password) == 0:
            return render(request, "recipes/login.html", status=406)

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "recipes/login.html", status=401)

    return render(request, "recipes/login.html")

def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
    return HttpResponseRedirect(reverse("index"))

def new_recipe(request):
    if request.user.is_authenticated:

        if request.method == "POST":
            print("post")
        
        return render(request, "recipes/new_recipe.html")
    else:
        return HttpResponseRedirect(reverse("index"))