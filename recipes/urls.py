from django.urls import path
from recipes import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login, name="login"),
    path("register", views.register, name="register"),
    path("logout", views.logout, name="logout"),
    path("recipe/new", views.new_recipe , name="newrecipe"),
    path("recipe/<int:recipe_id>", views.recipe , name="recipe"),
    path("search", views.search, name="search"),
    path("recipes/favorites", views.favorites, name="favorites"),
    path("recipes/favorites/<int:recipe_id>", views.addfavorites, name="addfavorites"),
]