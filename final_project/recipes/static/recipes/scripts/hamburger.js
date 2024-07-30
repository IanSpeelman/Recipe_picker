document.addEventListener("DOMContentLoaded", () => {
	nav = document.querySelector("#nav-items");
	burger = document.querySelector("#burger-button");

	burger.addEventListener("click", () => {
		nav.classList.toggle("is-active");
		burger.classList.toggle("is-active");
	});
});
