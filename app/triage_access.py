
import json, argparse
from app.llm import LLM

SYSTEM = """
You are an IAM assistant. Given an access request, propose: (1) recommended group/role, (2) risk level (low/med/high),
(3) why, (4) suggested approvers (manager + app owner), and (5) least-privilege alternative if any. Be concise, cite policy
names if provided.
"""

PROMPT_TMPL = """
ACCESS REQUEST
---
{req}

POLICY HINTS
---
- Follow least privilege and SoD.
- Break-glass only for Sev1 within 60 minutes.
- Contractors need time-bound access.
"""

def triage_line(d):
    llm = LLM()
    user = PROMPT_TMPL.format(req=json.dumps(d, ensure_ascii=False))
    ans = llm.chat(SYSTEM, user)
    d["ai_triage"] = ans
    return d

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="IN", required=True)
    ap.add_argument("--out", dest="OUT", required=True)
    args = ap.parse_args()

    out = []
    with open(args.IN) as f:
        for line in f:
            if line.strip():
                out.append(triage_line(json.loads(line)))
    with open(args.OUT, "w") as w:
        for d in out:
            w.write(json.dumps(d)+"\n")
    print(f"Wrote {len(out)} triage results to {args.OUT}")
