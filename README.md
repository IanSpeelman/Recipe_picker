# Ian Speelman's CS50Web Final Project 

## Distinctiveness and Complexity

Why is this project different and more complex than the projects we have had as assignments? This project uses many of the techniques required to build the previous projects but combines them in a more realistic way.

For example:
- **Frontend XHR Requests**: Used to add recipes to your watchlist without the need to reload the page.
- **DOM Manipulation**: Utilized in multiple parts of the website.

1. **Recipe Show Page: Changing the Serving Size**
    - Here, you can use a plus and minus button next to the indicator that shows for how many people this recipe is written. This button will re-calculate the needed amounts of the ingredients and update the ingredient list to reflect these changes.

2. **Recipe Create Page: Add Ingredients and Instructions Dynamically**
    - On the recipe create page, there is a single input field for ingredients and a single input field for instructions. If you want to add more, you can click the button below each field to add a new empty field so you can add as many ingredients or instructions as needed. If you have added too many fields, there will also be an "x" displayed to remove the fields that you don't need.

3. **Recipe Create Page: Drag and Drop**
    - Since instructions need to be in the correct order, it is very simple to re-arrange the order in which they will be displayed. You can drag and drop the items to change the order of the ingredients.

4. **Index: Filters**
    - On the index page, there is a box that contains filters relevant to recipes. Here you can filter recipes based on cuisine and category (e.g., main course, lunch, dessert). There is also a button to clear all the filters if you don't want them anymore. On mobile, this box will be hidden by default, and a button will be shown to hide/show the filter box.

The database is more complex than any of the projects we have had to do before. The reason is that each recipe is stored in a table, but the ingredients and instructions are stored in a different table. This allows for less data to be sent to the client while just looking at the recipes listed and only getting the information about ingredients and instructions when the user actually visits the show page for a recipe.

## Explanation of the Files

- **recipes/fixtures/**: Files in this folder are used to easily restore the database with some sample data, purely for ease of development.

- **recipes/scripts/addFavorites.js**: Responsible for adding a recipe to your favorites without reloading the page using an XHR request with JavaScript.

- **recipes/scripts/addFields.js**: Responsible for adding input fields on the create recipe page. This also ensures that instructions are drag-and-drop items. This file also ensures that the name tags in each input field are numbered correctly. For the backend, they need to be numbered like `instruction[0]`, `instruction[1]`, etc. Loading data on this page for editing will also get numbered appropriately by this file.

- **recipes/scripts/hamburger.js**: Responsible for making the navigation bar collapsible/expandable in mobile view.

- **recipes/scripts/changeServings.js**: Responsible for point 1 in the `Distinctiveness and Complexity` section.

- **recipes/scripts/filter.js**: Responsible for point 4 in the `Distinctiveness and Complexity` section.

- **recipes/templates/layout.html**: The basic layout of each page, including the navigation bar.

- **recipes/templates/index.html**: Lists all recipes created. If you are logged in, it shows a button where you can add a recipe to your favorites.

- **recipes/templates/register.html**: Form where you can register as a user.

- **recipes/templates/login.html**: Form where you can log in as a registered user.

- **recipes/templates/recipe.html**: Shows a single recipe with all information required to make it. If you are logged in, it shows a button where you can add a recipe to your favorites. It also shows an edit button if you are the creator of that recipe and if you are logged in.

- **recipes/templates/new_recipe.html**: Shows a form where you can create a new recipe, including the functions 2 and 3 described in `Distinctiveness and Complexity`. This form will also be loaded with data when you edit a form utilizing the functionality of renumbering the name fields described in `scripts/addFields.js` above.

- **recipes/tests/test_views.py**: Contains all the unit tests I have written for this project. It does not have full coverage but was meant to practice unit testing.

- **dockerfile**: The Dockerfile used to practice with Docker.

- **.github/workflows/UnitTesting.yml**: Adds testing to the GitHub workflow, also for practicing purposes.

## Running This Application

1. `python manage.py makemigrations`
2. `python manage.py migrate`
3. If you want some sample data, you can also run (**recipes.json** first the rest of the order does not matter):
    1.  `python manage.py loaddata recipes/fixtures/recipes.json`
    2.  `python manage.py loaddata recipes/fixtures/ingredients.json`
    3.  `python manage.py loaddata recipes/fixtures/instructions.json`
4. `python manage.py runserver`
