"""Finance & Wealth Compass: a practical US-focused money learning dashboard."""
import streamlit as st

from calculations import (
    cash_flow,
    compound_series,
    concentration,
    debt_schedule,
    net_worth,
    real_value,
    reserve_months,
)
from content import LESSONS, SOURCES
from visuals import show

st.set_page_config(page_title="Finance & Wealth Compass", page_icon="💰", layout="wide")

CHEATSHEET = "📌 Master cheatsheet"
START = "🏠 Start here"
CALCULATORS = "🧮 Money calculators"
SOURCES_PAGE = "📚 Sources & method"
LESSON_NAMES = [f"{x['icon']} {x['title']}" for x in LESSONS]
SECTIONS = [CHEATSHEET, START] + LESSON_NAMES + [CALCULATORS, SOURCES_PAGE]
QUIZ_OPTIONS = ["Yes", "No, or not necessarily"]

st.session_state.setdefault("section", START)
st.session_state.setdefault("understood", set())


def go_to(section):
    st.session_state.section = section


def progress_bar():
    done = len(st.session_state.understood)
    st.progress(done / len(LESSONS), text=f"{done} of {len(LESSONS)} lessons marked as understood")


# Only the selected section runs on each rerun, so calculator inputs stay fast.
with st.sidebar:
    st.title("💰 Compass")
    st.radio(
        "Section",
        SECTIONS,
        key="section",
        format_func=lambda s: f"✅ {s}" if s in LESSON_NAMES and s.split(" ", 1)[1] in st.session_state.understood else s,
    )
    # Filled at the end of the script so it reflects toggles made on this run.
    sidebar_progress = st.empty()

st.title("💰 Finance & Wealth Compass")
st.caption("Cash flow → credit → investing → taxes → wealth protection · US-focused · Sources reviewed 29 September 2026")
st.info(
    "General financial education. Examples and calculators are illustrations, not personal investment, tax or legal advice. "
    "Rules and limits change; follow the linked current IRS, CFPB, SEC and FDIC pages for your circumstances."
)
section = st.session_state.section


