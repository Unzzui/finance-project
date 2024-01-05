const body = document.querySelector("body");
const toggle = document.getElementById("toggle");

// Al cargar la página, verifica si el toggle estaba activo la última vez
var isDarkMode = localStorage.getItem("toggleActive") === "true";
if (isDarkMode) {
	toggle.classList.add("active");
	body.classList.add("active");
}

toggle.onclick = function () {
	toggle.classList.toggle("active");
	body.classList.toggle("active");

	// Al hacer clic en el toggle, guarda su estado actual en localStorage
	localStorage.setItem("toggleActive", toggle.classList.contains("active"));
};

// Escucha los cambios en prefers-color-scheme
window
	.matchMedia("(prefers-color-scheme: dark)")
	.addEventListener("change", (e) => {
		var newColorScheme = e.matches ? "dark" : "light";

		// Si el nuevo esquema de colores es oscuro y el toggle no está activo, activa el toggle
		if (newColorScheme === "dark" && !toggle.classList.contains("active")) {
			toggle.classList.add("active");
			body.classList.add("active");
			localStorage.setItem("toggleActive", true);
		}
		// Si el nuevo esquema de colores es claro y el toggle está activo, desactiva el toggle
		else if (
			newColorScheme === "light" &&
			toggle.classList.contains("active")
		) {
			toggle.classList.remove("active");
			body.classList.remove("active");
			localStorage.setItem("toggleActive", false);
		}
	});
