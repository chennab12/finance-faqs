import pytest

from calculations import (
    compound_projection,
    compound_series,
    concentration,
    debt_payoff,
    debt_schedule,
    real_value,
    reserve_months,
)


def test_zero_apr_payoff_is_balance_over_payment():
    assert debt_payoff(1000, 0, 100) == (10, 0.0, 0.0)


def test_payment_equal_to_interest_never_pays_off():
    assert debt_schedule(1200, 12, 12) is None


def test_extra_payment_saves_time_and_interest():
    _, base_interest = debt_schedule(5000, 20, 150)
    fast_balances, fast_interest = debt_schedule(5000, 20, 200)
    assert fast_interest < base_interest
    assert fast_balances[-1] == 0.0


def test_zero_balance_is_already_paid():
    assert debt_payoff(0, 20, 100) == (0, 0.0, 0.0)


def test_compound_with_zero_return_is_contributions():
    assert compound_projection(1000, 100, 0, 2) == pytest.approx(3400)


def test_compound_series_has_one_value_per_year():
    series = compound_series(1000, 0, 10, 3)
    assert len(series) == 4
    assert series[1] == pytest.approx(1100)


def test_fee_reduces_ending_value():
    assert compound_projection(10000, 200, 5.5, 20) < compound_projection(10000, 200, 6, 20)


def test_negative_return_loses_money():
    assert compound_projection(1000, 0, -10, 1) == pytest.approx(900)


def test_real_value_discounts_inflation():
    assert real_value(110, 10, 1) == pytest.approx(100)


def test_reserve_months():
    assert reserve_months(9000, 3000) == 3
    assert reserve_months(9000, 0) is None


def test_concentration():
    assert concentration(25, 100) == 25
    assert concentration(25, 0) is None