def render_cheatsheet():
    st.header("📌 Master finance cheatsheet")
    st.caption("One row per topic. Scroll the table horizontally; example numbers are not universal targets.")
    a, b, c = st.columns(3)
    a.metric("Learning topics", len(LESSONS))
    b.metric("Interactive calculators", 5)
    c.metric("Source organizations", "CFPB · SEC · IRS · FDIC")
    st.dataframe(
        [
            {
                "Level": x["level"],
                "Topic": x["title"],
                "Essential idea": x["takeaway"],
                "Key metric or formula 📏": x["metric"],
                "Do ✅": x["action"],
                "Don't ⛔": x["dont"],
                "Myth versus fact 💡": f"{x['question']} → {x['answer']}",
                "Original source": SOURCES[x["sources"][0]],
            }
            for x in LESSONS
        ],
        hide_index=True,
        use_container_width=True,
        height=570,
        column_config={"Original source": st.column_config.LinkColumn("Original source")},
    )
    st.subheader("🔢 Durable formulas and what they mean")
    st.dataframe(
        [
            {"Metric": "Cash flow", "Formula": "Take-home income − total outflows", "Use": "Can this month's plan fund goals and surprises?", "Important limit": "Include irregular bills"},
            {"Metric": "Net worth", "Formula": "Estimated assets − liabilities", "Use": "Track a dated financial snapshot", "Important limit": "Home equity is not spendable cash"},
            {"Metric": "Emergency reserve coverage", "Formula": "Liquid emergency cash ÷ essential monthly costs", "Use": "Estimate months of essential bills covered", "Important limit": "No one universal target"},
            {"Metric": "Debt interest approximation", "Formula": "Starting balance × APR ÷ 12", "Use": "Rough first month's interest", "Important limit": "Real card interest may accrue daily; terms and fees vary"},
            {"Metric": "Single-stock concentration", "Formula": "Holding value ÷ total investable assets × 100%", "Use": "See exposure to one firm", "Important limit": "No universal safe percentage"},
            {"Metric": "Fund cost approximation", "Formula": "Invested amount × annual expense ratio", "Use": "Compare recurring fund costs", "Important limit": "Other costs may apply; returns vary"},
        ],
        hide_index=True,
        use_container_width=True,
    )
    st.subheader("🚫 High-impact pitfalls")
    st.dataframe(
        [
            {"Mistake": "Ignoring irregular annual costs", "Why": "Monthly budget omits nonmonthly bills", "Better next step": "Set aside monthly sinking-fund amount", "Tool": "Calendar + budget sheet", "Source": SOURCES["CFPB spending"]},
            {"Mistake": "Investing all emergency cash", "Why": "Returns appear more exciting than liquidity", "Better next step": "Set accessible reserves appropriate to your risks", "Tool": "Emergency reserve calculator", "Source": SOURCES["CFPB emergency fund"]},
            {"Mistake": "Paying only high-APR debt minimums", "Why": "Minimum due feels like a payoff plan", "Better next step": "Model payoff time and total interest", "Tool": "Debt payoff calculator", "Source": SOURCES["CFPB debt"]},
            {"Mistake": "Concentrating wealth in one employer", "Why": "Familiarity and equity compensation accumulate", "Better next step": "Measure exposure and plan diversification with tax awareness", "Tool": "Holdings inventory", "Source": SOURCES["SEC allocation"]},
            {"Mistake": "Assuming past return or a projection is guaranteed", "Why": "A single forecast looks precise", "Better next step": "Compare scenarios and account for fees and losses", "Tool": "Scenario calculator", "Source": SOURCES["SEC investing basics"]},
            {"Mistake": "Using stale tax thresholds", "Why": "Year-specific limits change", "Better next step": "Check current IRS pages and plan documents", "Tool": "Tax-year checklist and IRS estimator", "Source": SOURCES["IRS withholding"]},
            {"Mistake": "Trusting urgent high-return promises", "Why": "Pressure and testimonials trigger fast decisions", "Better next step": "Pause, verify seller and independent registration", "Tool": "Investor.gov fraud resources", "Source": SOURCES["SEC fraud"]},
        ],
        hide_index=True,
        use_container_width=True,
        column_config={"Source": st.column_config.LinkColumn("Source")},
    )
    st.markdown(
        f"**Official tools:** [CFPB education worksheets ↗]({SOURCES['CFPB financial toolkit']}) · "
        f"[SEC compound calculator ↗]({SOURCES['SEC compound calculator']}) · "
        f"[IRS withholding estimator ↗]({SOURCES['IRS withholding']}) · "
        f"[FDIC deposit insurance ↗]({SOURCES['FDIC deposit insurance']})"
    )


def render_start():
    st.header("🏠 Start with a complete money picture")
    st.write(
        "Work through the lessons in order from the sidebar. First see cash flow and obligations, then protect reserves and credit, "
        "choose investments deliberately, and review taxes and household continuity. Different households need different priorities."
    )
    progress_bar()
    st.dataframe(
        [
            {"Order": i, "Topic": x["title"], "Level": x["level"], "Takeaway": x["takeaway"], "Understood": "✅" if x["title"] in st.session_state.understood else ""}
            for i, x in enumerate(LESSONS, 1)
        ],
        hide_index=True,
        use_container_width=True,
    )
    st.markdown("**First action:** collect two months of transactions, list debts with rates, and write down one near-term and one long-term goal.")
    st.markdown(f"[CFPB tools ↗]({SOURCES['CFPB financial toolkit']}) · [SEC investing basics ↗]({SOURCES['SEC investing basics']})")
    st.button("Begin the first lesson →", on_click=go_to, args=(LESSON_NAMES[0],), type="primary")
    show("Start here", ["See cash", "List debts", "Name goals", "Review"])


