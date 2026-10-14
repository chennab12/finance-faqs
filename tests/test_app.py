"""Smoke tests: every section renders without exceptions."""
from streamlit.testing.v1 import AppTest

from content import LESSONS


def run(section=None):
    at = AppTest.from_file("../app.py", default_timeout=30)
    if section is not None:
        at.session_state["section"] = section
    at.run()
    assert not at.exception, at.exception
    return at


def test_every_section_renders():
    at = run()
    for section in at.sidebar.radio[0].options:
        run(section)


def test_next_lesson_button_advances():
    first = f"{LESSONS[0]['icon']} {LESSONS[0]['title']}"
    at = run(first)
    next_button = [b for b in at.button if b.label == "Next lesson →"][0]
    next_button.click().run()
    assert at.session_state["section"] == f"{LESSONS[1]['icon']} {LESSONS[1]['title']}"


def test_each_calculator_renders():
    at = run("🧮 Money calculators")
    for option in ["Cash flow and net worth", "Emergency reserve", "Debt payoff", "Compound growth and fees", "Single-stock concentration"]:
        at.button_group[0].set_value(option).run()
        assert not at.exception, at.exception
