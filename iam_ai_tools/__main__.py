
# Simple CLI helper so users can run: python -m iam_ai_tools <tool>
import sys, subprocess

HELP = """
Usage:
  python -m iam_ai_tools triage IN OUT
  python -m iam_ai_tools policy "QUESTION"
  python -m iam_ai_tools explain IN OUT
  python -m iam_ai_tools review SIGNALS_CSV OUT

Examples:
  python -m iam_ai_tools policy "When is break-glass allowed?"
"""

def run():
    if len(sys.argv) < 2 or sys.argv[1] in {"-h", "--help", "help"}:
        print(HELP)
        return 0
    cmd = sys.argv[1]
    if cmd == "triage" and len(sys.argv) == 4:
        return subprocess.call(["python", "app/triage_access.py", "--in", sys.argv[2], "--out", sys.argv[3]])
    if cmd == "policy" and len(sys.argv) == 3:
        return subprocess.call(["python", "app/policy_qa.py", "--ask", sys.argv[2]])
    if cmd == "explain" and len(sys.argv) == 4:
        return subprocess.call(["python", "app/log_explainer.py", "--in", sys.argv[2], "--out", sys.argv[3]])
    if cmd == "review" and len(sys.argv) == 4:
        return subprocess.call(["python", "app/reviewer_helper.py", "--signals", sys.argv[2], "--out", sys.argv[3]])
    print(HELP)
    return 1

if __name__ == "__main__":
    raise SystemExit(run())
