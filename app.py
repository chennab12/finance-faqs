"""Finance & Wealth Compass: a practical US-focused money learning dashboard."""
import streamlit as st
from content import LESSONS,SOURCES
from visuals import show
from calculations import cash_flow,net_worth,debt_payoff,compound_projection,concentration

st.set_page_config(page_title="Finance & Wealth Compass",page_icon="💰",layout="wide")
st.title("💰 Finance & Wealth Compass")
st.caption("Cash flow → credit → investing → taxes → wealth protection · US-focused · Sources reviewed 29 September 2026")
st.info("General financial education. Examples and calculators are illustrations, not personal investment, tax or legal advice. Rules and limits change; follow the linked current IRS, CFPB, SEC and FDIC pages for your circumstances.")
NAMES=["📌 Master cheatsheet","🏠 Start here"]+[f"{x['icon']} {x['title']}" for x in LESSONS]+["🧮 Money calculators","📚 Sources & method"]
tabs=st.tabs(NAMES)

with tabs[0]:
    st.header("📌 Master finance cheatsheet")
    st.caption("One row per topic. Scroll the table horizontally; example numbers are not universal targets.")
    a,b,c=st.columns(3)
    a.metric("Learning topics",len(LESSONS));b.metric("Interactive calculators",4);c.metric("Source organizations","CFPB · SEC · IRS · FDIC")
    st.dataframe([{"Level":x["level"],"Topic":x["title"],"Essential idea":x["takeaway"],"Do ✅":x["action"],"Don't ⛔":"Assume last year's tax rules or a product label still applies" if x["title"].startswith(("Taxes","Retirement")) else "Act without checking costs, risks and your cash needs","Myth versus fact 💡":f"{x['question']} → {x['answer']}","Key metric or formula 📏":x["concepts"][0][0],"Next step ➡️":x["action"],"Original source":SOURCES[x["sources"][0]]} for x in LESSONS],hide_index=True,use_container_width=True,height=570,column_config={"Original source":st.column_config.LinkColumn("Original source")})
    st.subheader("🔢 Durable formulas and what they mean")
    st.dataframe([
        {"Metric":"Cash flow","Formula":"Take-home income − total outflows","Use":"Can this month's plan fund goals and surprises?","Important limit":"Include irregular bills"},
        {"Metric":"Net worth","Formula":"Estimated assets − liabilities","Use":"Track a dated financial snapshot","Important limit":"Home equity is not spendable cash"},
        {"Metric":"Emergency reserve coverage","Formula":"Liquid emergency cash ÷ essential monthly costs","Use":"Estimate months of essential bills covered","Important limit":"No one universal target"},
        {"Metric":"Debt interest approximation","Formula":"Starting balance × APR ÷ 12","Use":"Rough first month's interest","Important limit":"Real card interest may accrue daily; terms and fees vary"},
        {"Metric":"Single-stock concentration","Formula":"Holding value ÷ total investable assets × 100%","Use":"See exposure to one firm","Important limit":"No universal safe percentage"},
        {"Metric":"Fund cost approximation","Formula":"Invested amount × annual expense ratio","Use":"Compare recurring fund costs","Important limit":"Other costs may apply; returns vary"},
    ],hide_index=True,use_container_width=True)
    st.subheader("🚫 High-impact pitfalls")
    st.dataframe([
        {"Mistake":"Ignoring irregular annual costs","Why":"Monthly budget omits nonmonthly bills","Better next step":"Set aside monthly sinking-fund amount","Tool":"Calendar + budget sheet","Source":SOURCES["CFPB spending"]},
        {"Mistake":"Investing all emergency cash","Why":"Returns appear more exciting than liquidity","Better next step":"Set accessible reserves appropriate to your risks","Tool":"Separate insured savings bucket","Source":SOURCES["CFPB emergency fund"]},
        {"Mistake":"Paying only high-APR debt minimums","Why":"Minimum due feels like a payoff plan","Better next step":"Model payoff time and total interest","Tool":"Debt payoff calculator","Source":SOURCES["CFPB debt"]},
        {"Mistake":"Concentrating wealth in one employer","Why":"Familiarity and equity compensation accumulate","Better next step":"Measure exposure and plan diversification with tax awareness","Tool":"Holdings inventory","Source":SOURCES["SEC allocation"]},
        {"Mistake":"Assuming past return or a projection is guaranteed","Why":"A single forecast looks precise","Better next step":"Compare scenarios and account for fees and losses","Tool":"Scenario calculator","Source":SOURCES["SEC investing basics"]},
        {"Mistake":"Using stale tax thresholds","Why":"Year-specific limits change","Better next step":"Check current IRS pages and plan documents","Tool":"Tax-year checklist and IRS estimator","Source":SOURCES["IRS withholding"]},
        {"Mistake":"Trusting urgent high-return promises","Why":"Pressure and testimonials trigger fast decisions","Better next step":"Pause, verify seller and independent registration","Tool":"Investor.gov fraud resources","Source":SOURCES["SEC fraud"]},
    ],hide_index=True,use_container_width=True,column_config={"Source":st.column_config.LinkColumn("Source")})
    st.markdown(f"**Official tools:** [CFPB education worksheets ↗]({SOURCES['CFPB financial toolkit']}) · [SEC compound calculator ↗]({SOURCES['SEC compound calculator']}) · [IRS withholding estimator ↗]({SOURCES['IRS withholding']}) · [FDIC deposit insurance ↗]({SOURCES['FDIC deposit insurance']})")

