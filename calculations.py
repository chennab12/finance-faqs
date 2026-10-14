"""Transparent illustrative financial arithmetic; no tax or investment advice."""


def cash_flow(net_income, expenses):
    return net_income - expenses


def net_worth(assets, liabilities):
    return assets - liabilities


def reserve_months(liquid_cash, essential_monthly):
    """Months of essential costs covered by liquid emergency cash."""
    if essential_monthly <= 0:
        return None
    return liquid_cash / essential_monthly


def debt_schedule(balance, apr_percent, monthly_payment, max_months=1200):
    """Remaining balance after each month, starting with the opening balance.

    Simplified constant-rate monthly model; excludes fees and daily accrual.
    Returns (balances, total_interest), or None if the debt never pays off
    within max_months.
    """
    if balance <= 0:
        return [0.0], 0.0
    rate = apr_percent / 1200
    if monthly_payment <= balance * rate:
        return None
    remaining = float(balance)
    interest = 0.0
    balances = [remaining]
    for _ in range(max_months):
        charge = remaining * rate
        interest += charge
        remaining = max(0.0, remaining + charge - monthly_payment)
        balances.append(remaining)
        if remaining <= 0:
            return balances, interest
    return None


def debt_payoff(balance, apr_percent, monthly_payment, max_months=1200):
    """(months, total_interest, remaining) or None; kept for compatibility."""
    result = debt_schedule(balance, apr_percent, monthly_payment, max_months)
    if result is None:
        return None
    balances, interest = result
    return len(balances) - 1, interest, 0.0


def compound_series(initial, monthly, annual_return_percent, years):
    """Year-end values with end-of-month contributions and a constant effective annual return."""
    rate = (1 + annual_return_percent / 100) ** (1 / 12) - 1
    value = float(initial)
    values = [value]
    for month in range(1, int(years * 12) + 1):
        value = value * (1 + rate) + monthly
        if month % 12 == 0:
            values.append(value)
    if int(years * 12) % 12:
        values.append(value)
    return values


def compound_projection(initial, monthly, annual_return_percent, years):
    return compound_series(initial, monthly, annual_return_percent, years)[-1]


def real_value(nominal, inflation_percent, years):
    """Express a future amount in today's dollars."""
    return nominal / (1 + inflation_percent / 100) ** years


def concentration(holding, total):
    return 100 * holding / total if total > 0 else None
