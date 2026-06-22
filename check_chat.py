import re

with open('app.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's find all routes and see which one handles chat
matches = re.findall(r'@app\.route\([\s\S]*?def .*?\(.*?\):[\s\S]*?(?=@app\.route|if __name__)', text)
for m in matches:
    if 'chat' in m.lower() or 'ai' in m.lower():
        print(m[:300])
        print('---')
