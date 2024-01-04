function showFundamentals() {
	document.getElementById("charts-container").style.display = "block";

	// Asegúrate de que los datos existen antes de intentar renderizar los gráficos
	if (localStorage.getItem("toggleActive") === "true") {
		toggle.classList.add("active");
		body.classList.add("active");
	}
	renderCharts(
		revenueData,
		grossMarginData,
		operatingMarginData,
		profitMarginData,
		roeData,
		roaData,
		roicData,
		fcfData,
		qrData
	);
	toggle.onclick = function () {
		toggle.classList.toggle("active");
		body.classList.toggle("active");

		// Al hacer clic en el toggle, guarda su estado actual en localStorage
		localStorage.setItem("toggleActive", toggle.classList.contains("active"));
		renderCharts(
			revenueData,
			grossMarginData,
			operatingMarginData,
			profitMarginData,
			roeData,
			roaData,
			roicData,
			fcfData,
			qrData
		);
	};
	// Cambia el título y resalta el botón
	document.getElementById("pageTitle").textContent =
		"Fundamentals Ratios for " + selectedTicker;
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

// Llama a la función para mostrar Fundamentals Ratios por defecto
showFundamentals();

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
