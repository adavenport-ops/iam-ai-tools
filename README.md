
# IAM + AI: Practical Playbook

A fun, hands‑on GitHub project that shows exactly **how an IAM engineer uses AI in day‑to‑day work**. It includes small, runnable examples for:

1) **Access Request Triage** – turn messy access requests into structured decisions + suggested approvers.  
2) **Policy Q&A** – load your IAM/IT policies and ask natural‑language questions over them.  
3) **Log Explainer** – paste Okta (or similar) logs and get human‑readable root‑cause/explanations.  
4) **Reviewer Helper** – draft crisp access‑review notes (why keep/why remove) using signals + policy.

All modules are self‑contained, use realistic (sanitized) inputs, and support a **pluggable LLM** (OpenAI-compatible or local server) via environment variables.

---

## Repo Structure

```
.
├── README.md
├── LICENSE
├── CONTRIBUTING.md
├── SECURITY.md
├── .env.example
├── requirements.txt
├── Makefile
├── configs/
│   ├── provider.example.yml
│   └── policy_sources.example.yml
├── data/
│   └── sample/
│       ├── access_requests.jsonl
│       ├── okta_logs.jsonl
│       ├── policies/
│       │   ├── joiner_mover_leaver.md
│       │   ├── sso_standards.md
│       │   └── privileged_access.md
│       └── review_signals.csv
├── app/
│   ├── llm.py
│   ├── triage_access.py
│   ├── policy_qa.py
│   ├── log_explainer.py
│   └── reviewer_helper.py
└── tests/
    └── smoke_test.py
```

> **Quick demo:** Each app can run from the command line and reads from `data/sample`. Swap in your own files to make it real.

---

## How I (an IAM Engineer) Use AI — Narrative

**Day to day** I use AI to:

- **Speed up access decisions** by translating free‑text tickets into structured risk context, mapping to least‑privilege policy, and proposing the right group/role and approver chain.
- **Search & explain policy** so non‑IAM stakeholders get consistent answers (e.g., “When do we allow break‑glass?”) without me hunting wikis.
- **Explain authentication issues** by summarizing event payloads (Okta System Logs, OIDC errors) into probable causes + next actions.
- **Improve access reviews** by generating reviewer-ready blurbs that combine usage signals, group purpose, and policy language.

This repo packages those workflows into small scripts you can run locally or wire into Slack, Jira, or a workflow tool.

---

## Setup

1) **Clone & create env**
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

2) **Choose an LLM provider** in `.env` (only one needed):
```bash
LLM_PROVIDER=openai            # or: http
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini
# If using a local/server LLM (OpenAI-compatible):
OPENAI_BASE_URL=http://localhost:11434/v1
```

3) (Optional) **Point to live systems**: You can keep it offline, or set these for real calls in the future.
```bash
OKTA_ORG_URL=https://your-org.okta.com
OKTA_API_TOKEN=...
```

> The sample data works entirely offline. No vendor APIs are required to try the project.

---

## Running the Examples

### 1) Access Request Triage
Input: `data/sample/access_requests.jsonl` (one JSON per line).
```bash
python app/triage_access.py --in data/sample/access_requests.jsonl --out triage_results.jsonl
```

### 2) Policy Q&A
Loads docs from `data/sample/policies/` and lets you ask questions.
```bash
python app/policy_qa.py --ask "When is break-glass allowed? What’s the timeout?"
```

### 3) Log Explainer
Summarizes Okta (or similar) events and suggests next steps.
```bash
python app/log_explainer.py --in data/sample/okta_logs.jsonl --out explained_logs.jsonl
```

### 4) Reviewer Helper
Generates 2–3 sentence blurbs per user–group edge using `data/sample/review_signals.csv`.
```bash
python app/reviewer_helper.py --signals data/sample/review_signals.csv --out review_blurbs.csv
```

---

## Security & Privacy

- The project is **sample-first**. Keep real data out of the repo.
- If you wire to live systems, store secrets in `.env` or a secret store (not git!).
- Add redaction where you ingest logs or tickets.

See `SECURITY.md` for a quick disclosure policy.

---

## License
MIT (see `LICENSE`).