def render_lesson(index):
    lesson = LESSONS[index]
    title = lesson["title"]
    st.header(f"{lesson['icon']} {title}")
    st.caption(f"Lesson {index + 1} of {len(LESSONS)} · {lesson['level']} · {lesson['takeaway']}")
    st.dataframe(
        [{"Concept": n, "Plain meaning": meaning, "Intuitive example": example} for n, meaning, example in lesson["concepts"]],
        hide_index=True,
        use_container_width=True,
    )
    st.markdown("**Example:** " + lesson["example"])
    st.markdown("**Key metric:** " + lesson["metric"])
    st.markdown("**Practical next step:** " + lesson["action"])

    st.subheader("🧠 Knowledge check")
    choice = st.radio(lesson["question"], QUIZ_OPTIONS, index=None, key="quiz_" + title)
    if choice is not None:
        # Every myth question in the curriculum is answered "No" or "Not necessarily".
        if choice == QUIZ_OPTIONS[1]:
            st.success("Correct. " + lesson["answer"])
        else:
            st.error("Not quite. " + lesson["answer"])
    understood = st.toggle("I understand this lesson", value=title in st.session_state.understood, key="understood_" + title)
    if understood:
        st.session_state.understood.add(title)
    else:
        st.session_state.understood.discard(title)

    st.subheader("🔎 Read the original guidance")
    cols = st.columns(len(lesson["sources"]))
    for col, name in zip(cols, lesson["sources"]):
        col.markdown(f"**{name}**  \n[Open source ↗]({SOURCES[name]})")
    st.caption("Check the page's date and scope. A calculator result or past example does not predict investment returns or determine tax liability.")
    show(title, lesson["visual"])

    prev_col, next_col = st.columns(2)
    if index > 0:
        prev_col.button("← Previous lesson", on_click=go_to, args=(LESSON_NAMES[index - 1],), use_container_width=True)
    next_section = LESSON_NAMES[index + 1] if index + 1 < len(LESSONS) else CALCULATORS
    next_label = "Next lesson →" if index + 1 < len(LESSONS) else "Try the calculators →"
    next_col.button(next_label, on_click=go_to, args=(next_section,), type="primary", use_container_width=True)


