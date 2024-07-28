from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
# Create your views here.
def index(request):
    return render(request, "recipes/index.html")

def register(request):
    if(request.method == "POST"):
        return HttpResponseRedirect(reverse("index"))

    return render(request, "recipes/register.html")

def login(request):
    if(request.method == "POST"):
        return HttpResponseRedirect(reverse("index"))

    return render(request, "recipes/login.html")
