document.addEventListener("DOMContentLoaded", () => {
	setDragAndDrop()
	setIngredientNumbering()
	setInstructionNumbering()
	let dragAndDrop = document.querySelectorAll(".drag-and-drop");
	const newIngredient = document.querySelector("#new-ingredient");
	const newInstruction = document.querySelector("#new-instruction");
	const ingredientList = document.querySelector("#ingredient-list");
	const instructionList = document.querySelector("#instruction-list");
	let instructions = 1;
	let ingredients = 1;
	newInstruction.addEventListener("click", (e) => {
		e.preventDefault();
		instructionModel = document.querySelector(".instruction-model");
		clone = instructionModel.cloneNode(true);
		clone.children[0].children[0].setAttribute(
			"name",
			`instruction[${instructions}]`,
		);
		clone.children[0].children[0].value = "";
		instructionList.append(clone);
		instructions++;
		
		setDragAndDrop()
		destroyListeners();
		setInstructionNumbering()
		
	});
	
	function setDragAndDrop() {
		let items = document.querySelectorAll(".drag-and-drop");
		let container = document.querySelector("#instruction-list");
		
		function dragstart(e) {
			e.target.classList.add("dragging");
		}
		function dragend(e) {
			e.target.classList.remove("dragging");
			let items = document.querySelector("#instruction-list").children;
			items = [...items];
			setInstructionNumbering()
			
		}
		setInstructionNumbering()
		
		function dragover(e) {
			e.preventDefault();
			let dragging = document.querySelector(".dragging");
			siblings = document.querySelectorAll(
				".drag-and-drop:not(.dragging)",
			);
			closestElement = [...siblings].reduce(
				(closest, sibling) => {
					let box = sibling.getBoundingClientRect();
					let offset = e.clientY - box.top - box.height / 2;
					if (offset < 0 && offset > closest.offset) {
						return { element: sibling, offset: offset };
					} else {
						return closest;
					}
				},
				{ offset: -Infinity },
			);
			if (closestElement.element !== undefined) {
				container.insertBefore(dragging, closestElement.element);
			} else {
				container.append(dragging);
			}
		}
		
		items.forEach((item) => (item.ondragstart = dragstart));
		items.forEach((item) => (item.ondragend = dragend));
		container.ondragover = dragover;
	}
	const options = [
		{ unit: "Grams", short: "g" },
		{ unit: "Kilograms", short: "kg" },
		{ unit: "Milliliters", short: "ml" },
		{ unit: "Liters", short: "L" },
		{ unit: "Pieces", short: "pcs" },
		{ unit: "Teaspoons", short: "tsp" },
		{ unit: "Tablespoons", short: "tbsp" },
	];
	newIngredient.addEventListener("click", (e) => {
		e.preventDefault()
		let ingredientModel = document.querySelector(".ingredient-model");
		let clone = ingredientModel.cloneNode(true);
		clone.children[1].children[0].value = "";
		clone.children[2].children[0].value = "";
		
		ingredientList.append(clone);
		setIngredientNumbering()
		destroyListeners();
	});
});

function destroyListeners() {
	let destroy = document.querySelectorAll(".destroy");
	for (button of destroy) {
		button.onclick = (e) => {
			const target = e.target.parentElement.parentElement;
			if (target.id !== "instruction-model" && document.querySelectorAll(".instruction-model").length > 1 ) {
				if(e.target.tagName == "I"){
					let target = e.target.parentElement.parentElement.parentElement 
					target.remove();
				}
				else{
					let target = e.target.parentElement.parentElement
					target.remove();
				}				let c = 0;
				
			} else if (target.id !== "ingredient-model" && document.querySelectorAll(".ingredient-model").length > 1 ) {
				if(e.target.tagName == "I"){
					let target = e.target.parentElement.parentElement.parentElement 
					target.remove();
				}
				else{
					let target = e.target.parentElement.parentElement
					target.remove();
				}
				
			}
			setIngredientNumbering()
			setInstructionNumbering()
		};
	}
}
function setIngredientNumbering(){
	const items = document.querySelectorAll(".ingredient-group")
	let c = 0
	for (item of items){
		item.children[0].children[0].children[0].setAttribute("name", `unit[${c}]`)
		item.children[1].children[0].setAttribute("name", `amount[${c}]`)
		item.children[2].children[0].setAttribute("name", `ingredient[${c}]`)
		c++
	}
}
function setInstructionNumbering(){
	let items = document.querySelectorAll(".drag-and-drop");
	let c = 0;
	for (item of items) {
		item.children[0].children[0].setAttribute(
			"name",
			`instruction[${c}]`,
		);
		c++;
	}
}
destroyListeners();
