// financial_charts.js
function initChartPercentage(chartDivId, data, title) {
	var chartDom = document.getElementById(chartDivId);
	var myChart = echarts.init(chartDom);
	var option;

	option = {
		title: {
			text: title,
			left: "center",
			textStyle: {
				color: "white",
				fontSize: 18,
				fontWeight: "bold",
			},
		},
		tooltip: {
			trigger: "axis",
			axisPointer: {
				type: "cross",
				label: {
					backgroundColor: "#6a7985",
				},
			},
			formatter: function (params) {
				return params
					.map((param) => {
						const value = param.value.toFixed(2); // Assuming value is a number
						return `${param.axisValueLabel}: ${value}%`;
					})
					.join("<br/>");
			},
		},
		toolbox: {
			feature: {
				saveAsImage: {}, // Permite a los usuarios guardar el gráfico
				magicType: { type: ["line", "bar"] }, // Cambiar entre tipos de gráfico
				// ... otras herramientas ...
			},
		},
		grid: {
			left: "3%",
			right: "4%",
			bottom: "3%",
			containLabel: true,
		},
		xAxis: {
			type: "category",
			boundaryGap: false,
			data: Object.keys(data),
			axisLine: {
				lineStyle: {
					color: "white",
				},
			},
		},
		yAxis: {
			type: "value",
			axisLabel: {
				formatter: "{value}%",
				textStyle: {
					color: "white",
				},
			},
			axisLine: {
				lineStyle: {
					color: "white",
				},
			},
			splitLine: {
				lineStyle: {
					type: "dashed",
					color: "#ddd",
				},
			},
		},
		series: [
			{
				data: Object.values(data).map((value) => parseFloat(value.toFixed(2))),
				type: "line",
				smooth: true,
				symbol: "circle",
				symbolSize: 8,
				lineStyle: {
					width: 3,
				},
				itemStyle: {
					color: "#007bff",
					borderColor: "#fff",
					borderWidth: 2,
				},
				areaStyle: {
					color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
						{
							offset: 0,
							color: "rgba(0, 123, 255, 0.5)",
						},
						{
							offset: 1,
							color: "rgba(0, 123, 255, 0.2)",
						},
					]),
				},
			},
		],
	};

	option && myChart.setOption(option);
}

function initChartNumber(chartDivId, data, title) {
	var chartDom = document.getElementById(chartDivId);
	var myChart = echarts.init(chartDom);
	var option;

	option = {
		title: {
			text: title,
			left: "center",
			textStyle: {
				color: "white",
				fontSize: 18,
				fontWeight: "bold",
			},
		},
		tooltip: {
			trigger: "axis",
			axisPointer: {
				type: "cross",
				label: {
					backgroundColor: "#6a7985",
				},
			},
		},
		toolbox: {
			feature: {
				saveAsImage: {}, // Permite a los usuarios guardar el gráfico
				magicType: { type: ["line", "bar"] }, // Cambiar entre tipos de gráfico
				// ... otras herramientas ...
			},
		},
		grid: {
			left: "3%",
			right: "4%",
			bottom: "3%",
			containLabel: true,
		},
		xAxis: {
			type: "category",
			boundaryGap: false,
			data: Object.keys(data),
			axisLine: {
				lineStyle: {
					color: "white",
				},
			},
		},
		yAxis: {
			type: "value",
			axisLabel: {
				formatter: "{value}",
				textStyle: {
					color: "white",
				},
			},
			axisLine: {
				lineStyle: {
					color: "white",
				},
			},
			splitLine: {
				lineStyle: {
					type: "dashed",
					color: "#ddd",
				},
			},
		},
		series: [
			{
				data: Object.values(data).map((value) => parseFloat(value.toFixed(2))),
				type: "line",
				smooth: true,
				symbol: "circle",
				symbolSize: 8,
				lineStyle: {
					width: 3,
				},
				itemStyle: {
					color: "#007bff",
					borderColor: "#fff",
					borderWidth: 2,
				},
				areaStyle: {
					color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
						{
							offset: 0,
							color: "rgba(0, 123, 255, 0.5)",
						},
						{
							offset: 1,
							color: "rgba(0, 123, 255, 0.2)",
						},
					]),
				},
			},
		],
	};

	option && myChart.setOption(option);
}