with tabs[1]:
    st.header("🏠 Start with a complete money picture")
    st.write("Follow the tabs from left to right. First see cash flow and obligations, then protect reserves and credit, choose investments deliberately, and review taxes and household continuity. Different households need different priorities.")
    st.dataframe([{"Order":i,"Topic":x["title"],"Level":x["level"],"Takeaway":x["takeaway"]} for i,x in enumerate(LESSONS,1)],hide_index=True,use_container_width=True)
    st.markdown("**First action:** collect two months of transactions, list debts with rates, and write down one near-term and one long-term goal.")
    st.markdown(f"[CFPB tools ↗]({SOURCES['CFPB financial toolkit']}) · [SEC investing basics ↗]({SOURCES['SEC investing basics']})")
    show("Start here",["See cash","List debts","Name goals","Review"])

for tab,lesson in zip(tabs[2:2+len(LESSONS)],LESSONS):
    with tab:
        st.header(f"{lesson['icon']} {lesson['title']}")
        st.caption(lesson["level"]+" · "+lesson["takeaway"])
        st.dataframe([{"Concept":n,"Plain meaning":meaning,"Intuitive example":example} for n,meaning,example in lesson["concepts"]],hide_index=True,use_container_width=True)
        st.markdown("**Example:** "+lesson["example"])
        st.markdown("**Practical next step:** "+lesson["action"])
        with st.expander("🧠 Knowledge check: "+lesson["question"]):
            st.text_area("Answer in your own words",key="draft_"+lesson["title"],height=70)
            if st.checkbox("Reveal expected answer",key="reveal_"+lesson["title"]):st.success(lesson["answer"])
        st.subheader("🔎 Read the original guidance")
        cols=st.columns(len(lesson["sources"]))
        for col,name in zip(cols,lesson["sources"]):
            with col:st.markdown(f"**{name}**  \n[Open source ↗]({SOURCES[name]})")
        st.caption("Check the page's date and scope. A calculator result or past example does not predict investment returns or determine tax liability.")
        show(lesson["title"],lesson["visual"])

