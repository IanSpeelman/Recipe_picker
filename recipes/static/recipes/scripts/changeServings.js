document.addEventListener("DOMContentLoaded", () => {
    const minus = document.querySelector("#add-serving")
    const plus = document.querySelector("#remove-serving")
    const servings = document.querySelector("#servings")

    minus.addEventListener("click", () => {
        if(parseInt(servings.innerText) !== 1){
            changeAmounts("remove", parseInt(servings.innerText))
            servings.innerText = parseInt(servings.innerText) - 1
        }
    })
    plus.addEventListener("click", () => {
        changeAmounts("add", parseInt(servings.innerText))
        servings.innerText = parseInt(servings.innerText) + 1
    })


    function changeAmounts(operation,servings){
        const items = document.querySelectorAll(".amount")

        for (item of items){       

            if (operation === "add"){
                item.innerText = Math.round((parseInt(item.innerText) / servings) * (servings + 1))
            }
            else if (operation === "remove"){
                item.innerText = Math.round((parseInt(item.innerText) / servings) * (servings - 1))
            }
        }
    }
})