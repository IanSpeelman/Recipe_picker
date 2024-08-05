document.addEventListener("DOMContentLoaded", () => {
    // get required elements
    const recipes = document.querySelectorAll(".recipe")
    const checkbox = document.querySelectorAll("input[type=checkbox]")
    const cuisine_form = document.querySelector("#cuisine-form")
    const cuisine = document.querySelector("#cuisine")
    const cuisine_tags = document.querySelector("#cuisine-tags")
    const clear_filter = document.querySelector("#clear-filter")
    const colapse_btn = document.querySelector(".colapse-btn")
    const filters = document.querySelector(".filters")
    
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
    cuisine_form.addEventListener("submit", e => {
        e.preventDefault()
        const tag = document.createElement("span")
        const i = document.createElement("i")
        tag.classList.add("tag", "is-white", "is-rounded")
        i.classList.add("fa-sharp", "fa-solid", "fa-xmark", "ml", "cuisine-remove")
        tag.innerText = cuisine.value.charAt(0).toUpperCase() + cuisine.value.slice(1);
        cuisines.push(cuisine.value.charAt(0).toUpperCase() + cuisine.value.slice(1))
        tag.append(i)
        cuisine_tags.append(tag)
        cuisine.value = ""
        filterRecipes()
    })
    
    //check if the user tries to remove a cuisine tag
    cuisine_tags.addEventListener("click", e => {
        if(e.target.matches(".cuisine-remove")){
            cuisines.splice(cuisines.indexOf(e.target.parentElement.innerText),1)
            e.target.parentElement.remove()
            filterRecipes()
        }
    })
    
    //filter based on tags or checkboxes
    function filterRecipes() {
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

    clear_filter.addEventListener("click", e => {
        categories = []
        cuisines = []
        filterRecipes()
        while (cuisine_tags.children.length > 0) {
            cuisine_tags.children[0].remove()
        }
        for (box of checkbox) {
            box.checked = false
        }

    })
    

    colapse_btn.addEventListener("click", e => {
        console.log("click") 
        filters.classList.toggle("colapsed")
    })



    
    
    
    
})