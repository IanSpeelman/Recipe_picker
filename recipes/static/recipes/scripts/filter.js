document.addEventListener("DOMContentLoaded", () => {
    const recipes = document.querySelectorAll(".recipe")
    const checkbox = document.querySelectorAll("input[type=checkbox]")
    let categories = []

    checkbox.forEach(check => {
        check.addEventListener("input", e => {
            if (e.target.checked){
                categories.push(e.target.value)
                console.log(categories)
            }
            else{
                categories.splice(categories.indexOf(e.target.value),1)
                console.log(categories)
            }
            filterRecipes()
        })
    });


    function filterRecipes() {
        if (categories.length === 0){
            for (recipe of recipes){
                recipe.classList.remove("none")
            }
        }
        else{
            for (recipe of recipes){
                if(categories.indexOf(recipe.dataset.category) === -1){
                    recipe.classList.add("none")
                }
                else{
                    recipe.classList.remove("none")
                }
            }
        }
    }
})