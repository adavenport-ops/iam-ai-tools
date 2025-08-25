
import argparse, glob, os
from app.llm import LLM

SYSTEM = "You answer questions strictly by quoting and summarizing the provided policy text. If unsure, say what to check."

def load_policies(path: str) -> str:
    chunks = []
    for p in glob.glob(os.path.join(path, "**", "*"), recursive=True):
        if os.path.isfile(p):
            try:
                with open(p, "r", errors="ignore") as f:
                    chunks.append("FILE: " + os.path.basename(p) + "\n" + f.read())
            except Exception:
                pass
    return "\n\n".join(chunks)[:120_000]  # keep prompt small

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--ask", required=True)
    ap.add_argument("--dir", default="data/sample/policies")
    args = ap.parse_args()

    llm = LLM()
    corpus = load_policies(args.dir)
    prompt = f"POLICY CORPUS\n---\n{corpus}\n\nQUESTION: {args.ask}"
    print(llm.chat(SYSTEM, prompt))
