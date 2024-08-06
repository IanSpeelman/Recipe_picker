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

    def gramToOunce(self):
        return f"{self.amount}g is equal to {round(self.amount * 0.0353, 2)}oz (Ounce)"

    def gramToPound(self):
        return f"{self.amount}g is equal to {round(self.amount * 0.0022, 2)}lb (Pound)"

    def gramToStone(self):
        return f"{self.amount}g is equal to {round(self.amount * 0.000157, 2)}st (Stone)"

    def milliliterToFluidOunce(self):
        return f"{self.amount}ml is equal to {round(self.amount * 0.0338, 2)}fl oz (Fluid ounce)"

    def milliliterToCups(self):
        return f"{self.amount}ml is equal to {round(self.amount * 0.0042, 2)}cups"

    def milliliterToTableSpoon(self):
        return f"{self.amount}ml is equal to {round(self.amount * 0.06762, 2)}tbs (Tablespoon)"

    def milliliterToTeaSpoon(self):
        return f"{self.amount}ml is equal to {round(self.amount * 0.2028, 2)}tsp (Teaspoon)"

    

class Favorites(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)