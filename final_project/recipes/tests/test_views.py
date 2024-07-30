from django.test import  TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from ..models import Recipe, Ingredient, Instruction

import unittest

class test_index(TestCase):
    
    def test_index_GET(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)

class test_login(TestCase):
    def setUp(self):
        User.objects.create_user(username="test_user", password="password")

    def test_login_GET(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)

    def test_login_POST_correct_credentials(self):
        response = self.client.post(reverse("login"),{
            "username":"test_user",
            "password": "password"
        })
        self.assertEqual(response.status_code, 302)
        request = response.wsgi_request
        self.assertEqual(request.user.username, "test_user")

    def test_login_POST_incorrect_credentials(self):
        response = self.client.post(reverse("login"),{
            "username":"spielmiester",
            "password": "password"
        })
        self.assertEqual(response.status_code, 401)
        request = response.wsgi_request
        self.assertEqual(request.user.username, "")

    def test_login_POST_incomplete_credentials(self):
        response = self.client.post(reverse("login"),{
            "username":"test_user",
            "password": ""
        })
        self.assertEqual(response.status_code, 406)
        request = response.wsgi_request
        self.assertEqual(request.user.username, "")


class test_register(TestCase):

    def test_register_GET(self):
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)

    def test_register_POST_allowed_information(self):
        response = self.client.post(reverse("register"), {
            "username": "test_user",
            "email": "spielmeister@gmail.com",
            "email-confirmation": "spielmeister@gmail.com",
            "password": "password",
            "password-confirmation": "password",
        })
        request = response.wsgi_request
        self.assertEqual(request.user.username, "test_user")
        self.assertEqual(response.status_code, 302)

    def test_register_POST_missing_information(self):
        response = self.client.post(reverse("register"), {
            "username": "",
            "email": "spielmeister@gmail.com",
            "email-confirmation": "spielmeister@gmail.com",
            "password": "password",
            "password-confirmation": "password",
        })
        request = response.wsgi_request
        self.assertEqual(request.user.username, "")
        self.assertEqual(response.status_code, 406)

    def test_register_POST_passwords_no_match(self):
        response = self.client.post(reverse("register"), {
            "username": "test_user",
            "email": "spielmeister@gmail.com",
            "email-confirmation": "spielmeister@gmail.com",
            "password": "passwordd",
            "password-confirmation": "password",
        })
        request = response.wsgi_request
        self.assertEqual(request.user.username, "")
        self.assertEqual(response.status_code, 406)

    def test_register_POST_emails_no_match(self):
        response = self.client.post(reverse("register"), {
            "username": "test_user",
            "email": "spielmeister@gmial.com",
            "email-confirmation": "spielmeister@gmail.com",
            "password": "password",
            "password-confirmation": "password",
        })
        request = response.wsgi_request
        self.assertEqual(request.user.username, "")
        self.assertEqual(response.status_code, 406)

    # def test_register_POST_duplicate_user(self):
    #     response = self.client.post(reverse("register"), {
    #         "username": "test_user",
    #         "email": "spielmeister@gmail.com",
    #         "email-confirmation": "spielmeister@gmail.com",
    #         "password": "password",
    #         "password-confirmation": "password",
    #     })
    #     response = self.client.post(reverse("register"), {
    #         "username": "test_user",
    #         "email": "spielmeister@gmail.com",
    #         "email-confirmation": "spielmeister@gmail.com",
    #         "password": "password",
    #         "password-confirmation": "password",
    #     })
    #     self.assertEqual(response.status_code, 409)


class testNewRecipe(TestCase):
    def setUp(self):
        User.objects.create_user(username="test_user", password="password")
        self.client.login(username="test_user", password="password")
    
    def test_new_recipe_GET(self):
        response = self.client.get(reverse("newrecipe"))
        self.assertEqual(response.status_code, 200)

    def test_new_recipe_GET_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse("newrecipe"))
        self.assertEqual(response.status_code, 302)

    def test_new_recipe_POST(self):
        response = self.client.post(reverse("newrecipe"),{
            "title": "Chief Quality Orchestrator",
            "description": "Sit commodi est praesentium quo placeat a impedit.",
            "servings": "97",
            "cuisine": "Maxime eum id nemo.",
            "cooking-time": "207",
            "preperation-time": "265",
            "category": "Antigua and Barbuda",
            "image-url":"Doloremque deserunt recusandae repellat laborum non culpa.",
            "unit[0]": "g",
            "amount[0]": "651",
            "ingredient[0]":	"Numquam temporibus corporis.",
            "instruction[0]": "Recusandae ab hic deserunt reiciendis tenetur ab.",
        })
        recipe = Recipe.objects.all().last()
        instruction = Instruction.objects.filter(recipe=recipe).last()
        ingredient = Ingredient.objects.filter(recipe=recipe).last()
        self.assertEqual(recipe.title, "Chief Quality Orchestrator")
        self.assertEqual(instruction.instruction, "Recusandae ab hic deserunt reiciendis tenetur ab.")
        self.assertEqual(ingredient.ingredient, "Numquam temporibus corporis.")
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed("recipes/recipe.html")

    def test_new_recipe_POST_not_logged_in(self):
        self.client.logout()
        response = self.client.post(reverse("newrecipe"),{
            "title": "Chief Quality Orchestrator",
            "description": "Sit commodi est praesentium quo placeat a impedit.",
            "servings": "97",
            "cuisine": "Maxime eum id nemo.",
            "cooking-time": "207",
            "preperation-time": "265",
            "category": "Antigua and Barbuda",
            "image-url":"Doloremque deserunt recusandae repellat laborum non culpa.",
            "unit[0]": "g",
            "amount[0]": "651",
            "ingredient[0]":	"Numquam temporibus corporis.",
            "instruction[0]": "Recusandae ab hic deserunt reiciendis tenetur ab.",
        })
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed("recipes/login.html")

    def test_new_recipe_POST_requred_field_missing(self):
        response = self.client.post(reverse("newrecipe"),{
            "title": "Chief Quality Orchestrator",
            "description": "Sit commodi est praesentium quo placeat a impedit.",
            "servings": "97",
            "cuisine": "Maxime eum id nemo.",
            "category": "Antigua and Barbuda",
            "image-url":"Doloremque deserunt recusandae repellat laborum non culpa.",
            "unit[0]": "g",
            "amount[0]": "651",
            "ingredient[0]":	"Numquam temporibus corporis.",
            "instruction[0]": "Recusandae ab hic deserunt reiciendis tenetur ab.",
        })
        self.assertEqual(response.status_code, 406)
        self.assertTemplateUsed("recipes/new_recipe.html")

        