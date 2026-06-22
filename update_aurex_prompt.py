import re

with open('server.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Match the current system prompt
match = re.search(r'system_prompt\s*=\s*".*?"', text)
if match:
    new_prompt = 'system_prompt = "Ты - Aurex, нейро-ассистент студии Aurexis Studio. Отвечай прямо, четко и по делу. Не пиши огромные полотна текста, не используй лишнюю воду и длинные рассуждения. Будь вежливым, профессиональным, но лаконичным."'
    text = text.replace(match.group(0), new_prompt)
    with open('server.py', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Prompt updated successfully.")
else:
    print("Could not find system_prompt in server.py")
