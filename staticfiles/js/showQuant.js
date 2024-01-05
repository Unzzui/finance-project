// Quants

function showQuantAnalysis() {
	document.getElementById("quantSection").style.display = "block";

	// Llama a la función para renderizar los gráficos con los datos actuales
	// Al cargar la página, verifica si el toggle estaba activo la última vez
	if (localStorage.getItem("toggleActive") === "true") {
		toggle.classList.add("active");
		body.classList.add("active");
	}

	// Renderiza los gráficos de acuerdo al estado del toggle
	renderQuantCharts(priceData, cumulativeData);

	toggle.onclick = function () {
		toggle.classList.toggle("active");
		body.classList.toggle("active");

		// Al hacer clic en el toggle, guarda su estado actual en localStorage
		localStorage.setItem("toggleActive", toggle.classList.contains("active"));

		// Vuelve a renderizar los gráficos
		renderQuantCharts(priceData, cumulativeData);
	};
	// Cambia el título y resalta el botón
	document.getElementById("pageTitle").textContent =
		"Quant Analysis for " + selectedTicker;
	document
		.querySelectorAll(".btn")
		.forEach((btn) => btn.classList.remove("active"));
	document.querySelector(".btn:nth-child(1)").classList.add("active");
}
function highlightButton(section) {
	const buttons = document.querySelectorAll(".custom-button"); // Selecciona todos los botones personalizados
	buttons.forEach((button) => {
		if (button.getAttribute("onclick").includes(section)) {
			button.classList.add("active"); // Resalta el botón de la sección seleccionada
		} else {
			button.classList.remove("active"); // Quita el resaltado de los otros botones
		}
	});
}
function changeSection(section) {
	currentSection = section;
	// Cambia la sección actual
	highlightButton(section);
	submitForm(); // Envía el formulario
	// Resalta el botón correspondiente
}

function highlightButton(section) {
	const buttons = document.querySelectorAll(".custom-button"); // Selecciona todos los botones personalizados
	buttons.forEach((button) => {
		if (button.getAttribute("onclick").includes(section)) {
			button.classList.add("active"); // Resalta el botón de la sección seleccionada
		} else {
			button.classList.remove("active"); // Quita el resaltado de los otros botones
		}
	});
}

// Llama a la función para mostrar Fundamentals Ratios por defecto
showQuantAnalysis();

// Función para enviar el formulario al seleccionar un ticker
function submitForm() {
	var selectedTicker = document.getElementById("ticker").value; // Obtiene el ticker seleccionado
	var url = "";
	if (currentSection === "fundamentals") {
		url = "/fundamentals/?ticker=" + selectedTicker;
	} else {
		url = "/quant-analysis/?ticker=" + selectedTicker;
	}

	window.location.href = url;
}
highlightButton(currentSection);
