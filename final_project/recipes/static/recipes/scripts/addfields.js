document.addEventListener("DOMContentLoaded", () => {
	let dragAndDrop = document.querySelectorAll(".drag-and-drop");
	const newIngredient = document.querySelector("#new-ingredient");
	const newInstruction = document.querySelector("#new-instruction");
	const ingredientList = document.querySelector("#ingredient-list");
	const instructionList = document.querySelector("#instruction-list");
	let instructions = 1;
	let ingredients = 1;
	newInstruction.addEventListener("click", (e) => {
		e.preventDefault();
		let div = document.createElement("div");
		div.classList.add("field", "drag-and-drop");
		div.setAttribute("draggable", "true"); //! testing
		let input = document.createElement("input");
		input.classList.add("input");
		// input.setAttribute("draggable", "true"); //! testing
		input.setAttribute("type", "text");
		input.setAttribute("name", `instruction[${instructions}]`);
		input.setAttribute("aria-label", "instruction");
		input.setAttribute("placeholder", "Instruction");
		input.setAttribute("autocomplete", "off");
		div.append(input);
		instructionList.append(div);
		instructions++;
		// drag and drop functionality
		let items = document.querySelectorAll(".drag-and-drop");
		let container = document.querySelector("#instruction-list");

		function dragstart(e) {
			e.target.classList.add("dragging");
		}
		function dragend(e) {
			e.target.classList.remove("dragging");
			let items = document.querySelector("#instruction-list").children;
			items = [...items];

			let c = 0;
			for (item of items) {
				item.setAttribute("name", `instruction[${c}]`);
				c++;
			}
		}
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
		//end drag and drop functionality
	});
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
		e.preventDefault();
		let field = document.createElement("div");
		field.setAttribute("class", "field has-addons");
		let control = document.createElement("div");
		control.classList.add("control");
		let selectDiv = document.createElement("div");
		selectDiv.classList.add("select");
		let select = document.createElement("select");
		select.setAttribute("name", `unit[${ingredients}]`);
		for (option of options) {
			let selectOption = document.createElement("option");
			selectOption.setAttribute("value", option.short);
			selectOption.innerText = option.unit;
			select.append(selectOption);
		}
		selectDiv.append(select);
		control.append(selectDiv);
		field.append(control);
		control = document.createElement("div");
		control.classList.add("control");
		let input = document.createElement("input");
		input.setAttribute("type", "number");
		input.setAttribute("class", "input");
		input.setAttribute("name", `amount[${ingredients}]`);
		input.setAttribute("aria-label", "amount");
		input.setAttribute("placeholder", "Amount");
		input.setAttribute("autocomplete", "off");
		control.append(input);
		field.append(control);
		control = document.createElement("div");
		control.classList.add("control");
		input = document.createElement("input");
		input.setAttribute("type", "text");
		input.setAttribute("class", "input");
		input.setAttribute("name", `ingredient[${ingredients}]`);
		input.setAttribute("aria-label", "ingredient");
		input.setAttribute("placeholder", "Ingredient");
		input.setAttribute("autocomplete", "off");
		control.append(input);
		field.append(control);
		ingredientList.append(field);
		ingredients++;
	});
});
