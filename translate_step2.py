import json
import re
import requests
import os
from dotenv import load_dotenv

load_dotenv()

with open('ru_js_strings.json', 'r', encoding='utf-8') as f:
    strings = json.load(f)

# Filter out obvious html strings
filtered_strings = []
for s in strings:
    if '<' in s or '>' in s or 'style=' in s or len(s.strip()) <= 1 or s.startswith('t_'):
        continue
    filtered_strings.append(s.strip())

api_key = os.environ.get("GROQ_API_KEY")

prompt = "Translate this JSON array of Russian UI strings to English. Keep the output EXACTLY as a valid JSON array of strings in the exact same order. Do not add any markdown formatting or extra text. Just the raw JSON array. Here is the array: " + json.dumps(filtered_strings, ensure_ascii=False)

res = requests.post(
    "https://api.groq.com/openai/v1/chat/completions",
    headers={"Authorization": f"Bearer {api_key}"},
    json={
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.1
    }
)

try:
    trans_array = res.json()["choices"][0]["message"]["content"].strip()
    # Remove markdown ```json if exists
    if trans_array.startswith('```json'):
        trans_array = trans_array[7:]
    if trans_array.endswith('```'):
        trans_array = trans_array[:-3]

    trans_array = json.loads(trans_array.strip())

    js_trans_dict = {}
    for i, ru in enumerate(filtered_strings):
        js_trans_dict[ru] = trans_array[i]

    with open('js_trans_dict.json', 'w', encoding='utf-8') as f:
        json.dump(js_trans_dict, f, ensure_ascii=False, indent=2)
    print("Translation completed.")
except Exception as e:
    print("Translation failed:", e)
    print(res.text)
