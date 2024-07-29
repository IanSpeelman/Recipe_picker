from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User

# Create your views here.
def index(request):
    return render(request, "recipes/index.html")

def register(request):
    if(request.method == "POST"):
        # if fields are empty, redirect back to the register page
        if len(request.POST.get("username")) == 0 or len(request.POST.get("email")) == 0 or len(request.POST.get("email-confirmation")) == 0 or len(request.POST.get("password")) == 0 or len(request.POST.get("password-confirmation")) == 0:
            print("information incomplete")
            return render(request, "recipes/register.html", status=406)
    
        # if passwords do not match, do not continue
        if(request.POST.get("password") != request.POST.get("password-confirmation")):
            return render(request, "recipes/register.html", status=406)

        # if emails do not match, do not continue
        if(request.POST.get("email") != request.POST.get("email-confirmation")):
            return render(request, "recipes/register.html", status=406)
        
        #try to create a new user    
        # try:
        user = User.objects.create_user(username=request.POST.get("username"),
                            password=request.POST.get("password"),
                            email=request.POST.get("email"))
        user.save()
        return HttpResponseRedirect(reverse("index"))
        # # if new user cannot be created, handle the problem by rendering the page again
        # except:
        #     return render(request, "recipes/register.html", status=409)

    return render(request, "recipes/register.html")

def login(request):
    if(request.method == "POST"):
        return HttpResponseRedirect(reverse("index"))

    return render(request, "recipes/login.html")
