import os
import json
import time
from google import genai

# 設定
GENAI_API_KEY = "あなたのAPIキー" # ローカル実行用に直接貼るか環境変数から取得
OLD_JSONL = "00_meta/analytics/raw_data.jsonl"
NEW_JSONL = "00_meta/analytics/raw_data_new.jsonl"
PROMPT_PATH = ".github/prompts/analytics_prompt.txt"

def migrate():
    client = genai.Client(api_key=GENAI_API_KEY)
    
    # 新しいプロンプトテンプレートの読み込み
    with open(PROMPT_PATH, "r", encoding="utf-8") as f:
        prompt_template = f.read()

    if not os.path.exists(OLD_JSONL):
        print("過去のログデータが見つかりません。")
        return

    updated_lines = []
    
    with open(OLD_JSONL, "r", encoding="utf-8") as f:
        lines = f.readlines()

    print(f"{len(lines)} 件のログを変換します...")

    for i, line in enumerate(lines):
        if not line.strip(): continue
        
        # 既存のデータを解析
        old_data = json.loads(line)
        
        # 過去のOutcomeやTech Stackを材料に、新しいプロンプトで再生成を依頼
        # ここではコミットメッセージの代わりに「古いOutcome」を材料として渡します
        context_message = f"過去のログ内容: {old_data.get('outcome', '')} (Tech: {old_data.get('tech_stack', [])})"
        
        # プロンプトの作成（Diffは過去分がないため、contextとして古い情報を渡す）
        prompt = prompt_template.replace("{{message}}", context_message).replace("{{diff}}", "過去ログの変換につきDiffなし")

        try:
            response = client.models.generate_content(
                model='gemini-flash-latest',
                contents=prompt,
                config={'response_mime_type': 'application/json'}
            )
            
            new_data = json.loads(response.text)
            # タイムスタンプは過去のものを維持
            new_data["timestamp"] = old_data["timestamp"]
            
            updated_lines.append(json.dumps(new_data, ensure_ascii=False))
            print(f"[{i+1}/{len(lines)}] 変換成功: {new_data['outcome'][:30]}...")
            
            # APIのレートリミット対策（必要に応じて）
            time.sleep(1) 
            
        except Exception as e:
            print(f"[{i+1}/{len(lines)}] 失敗: {e}")
            # 失敗した場合は古いデータをそのまま保持
            updated_lines.append(line.strip())

    # 新しいファイルに保存
    with open(NEW_JSONL, "w", encoding="utf-8") as f:
        for line in updated_lines:
            f.write(line + "\n")

    print(f"\n完了！ {NEW_JSONL} を確認してください。")

if __name__ == "__main__":
    migrate()