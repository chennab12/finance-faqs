"""Transparent illustrative financial arithmetic; no tax or investment advice."""

def cash_flow(net_income, expenses):
    return net_income-expenses

def net_worth(assets, liabilities):
    return assets-liabilities

def debt_payoff(balance, apr_percent, monthly_payment, max_months=1200):
    """Simplified constant-rate monthly model; excludes fees and daily accrual."""
    if balance <= 0:return (0,0.0,0.0)
    rate=apr_percent/1200
    if monthly_payment <= balance*rate:
        return None
    remaining=float(balance);interest=0.0
    for month in range(1,max_months+1):
        charge=remaining*rate
        interest+=charge
        remaining=max(0.0,remaining+charge-monthly_payment)
        if remaining<=0:return (month,interest,0.0)
    return None

def compound_projection(initial,monthly,annual_return_percent,years):
    """Monthly end-of-month contributions and constant effective annual return."""
    rate=(1+annual_return_percent/100)**(1/12)-1
    value=float(initial)
    for _ in range(int(years*12)):
        value=value*(1+rate)+monthly
    return value

def concentration(holding,total):
    return 100*holding/total if total>0 else None
