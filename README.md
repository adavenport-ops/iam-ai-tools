
# IAM AI Tools

Production-ready, **shareable** utilities that show how IAM teams can apply AI to real workflows:
- **Access Request Triage** → turn free‑text tickets into structured, least‑privilege recommendations.
- **Policy Q&A** → ask questions over your policy corpus and get sourced, consistent answers.
- **Log Explainer** → summarize Okta/OIDC events into probable causes and next steps.
- **Reviewer Helper** → generate crisp, reviewer‑ready notes for access reviews.

This is not a boilerplate. It ships with runnable scripts, sample data, CI, Docker, and docs so others can clone & use immediately.

---

## ✨ Quick Start

**Local (Python 3.10+):**
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# (optional) set OPENAI_API_KEY in .env for real LLM calls
```

**Run demos (works offline without an API key):**
```bash
make demo
```

**Run each tool:**
```bash
# Access triage
python app/triage_access.py --in data/sample/access_requests.jsonl --out triage_results.jsonl

# Policy Q&A
python app/policy_qa.py --ask "When is break-glass allowed? What’s the timeout?"

# Log explainer
python app/log_explainer.py --in data/sample/okta_logs.jsonl --out explained_logs.jsonl

# Reviewer helper
python app/reviewer_helper.py --signals data/sample/review_signals.csv --out review_blurbs.csv
```

---

## 🐳 Docker (zero local setup)

```bash
docker build -t iam-ai-tools .
docker run --rm -it -v "$PWD":/app iam-ai-tools bash -lc "make demo"
```

To run a specific tool:
```bash
docker run --rm -it -v "$PWD":/app iam-ai-tools bash -lc       "python app/policy_qa.py --ask 'When is break-glass allowed?'"
```

---

## 🔧 Configure an LLM (optional but recommended)

By default, tools will **echo** results if no API key is set (so the demos run offline).
For real responses, set an OpenAI‑compatible endpoint in `.env`:
```dotenv
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini
# or point to a local OpenAI-compatible server
OPENAI_BASE_URL=http://localhost:11434/v1
```

---

## 📦 Use with your data

- Replace files under `data/sample/` with your own:
  - `access_requests.jsonl` for triage
  - `okta_logs.jsonl` for event explanations
  - `policies/` directory for policy Q&A
  - `review_signals.csv` for reviewer notes
- No vendor APIs are called by default. Keep secrets out of git (see `.gitignore`).

---

## 🛡️ Security & Privacy

- Samples are sanitized. Do **not** commit real user data, tokens, or org URLs.
- Store secrets in `.env` or your secret manager.
- See `SECURITY.md` for disclosure process.

---

## 🧪 CI

GitHub Actions runs `ruff`/`black` and a smoke test on pushes & PRs.
See `.github/workflows/ci.yml`.

---

## 📈 Why this exists

IAM work benefits massively from AI for policy interpretation, decision explainability, and consistent communications.
This repo demonstrates practical, incremental wins you can adopt without big rewrites.

---

## 📝 License

MIT — see `LICENSE`.
