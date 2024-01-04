from django.shortcuts import render
from django.http import HttpResponse
from .utils import (
    calcular_roa,
    calcular_roe,
    calcular_roic,
    free_cash_flow,
    quick_ratio,
    calcular_margen_bruto,
    calcular_margen_operacional,
    calcular_margen_neto,
    revenue_data,
)
import json
import quantstats as qs
import pandas as pd
import yfinance as yf
from django.shortcuts import redirect
from django.utils.html import format_html
import os
from django.core.cache import cache
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler

# Create your views here.
base_dir = os.path.dirname(os.path.abspath(__file__))


def index(request):
    datos_financieros = load_financial_data()
    tickers = list(datos_financieros.keys())

    context = {
        "tickers": tickers,  # Asegúrate de tener esta línea en tu contexto
        # Otros datos que quieras pasar al template
    }
    return render(
        request,
        "finance_app/index.html",
        context,
    )


def redirect_to_analysis(request):
    ticker = request.GET.get("ticker")
    return redirect(f"/fundamentals/?ticker={ticker}")


def load_financial_data():
    file_path = os.path.join(base_dir, "data", "financial_statements.json")
    with open(file_path, "r") as file:
        datos_financieros = json.load(file)
    return datos_financieros


def price_data():
    datos_ticker = load_financial_data()
    tickers = list(datos_ticker.keys())
    try:
        all_returns = yf.download(tickers, period="10y")["Close"]
        all_returns_dict = {}
        for ticker in tickers:
            returns = all_returns[ticker]
            returns_dict = {
                date.strftime("%Y-%m-%d"): price for date, price in returns.items()
            }
            all_returns_dict[ticker] = returns_dict

        # Guarda all_returns_dict en un archivo JSON en la carpeta data
        with open(os.path.join(base_dir, "data", "all_returns.json"), "w") as f:
            json.dump(all_returns_dict, f)

    except Exception as e:
        return HttpResponse("Error al descargar los precios", status=500)


def get_prices(ticker_seleccionado):
    try:
        # Abre el archivo JSON y carga los datos
        with open(os.path.join(base_dir, "data", "all_returns.json"), "r") as f:
            all_returns_dict = json.load(f)

        # Busca los retornos para el ticker seleccionado
        returns_dict = all_returns_dict.get(ticker_seleccionado, {})

        # Convierte el diccionario de retornos en una cadena JSON
        returns = json.dumps(returns_dict)
    except Exception as e:
        # Manejar el error adecuadamente
        return HttpResponse("Error al leer los precios del archivo JSON.", status=500)

    return returns


def get_cumulative_returns(ticker_seleccionado):
    try:
        # Abre el archivo JSON y carga los datos
        with open(os.path.join(base_dir, "data", "all_returns.json"), "r") as f:
            all_returns_dict = json.load(f)

        # Busca los retornos para el ticker seleccionado
        returns_dict = all_returns_dict.get(ticker_seleccionado, {})

        # Convierte el diccionario de retornos en un DataFrame de pandas
        returns_df = pd.DataFrame(list(returns_dict.items()), columns=["Date", "Close"])
        returns_df["Date"] = pd.to_datetime(returns_df["Date"])
        returns_df.set_index("Date", inplace=True)
        returns_df.sort_index(inplace=True)

        # Calcula los retornos porcentuales
        returns_df["Return"] = returns_df["Close"].pct_change()

        # Calcula los retornos acumulativos
        cumulative_returns = qs.stats.compsum(returns_df["Return"])
        cumulative_returns.dropna(inplace=True)
        cumulative_returns_dict = {
            date.strftime("%Y-%m-%d"): cumlative * 100
            for date, cumlative in cumulative_returns.items()
        }
        cumulative_returns = json.dumps(cumulative_returns_dict)

        # Almacena los retornos acumulativos en el caché
        cache.set(f"{ticker_seleccionado}_cumulative_returns", cumulative_returns)

    except Exception as e:
        return HttpResponse("Error al leer los precios del archivo JSON.", status=500)

    return cumulative_returns


