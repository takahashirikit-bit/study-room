import os
import json
import subprocess
from datetime import datetime
from google import genai 

GENAI_API_KEY = os.getenv("GEMINI_API_KEY")
JSONL_PATH = "00_meta/analytics/raw_data.jsonl"
LOG_DIR = "00_meta/study-log"
PROMPT_PATH = ".github/prompts/analytics_prompt.txt"

def analyze():
    diff = subprocess.check_output(["git", "diff", "HEAD^", "HEAD"]).decode("utf-8")
    message = subprocess.check_output(["git", "log", "-1", "--pretty=%B"]).decode("utf-8")

    client = genai.Client(api_key=GENAI_API_KEY)

    if not os.path.exists(PROMPT_PATH):
        raise FileNotFoundError(f"Prompt file not found at {PROMPT_PATH}")
        
    with open(PROMPT_PATH, "r", encoding="utf-8") as f:
        template = f.read()
    
    prompt = template.replace("{{message}}", message).replace("{{diff}}", diff[:5000])

    response = client.models.generate_content(
        model='gemini-flash-latest',
        contents=prompt,
        config={
            'response_mime_type': 'application/json',
        }
    )
    
    data = json.loads(response.text)
    data["timestamp"] = datetime.now().isoformat()

    os.makedirs(os.path.dirname(JSONL_PATH), exist_ok=True)
    with open(JSONL_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(data, ensure_ascii=False) + "\n")

    current_month = datetime.now().strftime("%Y-%m")
    os.makedirs(LOG_DIR, exist_ok=True)
    
    items = []
    if os.path.exists(JSONL_PATH):
        with open(JSONL_PATH, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line: continue
                try:
                    item = json.loads(line)
                    if item["timestamp"].startswith(current_month):
                        items.append(item)
                except json.JSONDecodeError:
                    continue

    with open(f"{LOG_DIR}/{current_month}.md", "w", encoding="utf-8") as f:
        f.write(f"# Activity Log {current_month}\n\n| Date | Cat | Outcome | Tech | Min |\n| :--- | :--- | :--- | :--- | :--- |\n")
        for act in sorted(items, key=lambda x: x['timestamp'], reverse=True):
            f.write(f"| {act['timestamp'][:10]} | {act['category']} | {act['outcome']} | {', '.join(act['tech_stack'])} | {act['effort_value']} |\n")

if __name__ == "__main__":
    if GENAI_API_KEY:
        analyze()
