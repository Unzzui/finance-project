import pandas as pd
import yfinance as yf
import quantstats as qs
import json
from datetime import datetime
from django.utils.html import format_html
import os
from utils import calcular_roa, calcular_roe, calcular_roic, free_cash_flow, quick_ratio


base_dir = os.path.dirname(os.path.abspath(__file__))

file_path = "/Users/diegobravo/Documents/Code/Finance_Tools/Portfolio/Utils/data/financial_statements.json"
with open(file_path, "r") as file:
    datos_financieros = json.load(file)

datos_aapl = datos_financieros["AAPL"]

returnss = qs.utils.download_returns("AAPL", period="10y")

re_ = qs.reports.basic(returnss, display=True)
re_1 = qs.reports.metrics(returnss, mode="full")
cumulative_returns = qs.stats.compsum(returnss)

ticker = "AAPL"
volatility = qs.stats.rolling_volatility(returnss)
volatility.dropna()

qttt_ = quick_ratio(datos_aapl, "Annually")

month = qs.utils.group_returns(returnss, groupby=returnss.index.year) * 100

metrics = qs.reports.metrics(returnss, mode="full", display=False)
qs.reports.metrics(returnss, mode="full", display=True)

metric = pd.DataFrame(metrics)

metric = metric.rename(columns={"Strategy": ticker})
print(metric.index)
selected_rows = metric.loc[
    [
        "Cumulative Return",  # Multiplicado por 100
        "CAGR﹪",  # Multiplicado por 100
        "Volatility (ann.)",  # Multiplicado por 100
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

selected_rows

ticker_seleccionado = "NVDA"
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
returns_df.dropna(inplace=True)
# quants = qs.utils.download_returns(ticker_seleccionado, period='10y')

returns_df = returns_df.drop(columns=["Close"])

returns_df = returns_df["Return"]

metrics = qs.reports.metrics(
    returns_df,
    mode="full",
    display=False,
)

metric = pd.DataFrame(metrics)

metric = metric.rename(columns={"Strategy": ticker})
selected_rows = metric.loc[
    [
        "Cumulative Return",  # Multiplicado por 100
        "CAGR﹪",  # Multiplicado por 100
        "Volatility (ann.)",  # Multiplicado por 100
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
