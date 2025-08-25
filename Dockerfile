
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Default command prints help info
CMD ["bash", "-lc", "echo 'Run: make demo  |  or  python app/policy_qa.py --ask "..."'"]
