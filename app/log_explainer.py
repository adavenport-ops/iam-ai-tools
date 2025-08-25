
import json, argparse
from app.llm import LLM

SYSTEM = "You are a troubleshooting copilot for Okta/System logs. Explain what likely happened and give next steps in 3 bullets."

PROMPT_TMPL = """
EVENT
---
{evt}

CONTEXT
---
- If authn failures: check factor enrollment, device posture, IP reputation, policy conditions.
- If token errors: look at clock skew, audience, redirect URI, PKCE.
- If rate limits: suggest backoff and client fix.
"""

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="IN", required=True)
    ap.add_argument("--out", dest="OUT", required=True)
    args = ap.parse_args()

    llm = LLM()
    out = []
    with open(args.IN) as f:
        for line in f:
            d = json.loads(line)
            prompt = PROMPT_TMPL.format(evt=json.dumps(d, ensure_ascii=False))
            d["ai_explain"] = llm.chat(SYSTEM, prompt)
            out.append(d)
    with open(args.OUT, "w") as w:
        for d in out:
            w.write(json.dumps(d)+"\n")
    print(f"Wrote {len(out)} explained events to {args.OUT}")
