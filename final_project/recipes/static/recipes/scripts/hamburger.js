document.addEventListener("DOMContentLoaded", () => {
	nav = document.querySelector("nav");
	hamburger = document.querySelector(".hamburger");
	hamburger.addEventListener("click", () => {
		nav.classList.toggle("collapse");
	});
});