def fundamentals_view(request):
    # Load financial data
    datos_financieros = load_financial_data()
    # List of available tickers
    tickers = list(datos_financieros.keys())

    # Get selected ticker from the request
    ticker_seleccionado = request.GET.get("ticker")
    ticker = request.GET.get(
        "ticker", "default_ticker"
    )  # Usa un valor predeterminado si no se proporciona un ticker

    datos_ticker = datos_financieros.get(ticker, {})

    # Calculate financial ratios
    revenue = revenue_data(datos_ticker, "Annually")
    gross_margin = calcular_margen_bruto(datos_ticker, "Annually")
    operating_margin = calcular_margen_operacional(datos_ticker, "Annually")
    profit_margin = calcular_margen_neto(datos_ticker, "Annually")
    roe = calcular_roe(datos_ticker, "Annually")
    roa = calcular_roa(datos_ticker, "Annually")
    roic = calcular_roic(datos_ticker, "Annually")
    fcf = free_cash_flow(datos_ticker, "Annually")
    # Quick Ratio
    qr = quick_ratio(datos_ticker, "Annually")

    # Crear la tabla HTML
    # Añadir filas a la tabla para cada métrica, incluyendo Quick Ratio
    table_html = "<table class='tables_'><thead><tr><th>Metric</th><th>Actual</th><th>Promedio</th></tr></thead><tbody>"

    for metric_name, metric_data in [
        ("Gross Margin", gross_margin),
        ("Operating Margin", operating_margin),
        ("Profit Margin", profit_margin),
        ("ROE", roe),
        ("ROA", roa),
        ("ROIC", roic),
        ("Quick Ratio", qr),
    ]:
        if metric_data:
            actual_value = next(iter(metric_data.values()))  # El último valor
            average_value = sum(metric_data.values()) / len(metric_data)  # El promedio

            if metric_name == "Quick Ratio":
                # Para Quick Ratio, no añades el símbolo %
                table_html += f"<tr><td>{metric_name}</td><td>{actual_value:.2f}</td><td>{average_value:.2f}</td></tr>"
            else:
                # Para las demás métricas, añades el símbolo %
                table_html += f"<tr><td>{metric_name}</td><td>{actual_value:.2f}%</td><td>{average_value:.2f}%</td></tr>"

    table_html += "</tbody></table>"
    table_html = format_html(table_html, border="0")

    # Ratio Metric
    context = {
        "tickers": tickers,
        "selected_ticker": ticker_seleccionado,  # Cambia 'ticker' a 'selected_ticker'
        "revenue": revenue,
        "gross_margin": gross_margin,
        "operating_margin": operating_margin,
        "profit_margin": profit_margin,
        "roe": roe,
        "roa": roa,
        "roic": roic,
        "fcf": fcf,
        "qr": qr,
        "table_metrics": table_html,
    }
    return render(request, "finance_app/fundamental_ratios.html", context)


# Define una función para formatear los valores como porcentajes
def format_percent(val):
    return f"{val:.2f}%"


# Define una función que aplica el formateador a las filas especificadas
def format_rows(df):
    # Lista de las filas que quieres formatear
    rows_to_format = [
        "Cumulative Return",  # Multiplicado por 100
        "CAGR﹪",  # Multiplicado por 100
        "Volatility (ann.)",  # Multiplicado por 100
        "Risk-Free Rate",
        "Max Drawdown",  # Multiplicado por 100
        "Expected Daily",  # Multiplicado por 100
        "Expected Monthly",  # Multiplicado por 100
        "Expected Yearly",  # Multiplicado por 100
        "Kelly Criterion",  # Multiplicado por 100
        "Daily Value-at-Risk",  # Multiplicado por 100
        "Expected Shortfall (cVaR)",  # Multiplicado por 100
        "MTD",  # Multiplicado por 100
        "3M",  # Multiplicado por 100
        "6M",  # Multiplicado por 100
        "YTD",  # Multiplicado por 100
        "1Y",  # Multiplicado por 100
        "3Y (ann.)",  # Multiplicado por 100
        "5Y (ann.)",  # Multiplicado por 100
        "10Y (ann.)",  # Multiplicado por 100
        "All-time (ann.)",  # Multiplicado por 100
        "Best Day",  # Multiplicado por 100
        "Worst Day",  # Multiplicado por 100
        "Best Month",  # Multiplicado por 100
        "Worst Month",  # Multiplicado por 100
        "Best Year",  # Multiplicado por 100
        "Worst Year",  # Multiplicado por 100
        "Avg. Drawdown",  # Multiplicado por 100
        "Win Days",  # Multiplicado por 100
        "Win Month",  # Multiplicado por 100
        "Win Quarter",  # Multiplicado por 100
        "Win Year",  # Multiplicado por 100
    ]  # Reemplaza esto con los nombres de tus filas
    for row in rows_to_format:
        if row in df.index:
            df.loc[row] = df.loc[row].apply(format_percent)
    return df