with tabs[-2]:
    st.header("🧮 Money calculators")
    st.caption("Inputs are processed in the Streamlit app session and are not saved by this code or sent to a financial institution. Use estimates; do not enter account numbers or passwords.")
    tool=st.selectbox("Choose a calculator",["Cash flow and net worth","Debt payoff","Compound growth and fee scenarios","Single-stock concentration"])
    if tool=="Cash flow and net worth":
        income=st.number_input("Monthly take-home income ($)",min_value=0.0,value=5000.0,step=100.0)
        expenses=st.number_input("Monthly total spending ($)",min_value=0.0,value=4300.0,step=100.0)
        assets=st.number_input("Estimated assets ($)",min_value=0.0,value=200000.0,step=1000.0)
        debts=st.number_input("Total liabilities ($)",min_value=0.0,value=100000.0,step=1000.0)
        a,b=st.columns(2);a.metric("Monthly cash flow",f"${cash_flow(income,expenses):,.0f}");b.metric("Net worth snapshot",f"${net_worth(assets,debts):,.0f}")
        st.caption("Assets may be illiquid; include taxes and irregular costs in spending where relevant.")
    elif tool=="Debt payoff":
        balance=st.number_input("Balance ($)",min_value=0.0,value=5000.0,step=100.0)
        apr=st.number_input("APR (%)",min_value=0.0,max_value=100.0,value=20.0,step=0.5)
        payment=st.number_input("Monthly payment ($)",min_value=0.0,value=150.0,step=10.0)
        result=debt_payoff(balance,apr,payment)
        if result is None:st.warning("Payment does not exceed monthly interest, or payoff exceeds the model's 100-year cap. Increase payment to see a finite result.")
        else:
            months,interest,_=result
            a,b=st.columns(2);a.metric("Illustrative payoff",f"{months} months");b.metric("Illustrative interest",f"${interest:,.0f}")
        st.caption("Simplified constant APR, monthly compounding and fixed payment; actual card interest may accrue daily and fees or rate changes alter results.")
    elif tool=="Compound growth and fee scenarios":
        initial=st.number_input("Initial investment ($)",min_value=0.0,value=10000.0,step=1000.0)
        monthly=st.number_input("Monthly contribution ($)",min_value=0.0,value=200.0,step=50.0)
        years=st.slider("Years",1,50,20)
        gross=st.slider("Assumed annual return before fee (%)",-10.0,20.0,6.0,0.5)
        fee=st.slider("Annual fee approximation (%)",0.0,3.0,0.5,0.1)
        before=compound_projection(initial,monthly,gross,years)
        after=compound_projection(initial,monthly,gross-fee,years)
        st.dataframe([{"Scenario":"Before modeled fee","Illustrative ending value":round(before,2)},{"Scenario":"After modeled fee","Illustrative ending value":round(after,2)},{"Scenario":"Difference","Illustrative ending value":round(before-after,2)}],hide_index=True,use_container_width=True)
        st.caption("Constant annual return and fee subtraction are simplifications. Real returns vary and may be negative; taxes and inflation are excluded. No return is guaranteed.")
    else:
        holding=st.number_input("Single stock or employer equity value ($)",min_value=0.0,value=25000.0,step=1000.0)
        total=st.number_input("Total investable assets ($)",min_value=0.0,value=100000.0,step=1000.0)
        share=concentration(holding,total)
        if share is None:st.warning("Enter a nonzero total investable-asset value.")
        else:
            st.metric("Share in one holding",f"{share:.1f}%")
            if holding>total:st.warning("The holding exceeds the total entered; review your inputs.")
        st.caption("There is no universal safe concentration threshold. Include tax, plan rules and the risk of relying on one employer for income and investments.")
    st.markdown(f"[SEC compound calculator ↗]({SOURCES['SEC compound calculator']}) · [SEC allocation guidance ↗]({SOURCES['SEC allocation']}) · [IRS withholding estimator ↗]({SOURCES['IRS withholding']})")
    show("Money calculators",["Input","Calculate","Check assumptions","Decide"])

with tabs[-1]:
    st.header("📚 Sources and method")
    st.write("This US-focused app links to consumer and investor authorities. It avoids automatic prices, stock ratings, specific tax thresholds and individualized recommendations. Check source dates, account terms, state rules and the current tax year.")
    st.dataframe([{"Source":name,"Direct link":url} for name,url in SOURCES.items()],hide_index=True,use_container_width=True,column_config={"Direct link":st.column_config.LinkColumn("Direct link")})
    st.caption("No account connection, data upload, file write or external API call is performed by this app.")
    show("Sources",["Question","Authority","Current rule","Personal fit"])