function initChartMoney(chartDivId, data, title) {
	var chartDom = document.getElementById(chartDivId);
	var myChart = echarts.init(chartDom);
	var option;
	var ticker = document.getElementById("ticker").value; // Obtiene el ticker seleccionado

	function currencyFormatter(value) {
		// Format as currency (e.g., 1,234,567$)
		return value.toLocaleString("en-US", { maximumFractionDigits: 2 }) + "$";
	}

	option = {
		title: {
			text: title,
			left: "center",
			textStyle: {
				color: "white",
				fontSize: 18,
				fontWeight: "bold",
			},
		},
		tooltip: {
			trigger: "axis",
			formatter: function (params) {
				return params
					.map(
						(param) =>
							`${param.axisValueLabel}: ${currencyFormatter(param.data)}`
					)
					.join("<br/>");
			},
			axisPointer: {
				type: "cross",
				label: {
					backgroundColor: "#6a7985",
				},
			},
		},
		toolbox: {
			feature: {
				saveAsImage: {}, // Permite a los usuarios guardar el gráfico
				magicType: { type: ["line", "bar"] }, // Cambiar entre tipos de gráfico
				// ... otras herramientas ...
			},
		},
		grid: {
			left: "3%",
			right: "4%",
			bottom: "3%",
			containLabel: true,
		},
		xAxis: {
			type: "category",
			boundaryGap: false,
			data: Object.keys(data),
			axisLine: {
				lineStyle: {
					color: "white",
				},
			},
		},
		yAxis: {
			type: "value",
			axisLabel: {
				formatter: "{value}$",
				textStyle: {
					color: "white",
				},
			},
			axisLine: {
				lineStyle: {
					color: "white",
				},
			},
			splitLine: {
				lineStyle: {
					type: "dashed",
					color: "#ddd",
				},
			},
		},
		series: [
			{
				name: ticker, // Nombre del "ticker" para la leyenda
				data: Object.values(data).map((value) => parseFloat(value.toFixed(2))),
				type: "line",
				smooth: true,
				symbol: "circle",
				symbolSize: 8,
				lineStyle: {
					width: 3,
				},
				itemStyle: {
					color: "#007bff",
					borderColor: "#fff",
					borderWidth: 2,
				},
				areaStyle: {
					color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
						{
							offset: 0,
							color: "rgba(0, 123, 255, 0.5)",
						},
						{
							offset: 1,
							color: "rgba(0, 123, 255, 0.2)",
						},
					]),
				},
			},
		],
	};

	option && myChart.setOption(option) && myChart.resize();
}

