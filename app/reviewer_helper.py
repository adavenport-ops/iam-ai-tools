
import argparse, csv
from app.llm import LLM

SYSTEM = (
    "You create concise access-review notes (2-3 sentences) using policy tone. "
    "If usage is low and purpose unclear, suggest removal. If in SoD conflict, flag high risk."
)

PROMPT_TMPL = """
EDGE
---
User: {user}
Group: {group}
Purpose: {purpose}
30d Sign-ins: {signins_30d}
App Usage CTA: {app_usage}
Notes: {notes}

POLICY: Follow least privilege; justify standing access; revoke unused over 30d; time-bound contractor access; SoD enforced.
"""

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--signals", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    llm = LLM()
    with open(args.signals) as f, open(args.out, "w", newline="") as w:
        reader = csv.DictReader(f)
        writer = csv.DictWriter(w, fieldnames=reader.fieldnames + ["ai_review_note"])
        writer.writeheader()
        for row in reader:
            prompt = PROMPT_TMPL.format(**row)
            row["ai_review_note"] = llm.chat(SYSTEM, prompt)
            writer.writerow(row)
    print(f"Wrote reviewer blurbs to {args.out}")
