import os
import json
import requests
import re
import sys

# Ensure utf-8 output to avoid charmap errors
sys.stdout.reconfigure(encoding='utf-8')

with open('static/translations.js', 'r', encoding='utf-8') as f:
    js_text = f.read()

json_str = js_text.replace('const translations = ', '').strip().rstrip(';')
data = json.loads(json_str)

ru_dict = data['ru']
en_dict = data['en']

to_translate = {k: v for k, v in en_dict.items() if v.startswith('[EN] ')}

if not to_translate:
    print("Nothing to translate.")
    exit(0)

from dotenv import load_dotenv
load_dotenv('.env')

api_key = os.environ.get("GROQ_API_KEY")

keys = list(to_translate.keys())
chunk_size = 50

for i in range(0, len(keys), chunk_size):
    chunk_keys = keys[i:i+chunk_size]
    chunk_dict = {k: ru_dict[k] for k in chunk_keys}
    
    prompt = "Translate the following JSON string values from Russian to English. Return ONLY valid JSON with the exact same keys, but translated values. Do not write anything else. Ensure valid JSON.\n\n"
    prompt += json.dumps(chunk_dict, ensure_ascii=False)
    
    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "system", "content": "You are a machine translation API that returns ONLY raw valid JSON."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3
    }
    
    print(f"Translating chunk {i//chunk_size + 1}...")
    res = requests.post("https://api.groq.com/openai/v1/chat/completions", json=payload, headers={"Authorization": f"Bearer {api_key}"})
    if res.status_code == 200:
        content = res.json()['choices'][0]['message']['content'].strip()
        if content.startswith('```'):
            content = re.sub(r'^```(json)?|```$', '', content).strip()
        try:
            translated = json.loads(content)
            for k, v in translated.items():
                if k in en_dict:
                    en_dict[k] = v
        except Exception as e:
            print("Failed JSON parse for chunk:", e)
            print("Content was:", content)

new_js = "const translations = " + json.dumps(data, ensure_ascii=False, indent=4) + ";\n"
with open('static/translations.js', 'w', encoding='utf-8') as f:
    f.write(new_js)
    
print("Translations updated.")
