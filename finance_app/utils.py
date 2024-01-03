import matplotlib.pyplot as plt
import json
import matplotlib.ticker as mtick
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, "data", "financial_statements.json")

# Cargar el JSON desde el archivo
with open(file_path, "r") as file:
    datos_financieros = json.load(file)

# Ticker de la compañía
tickers_ = list(datos_financieros.keys())

nvda__ = datos_financieros["AAPL"]


def revenue_data(datos_financieros, statement_type):
    revenue_dict = {}
    income_key = f"Income_Statement_{statement_type}"

    if income_key in datos_financieros:
        for income_statement in datos_financieros[income_key]:
            year = income_statement.get("Concepto")
            revenue_value = income_statement.get("Revenue")
            if isinstance(year, str) and isinstance(revenue_value, (int, float)):
                revenue_dict[year] = revenue_value
    return revenue_dict


revenue__ = revenue_data(nvda__, "Annually")


def calcular_margen_bruto(datos_financieros, statement_type):
    margen_bruto = {}
    income_key = f"Income_Statement_{statement_type}"

    if income_key in datos_financieros:
        for income_statement in datos_financieros[income_key]:
            year = income_statement.get("Concepto")
            gross_profit = income_statement.get("Gross Profit")
            revenue = income_statement.get("Revenue")
            if (
                isinstance(year, str)
                and isinstance(gross_profit, (int, float))
                and isinstance(revenue, (int, float))
            ):
                margen_bruto[year] = (gross_profit / revenue) * 100
    return margen_bruto


def calcular_margen_operacional(datos_financieros, statement_type):
    margen_operacional = {}
    income_key = f"Income_Statement_{statement_type}"

    if income_key in datos_financieros:
        for income_statement in datos_financieros[income_key]:
            year = income_statement.get("Concepto")
            operating_income = income_statement.get("Operating Income")
            revenue = income_statement.get("Revenue")
            if (
                isinstance(year, str)
                and isinstance(operating_income, (int, float))
                and isinstance(revenue, (int, float))
            ):
                margen_operacional[year] = (operating_income / revenue) * 100
    return margen_operacional


def calcular_margen_neto(datos_financieros, statement_type):
    margen_neto = {}
    income_key = f"Income_Statement_{statement_type}"

    if income_key in datos_financieros:
        for income_statement in datos_financieros[income_key]:
            year = income_statement.get("Concepto")
            net_income = income_statement.get("Net Income")
            revenue = income_statement.get("Revenue")
            if (
                isinstance(year, str)
                and isinstance(net_income, (int, float))
                and isinstance(revenue, (int, float))
            ):
                margen_neto[year] = (net_income / revenue) * 100
    return margen_neto


# Función para calcular ROE (Return on Equity)
def calcular_roe(datos_financieros, statement_type):
    roe = {}
    income_key = f"Income_Statement_{statement_type}"
    balance_key = f"Balance_Sheet_Statement_{statement_type}"

    if income_key in datos_financieros and balance_key in datos_financieros:
        for income_statement in datos_financieros[income_key]:
            year = income_statement.get("Concepto")
            net_income = income_statement.get("Net Income")
            for balance_sheet in datos_financieros[balance_key]:
                if balance_sheet.get("Concepto") == year:
                    shareholders_equity = balance_sheet.get("Shareholders' Equity")
                    if (
                        isinstance(year, str)
                        and isinstance(net_income, (int, float))
                        and isinstance(shareholders_equity, (int, float))
                    ):
                        roe[year] = (net_income / shareholders_equity) * 100
    return roe


def calcular_roa(datos_financieros, statement_type):
    roa = {}
    income_key = f"Income_Statement_{statement_type}"
    balance_key = f"Balance_Sheet_Statement_{statement_type}"

    if income_key in datos_financieros and balance_key in datos_financieros:
        for income_statement in datos_financieros[income_key]:
            year = income_statement.get("Concepto")
            net_income = income_statement.get("Net Income")
            for balance_sheet in datos_financieros[balance_key]:
                if balance_sheet.get("Concepto") == year:
                    total_assets = balance_sheet.get("Total Assets")
                    if (
                        isinstance(year, str)
                        and isinstance(net_income, (int, float))
                        and isinstance(total_assets, (int, float))
                    ):
                        roa[year] = (net_income / total_assets) * 100
    return roa


def calcular_roic(datos_financieros, statement_type):
    roic = {}
    income_key = f"Income_Statement_{statement_type}"
    balance_key = f"Balance_Sheet_Statement_{statement_type}"

    if income_key in datos_financieros and balance_key in datos_financieros:
        for income_statement in datos_financieros[income_key]:
            year = income_statement.get("Concepto")
            nopat = income_statement.get("Operating Income") * (1 - 0.27)
            for balance_sheet in datos_financieros[balance_key]:
                if balance_sheet.get("Concepto") == year:
                    capital_invested = balance_sheet.get(
                        "Total Debt"
                    ) + balance_sheet.get("Shareholders' Equity")
                    if (
                        isinstance(year, str)
                        and isinstance(nopat, (int, float))
                        and isinstance(capital_invested, (int, float))
                    ):
                        roic[year] = (nopat / capital_invested) * 100
    return roic


def free_cash_flow(datos_financieros, statement_type):
    fcf = {}
    cash_flow_key = f"Cash_Flow_Statement_{statement_type}"

    if cash_flow_key in datos_financieros:
        for cash_flow_statement in datos_financieros[cash_flow_key]:
            year = cash_flow_statement.get("Concepto")
            fcf[year] = cash_flow_statement.get("Free Cash Flow")

    return fcf


def quick_ratio(datos_financieros, statement_type):
    qr = {}
    balance_key = f"Balance_Sheet_Statement_{statement_type}"

    if balance_key in datos_financieros:
        for balance_sheet_statement in datos_financieros[balance_key]:
            year = balance_sheet_statement["Concepto"]
            try:
                current_assets = balance_sheet_statement["Total Current Assets"]
            except KeyError:
                current_assets = 0
            try:
                current_liabilities = balance_sheet_statement[
                    "Total Current Liabilities"
                ]
            except KeyError:
                current_liabilities = 0
            try:
                inventory = balance_sheet_statement["Inventory"]
            except KeyError:
                inventory = 0  # Asume que el inventario es 0 si no está presente
            # Calcula el Quick Ratio directamente sin un bucle anidado
            if current_liabilities > 0:  # Asegura que no hay división por cero
                qr[year] = (current_assets - inventory) / current_liabilities

    return qr
