# Finance & Wealth Compass

A separate Streamlit financial education app using the same progressive tab format. Its 17 lessons cover goals, cash flow, spending, reserves, assets and liabilities, credit, debt, housing, investing, funds, stocks and employer equity, fees, retirement, taxes, insurance, estate continuity and fraud. Each tab contains concepts, an intuitive example, a knowledge check, official links and an animated visual memory cue. The first tab consolidates lessons and durable formulas. Five calculators cover cash flow and net worth, emergency reserve coverage, debt payoff (with an extra-payment comparison chart), compound growth with fees and inflation (with a chart), and single-stock concentration. Lessons are picked from the sidebar, each has a quick knowledge check, and learners can mark lessons as understood to track progress.

The app focuses on US sources (CFPB, SEC, IRS, FDIC and NAIC). It provides general education, not investment, legal or tax advice. Rules, tax limits and account terms vary; follow the linked original guidance. Calculators do not fetch live rates or prices and do not request account credentials. The debt model uses simplified monthly interest; the compound model assumes a constant return and subtracts an annual fee approximately.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Run the tests with `pip install pytest && python -m pytest -q`. GitHub Actions runs them on every push.

For Streamlit Community Cloud, deploy this directory with `app.py` as the entry point. No API key is required. Visuals are code-native and honor reduced-motion settings.

## Deploy to Google Cloud Run

The `Dockerfile` runs Streamlit on port 8080 (or `$PORT`, which Cloud Run sets).

Test the container locally:

```bash
docker build -t finance-faqs .
docker run --rm -p 8080:8080 finance-faqs   # open http://localhost:8080
```

Deploy from source (Cloud Build builds the image for you):

```bash
gcloud run deploy finance-faqs --source . --region us-central1 \
  --allow-unauthenticated --timeout=3600 --session-affinity \
  --min-instances=0 --max-instances=2 --memory=512Mi
```

`.github/workflows/deploy-cloud-run.yml` redeploys on every push to `main` once these repository variables are set (Settings → Secrets and variables → Actions → Variables): `GCP_PROJECT_ID`, `GCP_REGION`, `GCP_WORKLOAD_IDENTITY_PROVIDER` and `GCP_SERVICE_ACCOUNT`. It authenticates with Workload Identity Federation, so no service account key is stored in GitHub. Until `GCP_PROJECT_ID` is set the job is skipped.