def render_calculators():
    st.header("🧮 Money calculators")
    st.caption("Inputs are processed in the Streamlit app session and are not saved by this code or sent to a financial institution. Use estimates; do not enter account numbers or passwords.")
    tool = st.segmented_control(
        "Choose a calculator",
        ["Cash flow and net worth", "Emergency reserve", "Debt payoff", "Compound growth and fees", "Single-stock concentration"],
        default="Cash flow and net worth",
    )
    if tool is None:
        st.info("Pick a calculator above.")
    elif tool == "Cash flow and net worth":
        income = st.number_input("Monthly take-home income ($)", min_value=0.0, value=5000.0, step=100.0)
        expenses = st.number_input("Monthly total spending ($)", min_value=0.0, value=4300.0, step=100.0)
        assets = st.number_input("Estimated assets ($)", min_value=0.0, value=200000.0, step=1000.0)
        debts = st.number_input("Total liabilities ($)", min_value=0.0, value=100000.0, step=1000.0)
        a, b = st.columns(2)
        a.metric("Monthly cash flow", f"${cash_flow(income, expenses):,.0f}")
        b.metric("Net worth snapshot", f"${net_worth(assets, debts):,.0f}")
        st.caption("Assets may be illiquid; include taxes and irregular costs in spending where relevant.")

    elif tool == "Emergency reserve":
        cash = st.number_input("Liquid emergency cash ($)", min_value=0.0, value=8000.0, step=500.0)
        essentials = st.number_input("Essential monthly costs ($)", min_value=0.0, value=3000.0, step=100.0, help="Housing, food, utilities, insurance, minimum debt payments, transport.")
        target = st.slider("Months of essentials you want covered", 1, 12, 6)
        months = reserve_months(cash, essentials)
        if months is None:
            st.warning("Enter nonzero essential monthly costs.")
        else:
            a, b = st.columns(2)
            a.metric("Months covered", f"{months:.1f}")
            gap = max(0.0, target * essentials - cash)
            b.metric(f"Gap to {target} months", f"${gap:,.0f}")
            st.progress(min(1.0, months / target), text=f"{min(100, 100 * months / target):.0f}% of your {target}-month target")
        st.caption("There is no universal target; job stability, dependents, insurance and health all change what is enough.")

    elif tool == "Debt payoff":
        balance = st.number_input("Balance ($)", min_value=0.0, value=5000.0, step=100.0)
        apr = st.number_input("APR (%)", min_value=0.0, max_value=100.0, value=20.0, step=0.5)
        payment = st.number_input("Monthly payment ($)", min_value=0.0, value=150.0, step=10.0)
        extra = st.number_input("Extra monthly payment to compare ($)", min_value=0.0, value=50.0, step=10.0)
        base = debt_schedule(balance, apr, payment)
        faster = debt_schedule(balance, apr, payment + extra)
        if base is None:
            st.warning("Payment does not exceed monthly interest, or payoff exceeds the model's 100-year cap. Increase payment to see a finite result.")
        else:
            base_balances, base_interest = base
            fast_balances, fast_interest = faster
            a, b, c = st.columns(3)
            a.metric("Illustrative payoff", f"{len(base_balances) - 1} months")
            b.metric("Illustrative interest", f"${base_interest:,.0f}")
            if extra > 0:
                c.metric(
                    f"With +${extra:,.0f}/month",
                    f"{len(fast_balances) - 1} months",
                    delta=f"${base_interest - fast_interest:,.0f} interest saved",
                )
            length = len(base_balances)
            chart = {"Month": list(range(length)), "Current payment": base_balances}
            if extra > 0:
                chart[f"+${extra:,.0f}/month"] = fast_balances + [0.0] * (length - len(fast_balances))
            st.line_chart(
                chart,
                x="Month",
                y_label="Remaining balance ($)",
            )
        st.caption("Simplified constant APR, monthly compounding and fixed payment; actual card interest may accrue daily and fees or rate changes alter results.")

    elif tool == "Compound growth and fees":
        initial = st.number_input("Initial investment ($)", min_value=0.0, value=10000.0, step=1000.0)
        monthly = st.number_input("Monthly contribution ($)", min_value=0.0, value=200.0, step=50.0)
        years = st.slider("Years", 1, 50, 20)
        gross = st.slider("Assumed annual return before fee (%)", -10.0, 20.0, 6.0, 0.5)
        fee = st.slider("Annual fee approximation (%)", 0.0, 3.0, 0.5, 0.1)
        inflation = st.slider("Assumed inflation (%)", 0.0, 8.0, 2.5, 0.1)
        before = compound_series(initial, monthly, gross, years)
        after = compound_series(initial, monthly, gross - fee, years)
        contributed = [initial + monthly * 12 * y for y in range(years + 1)]
        a, b, c = st.columns(3)
        a.metric("Ending value after fee", f"${after[-1]:,.0f}")
        b.metric("Lost to fees", f"${before[-1] - after[-1]:,.0f}")
        c.metric("After fee, in today's dollars", f"${real_value(after[-1], inflation, years):,.0f}")
        st.line_chart(
            {"Year": list(range(years + 1)), "Before fee": before, "After fee": after, "Amount contributed": contributed},
            x="Year",
            y_label="Illustrative value ($)",
        )
        st.caption("Constant annual return, inflation and fee subtraction are simplifications. Real returns vary and may be negative; taxes are excluded. No return is guaranteed.")

    elif tool == "Single-stock concentration":
        holding = st.number_input("Single stock or employer equity value ($)", min_value=0.0, value=25000.0, step=1000.0)
        total = st.number_input("Total investable assets ($)", min_value=0.0, value=100000.0, step=1000.0)
        share = concentration(holding, total)
        if share is None:
            st.warning("Enter a nonzero total investable-asset value.")
        else:
            st.metric("Share in one holding", f"{share:.1f}%")
            if holding > total:
                st.warning("The holding exceeds the total entered; review your inputs.")
        st.caption("There is no universal safe concentration threshold. Include tax, plan rules and the risk of relying on one employer for income and investments.")

    st.markdown(
        f"[SEC compound calculator ↗]({SOURCES['SEC compound calculator']}) · "
        f"[SEC allocation guidance ↗]({SOURCES['SEC allocation']}) · "
        f"[IRS withholding estimator ↗]({SOURCES['IRS withholding']})"
    )


def render_sources():
    st.header("📚 Sources and method")
    st.write(
        "This US-focused app links to consumer and investor authorities. It avoids automatic prices, stock ratings, specific tax thresholds "
        "and individualized recommendations. Check source dates, account terms, state rules and the current tax year."
    )
    st.dataframe(
        [{"Source": name, "Direct link": url} for name, url in SOURCES.items()],
        hide_index=True,
        use_container_width=True,
        column_config={"Direct link": st.column_config.LinkColumn("Direct link")},
    )
    st.caption("No account connection, data upload, file write or external API call is performed by this app.")
    show("Sources", ["Question", "Authority", "Current rule", "Personal fit"])


if section == CHEATSHEET:
    render_cheatsheet()
elif section == START:
    render_start()
elif section in LESSON_NAMES:
    render_lesson(LESSON_NAMES.index(section))
elif section == CALCULATORS:
    render_calculators()
else:
    render_sources()

with sidebar_progress.container():
    progress_bar()