def table_quant(inidividual_returns, ticker):
    metrics = qs.reports.metrics(
        inidividual_returns, mode="full", display=False, rf=0.039
    )

    metric = pd.DataFrame(metrics)
    metric = metric.rename(columns={"Strategy": ""})
    selected_rows = metric.loc[
        [
            "Cumulative Return",  # Multiplicado por 100
            "CAGR﹪",  # Multiplicado por 100
            "Volatility (ann.)",  # Multiplicado por 100
            "Risk-Free Rate",
            "Sharpe",
            "Sortino",
            "Calmar",
            "Max Drawdown",  # Multiplicado por 100
            "Longest DD Days",
            "Expected Daily",  # Multiplicado por 100
            "Expected Monthly",  # Multiplicado por 100
            "Expected Yearly",  # Multiplicado por 100
            "Kelly Criterion",  # Multiplicado por 100
            "Daily Value-at-Risk",  # Multiplicado por 100
            "Expected Shortfall (cVaR)",  # Multiplicado por 100
            "Max Consecutive Wins",
            "Max Consecutive Losses",
            "Gain/Pain Ratio",
            "Gain/Pain (1M)",
            "MTD",  # Multiplicado por 100
            "3M",  # Multiplicado por 100
            "6M",  # Multiplicado por 100
            "YTD",  # Multiplicado por 100
            "1Y",  # Multiplicado por 100
            "3Y (ann.)",  # Multiplicado por 100
            "5Y (ann.)",  # Multiplicado por 100
            "10Y (ann.)",  # Multiplicado por 100
            "All-time (ann.)",  # Multiplicado por 100
            "Best Day",  # Multiplicado por 100
            "Worst Day",  # Multiplicado por 100
            "Best Month",  # Multiplicado por 100
            "Worst Month",  # Multiplicado por 100
            "Best Year",  # Multiplicado por 100
            "Worst Year",  # Multiplicado por 100
            "Avg. Drawdown",  # Multiplicado por 100
            "Avg. Drawdown Days",
            "Win Days",  # Multiplicado por 100
            "Win Month",  # Multiplicado por 100
            "Win Quarter",  # Multiplicado por 100
            "Win Year",  # Multiplicado por 100
        ]
    ]

    rows_to_multiply = [
        "Cumulative Return",
        "CAGR﹪",
        "Volatility (ann.)",
        "Max Drawdown",
        "Expected Daily",
        "Expected Monthly",
        "Expected Yearly",
        "Kelly Criterion",
        "Daily Value-at-Risk",
        "Expected Shortfall (cVaR)",
        "MTD",
        "3M",
        "6M",
        "YTD",
        "1Y",
        "3Y (ann.)",
        "5Y (ann.)",
        "10Y (ann.)",
        "All-time (ann.)",
        "Best Day",
        "Worst Day",
        "Best Month",
        "Worst Month",
        "Best Year",
        "Worst Year",
        "Avg. Drawdown",
        "Win Days",
        "Win Month",
        "Win Quarter",
        "Win Year",
    ]

    for row in rows_to_multiply:
        selected_rows.loc[row] *= 100

    return selected_rows


def get_returns(ticker_seleccionado):
    try:
        # Abre el archivo JSON y carga los datos
        with open(os.path.join(base_dir, "data", "all_returns.json"), "r") as f:
            all_returns_dict = json.load(f)

        returns_dict = all_returns_dict.get(ticker_seleccionado, {})

        # Convierte el diccionario de retornos en un DataFrame de pandas
        returns_df = pd.DataFrame(list(returns_dict.items()), columns=["Date", "Close"])
        returns_df["Date"] = pd.to_datetime(returns_df["Date"])
        returns_df.set_index("Date", inplace=True)
        returns_df.sort_index(inplace=True)

        # Calcula los retornos porcentuales
        returns_df["Return"] = returns_df["Close"].pct_change()
        returns_df.dropna(inplace=True)
        # quants = qs.utils.download_returns(ticker_seleccionado, period='10y')

        returns_df = returns_df.drop(columns=["Close"])

        returns_df = returns_df["Return"]

    except Exception as e:
        return HttpResponse("Error al leer los precios del archivo JSON.", status=500)

    return returns_df


def quants_view(request):
    # Load financial data
    try:
        datos_financieros = load_financial_data()
    except Exception:
        return HttpResponse("Error al cargar los datos financieros.", status=500)
    # List of available tickers
    tickers = list(datos_financieros.keys())

    # Get selected ticker from the request
    ticker_seleccionado = request.GET.get(
        "ticker"
    )  # Valor predeterminado si no se selecciona ninguno
    ticker = request.GET.get(
        "ticker", "default_ticker"
    )  # Usa un valor predeterminado si no se proporciona un ticker

    if ticker_seleccionado not in tickers:
        return HttpResponse("Ticker no disponible.", status=404)

    try:
        price = get_prices(ticker_seleccionado)

    except Exception as e:
        # Manejar el error adecuadamente
        return HttpResponse("Error al descargar precios del ticker.", status=500)
    # Cumulative Returns
    try:
        cumulative_returns = get_cumulative_returns(ticker_seleccionado)
    except Exception as e:
        return HttpResponse("Error al descargar retornos del ticker.", status=500)

    # Ratio Metric
    returns_for_table = get_returns(ticker_seleccionado)
    table_metrics = table_quant(returns_for_table, ticker_seleccionado)
    table_metrics = format_rows(table_metrics)
    table_quants = table_metrics.to_html(
        classes="tables_", border="0"
    )  # Aplica la función de formateo a las filas especificadas

    context = {
        "tickers": tickers,
        "selected_ticker": ticker_seleccionado,  # Cambia 'ticker' a 'selected_ticker'
        "price": price,
        "cumulative_returns": cumulative_returns,
        "table_quants": table_quants,  # Añade la tabla HTML al contexto
    }
    return render(request, "finance_app/quants.html", context)


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(price_data, "interval", minutes=600)
    scheduler.start()


# Llama a price_data al iniciar la aplicación
price_data()

# Inicia el planificador
start_scheduler()
