document.addEventListener("DOMContentLoaded", () => {
    // get required elements
    const recipes = document.querySelectorAll(".recipe")
    const checkbox = document.querySelectorAll("input[type=checkbox]")
    const form = document.querySelector("#form")
    const cuisine = document.querySelector("#cuisine")
    const tags = document.querySelector(".tags")
    let categories = []
    let cuisines = []
    
    //check the state of the checkboxes
    checkbox.forEach(check => {
        check.addEventListener("input", e => {
            if (e.target.checked){
                categories.push(e.target.value)
            }
            else{
                categories.splice(categories.indexOf(e.target.value),1)
            }
            filterRecipes()
        })
    });
    
    // check for form inputs to add cuisine tag
    form.addEventListener("submit", e => {
        e.preventDefault()
        const tag = document.createElement("span")
        const i = document.createElement("i")
        tag.classList.add("tag")
        i.classList.add("fa-sharp", "fa-solid", "fa-xmark", "ml", "cuisine-remove")
        tag.innerText = cuisine.value
        cuisines.push(cuisine.value)
        tag.append(i)
        tags.append(tag)
        cuisine.value = ""
        filterRecipes()
    })
    
    //check if the user tries to remove a cuisine tag
    tags.addEventListener("click", e => {
        if(e.target.matches(".cuisine-remove")){
            cuisines.splice(cuisines.indexOf(e.target.parentElement.innerText),1)
            e.target.parentElement.remove()
            filterRecipes()
        }
    })
    
    //filter based on tags or checkboxes
function filterRecipes() {
    console.log("categories", categories)
    console.log("cuisines", cuisines)
        for (recipe of recipes){
            recipe.classList.remove("none")
        }
        // restrict based on categorie checkboxes
        if (categories.length !== 0){
            for (recipe of recipes){
                if(categories.indexOf(recipe.dataset.category) === -1){
                    recipe.classList.add("none")
                }
            } 
        }
        //restrict based on cuisine tags
        if (cuisines.length !== 0){
            for (recipe of recipes){
                if(cuisines.indexOf(recipe.dataset.cuisine) === -1){
                    recipe.classList.add("none")
                }
            }
        }
    }

    






})