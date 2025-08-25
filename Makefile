
    .PHONY: fmt lint demo
    fmt:
	python -m pip install ruff black --quiet
	ruff check --fix app || true
	black app

    lint:
	python -m pip install ruff black --quiet
	ruff check app

    # quick demo with echo LLM if no key set
    demo:
	python app/triage_access.py --in data/sample/access_requests.jsonl --out /tmp/triage.jsonl
	python app/policy_qa.py --ask "When is break-glass allowed?"
	python app/log_explainer.py --in data/sample/okta_logs.jsonl --out /tmp/logs.jsonl
	python app/reviewer_helper.py --signals data/sample/review_signals.csv --out /tmp/review.csv
