from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
import subprocess
import json
import time

from .models import Recipe, Ingredient, Instruction, Favorites

# Create your views here.
def index(request):
    recipes = Recipe.objects.all()
    if request.user.is_authenticated:
        results = Favorites.objects.filter(user=request.user, recipe__in=recipes)
        favorites = []
        for result in results:
            favorites.append(result.recipe)
    else:
        favorites = False
    return render(request, "recipes/index.html", {
        "recipes": recipes,
        "favorites": favorites,
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

            convert = {
                "grams": 1,
                "oz": round(28.35),
                "lb": round(453.59),
                "st": round(6350),
                "milliliters": 1,
                "cup": round(240),
                "floz": round(30),
                "tsp": round(5),
                "tbs": round(15),
                "units": 1,
            }
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
                    if request.POST.get(f"unit[{i}]") in ["grams", "oz", "lb", "st"]:
                        unit = "grams"
                    elif request.POST.get(f"unit[{i}]") in ["milliliters", "cup", "floz", "tsp", "tbs"]:
                        unit = "milliliters"
                    else:
                        unit = "units"
                    amount = int(request.POST.get(f"amount[{i}]")) * convert[request.POST.get(f"unit[{i}]")]
                    Ingredient.objects.create(recipe=recipe, unit=unit, 
                                            amount=amount, ingredient=request.POST.get(f"ingredient[{i}]"))
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
        try:
            favorite = Favorites.objects.get(user=request.user, recipe=recipe)
        except:
            favorite = False
        ingredients = Ingredient.objects.filter(recipe=recipe)
        instructions = Instruction.objects.filter(recipe=recipe)
        return render(request,"recipes/recipe.html", {
            "recipe": recipe,
            "instructions": instructions,
            "ingredients": ingredients,
            "favorite":favorite,
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

def addfavorites(request, recipe_id):
    if request.method == "POST":
        return HttpResponse(status=405)
    
    if request.user.is_authenticated:
        recipe = Recipe.objects.get(pk=recipe_id)
        user = request.user
        try:
            Favorites.objects.get(user=user, recipe=recipe).delete()
            return HttpResponse(json.dumps({"status": 200, "message": "favorites removed", "recipe": recipe.id}), status=200, content_type="application/json")
        except:
            Favorites.objects.create(user=user, recipe=recipe)
            return HttpResponse(json.dumps({"status": 200, "message": "favorites added", "recipe": recipe.id}), status=200, content_type="application/json")
    else:
        return HttpResponse(json.dumps({"status": 401, "message": "Not logged in!"}), status=401, content_type="application/json")
        
def favorites(request):
    if request.method == "POST":
        return HttpResponseRedirect(reverse("favorites"))
    
    if request.user.is_authenticated:
        results = Favorites.objects.filter(user=request.user)
        recipes = []
        for result in results:
            recipes.append(result.recipe)
        return render(request, "recipes/index.html", {
            "recipes": recipes,
            "favorites": recipes,
        })
    else:
        return HttpResponseRedirect(reverse("login"))
    

def editRecipe(request, recipe_id):
    recipe = Recipe.objects.get(pk=recipe_id)
    if request.user == recipe.creator:

        if request.method == "POST":

            convert = {
                "grams": 1,
                "oz": round(28.35),
                "lb": round(453.59),
                "st": round(6350),
                "milliliters": 1,
                "cup": round(240),
                "floz": round(30),
                "tsp": round(5),
                "tbs": round(15),
                "units": 1,
            }
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
                
                recipe.title=title
                recipe.description=description
                recipe.servings=servings
                recipe.cuisine=cuisine
                recipe.cooking_time=cooking_time
                recipe.preperation_time=preperation_time
                recipe.category=category
                recipe.image_url=image_url
                recipe.save()
                # get every ingredient and instruction that is added to the recipe and store them in a list
                i = 0
                instructions = Instruction.objects.filter(recipe=recipe).order_by("instruction_number")
                while bool(request.POST.get(f"instruction[{i}]")):
                    try:
                        instruction = instructions[i]
                        instruction.recipe=recipe
                        instruction.instruction_number=i+1
                        instruction.instruction=request.POST.get(f"instruction[{i}]")
                        instruction.save()
                    except:
                        Instruction.objects.create(recipe=recipe, instruction_number=i+1, instruction=request.POST.get(f"instruction[{i}]"))
                    i += 1
                if len(instructions) > i:
                    for c in range(i, len(instructions)):
                        instruction = instructions[c]
                        instruction.delete()
                i = 0
                ingredients = Ingredient.objects.filter(recipe=recipe)
                while bool(request.POST.get(f"ingredient[{i}]")):
                    if request.POST.get(f"unit[{i}]") in ["grams", "oz", "lb", "st"]:
                        unit = "grams"
                    elif request.POST.get(f"unit[{i}]") in ["milliliters", "cup", "floz", "tsp", "tbs"]:
                        unit = "milliliters"
                    else:
                        unit = "units"
                    amount = int(request.POST.get(f"amount[{i}]")) * convert[request.POST.get(f"unit[{i}]")]

                    try:
                        ingredient = ingredients[i]
                        ingredient.recipe=recipe
                        ingredient.unit=unit
                        ingredient.amount=amount
                        ingredient.ingredient=request.POST.get(f"ingredient[{i}]")
                        ingredient.save()
                    except:
                        Ingredient.objects.create(recipe=recipe, unit=unit, 
                                            amount=amount, ingredient=request.POST.get(f"ingredient[{i}]"))
                    i += 1
                if len(ingredients) > i:
                    for c in range(i, len(ingredients)):
                        ingredient = ingredients[c]
                        ingredient.delete()







            return HttpResponseRedirect(reverse("recipe", kwargs={"recipe_id": recipe_id}))
















        ingredients = Ingredient.objects.filter(recipe=recipe)
        instructions = Instruction.objects.filter(recipe=recipe)
        return render(request, "recipes/new_recipe.html", {
            "action": "edit",
            "recipe": recipe,
            "ingredients": ingredients,
            "instructions": instructions
        })
    else:
        return HttpResponseRedirect(reverse("index"))

def loadfixtures(request):
    subprocess.Popen('python manage.py loaddata recipes/fixtures/recipes.json', shell=True)
    time.sleep(1)
    subprocess.Popen('python manage.py loaddata recipes/fixtures/ingredients.json', shell=True)
    time.sleep(1)
    subprocess.Popen('python manage.py loaddata recipes/fixtures/instructions.json', shell=True)
    return HttpResponseRedirect(reverse("index"))