function stockPriceChart(chartDivId, data, title) {
	var chartDom = document.getElementById(chartDivId);
	var myChart = echarts.init(chartDom);
	var option;
	var ticker = document.getElementById("ticker").value; // Obtiene el ticker seleccionado

	function currencyFormatter(value) {
		// Format as currency (e.g., 1,234,567$)
		return value.toLocaleString("en-US", { maximumFractionDigits: 2 }) + "$";
	}

	option = {
		title: {
			text: title + ticker,
			left: "center",
			textStyle: {
				color: "#white",
				fontSize: 18,
				fontWeight: "bold",
			},
		},

		tooltip: {
			trigger: "axis",
			formatter: function (params) {
				return params
					.map(
						(param) =>
							`${param.axisValueLabel}: ${currencyFormatter(param.data)}`
					)
					.join("<br/>");
			},
			axisPointer: {
				type: "cross",
				label: {
					backgroundColor: "#6a7985",
				},
			},
		},
		toolbox: {
			feature: {
				saveAsImage: {}, // Permite a los usuarios guardar el gráfico
				magicType: { type: ["line"] }, // Cambiar entre tipos de gráfico
				// ... otras herramientas ...
			},
		},
		grid: {
			left: "3%",
			right: "4%",
			bottom: "3%",
			containLabel: true,
		},
		xAxis: {
			type: "category",
			boundaryGap: false,
			data: Object.keys(data),
			axisLine: {
				lineStyle: {
					color: "white",
				},
			},
		},
		yAxis: {
			type: "value",
			axisLabel: {
				formatter: "{value}$",
				textStyle: {
					color: "white",
				},
			},
			axisLine: {
				lineStyle: {
					color: "white",
				},
			},
			splitLine: {
				lineStyle: {
					type: "dashed",
					color: "#ddd",
				},
			},
		},
		series: [
			{
				name: ticker, // Nombre del "ticker" para la leyenda
				data: Object.values(data).map((value) => parseFloat(value.toFixed(2))),
				type: "line",
				smooth: true,
				symbol: "circle",
				symbolSize: 8,
				lineStyle: {
					width: 3,
				},
				itemStyle: {
					color: "#007bff",
					borderColor: "#fff",
					borderWidth: 2,
				},
				areaStyle: {
					color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
						{
							offset: 0,
							color: "rgba(0, 123, 255, 0.5)",
						},
						{
							offset: 1,
							color: "rgba(0, 123, 255, 0.2)",
						},
					]),
				},
			},
		],
	};

	option && myChart.setOption(option) && myChart.resize();
}
function renderCharts(
	revenueData,
	grossMarginData,
	operatingMarginData,
	profitMarginData,
	roeData,
	roaData,
	roicData,
	fcfData,
	qrData
) {
	// Verifica cada conjunto de datos antes de renderizar su gráfico correspondiente
	if (revenueData && Object.keys(revenueData).length > 0) {
		initChartMoney("revenueChart", revenueData, "Revenue");
	}
	if (grossMarginData && Object.keys(grossMarginData).length > 0) {
		initChartPercentage("grossMarginChart", grossMarginData, "Gross Margin");
	}
	if (operatingMarginData && Object.keys(operatingMarginData).length > 0) {
		initChartPercentage(
			"operatingMarginChart",
			operatingMarginData,
			"Operating Margin"
		);
	}
	if (profitMarginData && Object.keys(profitMarginData).length > 0) {
		initChartPercentage("profitMarginChart", profitMarginData, "Profit Margin");
	}

	if (roeData && Object.keys(roeData).length > 0) {
		initChartPercentage("roeChart", roeData, "ROE");
	}
	if (roaData && Object.keys(roaData).length > 0) {
		initChartPercentage("roaChart", roaData, "ROA");
	}
	if (roicData && Object.keys(roicData).length > 0) {
		initChartPercentage("roicChart", roicData, "ROIC");
	}
	if (fcfData && Object.keys(fcfData).length > 0) {
		initChartMoney("fcfChart", fcfData, "Free Cash Flow");
	}
	// Solo crea el gráfico Quick Ratio si qrData no está vacío
	if (qrData && Object.keys(qrData).length > 0) {
		initChartNumber("qrChart", qrData, "Quick Ratio");
	} else {
		// Oculta el contenedor del gráfico Quick Ratio si qrData está vacío
		document.getElementById("qrChart").style.display = "none";
	}
}

function renderQuantCharts(priceData, cumulativeData) {
	// Verifica cada conjunto de datos antes de renderizar su gráfico correspondiente
	if (priceData && Object.keys(priceData).length > 0) {
		stockPriceChart("priceChart", priceData, "Daily Stock Closing Price - ");
	} else {
		console.error("Error: Missing data for price chart.");
		document.getElementById("priceChart").style.display = "none";
	}
	if (cumulativeData && Object.keys(cumulativeData).length > 0) {
		initChartPercentage(
			"cumulativeChart",
			cumulativeData,
			"Cumulative Returns"
		);
	} else {
		console.error("Error: Missing data for cumulative returns chart.");
		document.getElementById("cumulativeChart").style.display = "none";
	}
}
