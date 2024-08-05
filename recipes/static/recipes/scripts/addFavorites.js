document.addEventListener("DOMContentLoaded", e => {
    const recipes = document.querySelectorAll(".recipe")
    const recipe_item = document.querySelector(".recipe-view")
    if (recipes.length){
        for (recipe of recipes){
            recipe.addEventListener("click", e => {
                if (e.target.classList.contains("favorites")){
                    e.preventDefault()
                    const url = `/recipes/favorites/${e.currentTarget.dataset.recipe}`
                    fetch(url)
                    .then(response => response.json())
                    .then(response => {
                        const recipe = document.querySelector(`.recipe[data-recipe='${response.recipe}']`)
                        recipe.children[0].children[0].children[1].children[0].children[1].children[0].classList.toggle("hidden")
                        recipe.children[0].children[0].children[1].children[0].children[1].children[1].classList.toggle("hidden")
                    })
                    .catch(err => console.log("oops, not logged in!"))
    
                }
            })
        }
    }    
    else{
        recipe_item.addEventListener("click", e => {
            if (e.target.classList.contains("favorites")){

                const url = `/recipes/favorites/${e.currentTarget.dataset.recipe}`
                fetch(url)
                .then(response => response.json())
                .then(response => {
                    for (item of document.querySelectorAll(".favorites"))
                        item.classList.toggle("hidden")
                })
                .catch(err => console.log("oops, not logged in!"))
            }
    })
    }
})