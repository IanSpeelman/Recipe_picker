from django.db import models
from django.contrib.auth.models import User



# Create your models here.
class Recipe(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    servings = models.IntegerField()
    cuisine = models.CharField(max_length=30)
    cooking_time = models.IntegerField()
    preperation_time = models.IntegerField()
    category = models.CharField(max_length=30)
    image_url = models.CharField(max_length=255)
    
class Instruction(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    instruction_number = models.IntegerField()    
    instruction = models.TextField()

class Ingredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    unit = models.CharField(max_length=15)
    amount = models.IntegerField()
    ingredient = models.CharField(max_length=100)