from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
import json

from .models import Recipe, Ingredient, Instruction

# Create your views here.
def index(request):
    recipes = Recipe.objects.all()
    return render(request, "recipes/index.html", {
        "recipes": recipes,
    })

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
    #check if user is logged in
    if request.user.is_authenticated:

        if request.method == "POST":
            # get all information to be stored
            title = request.POST.get("title")
            description = request.POST.get("description")
            servings = request.POST.get("servings")
            cuisine = request.POST.get("cuisine")
            cooking_time = request.POST.get("cooking-time")
            preperation_time = request.POST.get("preperation-time")
            category = request.POST.get("category")
            image_url = request.POST.get("image-url")
            if all(v is not None for v in [title,description,servings,cuisine,cooking_time,
                                           preperation_time,category,image_url]):
                
                Recipe.objects.create(title=title, description=description, servings=servings, cuisine=cuisine, cooking_time=cooking_time, 
                                    preperation_time=preperation_time, category=category, image_url=image_url, creator=request.user)
                recipe  = Recipe.objects.all().last()
                # get every ingredient and instruction that is added to the recipe and store them in a list
                i = 0
                while bool(request.POST.get(f"instruction[{i}]")):
                    Instruction.objects.create(recipe=recipe, instruction_number=i+1, instruction=request.POST.get(f"instruction[{i}]"))
                    i += 1
                i = 0
                while bool(request.POST.get(f"ingredient[{i}]")):
                    request.POST.get(f"amount[{i}]")
                    Ingredient.objects.create(recipe=recipe, unit=request.POST.get(f"unit[{i}]"), 
                                            amount=request.POST.get(f"amount[{i}]"), ingredient=request.POST.get(f"ingredient[{i}]"))
                    i += 1

                return HttpResponseRedirect(reverse("recipe", kwargs={"recipe_id": recipe.id}))
            else:
                return render(request, "recipes/new_recipe.html", status=406)
        
        return render(request, "recipes/new_recipe.html")
    else:
        return HttpResponseRedirect(reverse("login"))
    

def recipe(request, recipe_id):
    if request.method == "POST":
        return HttpResponseRedirect(reverse("index"))
    try:
        recipe = Recipe.objects.get(pk=recipe_id)
        ingredients = Ingredient.objects.filter(recipe=recipe)
        instructions = Instruction.objects.filter(recipe=recipe)
        return render(request,"recipes/recipe.html", {
            "recipe": recipe,
            "instructions": instructions,
            "ingredients": ingredients,
        })
    except:
        return HttpResponseRedirect(reverse("index"))
    

def search(request):
    q = request.GET.get("q")
    if len(q) == 0:
        return HttpResponseRedirect(reverse("index"))
    try:
        recipes = Recipe.objects.filter(title__contains=q)
        return render(request, "recipes/index.html", {
            "recipes":recipes,
        })
    except:
        return HttpResponseRedirect(reverse("index"))
