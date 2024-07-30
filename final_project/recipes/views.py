from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

from .models import Recipe, Ingredient, Instruction

# Create your views here.
def index(request):
    #! this can be removed when done testing
    #! comment out for unittest
    # recipe = Recipe.objects.get(title="test recipe")
    # steps = Instruction.objects.filter(recipe=recipe)
    # ingredients = Ingredient.objects.filter(recipe=recipe)
    # print(recipe.title)
    # for step in steps:
    #     print(f"step {step.instruction_number}:{step.instruction}")
    # for ingredient in ingredients:
    #     print(f"{ingredient.amount}{ingredient.unit} of {ingredient.ingredient}")
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
                print(recipe.id)
                # get every ingredient and instruction that is added to the recipe and store them in a list
                i = 0
                instructions = []
                while bool(request.POST.get(f"instruction[{i}]")):
                    Instruction.objects.create(recipe=recipe, instruction_number=i+1, instruction=request.POST.get(f"instruction[{i}]"))
                    # print(Instruction.objects.all().last())
                    i += 1
                i = 0
                ingredients = []
                while bool(request.POST.get(f"ingredient[{i}]")):
                    Ingredient.objects.create(recipe=recipe, unit=request.POST.get(f"unit[{i}]"), 
                                            amount=request.POST.get(f"amount[{i}]"), ingredient=request.POST.get(f"ingredient[{i}]"))
                    # print(Ingredient.objects.all().last())
                    i += 1

                return HttpResponseRedirect(reverse("recipe", kwargs={"recipe_id": recipe.id}))
            else:
                return render(request, "recipes/new_recipe.html", status=406)
        
        return render(request, "recipes/new_recipe.html")
    else:
        return HttpResponseRedirect(reverse("login"))
    

def recipe(request, recipe_id):
    return render(request,"recipes/recipe.html", {
        "recipe_id": recipe_id,
    })